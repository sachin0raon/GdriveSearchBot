const authConfig = {
  "client_id": "",
  "client_secret": "",
  "refresh_token": ""
};

class googleDrive {
  constructor(authConfig) {
    this.authConfig = authConfig;
  }

  async requestOption(headers = {}, method = 'GET') {
    if (this.authConfig.expires == undefined || this.authConfig.expires < Date.now()) {
      const oauth_url = "https://www.googleapis.com/oauth2/v4/token";
      const headers = {'Content-Type': 'application/x-www-form-urlencoded'};
      var post_data = {
        client_id: this.authConfig.client_id,
        client_secret: this.authConfig.client_secret,
        refresh_token: this.authConfig.refresh_token,
        grant_type: "refresh_token",
      };
      const encoded_post_data = [];
      for (let d in post_data) {
        encoded_post_data.push(encodeURIComponent(d) + '=' + encodeURIComponent(post_data[d]));
      }
      let requestParams = {
        'method': 'POST',
        'headers': headers,
        'body': encoded_post_data.join('&')
      };
      await fetch(oauth_url, requestParams).then((response) => {
        if (!response.ok) { throw new Error(`Failed to get access token! Status: ${response.status}`); }
        return response.json();
      }).then((response) => {
        this.authConfig.accessToken = response.access_token;
        this.authConfig.expires = Date.now() + 3500 * 1000;
      });
    }
    headers['authorization'] = 'Bearer ' + this.authConfig.accessToken;
    return {
      'method': method,
      'headers': headers
    };
  }

  async download(id, range = '', inline = false) {
    let url = `https://www.googleapis.com/drive/v3/files/${id}?alt=media`;
    let requestOption = await this.requestOption();
    requestOption.headers['Range'] = range;
    let response = await fetch(url, requestOption);
    if (response.ok) {
      const {headers} = response = new Response(response.body, response);
      headers.append('Access-Control-Allow-Origin', '*');
      headers.set('Content-Disposition', 'inline');
      return response;
    } else {
      return new Response("Failed to get file data", {
        headers: {
          "content-type": "text/html;charset=UTF-8",
        },
        status: 500,
        statusText: "Internal Server Error"
      });
    }
  }
}

async function handleRequest(request) {
  const { searchParams } = new URL(request.url);
  let fileId = searchParams.get('id');
  let range = request.headers.get('Range');
  if (fileId == null || fileId == undefined) {
    return new Response("<b>File ID missing!</b>", {
      headers: {"content-type": "text/html;charset=UTF-8"},
      status: 500,
      statusText: "Internal Server Error"
    });
  } else {
    const gd = new googleDrive(authConfig);
    return gd.download(fileId, range, true);
  }
}

addEventListener("fetch", event => {
  event.respondWith(handleRequest(event.request));
});
