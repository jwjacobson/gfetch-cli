import pytest

from gfetch.app import (
    create_dirs,
    delete_files,
    creds_check
)

def test_create_dirs_dont_exist(fake_dir_config_paths_only):
    raw_path = fake_dir_config_paths_only.RAW_EMAIL_DIR
    clean_path = fake_dir_config_paths_only.CLEAN_EMAIL_DIR
    attachments_path = fake_dir_config_paths_only.ATTACHMENTS_DIR

    assert not raw_path.exists()
    assert not clean_path.exists()
    assert not attachments_path.exists()

    create_dirs(fake_dir_config_paths_only)

    assert raw_path.exists()
    assert clean_path.exists()
    assert attachments_path.exists()

    assert raw_path.is_dir()
    assert clean_path.is_dir()
    assert attachments_path.is_dir()

    assert not any(raw_path.iterdir())
    assert not any(clean_path.iterdir())
    assert not any(attachments_path.iterdir())


def test_create_dirs_already_exist(fake_dir_config):
    raw_path = fake_dir_config.RAW_EMAIL_DIR
    clean_path = fake_dir_config.CLEAN_EMAIL_DIR
    attachments_path = fake_dir_config.ATTACHMENTS_DIR

    assert raw_path.exists()
    assert clean_path.exists()
    assert attachments_path.exists()

    create_dirs(fake_dir_config)

    assert raw_path.exists()
    assert clean_path.exists()
    assert attachments_path.exists()

    assert raw_path.is_dir()
    assert clean_path.is_dir()
    assert attachments_path.is_dir()

    assert not any(raw_path.iterdir())
    assert not any(clean_path.iterdir())
    assert not any(attachments_path.iterdir())

def test_creds_check_no_creds(fake_dir_config, capsys):
    with pytest.raises(SystemExit) as exit:
        creds_check(fake_dir_config)
    
    assert exit.value.code == 1
    output = capsys.readouterr().out
    assert "No credentials file" in output
    assert "generate credentials first" in output
    assert "github.com/jwjacobson/gfetch-cli"

def test_delete_files_all(fake_dir_config, temp_files_all, capsys):
    raw_path = fake_dir_config.RAW_EMAIL_DIR
    clean_path = fake_dir_config.CLEAN_EMAIL_DIR
    attachments_path = fake_dir_config.ATTACHMENTS_DIR
    expected_output = "Deleted 2 emails and 2 attachments."

    assert any(raw_path.iterdir())
    assert any(clean_path.iterdir())
    assert any(attachments_path.iterdir())

    delete_files(fake_dir_config)

    assert not any(raw_path.iterdir())
    assert not any(clean_path.iterdir())
    assert not any(attachments_path.iterdir())

    output = capsys.readouterr().out.rstrip()
    assert output == expected_output


def test_delete_files_no_attachments(
    fake_dir_config, temp_files_no_attachments, capsys
):
    raw_path = fake_dir_config.RAW_EMAIL_DIR
    clean_path = fake_dir_config.CLEAN_EMAIL_DIR
    attachments_path = fake_dir_config.ATTACHMENTS_DIR
    expected_status = "No attachments found."
    expected_output = "Deleted 2 emails."

    assert any(raw_path.iterdir())
    assert any(clean_path.iterdir())
    assert not any(attachments_path.iterdir())

    delete_files(fake_dir_config)

    assert not any(raw_path.iterdir())
    assert not any(clean_path.iterdir())
    assert not any(attachments_path.iterdir())

    output = capsys.readouterr().out.rstrip().split("\n")
    assert output[0] == expected_status
    assert output[1] == expected_output


