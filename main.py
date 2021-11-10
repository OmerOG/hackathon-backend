from face_cropper import FaceCropper
from simple_storage_client import SimpleStorageClient
import os


def main():
    event_storage = SimpleStorageClient("best-team-bucket-storage")
    face_cropper = FaceCropper()

    event_photos_folder = "event_photos"
    event_storage.download_all_from_bucket(event_photos_folder)
    
    cropped_faces_folder = "cropped_faces"
    for subdir, dirs, files in os.walk(event_photos_folder):
        for filename in files:
            filepath = subdir + os.sep + filename
            face_cropper.detect_and_crop(filepath, cropped_faces_folder + "/" + filename.rstrip("."))
            # continue hereee
    
    print("Success!")

if __name__ == '__main__':
    main()