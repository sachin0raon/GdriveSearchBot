import os
import re
import io
import gc
import time
import pickle
import logging
import humanize
import requests
import json
import threading
import asyncio
import random
import string
from multiprocessing import Pipe, connection
from urllib.parse import quote
from dotenv import load_dotenv
from telegram import Update, Message, error, ParseMode, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageFilter
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from html_data import HTML_DATA
from html_legacy import html_content

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
CONFIG_FILE_URL = os.getenv("CONFIG_FILE_URL")
AUTHORIZED_USERS = set()
DLWORKER_LIST = list()
BOT_TOKEN = None
CREDENTIALS = None
GDRIVE_FOLDER_ID = None
SRCH_ANIM = None
SRCH_ANIM_FRAMES = list()
PICKLE_FILE = "token.pickle"
START_CMD = "start"
SRCH_CMD = "srch"
MAX_RESULTS = 30
QUALITIES = ["360", "480", "720", "1080", "1440", "2160"]
HELP_TEXT = f"Use <code>/{SRCH_CMD} filename</code> to search files.\nExamples:\n<code>/{SRCH_CMD} doctor strange 2022\n/{SRCH_CMD} moon knight s01e06\n"\
    f"/{SRCH_CMD} black adam 1080\n/{SRCH_CMD} -r infinity war</code> <i>to remove duplicate files</i>\n"
WEBSITE_URL = "https://gdrive.workers.dev"
SRCH_WAIT_TXT = f"🧐 <b>Searching, Please wait</b>🔎\n👉 <i>You can also use this site to search files: </i>\n🌐 <a href='{WEBSITE_URL}'>{WEBSITE_URL}</a>"

class UsersFilter(MessageFilter):
    def filter(self, message: Message):
        if len(AUTHORIZED_USERS) == 0:
            return True
        else:
            return bool(message.chat.id in AUTHORIZED_USERS)

class GdriveSearchError(Exception):
    pass

def start(update: Update, context: CallbackContext) -> None:
    logger.info(f"/{START_CMD} sent by {update.message.chat.id}")
    msg = f"Hey, Welcome to <b>Google Drive Search Bot</b>.\n{HELP_TEXT}"
    try:
        context.bot.send_message(chat_id=update.message.chat.id, text=msg, parse_mode=ParseMode.HTML)
    except error.TelegramError:
        logger.error("Failed to send start message")

def isDownloadable(fileId, creds, shared_list) -> None:
    try:
        gdrive = build('drive', 'v3', credentials=creds, cache_discovery=False)
        req = gdrive.files().get_media(fileId=fileId)
        buf = io.BytesIO()
        MediaIoBaseDownload(buf, req, chunksize=1024*1024*2).next_chunk()
        buf.close()
        gdrive.close()
    except Exception:
        shared_list.append(fileId)

async def filter_files(fileId, creds, shared_list):
    await asyncio.to_thread(isDownloadable, fileId, creds, shared_list)

async def check_download(creds, files) -> None:
    shared_list = list()
    await asyncio.gather(*[asyncio.create_task(filter_files(fileId, creds, shared_list)) for fileId in files])
    for fileId in shared_list:
        files.pop(fileId)
    del shared_list

def contains(substr: list, fullstr: str) -> bool:
    for s in substr:
        if fullstr.find(s.lower()) == -1:
            return False
    return True

