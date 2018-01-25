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
# import the storage class


elapseHours = 0
totalMSecRemain = 0
isStarted = False
isInfoShown = False

class TimerWindow(QWidget):
    
    #Button control functions
    def handleStartBtn(self):
        global isStarted
        isStarted = True
        self.statusInput.setText("Timer Started!")
        self.statusInput.setStyleSheet('color: grey')
    def handleStopBtn(self):
        global isStarted
        if isStarted:
            isStarted = False
            self.statusInput.setText("Reset Timer?")
            self.statusInput.setStyleSheet('color: blue')
    def handleResetBtn(self):
        global isStarted
        global elapseHours
        isStarted = False
        elapseHours = 0
        self.stopwatchTime = QTime(0,0,0,0)
        self.curElapse.setText("00:00:00:000 ms")
        self.updateTimer()
    def handleCloseBtn(self):
        print ("Close Button Pressed!")
        self.hide()
        
    def formatTime(self):
        #Find current time
        timeNow = QTime.currentTime()
        fullTime = timeNow.toString("hh:mm:ss:zzz 'ms'")
        return fullTime
    
    def formatElapse(self):
        global elapseHours
        if self.stopwatchTime.hour() == 1:
            elapseHours += 1
            self.stopwatchTime = self.stopwatchTime.addSecs(-3600)
        if elapseHours < 10:
            elapseHoursS = "0" + str(elapseHours)
        else:
            elapseHoursS = str(elapseHours)
        fullElapseS = elapseHoursS + ":" + self.stopwatchTime.toString("mm:ss:zzz 'ms'")
        return fullElapseS
    
    def deductTimer(self):
        global totalMSecRemain
        totalMSecRemain -= 87
        
    def formatTimer(self):
        
        global totalMSecRemain
        global isInfoShown
        
        #Return zeros if miliseconds remaining are negative
        if totalMSecRemain <= 0:
            if not isInfoShown:
                showInfo("Time is Up!")
                isInfoShown = True
            return "00:00:00:000 ms"
            
        
        #Calculate timer values
        totalHours = int(totalMSecRemain / 3600000)
        totalMin = int((totalMSecRemain % 3600000) / 60000)
        totalSec = int(((totalMSecRemain % 3600000) % 60000) / 1000)
        totalMilSec = int(((totalMSecRemain % 3600000) % 60000) % 1000)
        
        #Update timer label
        if totalHours == 0:
            totalHoursS = "00"
        elif totalHours < 10:
            totalHoursS = "0" + str(totalHours)
        else:
            totalHoursS = str(totalHours)
        
        if totalMin == 0:
            totalMinS = "00"
        elif totalMin < 10:
            totalMinS = "0" + str(totalMin)
        else:
            totalMinS = str(totalMin)
            
        if totalSec == 0:
            totalSecS = "00"
        elif totalSec < 10:
            totalSecS = "0" + str(totalSec)
        else:
            totalSecS = str(totalSec)
            
        if totalMilSec == 0:
            totalMilSecS = "000"
        elif totalMilSec < 10:
            totalMilSecS = "00" + str(totalMilSec)
        elif totalMilSec < 100:
            totalMilSecS = "0" + str(totalMilSec)
        else:
            totalMilSecS = str(totalMilSec)
        
        fullTimerS = totalHoursS + ":" + totalMinS + ":" + totalSecS + ":" + totalMilSecS + " ms"
        return fullTimerS
    
    def updateTime(self):
        #Update of cur time clock
        self.curTime.setText(self.formatTime())
        #Update next two clocks if started
        if isStarted == True:
            #Update of elapsed time
            self.stopwatchTime = self.stopwatchTime.addMSecs(87)
            self.curElapse.setText(self.formatElapse())
            #Update of timer clock
            self.deductTimer()
            self.curTimer.setText(self.formatTimer())

        
    def updateTimer(self):
        if isStarted:
            return
        
        global totalMSecRemain 
        global isInfoShown
        
        inputPresent = False
        isAccepted = False
        
        #Value validation
        try:
            if self.hourInputFeild.text() != "":
                hourInputNum = int(float(self.hourInputFeild.text()))
                inputPresent = True
                isAccepted = True
            else:
                hourInputNum = 0
            if self.minInputFeild.text() != "":
                minInputNum = int(float(self.minInputFeild.text()))
                inputPresent = True
                isAccepted = True
            else:
                minInputNum = 0
            if self.secInputFeild.text() != "":
                secInputNum = int(float(self.secInputFeild.text()))
                inputPresent = True
                isAccepted = True
            else:
                secInputNum = 0
            self.statusInput.setText("Input Accepted!")
            self.statusInput.setStyleSheet('color: green')
        except ValueError:
            isAccepted = False
            inputPresent = True
            self.statusInput.setText("Input Declined")
            self.statusInput.setStyleSheet('color: red')
            
        if (inputPresent == False) or ((hourInputNum == 0) and (minInputNum == 0) and (secInputNum == 0)):
            totalMSecRemain = 1
            isAccepted = False
            self.curTimer.setText("00:00:00:000 ms")
            self.statusInput.setText("Awaiting Input!")
            self.statusInput.setStyleSheet('color: orange')

        
        #Update timer variable if value accepted
        if (isAccepted == True):
            #Calculate timer values
            isInfoShown = False
            totalMSecRemain = (hourInputNum * 3600000) + (minInputNum * 60000) + (secInputNum* 1000)     
            fullTimerS = self.formatTimer()
            
            self.curTimer.setText(fullTimerS)
        
        
    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()
    
    def horLine(self):
        hLine = QFrame()
        hLine.setFrameShape(QFrame.HLine)
        hLine.setFrameShadow(QFrame.Sunken)
        return hLine
    
    def __init__(self, screenW, screenH):
        
        super().__init__()
        self.title = "Simple Timer"
        self.width = 640
        self.height = 480
        self.left = (screenW / 2) - (self.width / 2) 
        self.top = (screenH / 2) - (self.height / 2)
        
        #Create button horizontal layout
        btnBox = QHBoxLayout()
        btnBox.addStretch(.5)
        #Create button instaces
        self.startBtn = QPushButton('Start',self)
        self.startBtn.clicked.connect(self.handleStartBtn)
        self.stopBtn = QPushButton('Stop',self)
        self.stopBtn.clicked.connect(self.handleStopBtn)
        self.resetBtn = QPushButton('Reset',self)
        self.resetBtn.clicked.connect(self.handleResetBtn)
        self.closeBtn = QPushButton('Close',self)
        self.closeBtn.clicked.connect(self.handleCloseBtn)
        #Add buttons to layout
        btnBox.addWidget(self.startBtn)
        btnBox.addWidget(self.stopBtn)
        btnBox.addWidget(self.resetBtn)
        btnBox.addWidget(self.closeBtn)
        btnBox.addStretch(.5)
        
        
        #Create Update Calls for All Clocks
        self.curTimeTimer = QTimer(self)
        self.curTimeTimer.timeout.connect(self.updateTime)
        self.curTimeTimer.start(87)
        
        #Create Three Info Clocks
        timeFont = QFont("Ariel", 40)
        #Set the initial current time at start
        curTimeBox = QHBoxLayout()
        curTimeBox.addStretch(.5)
        self.curTime = QLabel(self.formatTime(), self)
        self.curTime.setFont(timeFont)
        curTimeBox.addWidget(self.curTime)
        curTimeBox.addStretch(.5)
        #Set the initial timer time at start
        curTimerBox = QHBoxLayout()
        curTimerBox.addStretch(.5)
        self.curTimer = QLabel("00:00:00:000 ms", self)
        self.curTimer.setFont(timeFont)
        curTimerBox.addWidget(self.curTimer)
        curTimerBox.addStretch(.5)
        #Set the initial elapsed time at start
        self.stopwatchTime = QTime(0,0,0,0)
        curElapseBox = QHBoxLayout()
        curElapseBox.addStretch(.5)
        self.curElapse = QLabel("00:00:00:000 ms", self)
        self.curElapse.setFont(timeFont)
        curElapseBox.addWidget(self.curElapse)
        curElapseBox.addStretch(.5)
        
        #Create timer input feilds
        inputBox = QHBoxLayout()
        self.introInput = QLabel('Set timer to -', self)
        self.hourInput = QLabel(' Hours:', self)
        self.hourInputFeild = QLineEdit()
        self.minInput = QLabel(' Minutes:', self)
        self.minInputFeild = QLineEdit()
        self.secInput = QLabel(' Seconds:', self)
        self.secInputFeild = QLineEdit()
        self.statusInput = QLabel('Awaiting Input!', self)
        self.statusInput.setStyleSheet('color: orange')
        inputBox.addStretch(.2)
        inputBox.addWidget(self.introInput)
        inputBox.addStretch(.3)
        inputBox.addWidget(self.hourInput)
        inputBox.addWidget(self.hourInputFeild)
        inputBox.addWidget(self.minInput)
        inputBox.addWidget(self.minInputFeild)
        inputBox.addWidget(self.secInput)
        inputBox.addWidget(self.secInputFeild)
        inputBox.addStretch(.3)
        inputBox.addWidget(self.statusInput)
        inputBox.addStretch(.2)
        
        
        #Connect input signals to the apropriate function
        self.hourInputFeild.textChanged.connect(self.updateTimer)
        self.minInputFeild.textChanged.connect(self.updateTimer)
        self.secInputFeild.textChanged.connect(self.updateTimer)
        
        #Create all static labels
        titleFont = QFont("Courier", 20)
        self.curTimeTitle = QLabel('Current Time:', self)
        self.curTimeTitle.setFont(titleFont)
        self.curTimerTitle = QLabel('Time Remaining:', self)
        self.curTimerTitle.setFont(titleFont)
        self.curElapseTitle = QLabel('Elapsed Time:', self)
        self.curElapseTitle.setFont(titleFont)
        
        
        #Create and populate root layout
        rootBox = QVBoxLayout()
        rootBox.addWidget(self.curTimeTitle)
        rootBox.addLayout(curTimeBox)
        rootBox.addStretch(.165)
        rootBox.addWidget(self.horLine())
        rootBox.addStretch(.165)
        rootBox.addWidget(self.curTimerTitle)
        rootBox.addLayout(curTimerBox)
        rootBox.addStretch(.165)
        rootBox.addWidget(self.horLine())
        rootBox.addStretch(.165)
        rootBox.addWidget(self.curElapseTitle)
        rootBox.addLayout(curElapseBox)
        rootBox.addStretch(.165)
        rootBox.addWidget(self.horLine())
        rootBox.addStretch(.165)
        rootBox.addLayout(inputBox)
        rootBox.addLayout(btnBox)
        
        self.setLayout(rootBox)
        
        self.initWindow()
