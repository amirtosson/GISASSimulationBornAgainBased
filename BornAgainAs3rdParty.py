# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 11:12:24 2021

@author: Tosson
"""

import SiegMainWindow as _mainWin 
import sys
from PyQt5.QtWidgets import QApplication

def main():

    app = QApplication(sys.argv)

    mw = _mainWin.SiegMainWindow()
    mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()









