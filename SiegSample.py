# -*- coding: utf-8 -*-
"""
@author:    Amir Tosson
@license:   GNU General Public License v3 or higher
@copyright: Universität Siegen, Deutschland
@email:     tosson@physik.uni-siegen.de   
"""

"""
summary:    samole class contains all details of the sample

name:       SiegSample

date:       20-04-2021

"""

class SiegSample(object):
    def __init__(self, numOfLayer=1, isReferenceSample=False):
        super().__init__
        self._numOfLayer = numOfLayer
        self._isReferenceSample = isReferenceSample
        
    @property
    def numOfLayer(self):
        return self._numOfLayer
    
    @numOfLayer.setter
    def numOfLayer(self, num):
        self._numOfLayer = num
        
    @property
    def isReferenceSample(self):
        return self._isReferenceSample
    
    @isReferenceSample.setter
    def isReferenceSample(self, isReference):
        self._isReferenceSample = isReference
               
    @property
    def layersData(self):
        return self._layersData
    
    @layersData.setter
    def layersData(self, dataArr):
        self._layersData = dataArr