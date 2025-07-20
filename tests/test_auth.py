import pytest
from unittest.mock import Mock, patch, mock_open
from auth import get_credentials


@patch('pathlib.Path.exists')
@patch('auth.Credentials.from_authorized_user_file')
def test_get_credentials_token_valid(mock_from_file, mock_exists):
    mock_exists.return_value = True
    mock_creds = Mock()
    mock_creds.valid = True
    mock_from_file.return_value = mock_creds
    
    result = get_credentials()
    
    assert result == mock_creds
    mock_from_file.assert_called_once()


@patch('pathlib.Path.exists')
@patch('auth.InstalledAppFlow.from_client_secrets_file')
@patch('builtins.open', mock_open())
def test_get_credentials_no_token(mock_flow, mock_exists):
    mock_exists.return_value = False
    mock_flow_instance = Mock()
    mock_new_creds = Mock()
    mock_new_creds.to_json.return_value = '{"token": "new_token"}'
    mock_flow_instance.run_local_server.return_value = mock_new_creds
    mock_flow.return_value = mock_flow_instance
    
    result = get_credentials()
    
    mock_flow.assert_called_once()
    mock_flow_instance.run_local_server.assert_called_once_with(port=0)
    assert result == mock_new_creds