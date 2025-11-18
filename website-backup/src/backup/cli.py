import click
from backup.main import initiate_backup, restore_backup

@click.group()
def cli():
    """Command Line Interface for the Website Backup application."""
    pass

@cli.command()
@click.option('--config', default='configs/default.yaml', help='Path to the configuration file.')
def backup(config):
    """Initiate a backup process."""
    initiate_backup(config)

@cli.command()
@click.option('--backup-id', required=True, help='ID of the backup to restore.')
def restore(backup_id):
    """Restore a backup using the specified backup ID."""
    restore_backup(backup_id)

if __name__ == '__main__':
    cli()