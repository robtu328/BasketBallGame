import xml.etree.ElementTree as ET


class XMLObject:
  def __init__ (self, Ent, img):
    bndbox=Ent.find('bndbox')
    self.startx=int(bndbox.find('xmin').text)
    self.starty=int(bndbox.find('ymin').text)
    self.width=int(bndbox.find('xmax').text) - self.startx
    self.height=int(bndbox.find('ymax').text) - self.starty
    self.name = Ent.find('name').text
    self.pose = Ent.find('pose').text
    self.img = img


class XMLImage:
  def __init__ (self, imgEnt, img, path=""):
    self.imgName=imgEnt.find('filename').text
    if (path == ""):
      self.path=imgEnt.find('path').text
    else:
      self.path=path
      
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
      print(obj.startx, obj.starty, obj.width, obj.height, obj.name)



img=0
xmlfile=ET.parse("../2v2labeldata/2v2xml/IMG_6098 003.xml")
xmlImage=XMLImage(xmlfile, img, "./")


 



