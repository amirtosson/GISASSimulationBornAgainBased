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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.initUI()
        uic.loadUi("siegmainwindow.ui", self)
        self.fullscreenAction.triggered.connect(self.FullscreenAction)

    def initUI(self):
        self = uic.loadUi("siegmainwindow.ui")
        self.show()
        # QToolTip.setFont(QFont('SansSerif', 10))
        # self.setToolTip('This is a <b>QWidget</b> widget')
        # btn = QPushButton('Button', self)
        # btn.clicked.connect(self.speaking_method)
        # btn.setToolTip('This is a <b>QPushButton</b> widget')
        # btn.resize(btn.sizeHint())
        # btn.move(50, 50)
        # self.setGeometry(300, 300, 300, 200)
        # self.setWindowTitle('Tooltips')
        # #self.show()
        
    def speaking_method(self):                                              
        _siegSim.Test()
        
    def FullscreenAction(self):                                              
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()