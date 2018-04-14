import os
import argparse
from PIL import Image

location = 'SPIGa'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--images_dir', type=str)
    args = parser.parse_args()
    images_dir = args.images_dir
    for file_name in os.listdir(images_dir + location):
        if file_name.endswith('.JPG'):
            img = Image.open(images_dir + location + '/' + file_name)
            img = img.resize((448, 448), Image.ANTIALIAS)
            img.save(images_dir + 's' + location + '/' + file_name)


if __name__ == '__main__':
    main()
