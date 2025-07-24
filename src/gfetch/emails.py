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

import base64
import email
from pathlib import Path
from email import policy
from email.parser import BytesParser

from googleapiclient.discovery import build

from .auth import get_credentials


def fetch_emails(email_address, config):
    """
    Fetch all emails from a given email address.
    """
    creds = get_credentials()

    if not creds:
        return {"error": "Failed to obtain credentials."}

    try:
        service = build("gmail", "v1", credentials=creds)

    except Exception as e:
        print(f"Error building Gmail service: {e}")
        return {"error": f"Error building Gmail service: {e}"}

    query = f"to:{email_address} OR from:{email_address}"
    total_messages = 0
    total_attachments = 0
    next_page_token = None

    while True:
        messages, next_page_token = get_messages_and_next_page(
            service, query, next_page_token
        )

        if not messages:
            print("No messages remain.")
            break

        batch_attachments = process_message_batch(config, service, messages)
        total_messages += len(messages)
        total_attachments += batch_attachments

        if not next_page_token:
            break

    print("\nDone.")
    print(f"Retrieved {total_messages} messages and {total_attachments} attachments.")
    return {"total_messages": total_messages, "total_attachments": total_attachments}


def get_messages_and_next_page(service, query, next_page_token=None):
    """
    Get a list of messages and a next_page_token for a given query.
    """
    if next_page_token:
        results = (
            service.users()
            .messages()
            .list(userId="me", q=query, pageToken=next_page_token)
            .execute()
        )
    else:
        results = service.users().messages().list(userId="me", q=query).execute()

    messages = results.get("messages", [])
    next_page_token = results.get("nextPageToken")

    return messages, next_page_token


def process_message_batch(config, service, messages):
    """
    Process a batch of messages and return the attachment count.
    """
    raw_dir = config.RAW_EMAIL_DIR
    batch_attachments = 0

    for message in messages:
        message_id = message["id"]
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=message["id"], format="raw")
            .execute()
        )
        msg_str = base64.urlsafe_b64decode(msg["raw"].encode("ASCII"))
        raw_email_path = raw_dir / f"email_{message['id']}.eml"
        print(f"\nRetrieving message {raw_email_path.name}.")
        with open(raw_email_path, "wb") as f:
            f.write(msg_str)
        attachments = clean_email(raw_email_path, config, message_id)
        batch_attachments += attachments or 0

    return batch_attachments


def clean_email(email_file, config, message_id):
    """
    Take an eml file, clean and save it as a txt file, and save any attachments.
    """
    email_path = Path(email_file)
    raw_file = email_path.name
    print(f"Cleaning {raw_file}.")
    clean_dir = config.CLEAN_EMAIL_DIR
    attachments_dir = config.ATTACHMENTS_DIR

    with open(email_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    date = set_date(msg["Date"])
    subject = msg["Subject"]
    formatted_subject = format_subject(msg["Subject"])
    to = msg["To"]
    from_ = msg["From"]
    attachments = get_attachments(msg, attachments_dir, date, message_id)
    body = get_body(msg)

    email_content = build_email_content(
        raw_file, date, subject, to, from_, attachments, body
    )

    email_filename = clean_dir / f"{date}__{formatted_subject}__{message_id}.txt"
    with open(email_filename, "w", encoding="utf-8") as f:
        f.write(email_content)

    if attachments:
        return len(attachments)


def set_date(date_str):
    """
    Create a date string to use in the cleaned email's header.
    """
    if date_str:
        try:
            date_obj = email.utils.parsedate_to_datetime(date_str)
            return date_obj.strftime("%Y-%m-%d")
        except Exception as e:
            print(f"Error parsing date: {e}")
            return "Unknown"
    else:
        return "Unknown"


def format_subject(subject_str):
    """
    Format the subject line for use in the email filename.
    """
    if not subject_str:
        return "None"
    subj_list = []
    puncts = {
        ",",
        " ",
        ".",
        "—",
        "-",
        "'",
        '"',
        ":",
        ";",
        "!",
        "?",
        "(",
        ")",
        "/",
        "\\",
    }
    for char in subject_str:
        if char in puncts:
            continue
        elif char == " ":
            subj_list.append("_")
        else:
            subj_list.append(char.lower())

    return "".join(subj_list)


def get_attachments(msg, attachments_dir, date, message_id):
    """
    Download any attachments to the email and return a list of them.
    """
    attachments = []
    attachments_path = Path(attachments_dir)

    if not msg.is_multipart():
        return attachments

    for part in msg.iter_parts():
        if part.get_content_disposition() != "attachment" or not part.get_filename:
            continue
        filename = part.get_filename()
        print(f"Found attachment: {filename}")

        prefixed_filename = f"{date}__{message_id}__{filename}"
        attachments.append(prefixed_filename)

        filepath = attachments_path / prefixed_filename
        with open(filepath, "wb") as attachment_file:
            attachment_file.write(part.get_payload(decode=True))

    return attachments


def get_body(msg):
    """
    Get and return the message body as a string.
    """
    if not msg.is_multipart():
        charset = msg.get_content_charset() or "utf-8"
        return msg.get_payload(decode=True).decode(charset, errors="replace")

    plain_text = None

    for part in msg.walk():
        content_type = part.get_content_type()
        charset = part.get_content_charset() or "utf-8"

        if content_type == "text/plain":
            plain_text = part.get_payload(decode=True).decode(charset, errors="replace")
            break

    return (
        plain_text.split("\nOn ")[0]
        if plain_text
        else "This email has no text in the body."
    )


def build_email_content(raw_file, date, subject, to, from_, attachments, body):
    """
    Construct and return one big email string from all its component parts.
    """
    email_content = (
        f"***{raw_file}***\nDATE: {date}\nSUBJECT: {subject}\nTO: {to}\nFROM: {from_}\n"
    )

    if attachments:
        email_content += "ATTACHMENTS:\n"
        for attachment in attachments:
            email_content += f"- {attachment}\n"

    email_content += f"\n{body}"
    return email_content
