# coding=utf-8
import sys
import openslide
from skimage import morphology
import numpy as np
from skimage.measure import label, regionprops
from xml.dom import minidom
from matplotlib import pyplot as plt
import os
import imageio
import pickle
import time
import multiprocessing as mp
import threading as td

def start(root_path, png_path, save_path, scale, extend):
    orl_scale = 2 ** scale
    ############################### image list ##############################################
    img_names = [img_name.split('.')[0] for img_name in os.listdir(root_path) if ".ndpi" in img_name]
    png_names = [png_name for png_name in os.listdir(png_path) if 'png' in png_name]

    for png_name in png_names:
        if png_name.split('----')[0] not in img_names:
            assert "file error"
        else:
            img_path = root_path + "\\" + png_name.split('----')[0] + '.ndpi'
            start_time = time.time()
            slide = openslide.open_slide(img_path)
            print('openslide_time:', time.time()-start_time)
            # 一共有多少个倍率的图片，第0层是40x或者20x，看具体情况而定
            # slide_level_count = slide.level_count
            # magnification = img_path.split("\\")[-1].split(".")[0].split("_")[1]
            datadict = pickle.load(open(r"C:\code\PycharmProjects\readndpi\20180717.pkl", 'rb'))
            if "X20" in png_name:
                level = scale
            elif "WCH" in png_name:
                level = scale + 1
            else:
                # if '20' in png_name:
                #     if datadict[png_name.split(".")[0].split('----')[0]] == "20":
                #         level = scale
                # else:
                level = scale + 1
            # 获取某个层级的具体图像尺寸
            OVslide = slide.level_dimensions[0]
            [width, height] = OVslide
            # 读取图像slide.read_region(起始点坐标, 图像层级, 图像的宽高)
            # img_slide = np.array(slide.read_region((0, 0), level, (width-1, height-1)))[:, :, :3]

            coor = png_name.split('.')[0].split('----')[-1].split('_')
            X = int(coor[0])-extend if int(coor[0]) >= extend else 0
            Y = int(coor[1])-extend if int(coor[1]) >= extend else 0
            W = int(coor[2])+2*extend if (width-int(coor[0])-int(coor[2])) >= extend else width-X
            H = int(coor[3])+2*extend if (height-int(coor[1])-int(coor[3])) >= extend else height-Y
            # print(coor)
            # print(X,Y,W,H)
            start_time = time.time()
            png_slide = np.array(slide.read_region((X, Y), 0, (W, H)))[:, :, :3]
            print('read_slide_time:', time.time()-start_time)
            start_time = time.time()
            imageio.imwrite(save_path+"\\" + png_name.split("----")[0] + "----" + str(X) + "_" + str(Y) + "_" +
                            str(W) + "_" + str(H) + ".png", png_slide)
            print('imwrite_time:', time.time() - start_time)

    print("end")


if __name__ == '__main__':
    root_path = r"D:\dataset\all_ndpi"
    png_path = r"D:\all_patch\origin_picture"
    save_path = r"C:\Users\dake\Desktop\origin_picture_200_200"
    scale = 4  # 比20倍图像小2**3倍
    extend = 200
    start(root_path, png_path, save_path, scale, extend)

    # def job(q):
    #     q.put(start(root_path, png_path, save_path, scale, extend))

    # q = mp.Queue()
    # t1 = td.Thread(target=job, args=(q,), name='p1')
    # t2 = td.Thread(target=job, args=(q,), name='p2')
    # t3 = td.Thread(target=job, args=(q,), name='p3')
    # t4 = td.Thread(target=job, args=(q,), name='p4')
    # t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
    # t1.join()
    # t2.join()
    # t3.join()
    # t4.join()

    # res1 = q.get()
    # res2 = q.get()
    # res3 = q.get()
    # res4 = q.get()

    # q = mp.Queue()
    # p1 = mp.Process(target=job, args=(q,), name='p1')
    # p2 = mp.Process(target=job, args=(q,), name='p2')
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()


