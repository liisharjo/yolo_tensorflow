from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import numpy as np
import pickle
import json
import yolo.config as cfg
from tensorflow.python.lib.io import file_io


class pascal_voc(object):
    def __init__(self, phase, rebuild=False):
        # self.devkil_path = os.path.join(cfg.PASCAL_PATH, 'VOCdevkit')
        # self.data_path = os.path.join(self.devkil_path, 'VOC2007')
        self.data_path = cfg.DATA_PATH
        self.annotations_path = os.path.join(self.data_path, 'annotations')
        self.images_path = os.path.join(self.data_path, 'images')
        self.cache_path = cfg.CACHE_PATH
        self.batch_size = cfg.BATCH_SIZE
        self.image_size = cfg.IMAGE_SIZE
        self.cell_size = cfg.CELL_SIZE
        self.classes = cfg.CLASSES
        self.class_to_ind = dict(zip(self.classes, range(len(self.classes))))
        # self.flipped = cfg.FLIPPED
        self.phase = phase
        self.rebuild = rebuild
        self.cursor = 0
        self.epoch = 1
        self.gt_labels = None
        self.images = None
        self.images_train = {}
        self.image_names = []
        self.locations = cfg.LOCATIONS
        self.prepare()

    def get(self):
        images = np.zeros(
            (self.batch_size, self.image_size, self.image_size, 3))
        labels = np.zeros(
            (self.batch_size, self.cell_size, self.cell_size, 25))
        count = 0
        while count < self.batch_size:
            imname = str(self.image_names[self.cursor])
            if imname in self.images:
                images[count, :, :, :] = self.images[imname]
                labels[count, :, :, :] = self.gt_labels[imname]
                count += 1
                self.cursor += 1
                if self.cursor >= len(self.image_names):
                    # np.random.shuffle(self.gt_labels)
                    self.cursor = 0
                    self.epoch += 1
        return images, labels

    def prepare(self):
        gt_labels = self.load_labels()
        self.gt_labels = gt_labels
        self.load_images()
        return gt_labels

    def load_labels(self):
        # cache_file = os.path.join(
        #     self.cache_path, 'pascal_' + self.phase + '_gt_labels.pkl')
        #
        # if os.path.isfile(cache_file) and not self.rebuild:
        #     print('Loading gt_labels from: ' + cache_file)
        #     with file_io.FileIO(cache_file, mode='r+') as f:
        #         gt_labels = pickle.load(f)
        #     return gt_labels

        print('Processing gt_labels from: ' + self.data_path)

        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)

        gt_labels = {}
        for location in self.locations:
            labels = self.load_location_labels(location)
            gt_labels.update(labels)
        return gt_labels

    def load_location_labels(self, location):
        labels_json_file = os.path.join(self.annotations_path, location + '.json')
        with file_io.FileIO(labels_json_file, 'r') as file_stream:
            original_labels = json.load(file_stream)
            gt_labels = {}
            for image in original_labels:
                name = image['im_name']
                b_boxes = image['b_boxes']
                label = np.zeros((self.cell_size, self.cell_size, 25))
                for bbox in b_boxes:
                    x1 = max(min(bbox['xmin'], self.image_size - 1), 0)
                    y1 = max(min(bbox['ymin'], self.image_size - 1), 0)
                    x2 = max(min(bbox['xmax'], self.image_size - 1), 0)
                    y2 = max(min(bbox['ymax'], self.image_size - 1), 0)
                    boxes = [(x2 + x1) / 2.0, (y2 + y1) / 2.0, x2 - x1, y2 - y1]
                    x_ind = int(boxes[0] * self.cell_size / self.image_size)
                    y_ind = int(boxes[1] * self.cell_size / self.image_size)
                    if label[y_ind, x_ind, 0] == 1:
                        continue
                    label[y_ind, x_ind, 0] = 1
                    label[y_ind, x_ind, 1:5] = boxes
                    label[y_ind, x_ind, 6] = 1
                gt_labels[name + '.JPG'] = label
            return gt_labels

    def load_images(self):
        images = {}
        for location in self.locations:
            images_file = os.path.join(self.images_path, location + '_train.pickle')
            file_stream = file_io.FileIO(images_file, mode='r+')
            loc_images = pickle.load(file_stream)
            images.update(loc_images)
            self.image_names.extend(list(loc_images.keys()))
        self.images = images
