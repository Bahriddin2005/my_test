#!/bin/bash

# Define variables
BACKUP_DIR="/path/to/backup/directory"
SOURCE_DIR="/path/to/website/directory"
TIMESTAMP=$(date +"%Y%m%d%H%M%S")
BACKUP_FILE="backup_$TIMESTAMP.tar.gz"

# Create backup
echo "Starting backup of $SOURCE_DIR to $BACKUP_DIR/$BACKUP_FILE"
tar -czf "$BACKUP_DIR/$BACKUP_FILE" -C "$SOURCE_DIR" .

# Check if the backup was successful
if [ $? -eq 0 ]; then
    echo "Backup completed successfully: $BACKUP_DIR/$BACKUP_FILE"
else
    echo "Backup failed!"
    exit 1
fi

# Optional: Remove backups older than 7 days
find "$BACKUP_DIR" -type f -name "backup_*.tar.gz" -mtime +7 -exec rm {} \;
echo "Old backups removed."