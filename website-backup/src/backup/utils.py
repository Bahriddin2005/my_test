def log_message(message):
    # Function to log messages to the console
    print(f"[LOG] {message}")

def handle_error(error):
    # Function to handle errors
    print(f"[ERROR] {error}")

def validate_backup_path(path):
    # Function to validate the backup path
    import os
    if not os.path.exists(path):
        handle_error(f"Backup path '{path}' does not exist.")
        return False
    return True

def format_timestamp(timestamp):
    # Function to format timestamps for backup file names
    return timestamp.strftime("%Y%m%d_%H%M%S")