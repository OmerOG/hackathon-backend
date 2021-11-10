from google.cloud import storage
import os
import json
import utils
from constants import API_KEY_FILE


class SimpleStorageClient:
    def __init__(self, account_json=API_KEY_FILE):
        self.storage_client = storage.Client.from_service_account_json(account_json)

    def download_all_from_bucket(self, bucket_name, destination_folder_name):
        self.bucket = storage.Bucket(self.storage_client, bucket_name)
        all_blobs = list(self.storage_client.list_blobs(self.bucket))
        
        for blob in all_blobs:
            utils.safe_create_directory(destination_folder_name)
            blob.download_to_filename(destination_folder_name + "/" + blob.name)
            print("Saved " + blob.name + " in folder")

    def upload_file_to_bucket(self, bucket_name, file_path):
        self.bucket = storage.Bucket(self.storage_client, bucket_name)
        blob = self.bucket.blob(os.path.basename(file_path))
        blob.upload_from_filename(file_path)
        print("Uploaded " + file_path.name + " to '" + bucket_name + "' bucket")
