#!/bin/bash

# This script restores a website backup from a specified backup file.

# Check if the backup file is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <backup-file>"
    exit 1
fi

BACKUP_FILE=$1

# Check if the backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file '$BACKUP_FILE' not found!"
    exit 1
fi

# Restore the backup
echo "Restoring backup from '$BACKUP_FILE'..."
# Add your restore commands here, for example:
# tar -xzf "$BACKUP_FILE" -C /path/to/restore/location

echo "Backup restored successfully."