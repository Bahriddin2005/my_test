from pathlib import Path
import json

class StorageManager:
    def __init__(self, backup_directory):
        self.backup_directory = Path(backup_directory)
        self.backup_directory.mkdir(parents=True, exist_ok=True)

    def save_backup(self, backup_name, data):
        backup_file = self.backup_directory / f"{backup_name}.json"
        with open(backup_file, 'w') as f:
            json.dump(data, f)

    def retrieve_backup(self, backup_name):
        backup_file = self.backup_directory / f"{backup_name}.json"
        if backup_file.exists():
            with open(backup_file, 'r') as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"No backup found with the name: {backup_name}")

    def list_backups(self):
        return [f.stem for f in self.backup_directory.glob("*.json")]