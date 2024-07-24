from unittest.mock import MagicMock, mock_open
from google.oauth2.credentials import Credentials

from retrieve_emails import get_credentials

def test_get_credentials_happy_path(mocker):
    mocker.patch('os.path.exists', return_value=True)
    mock_open_instance = mock_open(read_data='{"token": "mock_token"}')
    mocker.patch('builtins.open', mock_open_instance)
    mock_creds = MagicMock(spec=Credentials)
    mock_creds.valid = True
    mocker.patch('google.oauth2.credentials.Credentials.from_authorized_user_file', return_value=mock_creds)
    
    creds = get_credentials()
    
    assert creds == mock_creds
