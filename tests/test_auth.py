from unittest.mock import Mock, patch, mock_open

from gfetch.auth import get_credentials


@patch("pathlib.Path.exists")
@patch("gfetch.auth.Credentials.from_authorized_user_file")
def test_get_credentials_token_valid(mock_from_file, mock_exists):
    mock_exists.return_value = True
    mock_creds = Mock()
    mock_creds.valid = True
    mock_from_file.return_value = mock_creds

    result = get_credentials()

    assert result == mock_creds
    mock_from_file.assert_called_once()


@patch("pathlib.Path.exists")
@patch("gfetch.auth.InstalledAppFlow.from_client_secrets_file")
@patch("builtins.open", mock_open())
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


@patch("pathlib.Path.exists")
@patch("gfetch.auth.Credentials.from_authorized_user_file")
@patch("gfetch.auth.Request")
def test_get_credentials_expired(mock_request, mock_from_file, mock_exists):
    mock_exists.return_value = True
    mock_creds = Mock()
    mock_creds.valid = False
    mock_creds.expired = True
    mock_creds.refresh_token = "some_refresh_token"
    mock_from_file.return_value = mock_creds

    def refresh_side_effect(request):
        mock_creds.valid = True

    mock_creds.refresh.side_effect = refresh_side_effect

    result = get_credentials()

    mock_from_file.assert_called_once()
    mock_creds.refresh.assert_called_once()
    assert result == mock_creds


@patch("pathlib.Path.exists")
@patch("gfetch.auth.Credentials.from_authorized_user_file")
@patch("gfetch.auth.InstalledAppFlow.from_client_secrets_file")
@patch("builtins.open", mock_open())
def test_get_credentials_cannot_load_token(mock_flow, mock_from_file, mock_exists, capsys):
    mock_exists.return_value = True
    mock_from_file.side_effect = Exception("Failed to load credentials")
    
    mock_flow_instance = Mock()
    mock_new_creds = Mock()
    mock_new_creds.to_json.return_value = '{"token": "new_token"}'
    mock_flow_instance.run_local_server.return_value = mock_new_creds
    mock_flow.return_value = mock_flow_instance

    result = get_credentials()

    output = capsys.readouterr().out.rstrip()
    assert output == "Error loading credentials: Failed to load credentials"
    mock_flow.assert_called_once()
    assert result == mock_new_creds


@patch("pathlib.Path.exists")
@patch("gfetch.auth.Credentials.from_authorized_user_file")
@patch("gfetch.auth.Request")
@patch("gfetch.auth.InstalledAppFlow.from_client_secrets_file")
@patch("builtins.open", mock_open())
def test_get_credentials_bad_refresh(mock_flow, mock_request, mock_from_file, mock_exists, capsys):
    mock_exists.return_value = True
    mock_creds = Mock()
    mock_creds.valid = False
    mock_creds.expired = True
    mock_creds.refresh_token = "Token"
    mock_from_file.return_value = mock_creds
    mock_creds.refresh.side_effect = Exception("Failed to refresh")
    mock_token = Mock()
    mock_token.unlink = Mock()
    mock_flow_instance = Mock()
    mock_new_creds = Mock()
    mock_new_creds.to_json.return_value = '{"token": "new_token"}'
    mock_flow_instance.run_local_server.return_value = mock_new_creds
    mock_flow.return_value = mock_flow_instance

    with patch("gfetch.auth.TOKEN", mock_token):
        result = get_credentials()

    output = capsys.readouterr().out.rstrip()
    assert output == "Error refreshing credentials: Failed to refresh"
    mock_token.unlink.assert_called_once()
    mock_flow.assert_called_once()
    assert result == mock_new_creds


@patch("pathlib.Path.exists")
@patch("gfetch.auth.InstalledAppFlow.from_client_secrets_file")
def test_get_credentials_bad_oauth_flow(mock_flow, mock_exists, capsys):
    mock_exists.return_value = False
    mock_flow.side_effect = Exception("OAuth flow failed")

    result = get_credentials()

    output = capsys.readouterr().out.rstrip()
    assert output == "Error during OAuth flow: OAuth flow failed"
    assert result is None