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
    sampleIsReady = False
    detectorIsReady = False
    simIsReady = False
    beamIsReady = False
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
        self.configBeamButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
        self.submitButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_ArrowRight')))
        self.autoRandCheckBox.stateChanged.connect(self.UseAutomaticRandomization)
        self.configSampleButton.clicked.connect(self.OpenSamplePage)
        self.configDetectorButton.clicked.connect(self.OpenDetectorPage)
        self.configBeamButton.clicked.connect(self.OpenBeamPage)
        self.configSimButton.clicked.connect(self.OpenSimPage)
        self.randomParaOKButton.clicked.connect(self.SubmitRandomizationPara)
        self.setButton.clicked.connect(self.SetLayers)
        self.tabWidget.currentChanged.connect(self.SubmitButtonText)
        self.submitButton.clicked.connect(self.SumbitUserInput)



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
            self.setButton.setEnabled(False)
        else:
           self.randGroupBox.setHidden(True)
    
    
    def SubmitButtonText(self, ind):
        self.submitButton.setEnabled(True)
        if ind == 0:
            self.submitButton.setText("Submit sample")
        elif ind == 1:
            self.submitButton.setText("Submit detector")
        elif ind == 2:
            self.submitButton.setText("Submit beam")
        else:   
            self.submitButton.setText("Start simulation")
            if not self.simIsReady or not self.sampleIsReady or not self.beamIsReady or not self.detectorIsReady:
                self.submitButton.setEnabled(False)
                
    
    def OpenSamplePage(self):                                              
        self.tabWidget.setCurrentIndex(0)
        self.SubmitButtonText(0)
    
    def OpenDetectorPage(self):                                              
        self.tabWidget.setCurrentIndex(1) 
        self.SubmitButtonText(1)
    
    def OpenBeamPage(self):                                              
        self.tabWidget.setCurrentIndex(2) 
        self.SubmitButtonText(2)
    
    def OpenSimPage(self):                                              
        self.tabWidget.setCurrentIndex(3)
        self.SubmitButtonText(3)
        
    def UpdateTODOButtonsIcons(self):
        if self.sampleIsReady:
            self.configSampleButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogApplyButton')))
        else:
            self.configSampleButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))

        if self.detectorIsReady:
            self.configDetectorButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogApplyButton')))
        else:
            self.configDetectorButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
            
        if self.beamIsReady:      
            self.configBeamButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogApplyButton')))
        else:                         
            self.configBeamButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
  
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
            self.setButton.setEnabled(True)
            
    def CheckRndParas(self,rndArr):   
        if rndArr[1] >= rndArr[0]:
            return True
        else:
            return False
        
    def SetLayers(self):
        numRows = self.numOfLayerSpinBox.value()
        self.layerTable.setRowCount(numRows)
        for row in range(self.numOfLayerSpinBox.value()):
            #self.layerTable.insertRow(self.layerTable.rowCount())
            item = QtWidgets.QTableWidgetItem(str(row+1))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.layerTable.setItem(row, 0, item)
            self.layerTable.setItem(row, 1, QtWidgets.QTableWidgetItem("Layer_" +  str(row+1)))
            if self.autoRandCheckBox.isChecked():
                self.layerTable.setItem(row, 2, QtWidgets.QTableWidgetItem("RANDOM " +  str(self.rndMatrix[0]) + ":" + str(self.rndMatrix[1])))
                self.layerTable.setItem(row, 3, QtWidgets.QTableWidgetItem("RANDOM " +  str(self.rndMatrix[2]) + ":" + str(self.rndMatrix[3])))
            else:
                self.layerTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(0.0)))
                self.layerTable.setItem(row, 3, QtWidgets.QTableWidgetItem(str(0.0)))

    def SumbitUserInput(self):
       switcher = {0: self.SubmitSample(), 1: self.SubmitDetector(), 2: self.SubmitBeam(), 3: self.StartSim()} 
       func = switcher.get(0) 
       func
       
    def SubmitSample(self):
        print("SubmitSample")
        
    def SubmitBeam(self):
        print("SubmitBeam")       
        
    def SubmitDetector(self):
        print("SubmitDetector")        
        
    def StartSim(self):
        print("StartSim")        
        
        