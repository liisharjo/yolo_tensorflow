import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import json


im = plt.imread('example_images/HALFc2013a_000001.JPG')

xs = []
ys = []
with open('converted_annotations/HALFc.json') as file:
    original_labels = json.load(file)
    bounding_boxes = []
    for image in original_labels:
        if image['im_name'] == 'HALFc2013a_000001':
            bounding_boxes = image['b_boxes']
            break
    for bounding_box in bounding_boxes:
        xs.append(bounding_box['xmin'])
        ys.append(bounding_box['ymin'])
        xs.append(bounding_box['xmin'])
        ys.append(bounding_box['ymax'])
        xs.append(bounding_box['xmax'])
        ys.append(bounding_box['ymin'])
        xs.append(bounding_box['xmax'])
        ys.append(bounding_box['ymax'])

implot = plt.imshow(im)

plt.scatter(x=xs, y=ys, c='r', s=2)

plt.show(block=True)
