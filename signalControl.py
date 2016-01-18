from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import *
from QtCore import *

class gestor_signal(QObject):
    seta = QtCore.pyqtSignal(int)
    set_range = QtCore.pyqtSignal(int)
    incrementa = QtCore.pyqtSignal(int)
    show_janela  = QtCore.pyqtSignal()
    hide_janela  = QtCore.pyqtSignal()
    menssagem  = QtCore.pyqtSignal(str)

    seta_up = QtCore.pyqtSignal(int)
    set_range_up = QtCore.pyqtSignal(int)
    incrementa_up = QtCore.pyqtSignal(int)
    show_janela_up  = QtCore.pyqtSignal()
    hide_janela_up  = QtCore.pyqtSignal()
    menssagem_up  = QtCore.pyqtSignal(str)

    def __init__(self,parent=None):
        super(gestor_signal,self).__init__()

    def setv_(self,valor):
        self.seta.emit(valor)

    def setr_(self,valor):
        self.set_range.emit(valor)

    def incrementa_(self,valor):
        self.incrementa.emit(valor)

    def show_janela_(self):
        self.show_janela.emit()

    def hide_janela_(self):
        self.hide_janela.emit()

    def msg(self,msg_):
        self.menssagem.emit(msg_)

    def setv_up_(self,valor):
        self.seta_up.emit(valor)

    def setr_up_(self,valor):
        self.set_range_up.emit(valor)

    def incrementa_up_(self,valor):
        self.incrementa_up.emit(valor)

    def show_janela_up_(self):
        self.show_janela_up.emit()

    def hide_janela_up_(self):
        self.hide_janela_up.emit()

    def msg_up_(self,msg_):
        self.menssagem_up.emit(msg_)