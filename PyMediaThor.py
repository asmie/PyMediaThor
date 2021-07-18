import argparse
import imghdr
import pathlib
import os

from PIL import Image
from PIL.ExifTags import TAGS

def extractDate(file):
    str = ''
    image = Image.open(file)
    exifdata = image.getexif()
    date = exifdata.get(306)
    if date == None:
        date = exifdata.get(36867)      # DateTime original
    if date == None:
        date = exifdata.get(36868)      # DateTime digitalized
    if (date != None):
        str = date.replace(':', '').replace(' ', '_')
    return str
    

parser = argparse.ArgumentParser(description='Swiss knife for manipulating set of media files.')
parser.add_argument('--dir', nargs='?', const='.', default=os.getcwd(), help='Directory with media files', type=pathlib.Path)
parser.add_argument('--recursive', '-R', action='store_true', help='Go into subdirectories recursively')
parser.add_argument('--verbose', '-v', action='count', default=0, help='Be more verbose. -vv to get much more verbose info.')

args = parser.parse_args()

print(args)

for p in pathlib.Path(args.dir).iterdir():
    if p.is_file():
        if imghdr.what(str(p)) != 'jpeg': continue
        filename = extractDate(p)
        if (filename == ''): continue
        found = False
        iter = 0
        new_name = str(args.dir) + '\\' + filename + p.suffix
        while not found:
            if os.path.isfile(new_name):
                new_name = str(args.dir) + '\\' + filename + '_' + iter + p.suffix
                iter += 1
            else:
                found = True;
        print('Replacing ' + str(p) + ' with ' + new_name)
        os.rename(str(p), new_name)


