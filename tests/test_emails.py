import base64
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from email import policy
from email.parser import BytesParser


from emails import (
    build_email_content,
    clean_email,
    fetch_emails,
    format_subject,
    get_attachments,
    get_messages_and_next_page,
    get_body,
    process_message_batch,
    set_date,
)


@pytest.fixture()
def no_attachments():
    """
    Read and yield a raw email file with no attachments.
    """
    filename = "no_attachments.eml"
    raw_email_path = Path(__file__).parent / "raw_emails" / filename

    with open(raw_email_path, "rb") as raw_email:
        message = BytesParser(policy=policy.default).parse(raw_email)
        message_id = 'test_id_01'
        yield message, filename, raw_email_path, message_id


@pytest.fixture()
def one_attachment():
    """
    Read and yield a raw email file with one attachment.
    """

    filename = "one_attachment.eml"
    raw_email_path = Path(__file__).parent / "raw_emails" / filename

    with open(raw_email_path, "rb") as raw_email:
        message = BytesParser(policy=policy.default).parse(raw_email)
        message_id = 'test_id_10'
        yield message, filename, raw_email_path, message_id


@pytest.fixture()
def many_attachments():
    """
    Read and yield a raw email file with many attachments.
    """
    filename = "many_attachments.eml"
    raw_email_path = Path(__file__).parent / "raw_emails" / filename

    with open(raw_email_path, "rb") as raw_email:
        message = BytesParser(policy=policy.default).parse(raw_email)
        message_id = 'test_id_11'
        yield message, filename, raw_email_path, message_id


@pytest.fixture()
def no_subject():
    """
    Read and yield a raw email file with no subject.
    """
    filename = "no_subject.eml"
    raw_email_path = Path(__file__).parent / "raw_emails" / filename

    with open(raw_email_path, "rb") as raw_email:
        message = BytesParser(policy=policy.default).parse(raw_email)
        message_id = 'test_id_11'
        yield message, filename, raw_email_path, message_id

@pytest.fixture()
def no_date():
    """
    Read and yield a raw email file with no date.
    """
    filename = "bad_date.eml"
    raw_email_path = Path(__file__).parent / "raw_emails" / filename

    with open(raw_email_path, "rb") as raw_email:
        message = BytesParser(policy=policy.default).parse(raw_email)
        message_id = 'test_id_11'
        yield message, filename, raw_email_path, message_id


def test_set_date_normal(no_attachments):
    message = no_attachments[0]
    raw_date = message["Date"]
    result = set_date(raw_date)
    expected = "2013-07-05"

    assert result == expected

def test_set_date_no_date(no_date):
    message = no_date[0]
    raw_date = message["Date"]
    result = set_date(raw_date)
    expected = "Unknown"

    assert result == expected

def test_format_subject_re_only(no_attachments):
    message = no_attachments[0]
    subject = message["Subject"]
    result = format_subject(subject)
    expected = "re"

    assert result == expected


def test_format_subject_normal_text_no_caps(one_attachment):
    message = one_attachment[0]
    subject = message["Subject"]
    result = format_subject(subject)
    expected = "beautifulandstunning"

    assert result == expected


def test_format_subject_no_subject(no_subject):
    message = no_subject[0]
    subject = message["Subject"]
    expected = 'None'

    assert subject == ""
    result = format_subject(subject)
    assert result == 'None'


def test_get_attachments_no_attachments(no_attachments, temp_dirs):
    message = no_attachments[0]
    message_id = no_attachments[3]
    attachments_dir = temp_dirs["attachments_dir"]
    date = set_date(message["Date"])  # Get the date from the message
    
    result = get_attachments(message, attachments_dir, date, message_id)
    expected = []

    assert result == expected
    assert not list(Path(attachments_dir).iterdir())


def test_get_attachments_one_attachment(one_attachment, temp_dirs):
    message = one_attachment[0]
    message_id = one_attachment[3]
    attachments_dir = temp_dirs["attachments_dir"]
    date = set_date(message["Date"])  # Get the date from the message
    
    result = get_attachments(message, attachments_dir, date, message_id)
    expected = [f"{date}__{message_id}__beautifulandstunning.png"]

    assert result == expected
    assert len(result) == 1
    
    attachments_path = Path(attachments_dir)
    dir_files = [f.name for f in attachments_path.iterdir()]
    assert len(dir_files) == 1
    
    for file in result:
        assert file in dir_files
    for file in dir_files:
        assert file in expected


