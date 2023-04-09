#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ScanBase import ScanBase
from selenium.webdriver.common.by import By
import re
import sys

pat_reso = re.compile(r'\((\d+) × (\d+)\)')

# need ref to webdriver to create it
class ParsingImageUrl():
    def __init__(self, driver:ScanBase):
        self.driver = driver

    # return img URL from img size page
    def GetDirectUrl(self, url_sizes):
        self.driver.get(url_sizes)
        # block with image sizes
        sizes_list = self.driver.find_element(By.CSS_SELECTOR, 'ol[class="sizes-list"]')
        # <li> of img resolution
        li_sizes_all = sizes_list.find_elements(By.XPATH, '//li[./small]')
        reso_max = 0
        li_size_max = None
        # find the highest resolution
        for li_size in li_sizes_all:
            reso = li_size.find_element(By.XPATH, './small').get_attribute('innerHTML')
            reso_parsed = pat_reso.fullmatch(reso)
            if not reso_parsed:
                sys.exit('Strange resolution label!')
            resolution = int(reso_parsed.group(1)) * int(reso_parsed.group(2))
            if resolution > reso_max:
                reso_max = resolution
                li_size_max = li_size
        # temporarily turn off wait time to speed up the following process
        self.driver.implicitly_wait(0)
        # get highest resolution img link tag (empty list if current resolution is the highest)
        a_size_max = li_size_max.find_elements(By.XPATH, './a')
        # if the current selected resolution is the highest, doesn't have to click link
        if a_size_max:
            self.driver.get( a_size_max[0].get_attribute('href').strip() )
        # get img URL
        src_img = self.driver.find_element(By.XPATH, '//div[@id="allsizes-photo"]/img').get_attribute('src').strip()
        self.driver.implicitly_wait( float(self.driver.scan_info['wait_time']) )
        return src_img
