#!/Users/robtu/opt/anaconda3/bin/python3

from PIL import Image
import os, sys
import imghdr
import argparse


path = "./"

parser = argparse.ArgumentParser()

# PATH
parser.add_argument('datapath', nargs='?', type=str, default=path, help='Full Path ')
# size Height
parser.add_argument('-d', '--height', type=int, default=128, help='Size Height.')
# size Width
parser.add_argument('-w', '--width', type=int, default=50, help='Size Width.')
# output format
parser.add_argument('-f', '--imfmt', type=str, default="", help='Size Width.')

args = parser.parse_args()


print(args)
print(args.height, args.width, args.datapath)




dirs = os.listdir( path )

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            if(imghdr.what(path+item)!=None):
              im = Image.open(path+item)
              f, e = os.path.splitext(path+item)
              print(item, f, e)
	      
              imResize = im.resize((args.width,args.height), Image.ANTIALIAS)
              if not args.imfmt:
                imResize.save(f + ' resized' + e)
              else:
                imResize.save(f + ' resized.jpg', args.imfmt)
resize()



