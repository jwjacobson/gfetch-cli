from app import create_dirs


def test_create_dirs_dont_exist(fake_dir_config_paths_only):
    raw_path = fake_dir_config_paths_only.RAW_EMAIL_DIR
    clean_path = fake_dir_config_paths_only.CLEAN_EMAIL_DIR
    attachments_path=fake_dir_config_paths_only.ATTACHMENTS_DIR

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
    attachments_path=fake_dir_config.ATTACHMENTS_DIR

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