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
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import csv
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
import time
import numpy as np
import sys
import SiegSimulationControls as _siegSim
import SiegSample as _siegSample
import SiegDetector as _siegDetector
import SiegParaChecker as _paraChecker
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
    runSimIsOk = False
    rndMatrix = [0, 0, 0, 0]
    rndParasAreOK = False
    RefImg = [ ]
    LineProfile = []
    electron_density1 = [ ]
    electron_density2 = []
    static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
    dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
    user_canvas = FigureCanvas(Figure(figsize=(5, 3)))
    electron_canvas = FigureCanvas(Figure(figsize=(5, 3)))
    _static_ax = static_canvas.figure.subplots()
    _user_ax = user_canvas.figure.subplots()
    _electron_ax = electron_canvas.figure.subplots()
    _simControls = _siegSim.SiegSimulationControls()
    _siegChecker = _paraChecker.SiegParaChecker()

    @pyqtSlot(int)
    def Progress(self, x):
        ''' Give evidence that a bag was punched. '''
        print(x)



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toolbar = NavigationToolbar(self.user_canvas, self)
        self.initUI()

    def initUI(self):
        #TODO: Set tooltips
        uic.loadUi("siegmainwindow.ui", self)
        # which defines a single set of axes as self.axes.
        layout = QtWidgets.QVBoxLayout(self.plotWidget)
        self._simControls.progressVal.connect(self.Progress)
        # static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.static_canvas)
        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)

        #self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(self.static_canvas, self))
        #NavigationToolbar(self.user_canvas, self)
        file_data_layout = QtWidgets.QVBoxLayout(self.controlWidget)
        file_data_layout.addWidget(self.user_canvas)

        electron_density_layout = QtWidgets.QVBoxLayout(self.electronWidget)
        electron_density_layout.addWidget(self.electron_canvas)

        #file_data_layout.addWidget(self.toolbar)
        #self.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(self.user_canvas, self))
        #self._timer = dynamic_canvas.new_timer(
        #    100, [(self._update_canvas, (), {})])
        #self._timer.start()
        self._dynamic_ax = dynamic_canvas.figure.subplots(1,1)
        self._dynamic_ax2 = self.user_canvas.figure.subplots(1,1)

        self.fullscreenAction.triggered.connect(self.FullscreenAction)
        self.randGroupBox.setHidden(True)
        self.diffGroupBox.setHidden(True)
        #self.backgroundValueSpinBox.setHidden(True)
        self.bgLabel.setHidden(True)
        self.beamDataWidget.setHidden(True)
        self.configSampleButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
        self.configDetectorButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
        self.configSimButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
        self.configBeamButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')))
        self.submitButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, 'SP_ArrowRight')))
        self.autoRandCheckBox.stateChanged.connect(self.UseAutomaticRandomization)
        self.incDiffCheckBox.stateChanged.connect(self.UseDifference)
        self.configSampleButton.clicked.connect(self.OpenSamplePage)
        self.configDetectorButton.clicked.connect(self.OpenDetectorPage)
        self.configBeamButton.clicked.connect(self.OpenBeamPage)
        self.configSimButton.clicked.connect(self.OpenSimPage)
        self.randomParaOKButton.clicked.connect(self.SubmitRandomizationPara)
        self.setButton.clicked.connect(self.SetLayers)
        self.uploadFromFileButton.clicked.connect(self.UploadFile)
        self.saveTXTPushButton.clicked.connect(self.SaveAsTxtFile)
        #self.setButton.setToolTip("")
        self.tabWidget.currentChanged.connect(self.SubmitButtonText)
        self.submitButton.clicked.connect(self.SumbitUserInput)
        self.sampleTypeComboBox.currentIndexChanged.connect(self.SampleTypeChanged)
        self.backgroundTypeComboBox.currentIndexChanged.connect(self.BackgroundTypeChanged)
        self.logScaleCheckBox.stateChanged.connect(self.UpdateImg)
        self.addBeamStopCheckBox.stateChanged.connect(self.ShowBeamStopData)
        self.setBeamStopPushButton.clicked.connect(self.SetBeamStop)
        self.submitButton.setEnabled(False)


        #TODO: remove
        self.autoRandCheckBox.setEnabled(False)
        self.incDiffCheckBox.setEnabled(False)

    def closeEvent(self, event):
        self.deleteLater()

    def StartSimButtonState(self):
        self.startSimulationButton.setEnabled(self.runSimIsOk)

    def speaking_method(self):
        _siegSim.Test()

    def ShowBeamStopData(self):
        if self.addBeamStopCheckBox.isChecked():
            self.beamDataWidget.setHidden(False)
        else:
            self.beamDataWidget.setHidden(True)

    def SetBeamStop(self):
        self._dynamic_ax.clear()
        helper = self.LineProfile


        helper[(self.yPixelBSSpinBox.value() - self.radiusBSSpinBox.value()): (self.yPixelBSSpinBox.value() + self.radiusBSSpinBox.value())] = 0
        t = np.linspace(0, 10, 1024)
        self._dynamic_ax.plot(t, helper)
        self._dynamic_ax.figure.canvas.draw()


    def onclick(self, event):
        ix, iy = event.xdata, event.ydata
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 1024)
        max_index_col = np.argmax(self.RefImg, axis=1)
        #TODO: make it better
        self.LineProfile = (self.RefImg[:, int(ix)]+self.RefImg[:, int(ix)-1] + self.RefImg[:, int(ix+1)]
               + self.RefImg[:, int(ix -2)] + self.RefImg[:, int(ix+2)] + self.RefImg[:, int(ix-3)] + self.RefImg[:, int(ix+3)]
               )/6

        print(self.LineProfile.shape)
        self._dynamic_ax.plot(t,self.LineProfile)
        """
        for i in range(1024):
            res = 0
            for j in range(-10,10):
                res = res + self.RefImg[int(ix)+j, i]
            cols.append(res/20)

        self._dynamic_ax.plot(t, cols)
        """
        #with open('data2.csv', 'a', encoding='UTF8', newline='') as fd:
            #np.savetxt(fd, self.RefImg[:, max_index_col[0]], delimiter=",")

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
            self.setButton.setEnabled(True)

    def UseDifference(self):
        if self.incDiffCheckBox.isChecked():
            self.diffGroupBox.setHidden(False)
            self.setButton.setEnabled(False)
        else:
            self.diffGroupBox.setHidden(True)

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
            self.submitButton.setText("Run")
            if self.sampleIsReady and self.detectorIsReady and self.beamIsReady and self.simIsReady:
                self.submitButton.setEnabled(True)
            else:
                self.submitButton.setEnabled(False)
        elif ind == 5:
            self.submitButton.setVisible(False)
        else:
            self.submitButton.setText("Submit simulation")

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

    def OpenProgressAndResPage(self):
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

        if self.sampleIsReady and self.detectorIsReady and self.beamIsReady and self.simIsReady:
            self.runSimIsOk = True
            self.StartSimButtonState()
        else:
            self.runSimIsOk = False
            self.StartSimButtonState()

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

        for row in range(numRows):
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
                self.layerTable.setItem(row, 5, QtWidgets.QTableWidgetItem(str(0.0)))
        self.submitButton.setEnabled(True)

    def SumbitUserInput(self):
        switcher = {0: self.SubmitSample, 1: self.SubmitDetector, 2: self.SubmitBeam, 3: self.SubmitSim, 4: self.StartSimulation}
        func = switcher.get(self.tabWidget.currentIndex())
        func()

    def SubmitSample(self):
        numOfLayer = self.numOfLayerSpinBox.value()
        s = _siegSample.SiegSample(numOfLayer)
        T = []
        for i in range(numOfLayer):
           T.append([self.layerTable.item(i, 1).text(),
                     float(self.layerTable.item(i, 2).text()),
                     float(self.layerTable.item(i, 3).text()),
                     float(self.layerTable.item(i, 4).text()),
                     float(self.layerTable.item(i, 5).text())])

        self.sampleIsReady = self._siegChecker.CheckSamplePara(False, T)
        if self.sampleIsReady:
            self._simControls.UserData = T
            self.UpdateTODOButtonsIcons()
            self.OpenDetectorPage()
        else:
            #TODO: error msg to user
            return
        #self._simControls.TestVar()
        #self.RefImg, self.electron_density1, self.electron_density2 = self._simControls.GenerateRefData(numOfLayer)
        #self._simControls.InitSample(numOfLayer)
        #print(T)
        """
        s.layersData = T
        self._simControls.Sample = s
        disData = [0] * 20
        thickData = [0] * 20
        absData = [0] * 20
        for i in range(20):
            x = 1
            y = 1
            if i % 2 == 0:
                x = 2
                y = 6
            dis_h = np.random.randint(1, 5) * 1e-05
            thi_h = 0.4 * np.random.randint(1, 10)
            abs_h = np.random.randint(8, 31) * 1e-06
            disData[i] = dis_h
            thickData[i] = thi_h
            absData[i] = abs_h
        for _ in range(1):
            self.RefImg, self.electron_density1, self.electron_density2 = self._simControls.GenerateRefData(numOfLayer, thickData, disData, absData)
            #max_index_col = np.argmax(self.RefImg, axis=1)
            #with open('dataTEST.csv', 'a', encoding='UTF8', newline='') as fd:
                #np.savetxt(fd, self.RefImg[:, max_index_col[0]])
                #np.savetxt(fd, self.RefImg[:, max_index_col[0]], delimiter=",")
        """

    def SubmitBeam(self):
        beam_dims = [0, 0, 0, 0]
        beam_dims[0] = self.beanmAlphaSpinBox.value()
        beam_dims[1] = self.beamPhiSpinBox.value()
        beam_dims[2] = self.beamIntensitySpinBox.value()
        beam_dims[3] = self.beamWaveLengthSpinBox.value()
        self.beamIsReady = self._siegChecker.CheckBeamPara(beam_dims)
        if self.detectorIsReady:
            self._simControls.BeamData = beam_dims
            self.UpdateTODOButtonsIcons()
            self.OpenSimPage()
        else:
            # TODO: error msg to user
            return

    def SubmitDetector(self):
        detector_dims = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        detector_dims[0] = self.xBinSpinBox.value()
        detector_dims[1] = self.yBinSpinBox.value()
        detector_dims[2] = self.detectorWidthSpinBox.value()
        detector_dims[3] = self.detectorHeightSpinBox.value()
        detector_dims[4] = self.resFncSigmaXSpinBox.value()
        detector_dims[5] = self.resFncSigmaYSpinBox.value()
        detector_dims[6] = self.detDistanceSpinBox.value()
        detector_dims[7] = self.detU0SpinBox.value()
        detector_dims[8] = self.detV0SpinBox.value()
        self.detectorIsReady = self._siegChecker.CheckDetectorPara(detector_dims)
        if self.detectorIsReady:
            self._simControls.DetectorData = detector_dims
            self.UpdateTODOButtonsIcons()
            self.OpenBeamPage()
        else:
            # TODO: error msg to user
            return

    def SubmitSim(self):
        sim_dims = [0, 0, 1, 1, 0]
        sim_dims[0] = self.simTypeComboBox.currentIndex()
        sim_dims[1] = self.matCalcTypeComboBox.currentIndex()
        sim_dims[2] = 1 if self.incSpecularCheckBox.isChecked() else 0
        sim_dims[3] = self.backgroundTypeComboBox.currentIndex()
        sim_dims[4] = self.backgroundValueSpinBox.value()
        self.simIsReady = self._siegChecker.CheckSimPara(sim_dims)
        if self.simIsReady:
            self._simControls.SimData = sim_dims
            self.UpdateTODOButtonsIcons()
            self.OpenProgressAndResPage()
        else:
            # TODO: error msg to user
            return

    def StartSimulation(self):
        print("OK")
        #self._simControls.GenerateData()

    def UploadFile(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setWindowTitle('Open Data File')
        dialog.setNameFilter('Data files (*.txt)')
        dialog.setDirectory(QtCore.QDir.currentPath())
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            file_full_path = str(dialog.selectedFiles()[0])
        lines = loadtxt(file_full_path, comments="#", delimiter=" ", unpack=False)
        self._dynamic_ax2.clear()
        self._dynamic_ax2.imshow(lines, interpolation='none')
        self._dynamic_ax2.figure.canvas.draw()

    def SaveAsTxtFile(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
        path = name[0]
        path += ".txt"
        with open(path, 'w') as f:
            np.savetxt(f, self.LineProfile)


    def UpdateImg(self):
        self._static_ax.clear()
        if self.logScaleCheckBox.isChecked():
            self._static_ax.imshow(np.log(self.RefImg), interpolation='none')
        else:
            self._static_ax.imshow(self.RefImg, interpolation='none')
        self._static_ax.figure.canvas.draw()
        self.static_canvas.mpl_connect('button_press_event', self.onclick)
        self._electron_ax.clear()
        #t = np.linspace(0, 10, 101)
        self._electron_ax.plot(self.electron_density1, np.real(self.electron_density2))
        self._electron_ax.figure.canvas.draw()
        #self.scene().addItem(QtGui.QGraphicsLineItem(QtCore.QLineF((200,100), (250,100))))

    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.figure.canvas.draw()

    def BackgroundTypeChanged(self, ind):
        if ind == 1:
            self.backgroundValueSpinBox.setHidden(False)
            self.bgLabel.setHidden(False)
        else:
            self.backgroundValueSpinBox.setHidden(True)
            self.bgLabel.setHidden(True)
