import pytest
from src.backup.storage import BackupStorage

@pytest.fixture
def storage():
    return BackupStorage()

def test_save_backup(storage):
    # Arrange
    backup_data = b'Test backup data'
    backup_name = 'test_backup.zip'

    # Act
    storage.save_backup(backup_name, backup_data)

    # Assert
    assert storage.exists(backup_name) is True

def test_retrieve_backup(storage):
    # Arrange
    backup_data = b'Test backup data'
    backup_name = 'test_backup.zip'
    storage.save_backup(backup_name, backup_data)

    # Act
    retrieved_data = storage.retrieve_backup(backup_name)

    # Assert
    assert retrieved_data == backup_data

def test_delete_backup(storage):
    # Arrange
    backup_name = 'test_backup.zip'
    storage.save_backup(backup_name, b'Test backup data')

    # Act
    storage.delete_backup(backup_name)

    # Assert
    assert storage.exists(backup_name) is False

def test_list_backups(storage):
    # Arrange
    storage.save_backup('backup1.zip', b'Test data 1')
    storage.save_backup('backup2.zip', b'Test data 2')

    # Act
    backups = storage.list_backups()

    # Assert
    assert 'backup1.zip' in backups
    assert 'backup2.zip' in backups