def test_get_attachments_many_attachments(many_attachments, temp_dirs):
    message = many_attachments[0]
    message_id = many_attachments[3]
    attachments_dir = temp_dirs["attachments_dir"]
    date = set_date(message["Date"])  # Get the date from the message
    
    result = get_attachments(message, attachments_dir, date, message_id)
    expected = [
        f"{date}__{message_id}__ADVICE TO NEW TEACHERS.pdf",
        f"{date}__{message_id}__CREDULOUDLY RAPT.pdf",
        f"{date}__{message_id}__HOW TO GRADE IMPERSONALLY.pdf",
        f"{date}__{message_id}__I'D RATHER SPEND NEW YEAR'S IN A BARN.pdf",
        f"{date}__{message_id}__THE DISASTER ODDS.pdf",
        f"{date}__{message_id}__TRESSPASSING AT THE PUMPING STATION.pdf",
    ]

    assert result == expected
    assert len(result) == 6
    
    attachments_path = Path(attachments_dir)
    dir_files = [f.name for f in attachments_path.iterdir()]
    assert len(dir_files) == 6
    
    for file in result:
        assert file in dir_files
    for file in dir_files:
        assert file in expected

def test_get_body_happy(no_attachments):
    message = no_attachments[0]
    result = get_body(message)
    expected = "Hey Will,\n\nJust wanted to confirm our plans for later.\n\nLet me know,\nStu\n\n"
    assert result == expected

def test_get_body_nested(many_attachments):
    message = many_attachments[0]
    result = get_body(message)
    expected = 'Just some drafts.\n'

    assert result == expected


def test_build_email_content_no_attachments(no_attachments, temp_dirs):
    message, raw_file = no_attachments[0], no_attachments[1]
    message_id = no_attachments[3]
    date = set_date(message["Date"])
    subject = message["Subject"]
    to = message["To"]
    from_ = message["From"]
    attachments = get_attachments(message, temp_dirs["attachments_dir"], date, message_id)
    body = get_body(message)

    result = build_email_content(raw_file, date, subject, to, from_, attachments, body)
    expected = "***no_attachments.eml***\nDATE: 2013-07-05\nSUBJECT: Re:\nTO: Will Jakobson <will@jmail.com>\nFROM: Stu Bettler <stu@bmail.com>\n\nHey Will,\n\nJust wanted to confirm our plans for later.\n\nLet me know,\nStu\n\n"

    assert result == expected


def test_build_email_content_one_attachment(one_attachment, temp_dirs):
    message, raw_file = one_attachment[0], one_attachment[1]
    message_id = one_attachment[3]
    date = set_date(message["Date"])
    subject = message["Subject"]
    to = message["To"]
    from_ = message["From"]
    attachments = get_attachments(message, temp_dirs["attachments_dir"], date, message_id)
    body = get_body(message)

    result = build_email_content(raw_file, date, subject, to, from_, attachments, body)
    expected = f"***one_attachment.eml***\nDATE: 2011-07-10\nSUBJECT: beautiful and stunning\nTO: stu bettler <stu@bmail.com>\nFROM: Will Jakobson <will@jmail.com>\nATTACHMENTS:\n- {date}__{message_id}__beautifulandstunning.png\n\ni just saw this.  made me chuckle, and reminded me of writing alone.\n"

    assert result == expected


