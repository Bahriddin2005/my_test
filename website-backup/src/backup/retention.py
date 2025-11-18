class BackupRetention:
    def __init__(self, retention_days):
        self.retention_days = retention_days

    def should_delete(self, backup_date):
        from datetime import datetime, timedelta
        return (datetime.now() - backup_date).days > self.retention_days

    def delete_old_backups(self, backups):
        return [backup for backup in backups if not self.should_delete(backup['date'])]