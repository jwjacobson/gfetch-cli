# gfetch -- save gmail emails locally
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


from pathlib import Path

from decouple import config

from emails import fetch_emails


class DirConfig:
    """
    Store dir configuration in a class to allow easy access by emails.py
    """
    BASE_DIR = Path(config("BASE_DIR"))
    RAW_EMAIL_DIR = BASE_DIR / config("RAW_EMAIL_DIR")
    CLEAN_EMAIL_DIR = BASE_DIR / config("CLEAN_EMAIL_DIR")
    ATTACHMENTS_DIR = BASE_DIR / config("ATTACHMENTS_DIR")


def create_dirs(config):
    config.RAW_EMAIL_DIR.mkdir(parents=True, exist_ok=True)
    config.CLEAN_EMAIL_DIR.mkdir(parents=True, exist_ok=True)
    config.ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)


dir_config = DirConfig()
create_dirs(dir_config)

def get_emails(email_address, config=dir_config):
    try:
        fetch_emails(email_address, config)

    except Exception as e:
        print(f"Error getting emails: {e}")


def delete_files(config=dir_config):
    attachments_dir = config.ATTACHMENTS_DIR
    clean_dir = config.CLEAN_EMAIL_DIR
    raw_dir = config.RAW_EMAIL_DIR

    attachments = list(attachments_dir.iterdir()) if attachments_dir.exists() else []
    clean_emails = [email for email in clean_dir.iterdir() if email.suffix == ".txt"] if clean_dir.exists() else []
    raw_emails = [email for email in raw_dir.iterdir() if email.suffix == ".eml"] if raw_dir.exists() else []

    deleted_emails = 0
    deleted_attachments = 0

    if not attachments:
        print("No attachments found.")
    else:
        for attachment in attachments:
            attachment.unlink()
            deleted_attachments += 1

    if not clean_emails:
        print("No cleaned emails found.")
    else:
        for email in clean_emails:
            email.unlink()
            deleted_emails += 1

    if not raw_emails:
        print("No raw emails found.")
    else:
        for email in raw_emails:
            email.unlink()

    if deleted_emails and deleted_attachments:
        print(f"Deleted {deleted_emails} emails and {deleted_attachments} attachments.")
    elif deleted_emails:
        print(f"Deleted {deleted_emails} emails.")
    elif deleted_attachments:
        print(f"Deleted {deleted_attachments} attachments.")
   

def menu():     # pragma: no cover
    while True:
        print_menu()
        choice = int(input())

        while choice not in {1, 2, 3}:
            print("Choose 1, 2, or 3.")
            choice = int(input())
        
        if choice == 1:
            email_address = input("\nDownload emails with which correspondent? ")
            get_emails(email_address)

        elif choice == 2:
            print()
            delete_files()
        
        else:
            break

def print_menu():   # pragma: no cover
    print("\nChoose an option:")
    print("1. Download emails")
    print("2. Delete saved emails")
    print("3. Quit")


def main():   # pragma: no cover
    print("Welcome to Gfetch!")
    menu()

if __name__ == "__main__":  # pragma: no cover
    main()
