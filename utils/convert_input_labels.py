import json
from PIL import Image

# locations = ['DAMOa', 'GEORa', 'HALFb', 'HALFc', 'LOCKb', 'NEKOc', 'PETEc', 'PETEd', 'PETEf', 'SPIGa']
locations = ['DAMOa', 'HALFc']
smaller_dimensions = ['DAMOa', 'GEORa', 'HALFb', 'NEKOc', 'PETEd', 'PETEf']

RESULT_DIM = 448
SMALLER_DIM_X = 2048
SMALLER_DIM_Y = 1536
LARGER_DIM_X = 1920
LARGER_DIM_Y = 1080
REDUCTION = 4


def all_inputs_valid(xy_list, max_x, max_y):
    for xy in xy_list:
        if not isinstance(xy, list):
            return False
        if xy[0] > max_x or xy[0] < 0:
            return False
        if xy[1] > max_y or xy[1] < 0:
            return False
    return True


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
                    loc_max_x = 0
                    loc_max_y = 0
                    if location in smaller_dimensions:
                        loc_max_x = SMALLER_DIM_X
                        loc_max_y = SMALLER_DIM_Y
                    else:
                        loc_max_x = LARGER_DIM_X
                        loc_max_y = LARGER_DIM_Y
                    if isinstance(xys, list) and all_inputs_valid(xys, loc_max_x, loc_max_y):
                        valid_xy_found = True
                        labels_dict[image_name] = xys
                        break
            if not valid_xy_found:
                labels_dict[image_name] = []

    size_image = Image.open('penguin_sizes/' + location + '.png', 'r')
    penguin_sizes = size_image.load()

    for key, xy_list in labels_dict.items():
        labels = []
        for xy in xy_list:
            penguin_size = 0
            if location in smaller_dimensions:
                x = xy[0]
                y = xy[1]
                if isinstance(x, int) and isinstance(y, int):
                    penguin_size = penguin_sizes[max(x-1, 0), max(y-1, 0)]
                y = (xy[1] * RESULT_DIM) / SMALLER_DIM_Y
                x = (xy[0] * RESULT_DIM) / SMALLER_DIM_X
            else:
                x = xy[0]
                y = xy[1]
                if isinstance(x, int) and isinstance(y, int):
                    penguin_size = penguin_sizes[max(x-1, 0), max(y-1, 0)]
                y = (xy[1] * RESULT_DIM) / LARGER_DIM_Y
                x = (xy[0] * RESULT_DIM) / LARGER_DIM_X

            x = int(round(x))
            y = int(round(y))
            size = int(round((penguin_size/4)/REDUCTION))

            bounding_box = {'xmin': x - size, 'xmax': x + size, 'ymin': y - size, 'ymax': y + size}
            labels.append(bounding_box)

        labels_dict[key] = labels
        labels_list.append({'im_name': key, 'b_boxes': labels})

    with open('converted_annotations/' + location + '.json', 'w') as file:
        json.dump(labels_list, file)
