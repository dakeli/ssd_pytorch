# coding=utf-8
import sys
import openslide
from skimage import morphology
import numpy as np
from skimage.measure import label, regionprops
from xml.dom import minidom
from matplotlib import pyplot as plt
import os
from scipy import misc
import pickle


def start(root_path, save_path, extend):
    ############################### image list ##############################################

    img_names = [img_name for img_name in os.listdir(root_path) if ".png" in img_name]

    for img_name in img_names:

        ndpi_path = 'D:\\downloads\\7.10xianxibao_wudadian' + "\\" + img_name.split('----')[0]+'.ndpi'

        if not os.path.exists(save_path):
            os.mkdir(save_path)
        slide = openslide.open_slide(ndpi_path)
        # 一共有多少个倍率的图片，第0层是40x或者20x，看具体情况而定
        # slide_level_count = slide.level_count
        # magnification = img_path.split("\\")[-1].split(".")[0].split("_")[1]
        datadict = pickle.load(open(r"C:\Users\dake\OneDrive\PycharmProjects\readndpi\20180717.pkl",'rb'))

        # 获取某个层级的具体图像尺寸
        OVslide = slide.level_dimensions[0]
        [width, height] = OVslide
        # 读取图像slide.read_region(起始点坐标, 图像层级, 图像的宽高)
        # img_slide = np.array(slide.read_region((0, 0), level, (width-1, height-1)))[:, :, :3]
        # png_names = [png_name for png_name in os.listdir((png_path+'\\'+img_name).split('.')[0]) if 'png' in  png_name]

        coor = img_name.split('.')[0].split('----')[1].split('_')
        X = int(coor[0])-extend if int(coor[0]) >= extend else 0
        Y = int(coor[1])-extend if int(coor[1]) >= extend else 0
        W = int(coor[2])+2*extend if (width-X-int(coor[2])) >= extend else width-X
        H = int(coor[3])+2*extend if (height-Y-int(coor[3])) >= extend else height-Y
        print(img_name)
        print(coor)
        print(X,Y,W,H)
        png_slide = np.array(slide.read_region((X, Y), 0, (W, H)))[:, :, :3]
        print(save_path + "\\" + img_name)
        misc.imsave(save_path + "\\"+img_name, png_slide)
        # misc.imsave(save_path+"\\"+img_name.split(".")[0].split('----')[0] + "----" + str(X) + "_" + str(Y) + "_"
        #             + str(W) + "_" + str(H) + '_' + str(int(coor[0])-X) + "_" + str(int(coor[1])-Y) + "_" +
        #             coor[2] + "_" + coor[3] + ".png", png_slide)
    print("end")

if __name__ == '__main__':
    root_path = r"C:\Users\dake\data\VOC_2940\VOC2007\JPEGImages"
    save_path = r"C:\Users\dake\data\VOC_2940\VOC2007\JPEGImages_"

    extend = 50
    start(root_path, save_path, extend)