def gdrive_list(fileName, quality=None, duplicate=True):
    global CREDENTIALS
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, 'rb') as f:
            credentials = pickle.load(f)
            if credentials and credentials.expired and credentials.refresh_token:
                try:
                    credentials.refresh(Request())
                    CREDENTIALS = credentials
                except RefreshError:
                    logger.error("Failed to refresh token")
                    raise GdriveSearchError
    else:
        err_msg = f"{PICKLE_FILE} not found"
        logger.error(err_msg)
        raise FileNotFoundError(err_msg)
    count = 0
    files_md5 = set()
    files = dict()
    html_data = ''
    try:
        service = build('drive', 'v3', credentials=credentials, cache_discovery=False)
        query = "mimeType != 'application/vnd.google-apps.folder' and "
        var = re.split(" ", fileName)
        for text in var:
            if quality is not None and re.search(quality, text):
                continue
            query += f"name contains '{text}' and "
        query += "trashed=false"
        results = service.files().list(supportsAllDrives=True, includeItemsFromAllDrives=True,
                                       q=query, corpora='allDrives', spaces='drive',
                                       fields='files(id, name, mimeType, size, md5Checksum)').execute()["files"]
        service.close()
        for file in results:
            md5 = file.get('md5Checksum')
            if count >= MAX_RESULTS:
                break
            elif duplicate is False and md5 in files_md5:
                continue
            else:
                files_md5.add(md5)
            if file.get('mimeType') == 'application/vnd.google-apps.shortcut' \
                    or contains(var, file.get('name').lower()) is False:
                continue
            files[file.get('id')] = {'name': file.get('name'), 'size': file.get('size'), 'mimeType': file.get('mimeType')}
            count += 1
        asyncio.run(check_download(credentials, files))
        count = len(files)
        for fileId in files:
            end_point = f'{quote(files.get(fileId).get("name"), safe="")}?id={fileId}'
            media_link = f'{DLWORKER_LIST[2]}/{end_point}'
            gdrive_link = f'https://drive.google.com/uc?id={fileId}&export=download'
            color_hex = format(random.randint(0, 16777215), 'x')
            html_data += f'<div class="col-lg-6 col-md-6 mt-3"><div class="icon-box" data-aos="zoom-in-left"><div class="icon"><i class="bx bxs-videos" style="color: #{color_hex};"></i></div>' \
                         f'<h4 class="title text-break fs-6"><a href="{gdrive_link}" target="_blank" referrerpolicy="same-origin">📂 {files.get(fileId).get("name")}</a></h4>' \
                         f'<p class="description fw-bold">💾 {humanize.naturalsize(files.get(fileId).get("size", 0))}</p><p class="description mt-1">' \
                         f'<a class="btn btn-outline-primary btn-sm" role="button" href="{DLWORKER_LIST[0]}/{end_point}" >⚡<strong> Download 1</strong></a>&nbsp;&nbsp;' \
                         f'<a class="btn btn-outline-success btn-sm" role="button" href="{DLWORKER_LIST[1]}/{end_point}" >⚡<strong> Download 2</strong></a></p>'
            if "video" in files.get(fileId).get('mimeType'):
                mxp_link = f'intent:{media_link}#Intent;package=com.mxtech.videoplayer.ad;S.title={files.get(fileId).get("name")};end'
                html_data += f'<p class="description mt-1"><a href="vlc://{media_link}" style="color: #444444;">▶️<strong> VLC</strong></a>&nbsp;&nbsp;' \
                             f'<a href="{mxp_link}" style="color: #444444;">▶️<strong> MX Player</strong></a>&nbsp;&nbsp;' \
                             f'<a href="nplayer-{media_link}" style="color: #444444;">▶️<strong> nPlayer</strong></a></p>'
            html_data += '</div></div>'
        logger.info(f"Query: {fileName} Found: {count}")
        if count > 0:
            reply_msg = f"💁🏻‍♂ <b>Found <code>{count}</code> results for </b><i>{fileName}</i>\n📄 Open the html file to view results"
            fname = f'{fileName.replace(" ", "_")}.html'
            with open(fname, 'w', encoding='utf-8') as fout:
                fout.write(HTML_DATA.replace('{search_query}', fileName).replace('{search_count}', str(count)).replace('{search_results}', html_data))
            del service, results, files_md5, html_data
            return reply_msg, fname, files
    except Exception as err:
        logger.error(f"ERROR: {str(err)}")
        raise GdriveSearchError
    return "", "", {}

def uploadFile(creds, file: str):
    try:
        logger.info(f'Uploading {file} to gdrive')
        gdrive = build('drive', 'v3', credentials=creds, cache_discovery=False)
        fileName = ''.join(random.choice(string.ascii_letters) for i in range(8))+'.html'
        file_metadata = {'name': fileName, 'mimeType': 'text/html', 'parents': [GDRIVE_FOLDER_ID]}
        html_file = MediaFileUpload(filename=file, mimetype='text/html')
        upload_file = gdrive.files().create(body=file_metadata, media_body=html_file, fields='id').execute()
        gdrive.close()
        return upload_file.get('id')
    except Exception as e:
        logger.error(f'Failed to upload {file}: {str(e)}')
        return None

