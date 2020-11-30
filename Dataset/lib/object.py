import xml.etree.ElementTree as ET
from PIL import Image
import os, sys
import imghdr
import argparse

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
      print(obj.startx, obj.starty, obj.endx, obj.endy, obj.name)


  def saveObjectImage (self, savelist=[]):
     f, e = os.path.splitext(self.savePath+self.imgName)
     print(f, e)
     for obj in self.objList:
      print(f+'_'+obj.name+e)
      cropImg=obj.crop()
      cropImg.save(f+'_'+obj.name+e)
      cropImg.show()

    

img=0
xmlfile=ET.parse("../2v2Label/IMG_6098 003.xml")
img = Image.open("../2v2Image/IMG_6098 003.jpg")
xmlImage=XMLImage(xmlfile, img, "./", "../2v2Image/", "../2v2Image/")
xmlImage.saveObjectImage()