def test_build_email_content_many_attachments(many_attachments, temp_dirs):
    message, raw_file = many_attachments[0], many_attachments[1]
    message_id = many_attachments[3]
    date = set_date(message["Date"])
    subject = message["Subject"]
    to = message["To"]
    from_ = message["From"]
    attachments = get_attachments(message, temp_dirs["attachments_dir"], date, message_id)
    body = get_body(message)

    result = build_email_content(raw_file, date, subject, to, from_, attachments, body)
    expected = f"***many_attachments.eml***\nDATE: 2015-06-19\nSUBJECT: Revisions\nTO: Stu Bettler <stu@bmail.com>, Will Jakobson <will@jmail.com>\nFROM: Stu Bettler <stu@bmail.com>\nATTACHMENTS:\n- {date}__{message_id}__ADVICE TO NEW TEACHERS.pdf\n- {date}__{message_id}__CREDULOUDLY RAPT.pdf\n- {date}__{message_id}__HOW TO GRADE IMPERSONALLY.pdf\n- {date}__{message_id}__I'D RATHER SPEND NEW YEAR'S IN A BARN.pdf\n- {date}__{message_id}__THE DISASTER ODDS.pdf\n- {date}__{message_id}__TRESSPASSING AT THE PUMPING STATION.pdf\n\nJust some drafts.\n"

    assert result == expected


def test_build_email_content_no_subject(no_subject, temp_dirs):
    message, raw_file = no_subject[0], no_subject[1]
    message_id = no_subject[3]
    date = set_date(message["Date"])
    subject = message["Subject"]
    to = message["To"]
    from_ = message["From"]
    attachments = get_attachments(message, temp_dirs["attachments_dir"], date, message_id)
    body = get_body(message)

    result = build_email_content(raw_file, date, subject, to, from_, attachments, body)
    expected = '***no_subject.eml***\nDATE: 2010-01-06\nSUBJECT: \nTO: stu@bmail.com\nFROM: Will Jakobson <will@jmail.com>\n\nGreetings from the tropics!\n'

    assert result == expected


def test_clean_email_no_attachments(no_attachments, fake_dir_config):
    filepath = no_attachments[2]
    message_id = no_attachments[3]
    expected_filename = '2013-07-05__re__test_id_01.txt'
    
    clean_path = fake_dir_config.CLEAN_EMAIL_DIR
    assert not list(clean_path.iterdir())  # Make sure the target directory is empty for comparison
    
    clean_email(filepath, fake_dir_config, message_id)

    dir_files = [f.name for f in clean_path.iterdir()]
    assert len(dir_files) == 1
    assert expected_filename in dir_files
    assert not list(fake_dir_config.ATTACHMENTS_DIR.iterdir())


def test_clean_email_one_attachment(one_attachment, fake_dir_config):
    filepath = one_attachment[2]
    message_id = one_attachment[3]
    expected_email_filename = '2011-07-10__beautifulandstunning__test_id_10.txt'
    expected_attachment_filename = '2011-07-10__test_id_10__beautifulandstunning.png'
    
    clean_path = fake_dir_config.CLEAN_EMAIL_DIR
    attachments_path = fake_dir_config.ATTACHMENTS_DIR
    
    assert not list(clean_path.iterdir())  # Make sure the target directories are empty for comparison
    assert not list(attachments_path.iterdir())

    clean_email(filepath, fake_dir_config, message_id)

    clean_files = [f.name for f in clean_path.iterdir()]
    attachment_files = [f.name for f in attachments_path.iterdir()]
    
    assert len(clean_files) == 1
    assert len(attachment_files) == 1
    assert expected_email_filename in clean_files
    assert expected_attachment_filename in attachment_files


def test_clean_email_many_attachments(many_attachments, fake_dir_config):
    filepath = many_attachments[2]
    message_id = many_attachments[3]
    expected_email_filename = '2015-06-19__revisions__test_id_11.txt'
    expected_attachment_filenames = [
        "2015-06-19__test_id_11__ADVICE TO NEW TEACHERS.pdf",
        "2015-06-19__test_id_11__CREDULOUDLY RAPT.pdf",
        "2015-06-19__test_id_11__HOW TO GRADE IMPERSONALLY.pdf",
        "2015-06-19__test_id_11__I'D RATHER SPEND NEW YEAR'S IN A BARN.pdf",
        "2015-06-19__test_id_11__THE DISASTER ODDS.pdf",
        "2015-06-19__test_id_11__TRESSPASSING AT THE PUMPING STATION.pdf",
    ]

    clean_path = fake_dir_config.CLEAN_EMAIL_DIR
    attachments_path = fake_dir_config.ATTACHMENTS_DIR

    assert not list(clean_path.iterdir())  # Make sure the target directories are empty for comparison
    assert not list(attachments_path.iterdir())

    clean_email(filepath, fake_dir_config, message_id)

    clean_files = [f.name for f in clean_path.iterdir()]
    attachment_files = [f.name for f in attachments_path.iterdir()]
    
    assert len(clean_files) == 1
    assert len(attachment_files) == 6
    assert expected_email_filename in clean_files
    for filename in expected_attachment_filenames:
        assert filename in attachment_files



