Download facebook photos you're tagged in

### App Setup
  * Create an application at https://developers.facebook.com

  * In the app's settings panel **+ Add Platform**: Website
    * Set the Site-URL to `http://localhost:8080`

  * Create a *secrets.json* file with your app's Oauth2 config

  ```
  {
    "web": {
      "client_id": "<your-app-id>",
      "client_secret": "<your-app-secret>",
      "redirect_uris": [],
      "auth_uri": "https://www.facebook.com/dialog/oauth",
      "token_uri": "https://graph.facebook.com/oauth/access_token"
    }
  }
  ```
