from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import *
from QtCore import QEventLoop
import threading,time
import sys,os,imp


class tela_init(QtWidgets.QMainWindow):

    def __init__(self,app_):

        super(tela_init, self).__init__()
        self.app = app_

        self.app2_= QtWidgets.QApplication([])
        self.app2_.setQuitOnLastWindowClosed(False)


        self.emissora = teste_seta()


        self.y = teste()



        self.emissora.seta.connect(self.y.seta)
        self.emissora.incrementa.connect(self.y.incrementa)
        self.emissora.show_janela.connect(self.y.show_window)
        self.emissora.hide_janela.connect(self.y.hide_window)


        self.y.show()


        self.emissora.show()



class teste_seta(QtWidgets.QMainWindow):


    seta = QtCore.pyqtSignal(int)

    incrementa = QtCore.pyqtSignal(int)

    show_janela  = QtCore.pyqtSignal()

    hide_janela  = QtCore.pyqtSignal()




    def __init__(self):
        super(teste_seta,self).__init__()

        self.lay_principal = QVBoxLayout()



        self.bn1 = QPushButton("seta")

        self.bn2 = QPushButton("incrementa")

        self.bn3 = QPushButton("show")
        self.bn4 = QPushButton("hide")


        self.l1 =  QLineEdit()
        self.l2 =  QLineEdit()




        def func_bn1():

            val1= 0
            if (self.l1.text()!=""):
                val1= int(self.l1.text())

            self.seta_(val1)



        def func_bn2():

            val2= 0
            if (self.l2.text()!=""):
                val2= int(self.l2.text())

            self.incrementa_(val2)


        self.lay_principal.addWidget(self.l1)
        self.lay_principal.addWidget(self.bn1)
        self.lay_principal.addWidget(self.l2)
        self.lay_principal.addWidget(self.bn2)

        self.lay_principal.addWidget(self.bn3)
        self.lay_principal.addWidget(self.bn4)


        self.bn1.clicked.connect(func_bn1)
        self.bn2.clicked.connect(func_bn2)


        self.bn3.clicked.connect(self.show_janela_)

        self.bn4.clicked.connect(self.hide_janela_)


        #self.app3_ = QtWidgets.QApplication([])
        #self.z = Window(self.app3_)
        #self.btn.clicked.connect(self.app3_.download)
        widgetfinal = QtWidgets.QWidget()
        widgetfinal.setLayout(self.lay_principal)
        self.setCentralWidget(widgetfinal)



    def seta_(self,valor):
        self.seta.emit(valor)

    def incrementa_(self,valor):
        self.incrementa.emit(valor)

    def show_janela_(self):
        self.show_janela.emit()

    def hide_janela_(self):
        self.hide_janela.emit()


class teste(QtWidgets.QMainWindow):

    def __init__(self):

        super(teste,self).__init__()

        #self.btn = QtWidgets.QPushButton("Download",self)
        #self.btn.move(200,120)
        self.lay_principal = QVBoxLayout()
        self.lay_progress = QHBoxLayout()
        self.progress = QtWidgets.QProgressBar(self)

        self.progress.setGeometry(200, 80, 1000, 20)
        self.progress.setRange(0,1000)


        self.bn = QPushButton("click")



        self.bn.clicked.connect(self.clear)
        self.lay_progress.addWidget(self.progress)
        self.lay_principal.addWidget(self.bn)
        self.lay_principal.addLayout(self.lay_progress)

        #self.app3_ = QtWidgets.QApplication([])
        #self.z = Window(self.app3_)
        #self.btn.clicked.connect(self.app3_.download)
        widgetfinal = QtWidgets.QWidget()
        widgetfinal.setLayout(self.lay_principal)
        self.setCentralWidget(widgetfinal)
        self.progress.setValue(0)


    def clear(self):
        self.progress.setValue(0)

    def incrementa(self,valor):

        if (self.progress.value()<1000):
            self.progress.setValue(self.progress.value()+valor)
        #while self.completed < 100:
        #    self.completed += 0.0001
        #    self.progress.setValue(self.completed)

    def seta(self,valor):
        self.progress.setValue(valor)
        #while self.completed < 100:
        #    self.completed += 0.0001
        #    self.progress.setValue(self.completed)


    def show_window(self):
        self.show()

    def hide_window(self):
        self.hide()


class Window(QtWidgets.QMainWindow):
    def __init__(self,app_):
        super(Window, self).__init__()
        self.app = app_
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PyQT tuts!")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
        extractAction = QtWidgets.QAction("&GET TO THE CHOPPAH!!!", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        #extractAction.triggered.connect(self.close_application)
        self.statusBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        btn.resize(btn.minimumSizeHint())
        btn.move(0,100)
        self.toolBar = self.addToolBar("Extraction")
        self.toolBar.addAction(extractAction)
        checkBox = QtWidgets.QCheckBox('Shrink Window', self)
        checkBox.move(100, 25)

        self.progress = QtWidgets.QProgressBar(self)
        self.progress.setGeometry(200, 80, 250, 20)



app = QtWidgets.QApplication([])
app.setQuitOnLastWindowClosed(False)
x = tela_init(app)
#x.show()
app.exec_()