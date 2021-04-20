import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
import os, sys
import imghdr
import argparse
import glob
#import cv2 as cv
#import numpy as np





class XMLObject:
  def __init__ (self, Ent, img):
    bndbox=Ent.find('bndbox')
    self.startx=int(bndbox.find('xmin').text)
    self.starty=int(bndbox.find('ymin').text)
    self.endx=int(bndbox.find('xmax').text)
    self.endy=int(bndbox.find('ymax').text) 
    self.name = Ent.find('name').text
    self.pose = Ent.find('pose').text
    self.img = img
  def crop(self):
    return self.img.crop((self.startx, self.starty, self.endx, self.endy))

class XMLImage:
  def __init__ (self, imgEnt, img, xmlPath="", imgPath="", savePath=""):
    self.imgName=imgEnt.find('filename').text
    self.img = img
    if (xmlPath == ""):
      self.imgNamemgPath=imgEnt.find('path').text
    else:
      self.imgPath=imgPath
      
    self.xmlPath=xmlPath
    self.savePath=savePath

    imgSource=imgEnt.find('source')
    self.dBaseName=imgSource.find('database').text
    
    imgSize=imgEnt.find('size')
    self.width=int(imgSize.find('width').text)
    self.height=int(imgSize.find('height').text)
    self.depth=int(imgSize.find('depth').text)
    
    self.xmlObjList=imgEnt.findall('object')
    self.objList=[]
    for obj in self.xmlObjList:
       self.objList.append(XMLObject(obj, img))
    
    for obj in self.objList:
      print("(",obj.startx, obj.starty, obj.endx, obj.endy, obj.name, ")", obj.endx-obj.startx, obj.endy - obj.starty, round((obj.endy - obj.starty)/(obj.endx-obj.startx),2))


  def saveObjectImage (self, savelist=[]):
     saveName=self.imgName.replace(' ', '_')
     f, e = os.path.splitext(saveName)
     #print(f, e)
     for obj in self.objList:
#      print(f+'_'+obj.name+e, '       ', obj.name)
      cropImg=obj.crop()
      cropImg.save(self.savePath+f+'_'+obj.name+e)
      #cropImg.show()

  def drawBBox (self, color=(0,0,255), lWidth=3):
     newImg = self.img
     draw = ImageDraw.Draw(newImg)
     
     for obj in self.objList:
       draw.rectangle([(obj.startx, obj.starty),(obj.endx,obj.endy)], fill=None, outline="red", width=lWidth)

     return newImg
    


def retrieve(imgPath, xmlPath, datapath):
    xmldirs = os.listdir( xmlPath )
    imgdirs = os.listdir( imgPath )
    
    for item in xmldirs:
        if os.path.isfile(xmlPath+item):
            f, e = os.path.splitext(item)
            if (e=='.xml'):
              xmlfile=ET.parse(xmlPath+item)
              imgname=glob.glob(imgPath+f+".*")
              for imgItem in imgname:
#                  if(imghdr.what(imgItem)!=None):
                      img = Image.open(imgItem)
                      xmlImage=XMLImage(xmlfile, img, xmlPath, imgPath, datapath)
                      xmlImage.saveObjectImage()
            

def drawBBox(imgPath, xmlPath, datapath):
    xmldirs = os.listdir( xmlPath )
    imgdirs = os.listdir( imgPath )
    
    for item in xmldirs:
        if os.path.isfile(xmlPath+item):
            f, e = os.path.splitext(item)
            if (e=='.xml'):
              xmlfile=ET.parse(xmlPath+item)
              imgname=glob.glob(imgPath+f+".*")
              for imgItem in imgname:
#                  if(imghdr.what(imgItem)!=None):
                img = Image.open(imgItem)
                xmlImage=XMLImage(xmlfile, img, xmlPath, imgPath, datapath)
                      
                newImg=xmlImage.drawBBox()
                saveName= xmlImage.imgName.replace(' ', '_')
                f, e = os.path.splitext(saveName)
                newImg.save(xmlImage.savePath+f+'_bbx'+e)
                      



      



path = "./"

parser = argparse.ArgumentParser()
# PATH
parser.add_argument('datapath', nargs='?', type=str, default=path, help='Destination Path')
# size Height
parser.add_argument('-i', '--imgPath', type=str, default=path, help='Image Path')
# size Width
parser.add_argument('-x', '--xmlPath', type=str, default=path, help='XML Path')

args = parser.parse_args()
print(args)
print(args.imgPath, args.xmlPath, args.datapath)

              
#retrieve(args.imgPath, args.xmlPath, args.datapath)
drawBBox(args.imgPath, args.xmlPath, args.datapath)


#img=0
#xmlfile=ET.parse("../2v2Label/IMG_6098 003.xml")
#img = Image.open("../2v2Image/IMG_6098 003.jpg")
#xmlImage=XMLImage(xmlfile, img, "./", "../2v2Image/", "../2v2Image/")
#xmlImage.saveObjectImage()


 



