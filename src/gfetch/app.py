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

    RAW_EMAIL_DIR = Path(config("RAW_EMAIL_DIR"))
    CLEAN_EMAIL_DIR = Path(config("CLEAN_EMAIL_DIR"))
    ATTACHMENTS_DIR = Path(config("ATTACHMENTS_DIR"))


def create_dirs(config):
    config.RAW_EMAIL_DIR.mkdir(parents=True, exist_ok=True)
    config.CLEAN_EMAIL_DIR.mkdir(parents=True, exist_ok=True)
    config.ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)


dir_config = DirConfig()
create_dirs(dir_config)

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         email_address = request.form["email_address"]

#         result = fetch_emails(email_address, app.dir_config)

#         if "error" in result:
#             flash(result["error"])
#             return redirect(url_for("index"))

#         flash(f"Saved and cleaned {result['total_messages']} messages.")
#         flash(f"Saved {result['total_attachments']} attachments.")

#         return redirect(url_for("index"))

#     return render_template("index.html")


def delete_files():
    attachments_dir = dir_config.ATTACHMENTS_DIR
    clean_dir = dir_config.CLEAN_EMAIL_DIR
    raw_dir = dir_config.RAW_EMAIL_DIR

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


def menu():
    while True:
        print("\nChoose an option:")
        print("1. Download emails")
        print("2. Delete saved emails")
        print("3. Quit")
        choice = int(input())

        while choice not in {1, 2, 3}:
            print("Choose 1, 2, or 3.")
            choice = int(input())
        if choice == 1:
            pass
        elif choice == 2:
            print()
            delete_files()
        else:
            break



def main():
    print("Welcome to Gfetch-cli!")
    menu()

if __name__ == "__main__":
    main()
