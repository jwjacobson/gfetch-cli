from app import create_dirs


def test_create_dirs(fake_dir_config_paths_only):
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