def sendFile(bot: Bot, message: Message, fname: str, files: {}, caption=""):
    try:
        html_data = f'<span class="container center rfontsize"><h4>Search Result For: {fname.replace(".html", "").replace("_", " ")}</h4></span>'
        for fileId in files:
            end_point = f'{quote(files.get(fileId).get("name"), safe="")}?id={fileId}'
            gdrive_link = f'https://drive.google.com/uc?id={fileId}&export=download'
            html_data += f'<span class="container start rfontsize"><div><a href="{gdrive_link}" target="_blank">{files.get(fileId).get("name")}</a> ({humanize.naturalsize(files.get(fileId).get("size", 0))})</div><div class="dlinks">'
            html_data += f'📥 <span><a class="forhover" href="{DLWORKER_LIST[0]}/{end_point}" target="_blank">Download 1</a></span>&nbsp;&nbsp;📥 <span><a class="forhover" href="{DLWORKER_LIST[1]}/{end_point}" target="_blank">Download 2</a></span>'
            if "video" in files.get(fileId).get('mimeType'):
                media_link = f'{DLWORKER_LIST[2]}/{end_point}'
                mxp_link = f'intent:{media_link}#Intent;package=com.mxtech.videoplayer.ad;S.title={files.get(fileId).get("name")};end'
                html_data += f'▶️&nbsp;<span><a class="forhover" href="vlc://{media_link}">VLC</a></span>&nbsp;&nbsp;▶️&nbsp;<span><a class="forhover" href="{mxp_link}">MX Player</a></span>&nbsp;&nbsp;▶️&nbsp;<span><a class="forhover" href="nplayer-{media_link}">nPlayer</a></span>'
            html_data += '</div></span>'
        bot.sendDocument(document=bytes(html_content.replace('{fileName}', fname.replace(".html", "").replace("_", " ")).replace('{msg}', html_data), 'utf-8'),
                         filename=fname, reply_to_message_id=message.message_id, caption=caption, parse_mode=ParseMode.HTML, chat_id=message.chat_id)
        del html_data, files
        return
    except error.RetryAfter as r:
        logger.warning(f"Failed to send: {fname}..Retrying")
        time.sleep(r.retry_after * 1.5)
        return sendFile(bot, message, fname, files, caption)
    except Exception as e:
        logger.error(f"Error while sending {fname}: {str(e)}")
        return

def searchAnimation(context: CallbackContext, chatId: int, messageId: int, conn: connection.Connection) -> None:
    while conn.poll() is False and len(SRCH_ANIM_FRAMES) > 0:
        for frame in SRCH_ANIM_FRAMES:
            time.sleep(0.1)
            try:
                context.bot.edit_message_text(text=f"{SRCH_WAIT_TXT}\n⏳ {frame}", chat_id=chatId, message_id=messageId, parse_mode=ParseMode.HTML)
            except error.TelegramError as err:
                logger.debug(f"error: {str(err)}")
    conn.close()
    return

