# Final Project
# Zachary Levin

import os
import errno

from classes import Image
from os import path

SRC_FOLDER = 'source'
OUT_FOLDER = 'output'
IMG_EXTS = ['png', 'jpeg', 'jpg', 'gif', 'tiff', 'tif', 'raw', 'bmp']

if __name__ == '__main__':
    try:
        os.makedirs(OUT_FOLDER)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    for filename in os.listdir(SRC_FOLDER):
        ext = filename[filename.rfind('.') + 1:]
        if ext not in IMG_EXTS:
            continue

        image = Image(path.join(SRC_FOLDER, filename))
        print '{} is {} pixels'.format(filename, image.dimensions())
        image.linear_center = raw_input('Tiltshift center: ')
        image.tiltshift_radius = raw_input('Tiltshift radius: ')
        image.tiltshift()
        image.write(path.join(OUT_FOLDER, filename))
