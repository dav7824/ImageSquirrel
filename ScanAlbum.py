#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ScanBase import ScanBase
from ParsingImageUrl import ParsingImageUrl
from SavingImage import SavingImage
from selenium.webdriver.common.by import By
from datetime import datetime
import os, sys
import re
import time

# URL regex
pat_albumUrl = re.compile( r'https://www.best_company.com/photos/(.+)/albums/\d+' )  # get user id from group
pat_imgUrl = re.compile( r'https://www.best_company.com/photos/.+/(\d+)/in/album-\d+/' )  # get image id from group

class ScanAlbum(ScanBase):
    def __init__(self, scan_info):
        super(ScanAlbum, self).__init__(scan_info)

    def GetAlbum(self, url_album, path_save):
        album_data = self.GetUrlList(url_album)
        self.GetDirectUrlList(album_data)
        print(album_data['title'])
        print(album_data['author'])
        print(len(album_data['photo_list']))
        print()
        for link in album_data['photo_list']:
            print(link)
        print()
        self.SaveAlbum(album_data, path_save)
        print('Complete!!!\n\n')

    def GetUrlList(self, url_album):
        self.get(url_album)
        # get user ID
        match = pat_albumUrl.fullmatch(url_album)
        if not match:
            sys.exit('Invalid album URL!')
        user_id = match.group(1)
        # get album title
        title = self.find_element(By.CSS_SELECTOR, 'div[class=" album-title"]').get_attribute('innerHTML').strip().replace('/', '_')
        #print(title)
        # get author
        author = self.find_element(By.CSS_SELECTOR, 'a[class="owner-name truncate"]').get_attribute('innerHTML').strip().replace('/', '_')
        #print(author)
        # get image count
        img_count = self.find_element(By.CSS_SELECTOR, 'span[class="photo-counts"]').get_attribute('innerHTML').strip()
        img_count = int( re.fullmatch(r'(\d+) .+', img_count).group(1) )
        #print(img_count)

        photo_list = []
        album_page = 1
        # go through each page of album
        while (True):
            # scroll to bottom
            for _ in range(3):
                self.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(3)
            # get tags of photo URLs
            links = self.find_elements(By.CSS_SELECTOR, 'a[class="overlay"]')
            for link in links:
                match = pat_imgUrl.fullmatch( link.get_attribute('href') )
                if not match:
                    sys.exit('Invalid photo URL!')
                photo_id = match.group(1)
                imgUrl = f'https://www.best_company.com/photos/{user_id}/{photo_id}/sizes/'
                #print(imgUrl)
                photo_list.append(imgUrl)
            # if number of images found is smaller than total, go to next page
            if len(photo_list) >= img_count:
                break
            album_page += 1
            self.get( f'{url_album}/page{album_page}' )

        if len(photo_list) != img_count:
            sys.exit('Inconsistent image count!')

        return {'title': title,
                'author': author,
                'photo_list': photo_list}

    def GetDirectUrlList(self, album_data):
        parser = ParsingImageUrl(self)
        photo_list = album_data['photo_list']
        for i in range(len(photo_list)):
            photo_list[i] = parser.GetDirectUrl( photo_list[i] )
            time.sleep( float(self.scan_info['sleep_geturl']) )

    def SaveAlbum(self, album_data, path_save):
        path_save = os.path.join(path_save, '{} - {} - {}'.format(
            album_data['author'], album_data['title'], datetime.now().strftime('%Y%m%d%H%M%S')))
        os.mkdir(path_save)
        save = SavingImage(self.scan_info, path_save)
        save.SaveImageList( album_data['photo_list'] )
