# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 15:06:07 2021

@author: tosson
"""
from PyQt5.QtWidgets import QApplication, QToolTip, QPushButton, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import SiegSimulationControls as _siegSim 


class SiegMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')
        btn = QPushButton('Button', self)
        btn.clicked.connect(self.speaking_method)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')
        #self.show()
        
    def speaking_method(self):                                              
        _siegSim.Test()