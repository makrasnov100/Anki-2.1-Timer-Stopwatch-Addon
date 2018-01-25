# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
# import PyQT libraries
from PyQt5.QtCore import QTime
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QPushButton, QLCDNumber

# import TimerWindow class
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import windowSetup


screenWidth = 1920
screenHeight = 1080
timeWin = None

def timerFunction():
    global screenWidth
    global screenHeight
    global timeWin
    
    # Get Current Screen Resolution
    QApp = QCoreApplication.instance()
    screenResolution = QApp.desktop().screenGeometry()
    screenWidth = screenResolution.width()
    screenHeight = screenResolution.height()
    
    #Create the timer window
    if timeWin == None:
        timeWin = windowSetup.TimerWindow(screenWidth, screenHeight)
    else:
        timeWin.show()


# Create a new menu item, "Timer"
action = QAction("Timer", mw)
# Set it to call timerFunction when it's clicked
action.triggered.connect(timerFunction)
# Add it to the tools menu
mw.form.menuTools.addAction(action)
