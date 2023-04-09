#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ScanInfo
from ScanAlbum import ScanAlbum

if __name__ == '__main__':
    scan_info = ScanInfo.ReadInfo('scan_info.txt')
    scan = ScanAlbum(scan_info)
    scan.GetAlbum('<url>', 'local')
