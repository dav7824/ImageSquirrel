#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

class ScanBase(webdriver.Chrome):
    def __init__(self, scan_info):
        self.scan_info = scan_info
        # Note: With the new updates of Selenium & Chrome, it seems that one no longer needs to manually download and set chrome driver. Hence, this line is commented.
        #os.environ['PATH'] += ':' + self.scan_info['path_driver']  # add driver to system path
        super(ScanBase, self).__init__()
        self.implicitly_wait( float(self.scan_info['wait_time']) )
        self.maximize_window()
        self.LoggingIn()
        time.sleep(5)  # wait for login to complete

    def LoggingIn(self):
        self.get( self.scan_info['url_login'] )
        nameInput = self.find_element(By.CSS_SELECTOR, 'input[data-testid="identity-email-input"]')
        nameInput.send_keys( self.scan_info['email'] )
        nextBtn = self.find_element(By.CSS_SELECTOR, 'button[data-testid="identity-form-submit-button"]')
        nextBtn.click()
        pwInput = self.find_element(By.CSS_SELECTOR, 'input[data-testid="identity-password-input"]')
        pwInput.send_keys( self.scan_info['password'] )
        nextBtn = self.find_element(By.CSS_SELECTOR, 'button[data-testid="identity-form-submit-button"]')
        nextBtn.click()
