# -*- coding: utf-8 -*-
"""
@author:    Amir Tosson
@license:   GNU General Public License v3 or higher
@copyright: Universität Siegen, Deutschland
@email:     tosson@physik.uni-siegen.de   
"""

"""
summary:    this model contains the controls and APIs of the 
            main-window 

name:       SiegMainWindow

date:       01-04-2021
     
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import csv
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
import time
import numpy as np
import sys
import SiegSimulationControls as _siegSim
import SiegSample as _siegSample
import SiegDetector as _siegDetector
from random import randint
from numpy import loadtxt

#from matplotlib.backends.qt_compat import QtCore, QtWidgets

if int(QtCore.qVersion()[0]) > 4:
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class SiegMainWindow(QtWidgets.QMainWindow):
    sampleIsReady = False
    detectorIsReady = False
    simIsReady = False
    beamIsReady = False
    rndMatrix = [0, 0, 0, 0]
    rndParasAreOK = False
    RefImg = [ ]
    static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
    dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
    user_canvas = FigureCanvas(Figure(figsize=(5, 3)))
    _static_ax = static_canvas.figure.subplots()
    _simControls = _siegSim.SiegSimulationControls();




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        #TODO: Set tooltips
        uic.loadUi("siegmainwindow.ui", self)
        # which defines a single set of axes as self.axes.
        layout = QtWidgets.QVBoxLayout(self.plotWidget)

        # static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.static_canvas)
        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)

        self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(self.static_canvas, self))
        #self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(self.user_canvas, self))
        user_canvas = FigureCanvas(Figure(figsize=(5, 5)))
        file_data_layout = QtWidgets.QVBoxLayout(self.controlWidget)
        file_data_layout.addWidget(user_canvas)
        #self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(self.user_canvas, self))
        #self._timer = dynamic_canvas.new_timer(
        #    100, [(self._update_canvas, (), {})])
        #self._timer.start()
        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._dynamic_ax2 = user_canvas.figure.subplots()

        self.fullscreenAction.triggered.connect(self.FullscreenAction)
        self.randGroupBox.setHidden(True)
        self.diffGroupBox.setHidden(True)
        self.configInitImgToolButton.setHidden(True)
        self.configSampleButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
        self.configInitImgToolButton.setIcon(
            self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
        self.configDetectorButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
        self.configSimButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
        self.configBeamButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
        self.submitButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_ArrowRight')))
        self.autoRandCheckBox.stateChanged.connect(self.UseAutomaticRandomization)
        self.incDiffCheckBox.stateChanged.connect(self.UseDifference)
        self.configSampleButton.clicked.connect(self.OpenSamplePage)
        self.configInitImgToolButton.clicked.connect(self.OpenInitImgPage)
        self.configDetectorButton.clicked.connect(self.OpenDetectorPage)
        self.configBeamButton.clicked.connect(self.OpenBeamPage)
        self.configSimButton.clicked.connect(self.OpenSimPage)
        self.randomParaOKButton.clicked.connect(self.SubmitRandomizationPara)
        self.setButton.clicked.connect(self.SetLayers)
        self.uploadFromFileButton.clicked.connect(self.UploadFile)
        #self.setButton.setToolTip("")
        self.tabWidget.currentChanged.connect(self.SubmitButtonText)
        self.submitButton.clicked.connect(self.SumbitUserInput)
        self.sampleTypeComboBox.currentIndexChanged.connect(self.SampleTypeChanged)

    def speaking_method(self):
        _siegSim.Test()


    def onclick(self, event):
        ix, iy = event.xdata, event.ydata
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 1024)
        # Shift the sinusoid as a function of time.
        max_index_col = np.argmax(self.RefImg, axis=1)
        print(max_index_col)
        self._dynamic_ax.plot(t, self.RefImg[:, max_index_col[0]])
        with open('data2.csv', 'a', encoding='UTF8', newline='') as fd:
            np.savetxt(fd, self.RefImg[:, max_index_col[0]], delimiter=",")

        self._dynamic_ax.figure.canvas.draw()

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

    def UseDifference(self):
        if self.incDiffCheckBox.isChecked():
            self.diffGroupBox.setHidden(False)
            self.setButton.setEnabled(False)
            self.configInitImgToolButton.setHidden(False)
        else:
            self.diffGroupBox.setHidden(True)
            self.configInitImgToolButton.setHidden(True)

    def SubmitButtonText(self, ind):
        self.submitButton.setEnabled(True)
        self.submitButton.setVisible(True)
        if ind == 0:
            self.submitButton.setText("Submit sample")
        elif ind == 1:
            self.submitButton.setText("Submit detector")
        elif ind == 2:
            self.submitButton.setText("Submit beam")
        elif ind == 4:
            self.submitButton.setText("Generate init-img")
        elif ind == 5:
            self.submitButton.setVisible(False)
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

    def SampleTypeChanged(self, ind):
        if ind == 0:
            self.autoRandCheckBox.setHidden(False)
            self.incDiffCheckBox.setHidden(False)
        elif ind == 1:
            self.autoRandCheckBox.setHidden(True)
            self.incDiffCheckBox.setHidden(True)
            self.autoRandCheckBox.setCheckState(False)
            self.incDiffCheckBox.setCheckState(False)

    def OpenInitImgPage(self):
        self.tabWidget.setCurrentIndex(4)
        self.SubmitButtonText(4)

    def UpdateTODOButtonsIcons(self):
        if self.sampleIsReady:
            self.configSampleButton.setIcon(
                self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogApplyButton')))
        else:
            self.configSampleButton.setIcon(
                self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))

        if self.detectorIsReady:
            self.configDetectorButton.setIcon(
                self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogApplyButton')))
        else:
            self.configDetectorButton.setIcon(
                self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))

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

    def CheckRndParas(self, rndArr):
        if rndArr[1] >= rndArr[0]:
            return True
        else:
            return False

    def SetLayers(self):
        numRows = self.numOfLayerSpinBox.value()
        self.layerTable.setRowCount(numRows)
        for row in range(self.numOfLayerSpinBox.value()):
            # self.layerTable.insertRow(self.layerTable.rowCount())
            item = QtWidgets.QTableWidgetItem(str(row + 1))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.layerTable.setItem(row, 0, item)
            self.layerTable.setItem(row, 1, QtWidgets.QTableWidgetItem("Layer_" + str(row + 1)))
            if self.autoRandCheckBox.isChecked():
                self.layerTable.setItem(row, 2, QtWidgets.QTableWidgetItem(
                    "RANDOM " + str(self.rndMatrix[0]) + ":" + str(self.rndMatrix[1])))
                self.layerTable.setItem(row, 3, QtWidgets.QTableWidgetItem(
                    "RANDOM " + str(self.rndMatrix[2]) + ":" + str(self.rndMatrix[3])))
                self.layerTable.setItem(row, 4, QtWidgets.QTableWidgetItem(str(0.0)))
            else:
                self.layerTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(0.0)))
                self.layerTable.setItem(row, 3, QtWidgets.QTableWidgetItem(str(0.0)))
                self.layerTable.setItem(row, 4, QtWidgets.QTableWidgetItem(str(0.0)))

    def SumbitUserInput(self):
        switcher = {0: self.SubmitSample, 1: self.SubmitDetector, 2: self.SubmitBeam, 3: self.StartSim, 4: self.UpdateImg}
        func = switcher.get(self.tabWidget.currentIndex())
        func()

    def SubmitSample(self):
        s = _siegSample.SiegSample(self.numOfLayerSpinBox.value())
        T = []
        for i in range(self.layerTable.rowCount()):
           T.append([float(self.layerTable.item(i, 2).text()), float(self.layerTable.item(i, 3).text()), float(self.layerTable.item(i, 4).text())])
        s.layersData = T
        self._simControls.Sample = s
        disData = [0] * 20
        thickData = [0] * 20
        for i in range(20):
            x = 1
            y = 1
            if i % 2 == 0:
                x = 2
                y = 6
            dis_h = (x + 0.2 * randint(0, 10)) * 1e-05
            thi_h = (y + (y / x) * 0.2 * randint(0, 10))
            disData[i] = dis_h
            thickData[i] = thi_h
        for _ in range(1):
            self.RefImg = self._simControls.GenerateRefData(True, thickData, disData)
            max_index_col = np.argmax(self.RefImg, axis=1)
            with open('dataTEST.csv', 'a', encoding='UTF8', newline='') as fd:
                np.savetxt(fd, self.RefImg[:, max_index_col[0]])
                #np.savetxt(fd, self.RefImg[:, max_index_col[0]], delimiter=",")

    def SubmitBeam(self):
        self._simControls.TestVar()

    def UploadFile(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setWindowTitle('Open Data File')
        dialog.setNameFilter('Data files (*.txt)')
        dialog.setDirectory(QtCore.QDir.currentPath())
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            file_full_path = str(dialog.selectedFiles()[0])
        print(file_full_path)
        lines = loadtxt(file_full_path, comments="#", delimiter=" ", unpack=False)
        self._dynamic_ax2.clear()
        self._dynamic_ax2.imshow(lines, interpolation='none')
        self._dynamic_ax2.figure.canvas.draw()

    def SubmitDetector(self):
        d = _siegDetector.SiegDetector(self.detectorTypeComboBox.currentIndex())
        detector_dims = [0, 0, 0, 0]
        detector_dims[0] = self.xBinSpinBox.value()
        detector_dims[1] = self.yBinSpinBox.value()
        detector_dims[2] = self.detectorWidthSpinBox.value()
        detector_dims[3] = self.detectorHeightSpinBox.value()
        d.detectorDimensions = detector_dims
        d.resolutionFunction = self.resolutionFncTypeComboBox.currentIndex()
        d.resolutionFunctionSigmaX = self.resFncSigmaXSpinBox.value()
        d.resolutionFunctionSigmaY = self.resFncSigmaYSpinBox.value()
        self._simControls.Detector = d

    def StartSim(self):
        print("StartSim")

    def UpdateImg(self):
        self._static_ax.clear()
        self._static_ax.imshow(self.RefImg, interpolation='none')
        self._static_ax.figure.canvas.draw()
        self.static_canvas.mpl_connect('button_press_event', self.onclick)

        #self.scene().addItem(QtGui.QGraphicsLineItem(QtCore.QLineF((200,100), (250,100))))

    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.figure.canvas.draw()
