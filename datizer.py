import argparse
import os
import shutil

import exifread


def parse_arguments():
    parser = argparse.ArgumentParser(description='Datizer photo catalog creator')
    parser.add_argument('-s', '--source', type=str, default=os.getcwd(), help='Enter source folder path')
    parser.add_argument('-d', '--destination', type=str, default=None, help='Enter output folder path')
    parser.add_argument('-e', '--suffix_list', nargs="*", default=['CR2', 'JPEG', 'JPG'])
    args = parser.parse_args()
    return args


class datizer():
    def __init__(self, folder_path, output_path, suffix_list):
        self.folder_path = folder_path
        if output_path is None:
            self.output_path = folder_path
        else:
            self.output_path = output_path
        self.suffix_list = suffix_list

    def get_images_in_folder(self, filter_with_suffix=True):
        if self.suffix_list is None:
            self.suffix_list = ['CR2']
        files = []
        for r, d, f in os.walk(self.folder_path):
            for file in f:
                if filter_with_suffix:
                    for s in self.suffix_list:
                        if s in file:
                            files.append(os.path.join(r, file))
                else:
                    files.append(os.path.join(r, file))
        return files

    @staticmethod
    def get_exif_data(img_path):
        if not img_path.split('/')[-1][0] == '.':
            f = open(img_path, 'rb')
            exif_data = exifread.process_file(f)
            return exif_data
        else:
            return None

    def get_date_time(self, img_path):
        exif_data = self.get_exif_data(img_path)
        if exif_data is not None:
            if 'EXIF DateTimeOriginal' in exif_data:
                date_and_time = exif_data['EXIF DateTimeOriginal']
                return date_and_time
        else:
            return None

    @staticmethod
    def get_folder_name(date):
        if date:
            date_time_components = str(date).split(' ')[0].split(':')
            return date_time_components[0] + '-' + date_time_components[1] + '-' + date_time_components[2]

    @staticmethod
    def create_folder(directory_name):
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)
            print("Directory ", directory_name.split('/')[-1], " Created ")

    def move_image_to_folder(self, img, destination_folder):
        if os.path.isfile(img) and os.path.isdir(destination_folder):
            if os.path.exists(destination_folder + '/' + img.split('/')[-1]):
                self.rename_image_and_move(img, destination_folder)
            else:
                shutil.move(img, destination_folder)
                print(img.split('/')[-1] + " is moved to " + destination_folder.split('/')[-1] + " folder.")

        else:
            print("Given image or destination folder is not pointing to correct path.")

    def rename_image_and_move(self, img, destination_folder, index=2):
        img_name = img.split('/')[-1]
        img_folder = img.split(img_name)[0]
        new_path = destination_folder + '/' + img_name.split('.')[0] + '_' + str(index) + '.' + img_name.split('.')[1]
        if os.path.isfile(new_path):
            self.rename_image_and_move(img, destination_folder, index + 1)
        else:
            new_img = img_folder + img_name.split('.')[0] + '_' + str(index) + '.' + img_name.split('.')[1]
            print(img.split('/')[-1] + " is renamed to " + new_img.split('/')[-1] + ".")
            print(new_img.split('/')[-1] + " is moved to " + destination_folder.split('/')[-1] + " folder.")
            os.rename(img, new_img)
            shutil.move(new_img, destination_folder)

    def process_files(self):
        images = self.get_images_in_folder()
        for img in images:
            date_time = self.get_date_time(img)
            if date_time is None:
                pass
            else:
                folder_name = self.get_folder_name(date_time)
                if self.output_path[-1] == '/':
                    folder_path = self.output_path + folder_name
                else:
                    folder_path = self.output_path + '/' + folder_name

                self.create_folder(folder_path)
                self.move_image_to_folder(img, folder_path)


if __name__ == '__main__':
    args = parse_arguments()
    app = datizer(args.source, args.destination, args.suffix_list)
    app.process_files()
