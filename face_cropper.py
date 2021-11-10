from google.cloud import vision
from PIL import Image, ImageDraw
import os
import utils
from constants import API_KEY_FILE


class FaceCropper:
    def __init__(self, account_json=API_KEY_FILE):
        self._vision_client = vision.ImageAnnotatorClient().from_service_account_json(account_json)
    
    def detect_and_crop(self, image_filename, output_folder):
        with open(image_filename, 'rb') as image:
            faces = self._detect_faces(image)
            print('Found {} face{}'.format(
                len(faces), '' if len(faces) == 1 else 's'))

            print('Writing to file {}'.format(output_folder))
            # Reset the file pointer, so we can read the file again
            image.seek(0)
            return self._save_cropped_faces(image, faces, output_folder)

    def _detect_faces(self, face_file, max_results=100):
        content = face_file.read()
        image = vision.Image(content=content)

        return self._vision_client.face_detection(
            image=image, max_results=max_results).face_annotations

    def _save_cropped_faces(self, image, faces, output_folder):
        file_paths = []
        utils.safe_create_directory(output_folder)
        im = Image.open(image)
        for index, face in enumerate(faces):
            print(str(format(face.detection_confidence, '.3f')) + '%')
            area = (face.bounding_poly.vertices[0].x,
                    face.bounding_poly.vertices[0].y,
                    face.bounding_poly.vertices[2].x,
                    face.bounding_poly.vertices[2].y)
            file_path = output_folder + "/" + str(index) + ".png"
            im.crop(area).save(file_path)
            file_paths.append(file_path)
        return file_paths