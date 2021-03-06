#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Image import Image #Heritage
import rawpy #Python wrapper for the LibRaw library (raw image decoder)
from rawpy import ColorSpace
from rawpy import DemosaicAlgorithm
import numpy as np

class ImageRaw(Image):
    """docstring for ImageRaw"""
    def __init__(self, path):
        """ Convert RAW images to 3-color array (ndarray) """
        # Load the RAW file
        self._file = rawpy.imread(path)
        # Save the size of the image
        raw_height, raw_width, height, width, top_margin, left_margin, iheight, iwidth, pixel_aspect, flip= (self._file).sizes
        size = (height,width)
        # Postprocess this file to obtain a numpy ndarray of shape (h,w,c) : 16 bits => la palette de couleur peut contenir 2^16 = 65536 couleurs
        ndarray = self._file.postprocess(output_bps=16, output_color=ColorSpace.raw, demosaic_algorithm=DemosaicAlgorithm.VNG, use_camera_wb=True, no_auto_bright=True)
        # SuperClass Constructor
        super(ImageRaw,self).__init__(path,ndarray,size)

    def getFile(self):
    	""" Return the file of ImageRaw"""
        return self._file
