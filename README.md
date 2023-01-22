# GDriveSearch
Hello there, 👽 I am tow-bot. My creator designed me to tow files from Google Drive and serve the seeker.

### Prepare config.env file
Create an env file in [Github Gist](https://gist.github.com/) or any other place but make sure to provide the direct download link of that file.
```sh
PICKLE_FILE_URL = ""
BOT_TOKEN = ""
DLWORKER_LIST = '["https://ABC.workers.dev", "https://DEF.workers.dev"]'
USER_LIST = '[12345, 67890]'
GDRIVE_FOLDER_ID = 'abcXYZ'
SRCH_ANIM = True
# https://github.com/sindresorhus/cli-spinners/blob/main/spinners.json
SRCH_ANIM_FRAMES = '[
  "∙∙∙",
  "●∙∙",
  "∙●∙",
  "∙∙●",
  "∙∙∙"
]'
```

### Build and run the docker image
```sh
docker build -t mybot:latest .
docker run -d --name=GDriveSearchBot -e CONFIG_FILE_URL="github gist link of config.env" --restart=unless-stopped mybot:latest
```
