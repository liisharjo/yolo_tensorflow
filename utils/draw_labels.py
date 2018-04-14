import cv2
import json

name = 'SPIGa2014b_000001'
im = cv2.imread('example_images/' + name + '.JPG')

with open('converted_annotations/SPIGa.json') as file:
    original_labels = json.load(file)
    bounding_boxes = []
    for image in original_labels:
        if image['im_name'] == name:
            bounding_boxes = image['b_boxes']
            break
    for bounding_box in bounding_boxes:
        cv2.rectangle(im, (bounding_box['xmin'], bounding_box['ymin']), (bounding_box['xmax'], bounding_box['ymax']), (255, 0, 0), 2)

cv2.imshow('Image', im)
cv2.waitKey(0)
