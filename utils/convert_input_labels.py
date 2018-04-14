import json
import argparse
from PIL import Image

locations = ['DAMOa', 'GEORa', 'HALFb', 'HALFc', 'LOCKb', 'NEKOc', 'PETEc', 'PETEd', 'PETEf', 'SPIGa']
# locations = ['DAMOa']
smaller_dimensions = ['DAMOa', 'GEORa', 'HALFb', 'NEKOc', 'PETEd', 'PETEf']

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
        labels_list = []
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
            try:
                size_image = Image.open('penguin_sizes/' + key[:10] + '_pengSize.png', 'r')
            except IOError:
                print('No size image matches with current image')
                print(key)
            penguin_sizes = size_image.load()
            labels = []
            for xy in xy_list:
                x = xy[0]
                y = xy[1]
                penguin_size = 0
                img = Image.open(images_dir + location + '/' + key + '.JPG')
                if img.width == 2048 and (x >= SMALLER_DIM_X or y >= SMALLER_DIM_Y):
                    break
                if img.width == 1920 and (x >= LARGER_DIM_X or y >= LARGER_DIM_Y):
                    break
                if img.width == 2048:
                    if isinstance(x, int) and isinstance(y, int):
                        penguin_size = penguin_sizes[max(x-2, 0), max(y-2, 0)]
                    penguin_size_y = (penguin_size * RESULT_DIM) / SMALLER_DIM_Y
                    penguin_size_x = (penguin_size * RESULT_DIM) / SMALLER_DIM_X
                    y = (xy[1] * RESULT_DIM) / SMALLER_DIM_Y
                    x = (xy[0] * RESULT_DIM) / SMALLER_DIM_X
                else:
                    if isinstance(x, int) and isinstance(y, int):
                        penguin_size = penguin_sizes[max(x-1, 0), max(y-1, 0)]
                    penguin_size_y = (penguin_size * RESULT_DIM) / LARGER_DIM_Y
                    penguin_size_x = (penguin_size * RESULT_DIM) / LARGER_DIM_X
                    y = (xy[1] * RESULT_DIM) / LARGER_DIM_Y
                    x = (xy[0] * RESULT_DIM) / LARGER_DIM_X

                x = int(round(x))
                y = int(round(y))
                size_x = int(round((penguin_size_x/4)))
                size_y = int(round((penguin_size_y/4)))

                bounding_box = {'xmin': max(x - size_x, 0),
                                'xmax': min(x + size_x, 447),
                                'ymin': max(y - size_y, 0),
                                'ymax': min(y + size_y, 447)}
                labels.append(bounding_box)

            labels_dict[key] = labels
            labels_list.append({'im_name': key, 'b_boxes': labels})

        with open('converted_annotations/' + location + '.json', 'w') as file:
            json.dump(labels_list, file)


if __name__ == '__main__':
    main()
