import os
import email
lfrom email import policy
from email.parser import BytesParser

OUTPUT_DIR = 'cleaned_emails'

def clean_email_file(email_file):
    """Take an eml file and output a cleaned .txt."""
    with open(email_file, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    date = msg['Date']
    subject = msg['Subject']
    to = msg['To']
    from_ = msg['From']

    body = ""

    if msg.is_multipart():
        for part in msg.iter_parts():
            if part.get_content_type() == 'text/plain':
                charset = part.get_content_charset()
                if charset is None:
                    charset = 'utf-8'
                body = part.get_payload(decode=True).decode(charset, errors='replace')
                break
    else:
        charset = msg.get_content_charset()
        if charset is None:
            charset = 'utf-8'
        body = msg.get_payload(decode=True).decode(charset, errors='replace')

    if not body:
        body = "This email has no body. Maybe it was just an attachment?"

    body = body.split('\nOn ')[0]

    email_content = f"DATE: {date}\nSUBJECT: {subject}\nTO: {to}\nFROM: {from_}\n\n{body}"

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    email_filename = os.path.join(OUTPUT_DIR, os.path.basename(email_file).replace('.eml', '.txt'))
    with open(email_filename, 'w', encoding='utf-8') as f:
        f.write(email_content)
