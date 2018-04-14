import os
import argparse
from PIL import Image

locations = ['DAMOa', 'GEORa', 'HALFb', 'HALFc', 'LOCKb', 'NEKOc', 'PETEc', 'PETEd', 'PETEf', 'SPIGa']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--images_dir', type=str)
    args = parser.parse_args()
    images_dir = args.images_dir
    for location in locations:
        for file_name in os.listdir(images_dir + location):
            if file_name.endswith('.JPG'):
                img = Image.open(images_dir + location + '/' + file_name)
                if img.width != 1920 and img.width != 2048 or img.height != 1080 and img.height != 1536:
                    print('Invalid dimensions')
                    print('Width')
                    print(img.width)
                    print('Height')
                    print(img.height)


if __name__ == '__main__':
    main()
