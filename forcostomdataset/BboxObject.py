import os
import xml.etree.ElementTree as et
import cv2
import numpy as np


class BboxObject :
    def __init__(self, p1, p2, name) :
        self.name = name
        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]
        if x1 > x2 :
            self.xmax = int(x1)
            self.xmin = int(x2)
        else :
            self.xmax = int(x2)
            self.xmin = int(x1)

        if y1 > y2 :
            self.ymax = int(y1)
            self.ymin = int(y2)
        else :
            self.ymax = int(y2)
            self.ymin = int(y1)

        # Debug
        # print(self.xmin, self.ymin, "~", self.xmax, self.ymax)



class FileData :

    def __init__(self, filefullpath, video_frame_count, video_frame, savefolder, labelname, debugmode = False):

        # Inner Data
        self.file_fullpath = filefullpath
        self.file_folderpath,   self.file_fullname = os.path.split(filefullpath)
        self.file_justfilename, self.file_justext  = os.path.splitext(self.file_fullname)
        self.file_savefolder = savefolder
        self.video_frame_count = video_frame_count
        self.labelname = labelname

        self.xml_file_name = str(self.file_justfilename) + "_" + str(labelname) + "_" + str(self.video_frame_count) + '.xml'
        self.img_file_name = str(self.file_justfilename) + "_" + str(labelname) + "_" + str(self.video_frame_count) + '.jpg'

        # XML nodes
        self.root = et.Element("annotation")

        self.folder = et.SubElement(self.root, "folder")
        self.folder.text = str(self.file_savefolder)

        self.filename = et.SubElement(self.root, "filename")
        self.filename.text = str(self.img_file_name)

        self.size = et.SubElement(self.root, "size")
        self.width = et.SubElement(self.size, "width")
        self.width.text = str(int(np.size(video_frame, 1)))
        self.height = et.SubElement(self.size, "height")
        self.height.text = str(int(np.size(video_frame, 0)))


        if debugmode == True :
            print('------------------OBJECT-------------------')
            print('full path  : ', self.file_fullpath)
            print('folderpath : ', self.file_folderpath)
            print('file name  : {}, (name : {}, ext : {})\n'.format(self.file_fullname, self.file_justfilename, self.file_justext))


    def writeAndSave(self, image) :
        tree = et.ElementTree(self.root)
        tree.write(file_or_filename =os.path.join(self.file_savefolder, self.xml_file_name))
        cv2.imwrite(os.path.join(self.file_savefolder, self.img_file_name), image)


    def setObject(self, bboxobj) :
        padding = 7
        obj = et.SubElement(self.root, "object")
        name = et.SubElement(obj, "name")
        name.text = bboxobj.name


        bbox = et.SubElement(obj, "bndbox")
        xmin = et.SubElement(bbox, "xmin")
        ymin = et.SubElement(bbox, "ymin")

        xmax = et.SubElement(bbox, "xmax")
        ymax = et.SubElement(bbox, "ymax")

        if int(bboxobj.xmin) - padding <= 0 :
            xmin.text = str(1)
        else :
            xmin.text = str(bboxobj.xmin - padding)

        if int(bboxobj.ymin) - padding <= 0 :
            ymin.text = str(1)
        else :
            ymin.text = str(bboxobj.ymin - padding)

        if int(bboxobj.xmax) + padding >= int(self.width.text) :
            xmax.text = str(self.width)
        else :
            xmax.text = str(bboxobj.xmax + padding)

        if int(bboxobj.ymax) + padding >= int(self.height.text) :
            ymax.text = str(self.height)
        else :
            ymax.text = str(bboxobj.ymax + padding)


'''
<?xml version="1.0"?>
<annontation>
    <folder>images</folder>
    <filename>10.jpg</filename>
    <size>
        <width>450</width>
        <height>328</height>
    </size>
    <object>
        <name>pig</name>
        <bndbox>
            <xmin>19</xmin>
            <ymin>84</ymin>
            <xmax>144</xmax>
            <ymax>236</ymax>
        </bndbox>
    </object>
    <object>
        <name>pig</name>
        <bndbox>
            <xmin>19</xmin>
            <ymin>84</ymin>
            <xmax>144</xmax>
            <ymax>236</ymax>
        </bndbox>
    </object>
    ...
</annontation>
'''