def test_get_messages_and_next_page_no_token():
    mock_service = Mock()
    query = "queequeg@pequod.com"
    mock_response = {
        "messages": [{"id": "123"}, {"id": "456"}],
        "nextPageToken": "Token"
    }
    mock_list = mock_service.users().messages().list
    mock_list.return_value.execute.return_value = mock_response
    
    messages, next_token = get_messages_and_next_page(mock_service, query)
    
    mock_list.assert_called_once_with(userId="me", q=query)
    assert len(messages) == 2
    assert next_token == "Token"

def test_get_messages_and_next_page_token():
    mock_service = Mock()
    query = "queequeg@pequod.com"
    page_token = "Token"
    mock_response = {
        "messages": [{"id": "123"}],
        "nextPageToken": None
    }
    mock_list = mock_service.users().messages().list
    mock_list.return_value.execute.return_value = mock_response

    messages, next_token = get_messages_and_next_page(mock_service, query, page_token)
    
    mock_service.users().messages().list.assert_called_once_with(
        userId="me", q=query, pageToken=page_token
    )
    assert len(messages) == 1
    assert next_token is None

def test_get_messages_and_next_page_empty_response():
    mock_service = Mock()
    query = "queequeg@pequod.com"
    mock_response = {}
    mock_service.users().messages().list().execute.return_value = mock_response
    
    messages, next_token = get_messages_and_next_page(mock_service, query)
    
    assert messages == []
    assert next_token is None

def test_get_messages_and_next_page_no_messages():
    mock_service = Mock()
    query = "queequeg@pequod.com"
    mock_response = {"nextPageToken": "Token"}
    mock_service.users().messages().list().execute.return_value = mock_response
    
    messages, next_token = get_messages_and_next_page(mock_service, query)
    
    assert messages == []
    assert next_token == "Token"

def test_get_messages_and_next_page_no_response_token():
    mock_service = Mock()
    query = "queequeg@pequod.com"
    mock_response = {"messages": [{"id": "123"}]}
    mock_service.users().messages().list().execute.return_value = mock_response
    
    messages, next_token = get_messages_and_next_page(mock_service, query)
    
    assert len(messages) == 1
    assert next_token is None

def test_get_messages_and_next_page_api_error():
    mock_service = Mock()
    query = "queequeg@pequod.com"
    
    mock_service.users().messages().list().execute.side_effect = Exception("API Error")
    
    with pytest.raises(Exception, match="API Error"):
        get_messages_and_next_page(mock_service, query)

def test_get_messages_and_next_page_many_messages():
    mock_service = Mock()
    query = "queequeg@pequod.com"
    mock_messages = [{"id": f"msg_{i}"} for i in range(100)]
    mock_response = {
        "messages": mock_messages,
        "nextPageToken": "Token"
    }
    mock_service.users().messages().list().execute.return_value = mock_response
    
    messages, next_token = get_messages_and_next_page(mock_service, query)
    
    assert len(messages) == 100
    assert next_token == "Token"
    assert messages[0]["id"] == "msg_0"
    assert messages[-1]["id"] == "msg_99"


def test_process_message_batch_no_messages(fake_dir_config):
    mock_service = Mock()
    messages = []

    result = process_message_batch(fake_dir_config, mock_service, messages)

    assert result == 0

def test_process_message_batch_one_message_no_attachments(fake_dir_config):
    mock_service = Mock()
    messages = [{"id": "msg123"}]
    
    mock_raw_response = {
        "raw": base64.urlsafe_b64encode(b"fake email content").decode("ASCII")
    }
    mock_get = mock_service.users().messages().get
    mock_get.return_value.execute.return_value = mock_raw_response

    with patch('emails.clean_email', return_value=0) as mock_clean:
        result = process_message_batch(fake_dir_config, mock_service, messages)
    
    mock_service.users().messages().get.assert_called_once_with(
        userId="me", id="msg123", format="raw"
    )
    mock_clean.assert_called_once()
    assert result == 0

