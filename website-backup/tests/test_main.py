import unittest
from src.backup.main import initiate_backup, manage_configurations

class TestBackupFunctionality(unittest.TestCase):

    def test_initiate_backup(self):
        result = initiate_backup()
        self.assertTrue(result)  # Assuming initiate_backup returns True on success

    def test_manage_configurations(self):
        config = manage_configurations()
        self.assertIsNotNone(config)  # Ensure configurations are loaded

if __name__ == '__main__':
    unittest.main()