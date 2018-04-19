import json
import argparse
from PIL import Image

locations = ['DAMOa', 'GEORa', 'HALFb', 'HALFc', 'LOCKb', 'NEKOc', 'PETEc', 'PETEd', 'PETEf', 'SPIGa']
#locations = ['DAMOa']

RESULT_DIM = 448
SMALLER_DIM_X = 2048
SMALLER_DIM_Y = 1536
LARGER_DIM_X = 1920
LARGER_DIM_Y = 1080


def all_inputs_valid(xy_list):
    for xy in xy_list:
        if not isinstance(xy, list):
            return False
        if xy[0] < 0:
            return False
        if xy[1] < 0:
            return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--images_dir', type=str)
    args = parser.parse_args()
    images_dir = args.images_dir
    for location in locations:
        labels_dict = {}
        with open('original_annotations/' + location + '.json') as file:
            original_labels = json.load(file)
            for dots in original_labels['dots']:
                image_name = dots['imName']
                valid_xy_found = False
                if isinstance(dots['xy'], list):
                    for xys in dots['xy']:
                        if isinstance(xys, list) and len(xys) > 0 and all_inputs_valid(xys):
                            valid_xy_found = True
                            labels_dict[image_name] = xys
                            break
                if not valid_xy_found:
                    labels_dict[image_name] = []

        for key, xy_list in labels_dict.items():
            labels = []
            for xy in xy_list:
                x = xy[0]
                y = xy[1]
                img = Image.open(images_dir + location + '/' + key + '.JPG')
                if img.width == 2048 and (x >= SMALLER_DIM_X or y >= SMALLER_DIM_Y):
                    break
                if img.width == 1920 and (x >= LARGER_DIM_X or y >= LARGER_DIM_Y):
                    break
                if img.width == 2048:
                    y = (xy[1] * RESULT_DIM) / SMALLER_DIM_Y
                    x = (xy[0] * RESULT_DIM) / SMALLER_DIM_X
                else:
                    y = (xy[1] * RESULT_DIM) / LARGER_DIM_Y
                    x = (xy[0] * RESULT_DIM) / LARGER_DIM_X

                x = int(round(x))
                y = int(round(y))
                label = {'x': x, 'y': y}
                labels.append(label)

            labels_dict[key] = labels

        with open('converted_labels/' + location + '.json', 'w') as file:
            json.dump(labels_dict, file)


if __name__ == '__main__':
    main()
