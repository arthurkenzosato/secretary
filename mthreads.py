
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QEventLoop
from Configer import configer
import os,sys,imp
import threading

class WrapperSplashScreen(QtCore.QObject):

    def __init__(self,parent=None):
        super(WrapperSplashScreen,self).__init__(parent)
        self.splash_pix = QtGui.QPixmap('Splash_Kondor_Up.png')
        self.splash = QSplashScreen(self.splash_pix, QtCore.Qt.WindowStaysOnTopHint)
        self.parent=parent

    def showSplash(self):
        print "Thread",threading.currentThread()
        self.splash.show()
        print "teste",self.parent
        self.parent.processEvents()

        def emit_depois():
            print "teste"

        QtCore.QTimer.singleShot(5000, emit_depois)

    def hideSplash(self):
        self.splash.close()



class ThreadSplash(QtCore.QThread):


    def __init__(self,parent=None):
        super(ThreadSplash,self).__init__(parent)
        self.parent=parent

    def run(self):
        self.loop = QEventLoop()
        print "Dummy",threading.currentThread()
        self.splash = WrapperSplashScreen(self.loop)

        self.loop.exec_()


showSplash = QtCore.pyqtSignal()
hideSplash = QtCore.pyqtSignal()

self.showSplash.emit()
self.hideSplash.emit()



self.TSpl=ThreadSplash(app_)

self.TSpl.start()
def emit_depois():

    self.hideSplash.connect(self.TSpl.splash.hideSplash)
    self.showSplash.connect(self.TSpl.splash.showSplash)


QtCore.QTimer.singleShot(1, emit_depois)