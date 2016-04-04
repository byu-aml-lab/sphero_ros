#!/usr/bin/python

import sys, rospy
from PyQt4 import QtGui, QtCore
from geometry_msgs.msg import Twist
from std_msgs.msg import ColorRGBA, Float32, Bool

class LEDWidget(QtGui.QLabel):
   
    def __init__(self, size, rgb):
        super(QtGui.QLabel, self).__init__()
        pixmap = QtGui.QPixmap(size[0], size[1])
        self.setPixmap(pixmap)
        self.rgb = rgb
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Base)

    def setRGB(self, r, g, b):
        self.rgb = [r,g,b]
        p = QtGui.QPalette()
        p.setColor(self.backgroundRole(), QtGui.QColor(self.rgb[0], self.rgb[1], self.rgb[2]))
        self.setPalette(p)
        self.update()
  
    def paintEvent(self, e):
        super(QtGui.QLabel, self).paintEvent(e)
        #qp = QtGui.QPainter()
        #qp.begin(self)
        #qp.end()         

class LEDConfig(QtGui.QWidget):

    def __init__(self, parentWindow):
        super(QtGui.QWidget, self).__init__()
        self.parentWindow = parentWindow
        self.initUI()
        self.hide()
    
    def initUI(self):   

        self.bk_label = QtGui.QLabel("back LED")
        self.bk_sl = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.bk_sl.setMinimum(0)
        self.bk_sl.setMaximum(255)
        self.bk_sl.setValue(self.parentWindow.backLEDVal)
        self.bk_sl.setTickPosition(QtGui.QSlider.TicksBelow)
        self.bk_sl.setTickInterval(1)

        self.r_label = QtGui.QLabel("R")
        self.r_sl = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.r_sl.setMinimum(0)
        self.r_sl.setMaximum(255)
        self.r_sl.setValue(self.parentWindow.ledRVal)
        self.r_sl.setTickPosition(QtGui.QSlider.TicksBelow)
        self.r_sl.setTickInterval(1)
        self.r_sl.valueChanged.connect(self.valuechange)

        self.g_label = QtGui.QLabel("G")
        self.g_sl = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.g_sl.setMinimum(0)
        self.g_sl.setMaximum(255)
        self.g_sl.setValue(self.parentWindow.ledGVal)
        self.g_sl.setTickPosition(QtGui.QSlider.TicksBelow)
        self.g_sl.setTickInterval(1)
        self.g_sl.valueChanged.connect(self.valuechange)

        self.b_label = QtGui.QLabel("B")
        self.b_sl = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.b_sl.setMinimum(0)
        self.b_sl.setMaximum(255)
        self.b_sl.setValue(self.parentWindow.ledBVal)
        self.b_sl.setTickPosition(QtGui.QSlider.TicksBelow)
        self.b_sl.setTickInterval(1)
        self.b_sl.valueChanged.connect(self.valuechange)

        self.led = LEDWidget([20,20],
                             [self.parentWindow.ledRVal,
                              self.parentWindow.ledGVal,
                              self.parentWindow.ledBVal])
        
        self.btnUpdate = QtGui.QPushButton("Update")
        self.btnOK = QtGui.QPushButton("OK")
        self.btnCancel = QtGui.QPushButton("Cancel")
        self.btnUpdate.clicked.connect(self.updateConfig)
        self.btnOK.clicked.connect(self.ok)
        self.btnCancel.clicked.connect(self.cancel)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.led)
        r_layout = QtGui.QHBoxLayout()
        r_layout.addWidget(self.r_label)
        r_layout.addWidget(self.r_sl)
        layout.addLayout(r_layout)
        g_layout = QtGui.QHBoxLayout()
        g_layout.addWidget(self.g_label)
        g_layout.addWidget(self.g_sl)
        layout.addLayout(g_layout)
        b_layout = QtGui.QHBoxLayout()
        b_layout.addWidget(self.b_label)
        b_layout.addWidget(self.b_sl)
        layout.addLayout(b_layout)
        bk_layout = QtGui.QHBoxLayout()
        bk_layout.addWidget(self.bk_label)
        bk_layout.addWidget(self.bk_sl)
        layout.addLayout(bk_layout)
        btn_layout = QtGui.QHBoxLayout()
        btn_layout.addWidget(self.btnUpdate)
        btn_layout.addWidget(self.btnOK)
        btn_layout.addWidget(self.btnCancel)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        self.show()

    def updateConfig(self):
        
        self.parentWindow.ledRVal = self.r_sl.value()
        self.parentWindow.ledGVal = self.g_sl.value()
        self.parentWindow.ledBVal = self.b_sl.value()        
        self.parentWindow.setLEDColor(self.parentWindow.ledRVal,
                                 self.parentWindow.ledGVal,
                                 self.parentWindow.ledBVal)
        self.led.setRGB(self.parentWindow.ledRVal,
                        self.parentWindow.ledGVal,
                        self.parentWindow.ledBVal)

        self.parentWindow.backLEDVal = self.bk_sl.value()
        self.parentWindow.setBackLED(self.parentWindow.backLEDVal)
        self.update()

    def ok(self):
        self.updateConfig()
        self.hide()
        
    def cancel(self):
        self.r_sl.setValue(self.parentWindow.ledRVal)
        self.g_sl.setValue(self.parentWindow.ledGVal)
        self.b_sl.setValue(self.parentWindow.ledBVal)
        self.hide()

    def valuechange(self):
        self.led.setRGB(self.r_sl.value(),
                        self.g_sl.value(),
                        self.b_sl.value())
        self.led.update()

