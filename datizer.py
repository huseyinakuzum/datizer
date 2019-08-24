import os
import shutil

import exifread


class datizer():
    def __init__(self, folder_path, output_path):
        self.folder_path = folder_path
        self.output_path = output_path

    def get_images_in_folder(self, filter_with_suffix=True, suffix=None):
        if suffix is None:
            suffix = ['CR2']
        files = []
        for r, d, f in os.walk(self.folder_path):
            for file in f:
                if filter_with_suffix:
                    for s in suffix:
                        if s in file:
                            files.append(os.path.join(r, file))
                else:
                    files.append(os.path.join(r, file))
        return files

    @staticmethod
    def get_exif_data(img_path):
        """Returns a dictionary from the exif data of an PIL Image item. Also
        converts the GPS Tags"""
        f = open(img_path, 'rb')
        exif_data = exifread.process_file(f)
        return exif_data
        # return exif_data

    def get_date_time(self, img_path):
        exif_data = self.get_exif_data(img_path)
        if 'EXIF DateTimeOriginal' in exif_data:
            date_and_time = exif_data['EXIF DateTimeOriginal']
            return date_and_time

    @staticmethod
    def get_folder_name(date):
        if date:
            date_time_components = str(date).split(' ')[0].split(':')
            return date_time_components[2] + '.' + date_time_components[1] + '.' + date_time_components[0]

    def create_folder(self, directory_name):
        print(directory_name)
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)
            print("Directory ", directory_name, " Created ")
        else:
            print("Directory ", directory_name, " already exists")

    @staticmethod
    def move_image_to_folder(img, destination_folder):
        if os.path.isfile(img) and os.path.isdir(destination_folder):
            shutil.move(img, destination_folder)
            print(img.split('/')[-1] + " is moved to " + destination_folder)

        else:
            print("Given image or destination folder is not pointing to correct path.")

    def process_files(self):
        images = self.get_images_in_folder()
        for img in images:
            date_time = self.get_date_time(img)
            folder_name = self.get_folder_name(date_time)
            folder_path = self.output_path + folder_name
            self.create_folder(folder_path)
            self.move_image_to_folder(img, folder_path)
