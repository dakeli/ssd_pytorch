from lxml.etree import Element, SubElement, tostring, ElementTree
# from xml.etree.ElementTree import Element, SubElement, tostring
import lxml.etree as ET
import pprint
import cv2
import os
from scipy import misc
from xml.dom.minidom import parseString
# VOC_ClASSES = ('aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow',
#                'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa',
#                'train', 'tvmonitor')
VOC_ClASSES = ('cluster')


def create_xml(filename, width, height, depth, bbox):
    node_root = Element('annotation')

    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'VOC2007'

    node_filename = SubElement(node_root, 'filename')
    # node_filename.text = '000001.jpg'

    node_source = SubElement(node_root, 'source')
    node_database = SubElement(node_source, 'database')
    node_database.text = '91360'
    node_annotation = SubElement(node_source, 'annotation')
    node_annotation.text = 'PASCAL VOC2007'
    node_image = SubElement(node_source, 'image')
    node_image.text = 'focal loss'
    node_flickrid = SubElement(node_source, 'flickrid')
    node_flickrid.text = 'NULL'

    node_owner = SubElement(node_root, 'owner')
    node_flickrid = SubElement(node_owner, 'flickrid')
    node_flickrid.text = 'NULL'
    node_name = SubElement(node_owner, 'name')
    node_name.text = 'lijindong'

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    # node_width.text = '353'
    node_height = SubElement(node_size, 'height')
    # node_height.text = '500'
    node_depth = SubElement(node_size, 'depth')
    # node_depth.text = '3'

    node_segmented = SubElement(node_root, 'segmented')
    node_segmented.text = '0'
    #################### 注入参数 ##########################
    node_filename.text = filename
    node_width.text = str(width)
    node_height.text = str(height)
    node_depth.text = str(depth)
    #################### 注入参数 ##########################
    for k, v in enumerate(bbox):
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        # node_name.text = 'dog'
        node_pose = SubElement(node_object, 'pose')
        # node_pose.text = 'Left'
        node_truncated = SubElement(node_object, 'truncated')
        # node_truncated.text = '1'
        node_difficult = SubElement(node_object, 'difficult')
        # node_difficult.text = '0'
        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        # node_xmin.text = '48'
        node_ymin = SubElement(node_bndbox, 'ymin')
        # node_ymin.text = '240'
        node_xmax = SubElement(node_bndbox, 'xmax')
        # node_xmax.text = '195'
        node_ymax = SubElement(node_bndbox, 'ymax')
        # node_ymax.text = '371'
        #################### 注入参数 ##########################
        node_name.text = v['name']
        node_pose.text = v['pose']
        node_truncated.text = str(v['truncated'])
        node_difficult.text = str(v['difficult'])

        node_xmin.text = str(v['bbox'][0])
        node_ymin.text = str(v['bbox'][1])
        node_xmax.text = str(v['bbox'][2])
        node_ymax.text = str(v['bbox'][3])

        #################### 注入参数 ##########################

    xml = tostring(node_root, pretty_print=True)  #格式化显示，该换行的换行
    dom = parseString(xml)
    # print(xml)

    try:
        with open(dst_path + '.txt', 'a+', encoding='UTF-8') as txtf:
            txtf.write(filename + ' ')
            # txtf.write('/home/dake/data/VOC_try/VOC2007/JPEGImages/'+filename + ' ')
            # for k, v in enumerate(bbox):
                # id_s = VOC_ClASSES.index(v['name'])
                # txtf.write(str(id_s))
                # txtf.write(str(v['bbox'][0]) + ' ' + str(v['bbox'][1]) + ' ' + str(v['bbox'][2]) + ' ' +
                #            str(v['bbox'][3]) + ' ' + str(id_s) + ' ')
            txtf.write(str(v['bbox'][0]) + ' ' + str(v['bbox'][1]) + ' ' + str(v['bbox'][2]) + ' ' +
                       str(v['bbox'][3]) + ' ' + v['name'] + ' ')
            txtf.write('\n')

            # print('bingo')
    except Exception as err:

        print('error')


    try:
        with open(dst_path+r'\\' + filename[:-4]+'.xml', 'w', encoding='UTF-8') as fh:
            # 4.writexml()第一个参数是目标文件对象，第二个参数是根节点的缩进格式，第三个参数是其他子节点的缩进格式，
            # 第四个参数制定了换行格式，第五个参数制定了xml内容的编码。
            dom.writexml(fh, indent='', addindent='\t', newl='\n', encoding='UTF-8')
            # print('写入xml OK!')
    except Exception as err:
            print('错误信息：{0}'.format(err))


def read_xml(filename, xmlpath):
    # anno = ET.parse(xml_path).getroot()
    tree = ET.parse(xmlpath)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        obj_struct['pose'] = obj.find('pose').text
        obj_struct['truncated'] = int(obj.find('truncated').text)
        obj_struct['difficult'] = int(obj.find('difficult').text)
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text) + 180,
                              int(bbox.find('ymin').text) + 180,
                              int(bbox.find('xmax').text) + 220,
                              int(bbox.find('ymax').text) + 220]
        objects.append(obj_struct)
        show_bbox(filename, objects)
        create_xml(filename, width, height, depth, objects)


    # return create_xml(filename, width, height, depth, objects)
def show_bbox(filename, bbox):
    for k, v in enumerate(bbox):
        cv2.rectangle(img, (v['bbox'][0],v['bbox'][1]), (v['bbox'][2],v['bbox'][3]),(0,0,255),4)
    cv2.imwrite(image_path+'\\'+'modify_' + filename, img)


if __name__ == '__main__':
    image_path = r'C:\Users\dake\Desktop\diff_picture_200_200'
    xml_path = r'C:\Users\dake\Desktop\origin_xml'
    images = [obj for obj in os.listdir(image_path) if 'png' in obj]
    xmls = [obj for obj in os.listdir(xml_path) if 'xml' in obj]
    dst_path = r'C:\Users\dake\Desktop\xml'
    # for image, xml in zip(images, xmls):
    # for k, v in enumerate(list(zip(images, xmls))):
    for image in images:
        # print(k)
        # image = v[0]
        # xml = v[1]
        img = cv2.imread(image_path+r'\\'+image)
        filename = image
        width = img.shape[1]
        height = img.shape[0]
        depth = img.shape[2]
        num = image.split('----')[-1].split('.')[0].split('_')
        x = int(num[0]) + 200
        y = int(num[1]) + 200
        w = int(num[2]) - 400
        h = int(num[3]) - 400
        xml_name = image.split('----')[0] + '----' + str(x) + '_' + str(y) + '_' + str(w) + str('_') + str(h) + '.xml'
        if xml_name in xmls:
            read_xml(filename, xml_path+r'\\'+xml_name)
        else:
            print(xml_name, '@', image)


        # class_name = 'cluster'
        # xmin = 1
        # ymin = 1
        # xmax = 2
        # ymax = 2
        # create_xml(filename, width, height, depth, class_name, xmin, ymin, xmax, ymax)





