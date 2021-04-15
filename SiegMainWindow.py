# -*- coding: utf-8 -*-
"""
@author:    Amir Tosson
@license:   GNU General Public License v3 or higher
@copyright: Universität Siegen, Deutschland
@email:     tosson@physik.uni-siegen.de   
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import SiegSimulationControls as _siegSim 


class SiegMainWindow(QtWidgets.QMainWindow):
    g = 0
    sampleIsReady = False
    detectorIsReady = False
    simIsReady = False
    rndMatrix = [0,0,0,0]
    rndParasAreOK = False
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        uic.loadUi("siegmainwindow.ui", self)
        self.fullscreenAction.triggered.connect(self.FullscreenAction)
        self.randGroupBox.setHidden(True)
        self.configSampleButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
        self.configDetectorButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
        self.configSimButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
        self.autoRandCheckBox.stateChanged.connect(self.UseAutomaticRandomization)
        self.configSampleButton.clicked.connect(self.OpenSamplePage)
        self.configDetectorButton.clicked.connect(self.OpenDetectorPage)
        self.configSimButton.clicked.connect(self.OpenSimPage)
        self.randomParaOKButton.clicked.connect(self.SubmitRandomizationPara)
        
    def speaking_method(self):                                              
        _siegSim.Test()
        
    def FullscreenAction(self):                                              
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
            
    def UseAutomaticRandomization(self):
        if self.autoRandCheckBox.isChecked():
            self.randGroupBox.setHidden(False)
        else:
           self.randGroupBox.setHidden(True)
    
    def OpenSamplePage(self):                                              
        self.tabWidget.setCurrentIndex(0)
    
    def OpenDetectorPage(self):                                              
        self.tabWidget.setCurrentIndex(1)    
    
    def OpenSimPage(self):                                              
        self.tabWidget.setCurrentIndex(2)
        
    def UpdateTODOButtonsIcons(self):
        if self.sampleIsReady:
            self.configSampleButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogApplyButton')))
        else:
            self.configSampleButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))

        if self.detectorIsReady:
            self.configDetectorButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogApplyButton')))
        else:
            self.configDetectorButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
  
        if self.simIsReady:      
            self.configSimButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogApplyButton')))
        else:                         
            self.configSimButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
            
    def SubmitRandomizationPara(self):
        self.rndMatrix[0] = self.disSpinBoxMin.value()
        self.rndMatrix[1] = self.disSpinBoxMax.value()
        self.rndMatrix[2] = self.thickSpinBoxMin.value()
        self.rndMatrix[3] = self.thickSpinBoxMax.value()
        self.rndParasAreOK = self.CheckRndParas(self.rndMatrix)
        if not self.rndParasAreOK:
            self.errorText.setText("Enteries are not valid")
        else:
            self.errorText.setText("")
    def CheckRndParas(self,rndArr):   
        if rndArr[1] >= rndArr[0]:
            return True
        else:
            return False