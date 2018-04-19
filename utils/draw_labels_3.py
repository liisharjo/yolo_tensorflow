import cv2
import json

# display image with original dot annotations and generated bounding box

name = 'NEKOc2013c_000001'
im = cv2.imread('example_images/' + name + '.JPG')

with open('converted_annotations/NEKOc.json') as b_boxes_file:
    with open('converted_labels/NEKOc.json') as dots_file:

        dots_images = json.load(dots_file)
        dots = dots_images[name]
        for dot in dots:
            cv2.circle(im, (int(dot['x']), int(dot['y'])), 2, (0, 0, 255), -1)

        b_boxes_images = json.load(b_boxes_file)
        for image in b_boxes_images:
            if image['im_name'] == name:
                boxes = image['b_boxes']
                break

        for box in boxes:
            cv2.rectangle(im, (box['xmin'], box['ymin']),
                          (box['xmax'], box['ymax']), (255, 0, 0), 2)

cv2.imshow('Image', im)
cv2.waitKey(0)
