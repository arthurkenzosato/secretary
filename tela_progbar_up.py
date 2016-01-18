from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import *
from QtCore import QEventLoop
import threading,time
import sys,os,imp

class tela_progbar_up(QtWidgets.QMainWindow):

    def __init__(self):

        super(tela_progbar_up,self).__init__()
        self.lay_principal = QVBoxLayout()
        self.setGeometry(500, 500, 420, 200)
        self.setWindowTitle("Enviando Arquivos...")
        self.lay_imagem = QHBoxLayout()
        self.setStyleSheet("""
        QLabel{
            background: transparent;
            }
        .QWidget {
            /*background-color: rgb(255, 0, 0); */
            background-image: url(im/Splash_Kondor_Up.png);
            }
        """)
        self.label1 = QLabel('')
        self.lay_imagem.addWidget(self.label1)
        self.lay_imagem.setProperty("progress_window",True)
        self.lay_progress = QHBoxLayout()
        self.progress = QtWidgets.QProgressBar(self)
        self.progress.setRange(0,1000)
        self.lay_progress.addWidget(self.progress)
        self.lay_principal.addLayout(self.lay_imagem)
        self.lay_principal.addLayout(self.lay_progress)
        widgetfinal = QtWidgets.QWidget()
        widgetfinal.setLayout(self.lay_principal)
        self.setCentralWidget(widgetfinal)
        self.progress.setValue(0)


    def incrementa(self,valor):
        self.progress.setValue(self.progress.value()+valor)

    def seta(self,valor):
        self.progress.setValue(valor)

    def set_range(self,valor):
        self.progress.setRange(0,valor)

    def show_window(self):
        self.show()

    def hide_window(self):
        self.hide()

    def receive_msg(self,valor):
        self.label1.setText(valor)
