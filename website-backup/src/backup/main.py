import os
import shutil
import logging
import yaml

class BackupManager:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.backup_dir = self.config.get('backup_directory', './backups')
        self.setup_logging()

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def create_backup(self, source_directory):
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            logging.info(f'Created backup directory: {self.backup_dir}')

        backup_name = f'backup_{self.get_current_timestamp()}.zip'
        backup_path = os.path.join(self.backup_dir, backup_name)

        shutil.make_archive(backup_path.replace('.zip', ''), 'zip', source_directory)
        logging.info(f'Backup created: {backup_path}')

    def get_current_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime('%Y%m%d_%H%M%S')

    def restore_backup(self, backup_name, restore_directory):
        backup_path = os.path.join(self.backup_dir, backup_name)
        if os.path.exists(backup_path):
            shutil.unpack_archive(backup_path, restore_directory)
            logging.info(f'Restored backup from: {backup_path} to {restore_directory}')
        else:
            logging.error(f'Backup not found: {backup_path}')

if __name__ == '__main__':
    backup_manager = BackupManager('configs/default.yaml')
    # Example usage
    # backup_manager.create_backup('/path/to/website')
    # backup_manager.restore_backup('backup_20230101_120000.zip', '/path/to/restore')