from google.cloud import storage
import os
import json
import utils
from constants import API_KEY_FILE


class SimpleStorageClient:
    def __init__(self, bucket_name, account_json=API_KEY_FILE):
        self.storage_client = storage.Client.from_service_account_json(account_json)
        self.bucket = storage.Bucket(self.storage_client, bucket_name)

    def download_all_from_bucket(self, folder_name):
        all_blobs = list(self.storage_client.list_blobs(self.bucket))
        
        for blob in all_blobs:
            utils.safe_create_directory(folder_name)
            blob.download_to_filename(folder_name + "/" + blob.name)
            print("Saved " + blob.name + " in folder")