def searchBot(update: Update, context: CallbackContext) -> None:
    reply_to = None
    quality = None
    duplicate = True
    try:
        query = update.message.text.split(' ', maxsplit=1)[1].strip()
        if re.search("^-r", query, re.IGNORECASE):
            duplicate = False
            query = query[2: len(query)].strip()
        query = re.sub('[^a-zA-Z0-9-_. ]', '', query)
        for res in QUALITIES:
            if re.search(res, query):
                quality = res
                break
        logger.info(f"Searching: {query}")
        reply_to = context.bot.send_message(chat_id=update.message.chat.id, text=SRCH_WAIT_TXT,
                                            parse_mode=ParseMode.HTML, reply_to_message_id=update.message.message_id)
        if SRCH_ANIM is True:
            parent_conn, child_conn = Pipe(duplex=True)
            animator = threading.Thread(target=searchAnimation, daemon=True, args=(context, reply_to.chat.id, reply_to.message_id, child_conn))
            animator.start()
        reply_msg, fname, files_data = gdrive_list(query, quality, duplicate)
        if SRCH_ANIM is True:
            parent_conn.send(True)
            animator.join()
        if reply_msg:
            gdrive_fileId = uploadFile(CREDENTIALS, fname)
            if gdrive_fileId is not None:
                button = [InlineKeyboardButton(text="🔎 Tap here to view", url=f"{DLWORKER_LIST[0]}/results?id={gdrive_fileId}")]
                context.bot.edit_message_text(text=reply_msg.split('\n')[0], chat_id=reply_to.chat.id, message_id=reply_to.message_id,
                                              parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([button]))
                os.remove(fname)
            else:
                context.bot.delete_message(chat_id=update.message.chat.id, message_id=reply_to.message_id)
                sendFile(context.bot, update.message, fname, files_data, reply_msg)
        else:
            context.bot.edit_message_text(chat_id=reply_to.chat.id, text=f'🙅‍♂ <b>No result found for</b> <i>{query}</i>❗',
                                          parse_mode=ParseMode.HTML, message_id=reply_to.message_id)
    except IndexError:
        msg = f"😡 <b>Send a search query along with the command</b>❗\n{HELP_TEXT}"
        context.bot.send_message(chat_id=update.message.chat.id, text=msg, parse_mode=ParseMode.HTML,
                                 reply_to_message_id=update.message.message_id)
    except AttributeError:
        pass
    except (FileNotFoundError, GdriveSearchError):
        if reply_to is not None:
            context.bot.delete_message(chat_id=update.message.chat.id, message_id=reply_to.message_id)
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text="<b>Error occurred while searching..Please retry</b> ❗",
                                 parse_mode=ParseMode.HTML, reply_to_message_id=update.message.message_id)
    except error.TelegramError as err:
        logger.error(f"Failed to send results: {str(err)}")
    finally:
        gc.collect()

def starter(users_filter: UsersFilter) -> None:
    logger.info("Starting bot")
    updater = Updater(token=BOT_TOKEN, use_context=True)
    logger.info("Registering commands")
    try:
        dispatcher = updater.dispatcher
        bot = updater.bot
        bot.delete_my_commands()
        bot.set_my_commands([(START_CMD, 'Start the bot'), (SRCH_CMD, 'Search files')])
        dispatcher.add_handler(CommandHandler(START_CMD, start, filters=users_filter, run_async=True))
        dispatcher.add_handler(CommandHandler(SRCH_CMD, searchBot, filters=users_filter, run_async=True))
    except error.TelegramError:
        logger.error("Failed to set commands")
    else:
        logger.info("Bot started")
        updater.start_polling(drop_pending_updates=True)
        updater.idle()

def setup_bot() -> None:
    global BOT_TOKEN
    global AUTHORIZED_USERS
    global DLWORKER_LIST
    global GDRIVE_FOLDER_ID
    global SRCH_ANIM
    global SRCH_ANIM_FRAMES
    if CONFIG_FILE_URL is not None:
        logger.info("Downloading config file")
        try:
            config_file = requests.get(url=CONFIG_FILE_URL)
            if config_file.ok:
                with open('config.env', 'wt', encoding='utf-8') as f:
                    f.write(config_file.text)
                logger.info("Loading config values")
                if load_dotenv('config.env', override=True):
                    AUTHORIZED_USERS = json.loads(os.environ['USER_LIST'])
                    GDRIVE_FOLDER_ID = os.environ['GDRIVE_FOLDER_ID']
                    BOT_TOKEN = os.environ['BOT_TOKEN']
                    SRCH_ANIM = os.environ['SRCH_ANIM'].lower() == "true"
                    if SRCH_ANIM is True:
                        SRCH_ANIM_FRAMES = json.loads(os.environ['SRCH_ANIM_FRAMES'])
                    pickle_file = requests.get(url=os.environ['PICKLE_FILE_URL'])
                    if pickle_file.ok:
                        with open(PICKLE_FILE, 'wb') as f:
                            f.write(pickle_file.content)
                    else:
                        raise requests.exceptions.HTTPError
                    DLWORKER_LIST = json.loads(os.environ['DLWORKER_LIST'])
                    if len(DLWORKER_LIST) == 0:
                        raise KeyError
                    else:
                        starter(UsersFilter())
            else:
                logger.error("Error while downloading config file")
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, KeyError, json.JSONDecodeError):
            logger.error("Failed to setup config")
    else:
        logger.error("CONFIG_FILE_URL is None")

if __name__ == '__main__':
    setup_bot()