def test_delete_files_no_clean(fake_dir_config, temp_files_no_clean, capsys):
    raw_path = fake_dir_config.RAW_EMAIL_DIR
    clean_path = fake_dir_config.CLEAN_EMAIL_DIR
    attachments_path = fake_dir_config.ATTACHMENTS_DIR
    expected_status = "No cleaned emails found."
    expected_output = "Deleted 2 attachments."

    assert any(raw_path.iterdir())
    assert not any(clean_path.iterdir())
    assert any(attachments_path.iterdir())

    delete_files(fake_dir_config)

    assert not any(raw_path.iterdir())
    assert not any(clean_path.iterdir())
    assert not any(attachments_path.iterdir())

    output = capsys.readouterr().out.rstrip().split("\n")
    assert output[0] == expected_status
    assert output[1] == expected_output


def test_delete_files_no_raw(fake_dir_config, temp_files_no_raw, capsys):
    raw_path = fake_dir_config.RAW_EMAIL_DIR
    clean_path = fake_dir_config.CLEAN_EMAIL_DIR
    attachments_path = fake_dir_config.ATTACHMENTS_DIR
    expected_status = "No raw emails found."
    expected_output = "Deleted 2 emails and 2 attachments."

    assert not any(raw_path.iterdir())
    assert any(clean_path.iterdir())
    assert any(attachments_path.iterdir())

    delete_files(fake_dir_config)

    assert not any(raw_path.iterdir())
    assert not any(clean_path.iterdir())
    assert not any(attachments_path.iterdir())

    output = capsys.readouterr().out.rstrip().split("\n")
    assert output[0] == expected_status
    assert output[1] == expected_output


def test_delete_files_only_attachments(
    fake_dir_config, temp_files_only_attachments, capsys
):
    raw_path = fake_dir_config.RAW_EMAIL_DIR
    clean_path = fake_dir_config.CLEAN_EMAIL_DIR
    attachments_path = fake_dir_config.ATTACHMENTS_DIR
    expected_status_1 = "No raw emails found."
    expected_status_2 = "No cleaned emails found."
    expected_output = "Deleted 2 attachments."

    assert not any(raw_path.iterdir())
    assert not any(clean_path.iterdir())
    assert any(attachments_path.iterdir())

    delete_files(fake_dir_config)

    assert not any(raw_path.iterdir())
    assert not any(clean_path.iterdir())
    assert not any(attachments_path.iterdir())

    output = capsys.readouterr().out.rstrip().split("\n")
    assert expected_status_1 in output
    assert expected_status_2 in output
    assert output[-1] == expected_output


def test_delete_files_only_clean(fake_dir_config, temp_files_only_clean, capsys):
    raw_path = fake_dir_config.RAW_EMAIL_DIR
    clean_path = fake_dir_config.CLEAN_EMAIL_DIR
    attachments_path = fake_dir_config.ATTACHMENTS_DIR
    expected_status_1 = "No raw emails found."
    expected_status_2 = "No attachments found."
    expected_output = "Deleted 2 emails."

    assert not any(raw_path.iterdir())
    assert any(clean_path.iterdir())
    assert not any(attachments_path.iterdir())

    delete_files(fake_dir_config)

    assert not any(raw_path.iterdir())
    assert not any(clean_path.iterdir())
    assert not any(attachments_path.iterdir())

    output = capsys.readouterr().out.rstrip().split("\n")
    assert expected_status_1 in output
    assert expected_status_2 in output
    assert output[-1] == expected_output


def test_delete_files_only_raw(fake_dir_config, temp_files_only_raw, capsys):
    raw_path = fake_dir_config.RAW_EMAIL_DIR
    clean_path = fake_dir_config.CLEAN_EMAIL_DIR
    attachments_path = fake_dir_config.ATTACHMENTS_DIR
    expected_status_1 = "No cleaned emails found."
    expected_status_2 = "No attachments found."

    assert any(raw_path.iterdir())
    assert not any(clean_path.iterdir())
    assert not any(attachments_path.iterdir())

    delete_files(fake_dir_config)

    assert not any(raw_path.iterdir())
    assert not any(clean_path.iterdir())
    assert not any(attachments_path.iterdir())

    output = capsys.readouterr().out.rstrip().split("\n")
    assert expected_status_1 in output
    assert expected_status_2 in output
