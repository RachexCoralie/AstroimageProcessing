#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import imageio
import rawpy #Python wrapper for the LibRaw library (raw image decoder)
from rawpy import ColorSpace
from rawpy import DemosaicAlgorithm

# The FITS format is the most popular way to save and interchange astronomical data. The files are organized in units each of which contains a human readable header and a data. This structure is refereed as HDUs (Header/DATA Unit).
# http://python-astro.blogspot.fr/2012/03/play-with-fits-files.html
import pyfits
import numpy as np



#-------------------- Image --------------------#
class Image(object):
    """docstring for Image"""
    def __init__(self, path):
        super(Image, self).__init__()
        print('path : ' + path)
        self.path = path


    # To get back the size of the image
    def getSize(self):
    	return (self._height, self._width)




#-------------------- ImageRaw --------------------#
class ImageRaw(Image):
    """docstring for ImageRaw"""
    def __init__(self, path):
        super(ImageRaw, self).__init__(path)
        # Load a RAW file
        self._file = rawpy.imread(_path)
        # Erreur sur cette ligne, me dit que size n'existe pas
    	# self.raw_height, self.raw_width, self.height, self.width, self.top_margin, self.left_margin, self.iheight, self.iwidth, self.pixel_aspect, self.flip = self.file.size


    # Postprocess this file to obtain a numpy ndarray of shape (h,w,c)
    # 16 bits => la palette de couleur peut contenir 2^16 = 65536 couleurs
    def debayeurization(self):
    	self._img = self._file.postprocess(output_bps=16, output_color=ColorSpace.sRGB, demosaic_algorithm=DemosaicAlgorithm.AAHD, use_camera_wb=True, no_auto_bright=True)


    def getImageDebayeurization(self):
        return self._img


    def getFile(self):
        return self._file



#-------------------- ImageFits --------------------#
class ImageFits(Image):
    """docstring for ImageFits"""
    def __init__(self, path):
        super(ImageFits, self).__init__(path)


    # Opening FITS files and loading the image data
    def readFITS(self):
    	self._hduList = pyfits.open(self._path, uint=True, do_not_scale_image_data=False) # returns an object called an HDUList which is a list-like collection of HDU objects.
    	self._imageData = self._hduList[0].data # hdulist[0] is the primary HDU, hdulist[1] is the first extension HDU, etc. The data attribute of the HDU object will return a numpy ndarray object.
    	self._hduList.close() # the headers will still be accessible after the HDUList is closed

    #hdu,imageDataRed, imageDataGreen, imageDataBlue = readFITS('M13_blue_0001.fits')
    #print(hdu.info())


    # Convert separate FITS images (RGB) to 3-color array (nparray)
    # Need fitsPathRed, fitsPathGreen, fitsPathBlue : each file is inside a folder give by the path
    # Name of the file : red.fits / green.fits / blue.fits
    def convertFITSToRGB(self):
        fitsPathRed = self._path + "red.fits"
        fitsPathGreen = self._path + "green.fits"
        fitsPathBlue = self._path + "blue.fits"

    	hduListRed, imageDataRed = readFITS(fitsPathRed)
    	hduListGreen, imageDataGreen = readFITS(fitsPathGreen)
    	hduListBlue, imageDataBlue = readFITS(fitsPathBlue)
    	height,width = imageDataRed.shape
    	dataType = imageDataRed.dtype.name
    	#print('')
    	#print('DATATYPE')
    	#print(dataType)
    	self._rgbArray = np.empty(shape=(height,width,3),dtype=dataType)
    	self._rgbArray[:,:,0] = imageDataRed
    	self._rgbArray[:,:,1] = imageDataGreen
    	self._rgbArray[:,:,2] = imageDataBlue
    	#print('ConvertFIFTS')
    	#print(rgbArray[:,:,0])


    # Converting a 3-color array to separate FITS images
    def convertRGBToFITS(self, rgbArray, fitsName, LATOBS='Not informed', LONGOBS='Not informed'):
        self._rgbArray = rgbArray
    	npr = self._rgbArray[:,:,0]
    	#print("CONVERT TO FITS")
    	#print(npr)
    	npg = self._rgbArray[:,:,1]
    	npb = self._rgbArray[:,:,2]

    	red = pyfits.PrimaryHDU()
    	red.header['LATOBS'] = LATOBS
    	red.header['LONGOBS'] = LONGOBS
    	red.data = npr
    	#print("DATA LOAD")
    	#print(red.data)
    	red.writeto(fitsName+'_red.fits')

    	green = pyfits.PrimaryHDU()
    	green.header['LATOBS'] = LATOBS
    	green.header['LONGOBS'] = LONGOBS
    	green.data = npg
    	green.writeto(fitsName+'_green.fits')

    	blue = pyfits.PrimaryHDU()
    	blue.header['LATOBS'] = LATOBS
    	blue.header['LONGOBS'] = LONGOBS
    	blue.data = npb
    	blue.writeto(fitsName+'_blue.fits')

    def getRGBArray(self):
        return self._rgbArray

    def getHduListImageData(self, arg):
        return (self._hduList, self._imageData)



#---------- TESTS -------------#

#import imageio

#path = 'DSC_0599.NEF'
#file = loadRaw(path)
#array = debayeurization(file)



if __name__ == '__main__':
    path = '../../Pictures_test/'
    iR1 = ImageRaw(path + 'DSC_0599.NEF')
    iR1.debayeurization()
    imageio.imsave('../../Pictures_test/testFITS.tiff', iR1.getImageDebayeurization())

    # iF1 = ImageFits(path)
    # iF2 = ImageFits(path + 'FITS/')
    # # iF1.convertRGBToFITS(iR1.getImageDebayeurization(),'test')
    # iF2.convertFITSToRGB()
    # imageio.imsave('testFITS.tiff', iF2.getRGBArray)
