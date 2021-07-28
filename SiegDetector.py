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
    RectangularDetector = 0
    CircularDetector = 1



class SiegDetector(object):
    def __init__(self, detectorType=0):
        super().__init__
        self._detectorType = detectorType

    @property
    def detectorType(self):
        return self._dectorType

    @detectorType.setter
    def detectorType(self, t):
        self._detectorType = t

    @property
    def resolutionFunction(self):
        return self._resolutionFunction

    @resolutionFunction.setter
    def resolutionFunction(self, rf):
        self._resolutionFunction = rf

    @property
    def resolutionFunctionSigmaX(self):
        return self._resolutionFunctionSigmaX

    @resolutionFunctionSigmaX.setter
    def resolutionFunctionSigmaX(self, sig_x):
        self._resolutionFunctionSigmaX = sig_x

    @property
    def resolutionFunctionSigmaY(self):
        return self._resolutionFunctionSigmaX

    @resolutionFunctionSigmaY.setter
    def resolutionFunctionSigmaY(self, sig_y):
        self._resolutionFunctionSigmaY = sig_y

    @property
    def detectorDimensions(self):
        return self._detectorDimensions

    @detectorDimensions.setter
    def detectorDimensions(self, dims):
        self._detectorDimensions = dims