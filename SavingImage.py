#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image
import requests
import io
import os
import time

class SavingImage():
    def __init__(self, scan_info, path_save):
        self.scan_info = scan_info
        self.path_save = path_save

    # save according to list of links
    def SaveImageList(self, url_list):
        for img_url in url_list:
            img_cont = requests.get(img_url).content
            img_file = io.BytesIO(img_cont)
            image = Image.open(img_file)
            img_path = os.path.join( self.path_save, os.path.basename(img_url) )
            with open(img_path, 'wb') as f:
                image.save(f)
            print( f'Img successfully saved: {img_path}' )
            time.sleep( float(self.scan_info['sleep_save']) )
