import json

locations = ['DAMOa', 'GEORa', 'HALFb', 'HALFc', 'LOCKb', 'NEKOc', 'PETEc', 'PETEd', 'PETEf', 'SPIGa']
locations = ['SPIGa']


labels = {}
for location in locations:
    with open('converted_labels/' + location + '.json') as labels_file:
        labels.update(json.load(labels_file))

all_true_positives = 0
all_false_positives = 0
all_false_negatives = 0

for location in locations:
    with open('results2/' + location + '.json') as results_file:
        results = json.load(results_file)

        for im_name, results_list in results.items():
            if im_name.startswith(location):
                true_positives = 0
                false_positives = 0
                labels_list = labels[im_name[:-4]]
                labels_list_copy = list(labels_list)
                for result in results_list:
                    x = int(result[1])
                    y = int(result[2])
                    w = int(result[3] / 2)
                    h = int(result[4] / 2)
                    found = False
                    for label in list(labels_list_copy):
                        if label['x'] <= x + w and label['x'] >= x - w and label['y'] <= y + h and label['y'] >= y - h:
                            true_positives += 1
                            found = True
                            labels_list_copy.remove(label)
                            break
                    if not found:
                        false_positives += 1
                all_true_positives += true_positives
                all_false_positives += false_positives
                all_false_negatives += (len(labels_list) - true_positives)

print('true positives')
print(all_true_positives)
print('false positives')
print(all_false_positives)
print('false negatives')
print(all_false_negatives)
