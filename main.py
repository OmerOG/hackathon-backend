from face_cropper import FaceCropper
from simple_storage_client import SimpleStorageClient
import os
from constants import EVENT_BUCKET_NAME, ZIP_BUCKET_NAME
import utils


def main():
    photos_of_people_dict = {}
    storage_client = SimpleStorageClient()
    face_cropper = FaceCropper()

    event_photos_folder = "event_photos"
    storage_client.download_all_from_bucket(EVENT_BUCKET_NAME, event_photos_folder)
    
    cropped_faces_folder = "cropped_faces"

    # map between people and the photos they appear in
    for subdir, dirs, files in os.walk(event_photos_folder):
        for filename in files:
            filepath = subdir + os.sep + filename
            photo_paths = face_cropper.detect_and_crop(filepath, cropped_faces_folder)
            people = [] # TODO: get people in photo
            for person in people:
                if person.id not in photos_of_people_dict:
                    photos_of_people_dict[person.id] = []
                photos_of_people_dict[person.id].push(filepath)
    
    all_people = [] # TODO: get all people details

    # create zip for each person and upload to bucket
    for person_id, photos_paths in photos_of_people_dict.items():
        zip_file_path = person_id + ".zip"
        utils.create_zip_file(zip_file_path, photos_paths)
        storage_client.upload_file_to_bucket(ZIP_BUCKET_NAME, zip_file_path)
        utils.safe_remove_file(zip_file_path)
        # TODO: send to person each
        person = all_people[person_id]
    
    print("Success!")

if __name__ == '__main__':
    main()