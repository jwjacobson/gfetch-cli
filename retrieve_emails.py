# gmailfetcher -- save gmail emails locally
# Copyright (C) 2024 Jeff Jacobson <jeffjacobsonhimself@gmail.com>
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from clean_emails import clean_email_file

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

RAW_EMAIL_DIR = 'raw_emails'
CLEANED_EMAIL_DIR = 'cleaned_emails'

def get_credentials():
    """
    Load or obtain new credentials for the Google API.
    """
    creds = None
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except Exception as e:
            print(f'Error loading credentials: {e}')
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f'Error refreshing credentials: {e}')
                creds = None

        if not creds:
            try:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                print(f'Error during OAuth flow: {e}')
                return None

    return creds

def main(email_address):
    """
    Download all emails to or from EMAIL_ADDRESS. Save the raw .eml files to RAW_EMAIL_DIR and the the cleaned ones to CLEANED_EMAIL_DIR.
    """
    if not email_address:
        email_address = input("Enter the gmail address whose correspondence you want to back up: ")

    if email_address.split('@')[1] != "gmail.com":
        raise ValueError("This script only works for gmail addresses.")

    creds = get_credentials()

    if not creds:
        print('Failed to obtain credentials.')
        return

    try:
        service = build('gmail', 'v1', credentials=creds)
    except Exception as e:
        print(f'Error building Gmail service: {e}')
        return


    if not os.path.exists(RAW_EMAIL_DIR):
        os.makedirs(RAW_EMAIL_DIR)

    query = f"to:{email_address} OR from:{email_address}"
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
    EMAIL_ADDRESS = input("Enter the gmail address whose correspondence you want to back up: ")
    main(EMAIL_ADDRESS)