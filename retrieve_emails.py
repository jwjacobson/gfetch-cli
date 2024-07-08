import os
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from clean_emails import clean_email_file

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

EMAIL_ADDRESS = ''
RAW_EMAIL_DIR = 'raw_emails'
CLEANED_EMAIL_DIR = 'cleaned_emails'


def main():
    """Download all emails to or from EMAIL_ADDRESS. Save the raw .eml files to RAW_EMAIL_DIR and the the cleaned ones to CLEANED_EMAIL_DIR.
    """
    if not EMAIL_ADDRESS:
        raise ValueError("Please set the value of EMAIL_ADDRESS in retrieve_emails.py.")

    if EMAIL_ADDRESS.split('@') != "gmail.com":
        raise ValueError("This script only works for gmail addresses.")

    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    if not os.path.exists(RAW_EMAIL_DIR):
        os.makedirs(RAW_EMAIL_DIR)

    query = f"to:{EMAIL_ADDRESS} OR from:{EMAIL_ADDRESS}"
    next_page_token = None

    while True:
        if next_page_token:
            results = service.users().messages().list(userId='me', q=query, pageToken=next_page_token).execute()
        else:
            results = service.users().messages().list(userId='me', q=query).execute()
        
        messages = results.get('messages', [])
        next_page_token = results.get('nextPageToken', None)

        if not messages:
            print('No more messages found.')
            break
        else:
            print(f'Found {len(messages)} messages.')
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()

                msg_str = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
                raw_email_path = os.path.join(RAW_EMAIL_DIR, f'email_{message["id"]}.eml')
                with open(raw_email_path, 'wb') as f:
                    f.write(msg_str)
                print(f'Saved raw email_{message["id"]}.eml')

                clean_email_file(raw_email_path)
                print(f'Cleaned and saved email_{message["id"]}.txt')

        if not next_page_token:
            break

if __name__ == '__main__':
    main()