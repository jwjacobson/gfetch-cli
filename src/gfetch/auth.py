from pathlib import Path

from decouple import config
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = config("SCOPES", default='https://www.googleapis.com/auth/gmail.readonly')
BASE_DIR = Path(config("BASE_DIR", default='gfetch'))
CREDS = BASE_DIR / config("CREDS", default='credentials.json')
TOKEN = BASE_DIR / config("TOKEN", default='token.json')


def get_credentials():
    
    creds = None
    if TOKEN.exists():
        try:
            creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
        except Exception as e:
            print(f"Error loading credentials: {e}")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                if TOKEN.exists():
                    TOKEN.unlink()
                creds = None

        if not creds:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CREDS, SCOPES)
                creds = flow.run_local_server(port=0)
                with open(TOKEN, "w") as token:
                    token.write(creds.to_json())
            except Exception as e:
                print(f"Error during OAuth flow: {e}")

    return creds
