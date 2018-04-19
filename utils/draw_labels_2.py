import cv2
import json

# display image with original dot annotation and model generated bounding box

name = 'PETEf2014a_000005'
im = cv2.imread('example_images/' + name + '.JPG')

with open('converted_labels/PETEf.json') as file:
    with open('results2/PETEf.json') as results_file:
        original_labels = json.load(file)
        labels = original_labels[name]
        for label in labels:
            cv2.circle(im, (int(label['x']), int(label['y'])), 2, (0, 0, 255), -1)

        results = json.load(results_file)
        result_list = results[name + '.JPG']
        for result in result_list:
            x = int(result[1])
            y = int(result[2])
            w = int(result[3] / 2)
            h = int(result[4] / 2)
            cv2.rectangle(im, (x-w, y-h), (x+w, y+h), (255, 0, 0), 2)

cv2.imshow('Image', im)
cv2.waitKey(0)
