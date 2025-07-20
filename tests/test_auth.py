import pytest
from unittest.mock import Mock, patch, mock_open
from auth import get_credentials


@patch('pathlib.Path.exists')
@patch('auth.Credentials.from_authorized_user_file')
def test_get_credentials_token_exists_valid(mock_from_file, mock_exists):
    mock_exists.return_value = True
    mock_creds = Mock()
    mock_creds.valid = True
    mock_from_file.return_value = mock_creds
    
    result = get_credentials()
    
    assert result == mock_creds
    mock_from_file.assert_called_once()