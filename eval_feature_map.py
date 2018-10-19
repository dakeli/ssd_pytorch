from __future__ import print_function
import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.autograd import Variable
from data import VOC_ROOT, VOCAnnotationTransform, VOCDetection, BaseTransform
from data import VOC_CLASSES as labelmap
import torch.utils.data as data

from ssd import build_ssd
from cnn_layer_visualization import *

import sys
import os
import time
import argparse
import numpy as np
import pickle
import cv2
import skimage
import matplotlib.pyplot as plt
from output_xml import *
import copy


if sys.version_info[0] == 2:
    import xml.etree.cElementTree as ET
else:
    import xml.etree.ElementTree as ET


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


parser = argparse.ArgumentParser(description='Single Shot MultiBox Detector Evaluation')
parser.add_argument('--trained_model',default='weights/VOC.pth', type=str,help='Trained state_dict file path to open')
parser.add_argument('--save_folder', default='eval/', type=str,help='File path to save results')
parser.add_argument('--confidence_threshold', default=0.01, type=float,help='Detection confidence threshold')
parser.add_argument('--top_k', default=5, type=int,help='Further restrict the number of predictions to parse')
parser.add_argument('--cuda', default=True, type=str2bool,help='Use cuda to train model')
parser.add_argument('--voc_root', default=VOC_ROOT,help='Location of VOC root directory')
parser.add_argument('--cleanup', default=True, type=str2bool,help='Cleanup and remove results files following eval')
parser.add_argument('--show_results', default=True, type=str2bool,help='show image detection results after detection')
args = parser.parse_args()

if not os.path.exists(args.save_folder):
    os.mkdir(args.save_folder)

if torch.cuda.is_available():
    if args.cuda:
        torch.set_default_tensor_type('torch.cuda.FloatTensor')
    if not args.cuda:
        print("WARNING: It looks like you have a CUDA device, but aren't using \
              CUDA.  Run with --cuda for optimal eval speed.")
        torch.set_default_tensor_type('torch.FloatTensor')
else:
    torch.set_default_tensor_type('torch.FloatTensor')

annopath = os.path.join(args.voc_root, 'VOC2007', 'Annotations', '%s.xml')
imgpath = os.path.join(args.voc_root, 'VOC2007', 'JPEGImages', '%s.png')
imgsetpath = os.path.join(args.voc_root, 'VOC2007', 'ImageSets','Main', '{:s}.txt')
YEAR = '2007'
devkit_path = args.voc_root + 'VOC' + YEAR
dataset_mean = (104, 117, 123)
set_type = 'test'


if __name__ == '__main__':
    # load net
    num_classes = len(labelmap) + 1                      # +1 for background
    net = build_ssd('test', 300, num_classes)            # initialize SSD
    net.load_state_dict(torch.load(args.trained_model))
    net.eval()
    print('Finished loading model!')
    # load data
    dataset = VOCDetection(args.voc_root, [('2007', set_type)],BaseTransform(300, dataset_mean),VOCAnnotationTransform())
    if args.cuda:
        net = net.cuda()
        cudnn.benchmark = True
    # evaluation

    num_images = len(dataset)
    for i in range(num_images):
        print('i=', i)
        im, gt, h, w, img_id = dataset.pull_item(i)
        # cv2.imwrite('D:/image/'+img_id[-1]+'.png', im.permute(2, 1, 0).cpu().numpy())
        layer_vis = CNNLayerVisualization(im, net.vgg, selected_layer=34, selected_filter=0)
        layer_vis.visualise_layer_with_hooks(img_id)


