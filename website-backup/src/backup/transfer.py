from ftplib import FTP
import os

def transfer_to_ftp(local_file_path, remote_file_path, ftp_server, ftp_user, ftp_password):
    """Transfer a file to an FTP server."""
    with FTP(ftp_server) as ftp:
        ftp.login(user=ftp_user, passwd=ftp_password)
        with open(local_file_path, 'rb') as file:
            ftp.storbinary(f'STOR {remote_file_path}', file)

def transfer_to_s3(local_file_path, bucket_name, s3_file_path, s3_client):
    """Transfer a file to an S3 bucket."""
    s3_client.upload_file(local_file_path, bucket_name, s3_file_path)

def transfer_backup(local_backup_dir, remote_storage, storage_credentials):
    """Transfer backups to the specified remote storage."""
    for filename in os.listdir(local_backup_dir):
        local_file_path = os.path.join(local_backup_dir, filename)
        if os.path.isfile(local_file_path):
            if remote_storage == 'ftp':
                transfer_to_ftp(local_file_path, filename, **storage_credentials)
            elif remote_storage == 's3':
                transfer_to_s3(local_file_path, **storage_credentials)