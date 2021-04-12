# -*- coding: utf-8 -*-
"""
@author:    Amir Tosson
@license:   GNU General Public License v3 or higher
@copyright: Universität Siegen, Deutschland
@email:     tosson@physik.uni-siegen.de   
"""

from PyQt5 import QtWidgets
import SiegMainWindow as _mainWin 
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    mw = _mainWin.SiegMainWindow()
    mw.show();
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()