class DashboardWidget(QtGui.QWidget):

    def __init__(self):
        super(QtGui.QWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.cmdVelLabel = QtGui.QLabel("cmd_vel")
        self.cmdVelTextbox = QtGui.QTextEdit()
        self.cmdVelTextbox.setReadOnly(True)   
        self.keyEventLabel = QtGui.QLabel("Key")
        self.keyEventTextbox = QtGui.QTextEdit()
        self.keyEventTextbox.setReadOnly(True)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.cmdVelLabel)
        layout.addWidget(self.cmdVelTextbox)
        layout.addWidget(self.keyEventLabel)
        layout.addWidget(self.keyEventTextbox)
        self.setLayout(layout)
        self.show()

    def handleCmdVelMsg(self, cmd_vel_text):
        self.cmdVelTextbox.moveCursor(QtGui.QTextCursor.End)
        self.cmdVelTextbox.ensureCursorVisible()
        self.cmdVelTextbox.insertPlainText(cmd_vel_text+"\n")
        self.cmdVelTextbox.update()

    def handleKeyText(self, key_text):
        self.keyEventTextbox.moveCursor(QtGui.QTextCursor.End)
        self.keyEventTextbox.ensureCursorVisible()
        self.keyEventTextbox.insertPlainText(key_text+"\n")
        self.keyEventTextbox.update()

class SpheroDashboardForm(QtGui.QMainWindow):
    
    def __init__(self):
        super(QtGui.QMainWindow, self).__init__()
        self.resize(600, 480) 

        rospy.init_node('sphero_dashboard', anonymous=True)
        self.cmdVelPub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.cmdVelSub = rospy.Subscriber("cmd_vel", Twist, self.cmdVelCallback)
      
        self.ledPub = rospy.Publisher('set_color', ColorRGBA, queue_size=1)
        self.backLedPub = rospy.Publisher('set_back_led', Float32, queue_size=1)   

        self.ledRVal = 0
        self.ledGVal = 0
        self.ledBVal = 0
        self.backLEDVal = 0
        self.ledConfig = LEDConfig(self)
        self.ledConfig.move(10, 10)
        self.setLEDColor(self.ledRVal, self.ledGVal, self.ledBVal)
        self.setBackLED( self.backLEDVal )
        
        self.initUI()
       
        
    def initUI(self):
        
        ledAction = QtGui.QAction('LED', self)
        ledAction.triggered.connect(self.showLedConfig)
        
        menubar = self.menuBar()
        ledMenu = menubar.addMenu('&LED')
        ledMenu.addAction(ledAction)        

        self.dashboard = DashboardWidget()
        self.setCentralWidget(self.dashboard)

        self.setWindowTitle("Sphero dashboard")
        self.show()

    def showLedConfig(self):
        self.ledConfig.show()     

    def setLEDColor(self, r, g, b):
        color = ColorRGBA(float(r)/255.0, float(g)/255.0, float(b)/255.0, 1.0)
        self.ledPub.publish(color)

    def setBackLED(self, val):
        light = Float32()
        light.data = float(val)
        self.backLedPub.publish(light)

    def cmdVelCallback(self, msg):
        msg_text = "x=" + str(msg.linear.x) + " y=" + str(msg.linear.y)
        self.dashboard.handleCmdVelMsg(msg_text)

    def processDirectionKey(self, key):
        key_text = ""
        if key == 0:
            # left
            key_text = "LEFT"
            cv = Twist()
            cv.linear.x = 100.0
            cv.linear.y = 0.0
            cv.linear.z = 0.0
            cv.angular.x = 0.0
            cv.angular.y = 0.0
            cv.angular.z = 0.0
            self.cmdVelPub.publish(cv)
        elif key == 1:
            # up
            key_text = "UP"
            cv = Twist()
            cv.linear.x = 0.0
            cv.linear.y = 100.0
            cv.linear.z = 0.0
            cv.angular.x = 0.0
            cv.angular.y = 0.0
            cv.angular.z = 0.0
            self.cmdVelPub.publish(cv)
        elif key == 2:
            # right
            key_text = "RIGHT"
            cv = Twist()
            cv.linear.x = -100.0
            cv.linear.y = 0.0
            cv.linear.z = 0.0
            cv.angular.x = 0.0
            cv.angular.y = 0.0
            cv.angular.z = 0.0
            self.cmdVelPub.publish(cv)
        elif key == 3:
            # down
            key_text = "DOWN"
            cv = Twist()
            cv.linear.x = 0.0
            cv.linear.y = -100.0
            cv.linear.z = 0.0
            cv.angular.x = 0.0
            cv.angular.y = 0.0
            cv.angular.z = 0.0
            self.cmdVelPub.publish(cv)

        if key_text != "":
            self.dashboard.handleKeyText(key_text)

    def keyPressEvent(self, e):    
        print "key press " + str(e.key())     
        if e.key() == QtCore.Qt.Key_L:
            print "letf"
            self.processDirectionKey(0)
        elif e.key() == QtCore.Qt.Key_R:
            print "right"
            self.processDirectionKey(2)        
        elif e.key() == QtCore.Qt.Key_U:
            print "up"
            self.processDirectionKey(1)
        elif e.key() == QtCore.Qt.Key_D:
            print "down"
            self.processDirectionKey(3)

        

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    w = SpheroDashboardForm()
    w.show()
    sys.exit(app.exec_())
  
        
