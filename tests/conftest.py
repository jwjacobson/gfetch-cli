import pytest


@pytest.fixture(scope="function")
def temp_dir_paths(tmp_path):
    """
    Create temporary directory paths.
    """

    return {
        "attachments_dir": tmp_path / "attachments",
        "clean_email_dir": tmp_path / "clean_emails",
        "raw_email_dir": tmp_path / "raw_emails",
    }


@pytest.fixture(scope="function")
def temp_dirs(temp_dir_paths):
    """
    Create temporary directories.
    """

    for path in temp_dir_paths.values():
        path.mkdir()

    return temp_dir_paths


@pytest.fixture
def temp_files_all(temp_dirs):
    """
    Create fake email and attachment files in all temp directories.
    """
    (temp_dirs["attachments_dir"] / "file1.pdf").touch()
    (temp_dirs["attachments_dir"] / "file2.docx").touch()

    (temp_dirs["clean_email_dir"] / "email1.txt").touch()
    (temp_dirs["clean_email_dir"] / "email2.txt").touch()

    (temp_dirs["raw_email_dir"] / "email1.eml").touch()
    (temp_dirs["raw_email_dir"] / "email2.eml").touch()

    return temp_dirs


@pytest.fixture
def temp_files_no_attachments(temp_dirs):
    """
    Create fake email files in email temp directories.
    """
    (temp_dirs["clean_email_dir"] / "email1.txt").touch()
    (temp_dirs["clean_email_dir"] / "email2.txt").touch()

    (temp_dirs["raw_email_dir"] / "email1.eml").touch()
    (temp_dirs["raw_email_dir"] / "email2.eml").touch()

    return temp_dirs


@pytest.fixture
def temp_files_no_clean(temp_dirs):
    """
    Create fake raw email and attachment files in relevant temp directories.
    """
    (temp_dirs["attachments_dir"] / "file1.pdf").touch()
    (temp_dirs["attachments_dir"] / "file2.docx").touch()

    (temp_dirs["raw_email_dir"] / "email1.eml").touch()
    (temp_dirs["raw_email_dir"] / "email2.eml").touch()

    return temp_dirs


@pytest.fixture
def temp_files_no_raw(temp_dirs):
    """
    Create fake clean email and attachment files in relevant temp directories.
    """
    (temp_dirs["attachments_dir"] / "file1.pdf").touch()
    (temp_dirs["attachments_dir"] / "file2.docx").touch()

    (temp_dirs["clean_email_dir"] / "email1.txt").touch()
    (temp_dirs["clean_email_dir"] / "email2.txt").touch()

    return temp_dirs


@pytest.fixture
def temp_files_only_attachments(temp_dirs):
    """
    Create fake attachment files only in the attachment directory.
    """
    (temp_dirs["attachments_dir"] / "file1.pdf").touch()
    (temp_dirs["attachments_dir"] / "file2.docx").touch()

    return temp_dirs


@pytest.fixture
def temp_files_only_clean(temp_dirs):
    """
    Create fake clean email files only in the clean email directory.
    """
    (temp_dirs["clean_email_dir"] / "email1.txt").touch()
    (temp_dirs["clean_email_dir"] / "email2.txt").touch()

    return temp_dirs


@pytest.fixture
def temp_files_only_raw(temp_dirs):
    """
    Create fake raw email files only in the raw email directory.
    """
    (temp_dirs["raw_email_dir"] / "email1.eml").touch()
    (temp_dirs["raw_email_dir"] / "email2.eml").touch()

    return temp_dirs


class FakeDirConfig:
    """
    A DirConfig that points to the temporary test directories.
    """

    def __init__(self, temp_dirs):
        self.BASE_DIR = temp_dirs["raw_email_dir"].parent
        self.RAW_EMAIL_DIR = temp_dirs["raw_email_dir"]
        self.CLEAN_EMAIL_DIR = temp_dirs["clean_email_dir"]
        self.ATTACHMENTS_DIR = temp_dirs["attachments_dir"]
        self.CREDS = self.BASE_DIR / "credentials.json"


@pytest.fixture()
def fake_dir_config(temp_dirs):
    return FakeDirConfig(temp_dirs)


@pytest.fixture()
def fake_dir_config_paths_only(temp_dir_paths):
    return FakeDirConfig(temp_dir_paths)