def test_process_message_batch_one_message_attachments(fake_dir_config):
    mock_service = Mock()
    messages = [{"id": "msg456"}]
    mock_raw_response = {
        "raw": base64.urlsafe_b64encode(b"email with attachments").decode("ASCII")
    }
    mock_get = mock_service.users().messages().get
    mock_get.return_value.execute.return_value = mock_raw_response
    
    with patch('emails.clean_email', return_value=3) as mock_clean:
        result = process_message_batch(fake_dir_config, mock_service, messages)
    
    assert result == 3
    mock_clean.assert_called_once()


def test_process_message_batch_many_messages(fake_dir_config):
    mock_service = Mock()
    messages = [
        {"id": "msg123"},
        {"id": "msg456"},
        {"id": "msg789"}
    ]
    
    mock_raw_response = {
        "raw": base64.urlsafe_b64encode(b"sample email").decode("ASCII")
    }
    mock_get = mock_service.users().messages().get
    mock_get.return_value.execute.return_value = mock_raw_response
    
    with patch('emails.clean_email', side_effect=[3, 0, 2]) as mock_clean:
        result = process_message_batch(fake_dir_config, mock_service, messages)
    
    assert mock_get.call_count == 3
    assert mock_clean.call_count == 3
    assert result == 5


@patch('emails.get_credentials', return_value=None)
def test_fetch_emails_no_credentials(mock_get_credentials):
    mock_config = Mock()
    
    result = fetch_emails("queequeg@pequod.com", mock_config)
    
    assert result == {"error": "Failed to obtain credentials."}


@patch('emails.get_credentials', return_value="valid_creds")
@patch('emails.build', side_effect=Exception("Service build failed"))
def test_fetch_emails_no_service(mock_build, mock_get_credentials):
    mock_config = Mock()
 
    result = fetch_emails("queequeg@pequod.com", mock_config)
    
    mock_get_credentials.assert_called_once()
    mock_build.assert_called_once_with("gmail", "v1", credentials="valid_creds")
    assert result == {"error": "Error building Gmail service: Service build failed"}


@patch('emails.get_credentials', return_value="valid_creds")
@patch('emails.build')
@patch('emails.get_messages_and_next_page')
@patch('emails.process_message_batch')
def test_fetch_emails_one_page(mock_process, mock_get_messages, mock_build, mock_get_credentials):
    mock_config = Mock()
    mock_service = Mock()
    mock_build.return_value = mock_service
    mock_get_messages.return_value = ([{"id": "msg123"}, {"id": "msg456"}], None)
    mock_process.return_value = 3
    
    result = fetch_emails("queequeg@pequod.com", mock_config)
    
    mock_get_messages.assert_called_once_with(mock_service, "to:queequeg@pequod.com OR from:queequeg@pequod.com", None)
    mock_process.assert_called_once_with(mock_config, mock_service, [{"id": "msg123"}, {"id": "msg456"}])
    assert result == {"total_messages": 2, "total_attachments": 3}


@patch('emails.get_credentials', return_value="valid_creds")
@patch('emails.build')
@patch('emails.get_messages_and_next_page')
@patch('emails.process_message_batch')
def test_fetch_emails_two_pages(mock_process, mock_get_messages, mock_build, mock_get_creds):
    mock_config = Mock()
    mock_service = Mock()
    mock_build.return_value = mock_service
    mock_get_messages.side_effect = [
        ([{"id": "msg123"}], "Token"),
        ([{"id": "msg456"}, {"id": "msg789"}], None)
    ]
    mock_process.side_effect = [3, 2]

    result = fetch_emails("queequeg@pequod.com", mock_config)
    
    assert mock_get_messages.call_count == 2
    assert mock_process.call_count == 2
    mock_get_messages.assert_any_call(mock_service, "to:queequeg@pequod.com OR from:queequeg@pequod.com", None)
    mock_get_messages.assert_any_call(mock_service, "to:queequeg@pequod.com OR from:queequeg@pequod.com", "Token")
    
    assert result == {"total_messages": 3, "total_attachments": 5}