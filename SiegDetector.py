# -*- coding: utf-8 -*-
"""
@author:    Amir Tosson
@license:   GNU General Public License v3 or higher
@copyright: Universität Siegen, Deutschland
@email:     tosson@physik.uni-siegen.de
"""

"""
summary:    detector class contains all details of the detector

name:       SiegDetector

date:       20-04-2021

"""
import enum


class DetectorType(enum.Enum):
    RectangularDetector = 1
    CircularDetector = 2



class SiegDetector(object):
    def __init__(self, detectorType=1, resFunction1=0.2, resFunction2=0.2):
        super().__init__
        self._detectorType = detectorType
        self._resolutionFunction1 = resFunction1
        self._resolutionFunction2 = resFunction2

    @property
    def detectorType(self):
        return self._dectorType

    @detectorType.setter
    def detectorType(self, t):
        self._detectorType = t

    @property
    def resolutionFunction1(self):
        return self._resolutionFunction1

    @resolutionFunction1.setter
    def resolutionFunction1(self, resFunction1):
        self._resolutionFunction1 = resFunction1


    @property
    def resolutionFunction2(self):
        return self._resolutionFunction2

    @resolutionFunction2.setter
    def resolutionFunction2(self, resFunction2):
        self._resolutionFunction2 = resFunction2
