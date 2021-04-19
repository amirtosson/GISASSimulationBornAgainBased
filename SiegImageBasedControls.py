# -*- coding: utf-8 -*-
"""
@author:    Amir Tosson
@license:   GNU General Public License v3 or higher
@copyright: Universität Siegen, Deutschland
@email:     tosson@physik.uni-siegen.de   
"""

"""
summary:    this model contains the functions required to perform
            image-wise processes.

name:       SiegImageBasedControls

date:       19-04-2021
     
"""
from skimage import measure
import numpy as np
from math import log10, sqrt

class SiegImageBasedControls(object):
    def __init__(self):
        super().__init__
        
       
    def MSE(imageA, imageB):
        
        """
        Description
        -----------
        the 'Mean Squared Error' between the two images
        
        Parameters
        ----------
        imageA : TYPE array
                DESCRIPTION the 1st image array
        imageB : TYPE array
                DESCRIPTION the 2nd image array
    
        Returns
        -------
        MSE :   TYPE float
                DESCRIPTION the MSE difference , the lower the error, the more "similar"
                the two images are
        """ 
        return np.mean((imageA.astype("float") - imageB.astype("float")) ** 2)
        
    
    def SSIM(imageA, imageB):
        
        """
        Description
        -----------
        the 'Structural Similarity Index Method' between the two images
        
        Parameters
        ----------
        imageA : TYPE array
                DESCRIPTION the 1st image array
        imageB : TYPE array
                DESCRIPTION the 2nd image array
    
        Returns
        -------
        SSIM :   TYPE float
                DESCRIPTION the SSIM difference 
        """ 
        return measure.compare_ssim(imageA, imageB)    
       
    
    def PSNR(imageA, imageB, self):
                
        """
        Description
        -----------
        the 'Peak Signal to Noise Ratio' between the two images
        
        Parameters
        ----------
        imageA : TYPE array
                DESCRIPTION the 1st image array
        imageB : TYPE array
                DESCRIPTION the 2nd image array
    
        Returns
        -------
        PNSR :   TYPE float
                DESCRIPTION the PNSR difference 
        """ 
        mse = self.MSE(imageA, imageB)
        if(mse == 0):
            return 100
        return 20 * log10(255.0 / sqrt(mse))    
    
    
    
    
    
    
    
    
    
    
    
    
    