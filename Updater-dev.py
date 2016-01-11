# -*- coding: utf-8 -*-

from controlador import *
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QEventLoop
from Configer import configer
import os,sys,imp
import threading
from Templates import *

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

class tela_inicial(QtWidgets.QMainWindow):
    def main_is_frozen(self):
        return (hasattr(sys, "frozen") or # new py2exe
                hasattr(sys, "importers") # old py2exe
                or imp.is_frozen("__main__")) # tools/freeze
    def get_main_dir(self):
        if self.main_is_frozen():
            return os.path.dirname(sys.executable)
        return os.path.dirname(sys.argv[0])
    def __init__(self,app_):
        super(tela_inicial,self).__init__()
        self.cfg = configer(self.get_main_dir()+"/"+"config.txt")
        self.cfg.read()
        self.app = app_
        if self.cfg.dictado['MODO']=='DEV':
            self.app2_= QtWidgets.QApplication([])
            self.app2_.setQuitOnLastWindowClosed(False)
            self.y = main_window(self.app2_)

        elif self.cfg.dictado['MODO']=='CLIENT':
            self.app2_= QtWidgets.QApplication([])
            self.app2_.setQuitOnLastWindowClosed(False)
            self.y = tela_cliente(self.app2_,self)


class tela_cliente(QtWidgets.QMainWindow):
    def __init__(self,app_,mainw):
        super(tela_cliente,self).__init__()
        self.controlador = controlador()
        self.parentwindow = mainw
        #icon_path =self.controlador.get_main_dir()  + "/Updater-icon.png"
        icon_path =self.controlador.get_main_dir() + "/suits_icon.png"
        icon = QtGui.QIcon(icon_path)
        self.tray_cliente = QtWidgets.QSystemTrayIcon(icon)
        self.menu_tray = QtWidgets.QMenu()
        self.tray_cliente.setContextMenu(self.menu_tray)
        self.tray_cliente.setToolTip(u"Ola Cliente, eu sou o UPDATER")
        self.tray_cliente.show()

        #acrescentar funcao de abrir programa
        def abrir_progama():
            objeto_ = self.sender()
            nome =objeto_.property("NAME")
            self.controlador.instalar_executar_projeto(nome)
        self.abrirprograma_fnc = abrir_progama
        self.popula_tray()
    def popula_tray(self):
        #Zera toda a tray
        self.ref_tray=[]
        self.lista_projetos = self.controlador.pegar_todos_projetos()
        self.menu_tray.clear()
        if self.controlador.dbg=='ON':
            self.controlador.gm.enviar_msg_("ATUALIZACAO INICIADA, tray limpa","MAIN_WINDOW")
        #Adiciona QAction do novo projeto
        #abrir_new_project.triggered.connect(self.janelanovoprojeto_fnc)
        #Adiciona SubMenu dos Projetos
        #self.menu_tray.addSeparator()
        self.menu_projetos = self.menu_tray.addMenu("Projetos")

        for projeto in self.lista_projetos:
            if self.controlador.dbg=='ON':
                warum = "Projeto adicionado na tray: " + projeto
                self.controlador.gm.enviar_msg_(warum,"MAIN_WINDOW")

            aba_project = QtWidgets.QAction(projeto,self)
            aba_project.setProperty("NAME",projeto)
            self.ref_tray.append(aba_project)
            self.menu_projetos.addAction(aba_project)
            aba_project.triggered.connect(self.abrirprograma_fnc)
        #Adciona QAction Saida do Sistema
        self.menu_tray.addSeparator()
        quit_action = QtWidgets.QAction("Sair",self)
        self.menu_tray.addAction(quit_action)
        quit_action.triggered.connect(self.parentwindow.app.quit)

class main_window(QtWidgets.QMainWindow):

    showSplash = QtCore.pyqtSignal()
    hideSplash = QtCore.pyqtSignal()


    def __init__(self,app_):
        super(main_window,self).__init__()

        self.controlador = controlador()
        icon_path =self.controlador.get_main_dir()  + "/Updater-icon.png"

        icon_path2 = self.controlador.get_main_dir()+'/Splash_Kondor_Up.png'
        icon = QtGui.QIcon(icon_path)
        self.tray_ = QtWidgets.QSystemTrayIcon(icon)
        self.app = app_
        #inicializando a janela de edicao
        self.app2= QtWidgets.QApplication([])
        self.app2.setQuitOnLastWindowClosed(False)
        self.y = janela_edicao(self.app2,self)
        self.timer_ = QtCore.QTimer()
        self.splash_pix = QtGui.QPixmap(icon_path2)
        self.splash = QSplashScreen(self.splash_pix, QtCore.Qt.WindowStaysOnTopHint)
        #Declarando as funcoes de que as trays contem
        def janela_novo_projeto():
            widgetfinal.setLayout(self.lay1)
            self.setCentralWidget(widgetfinal)
            self.show()
        self.janelanovoprojeto_fnc = janela_novo_projeto
        def pre_deploy():
            self.showSplash.emit()
            objeto_ = self.sender()
            nome =objeto_.property("NAME")
            self.controlador.deploy(nome)
            self.hideSplash.emit()
        self.predeploy_fnc = pre_deploy
        def pre_edit():
            objeto_ = self.sender()
            nome =objeto_.property("NAME")
            dict_dados = self.controlador.pegar_dados_projeto(nome)
            self.y.le_nomeprod2.setText(nome)
            self.y.le_tiporepo2.setText(dict_dados['TIPOREPOSITORIO'])
            self.y.le_dire2.setText(dict_dados['DIRETORIO'])
            self.y.le_repo2.setText(dict_dados['REPOSITORIO'])
            self.y.le_executavel2.setText(dict_dados['EXECUTAVEL'])
            self.y.show()
        self.preedit_fnc = pre_edit
        def abrir_progama():
            objeto_ = self.sender()
            nome =objeto_.property("NAME")
            self.controlador.instalar_executar_projeto(nome)
        self.instar_fnc = abrir_progama

        #Populando a tray
        self.menu_tray = QtWidgets.QMenu()
        self.popula_tray()
        self.app=app_

        #Desenho da TELA DE NOVO PROJETO
        self.setWindowTitle("UPDATER-DEV Novo Projeto")
        self.lay1 =  QVBoxLayout()
        self.lay_nomeprod = QHBoxLayout()
        self.label1 = QLabel('Nome do Projeto')
        self.le1 = QLineEdit()
        self.lay_nomeprod.addWidget(self.label1)
        self.lay_nomeprod.addWidget(self.le1)
        self.lay_tiporepo = QHBoxLayout()
        self.label2 = QLabel('Tipo do Repositorio')
        self.le2 = QLineEdit()
        self.lay_tiporepo.addWidget(self.label2)
        self.lay_tiporepo.addWidget(self.le2)
        self.lay_dire = QHBoxLayout()
        self.label3 = QLabel(u'Endereço do Diretório')
        self.le3 = QLineEdit()
        self.button_dir = QPushButton("...")
        self.lay_dire.addWidget(self.label3)
        self.lay_dire.addWidget(self.le3)
        self.lay_dire.addWidget(self.button_dir)
        self.lay_repo = QHBoxLayout()
        self.label4 = QLabel(u'Endereço do Repositório')
        self.le4 = QLineEdit()
        self.lay_repo.addWidget(self.label4)
        self.lay_repo.addWidget(self.le4)
        self.button_repo = QPushButton("...")
        self.lay_executavel = QHBoxLayout()
        self.label5 = QLabel(u'Endereço do Executavel')
        self.le5 = QLineEdit()
        self.lay_executavel.addWidget(self.label5)
        self.lay_executavel.addWidget(self.le5)
        self.button_executavel = QPushButton("...")
        self.lay1.addLayout(self.lay_nomeprod)
        self.lay1.addLayout(self.lay_tiporepo)
        self.lay1.addLayout(self.lay_dire)
        self.lay1.addLayout(self.lay_repo)
        self.lay1.addLayout(self.lay_executavel)
        self.lay_repo.addWidget(self.button_repo)
        self.lay_executavel.addWidget(self.button_executavel)
        self.button_novoproj = QPushButton('Novo Projeto')
        self.lay1.addWidget(self.button_novoproj)
        widgetfinal = QtWidgets.QWidget()
        widgetfinal.setLayout(self.lay1)
        self.setCentralWidget(widgetfinal)
        #SETANDO o STYLE da TELA
        self.diretorio = self.controlador.get_main_dir()
        self.arquivo = open(self.diretorio+'/stylesheet.txt','r')
        self.style = self.arquivo.read()
        self.setStyleSheet(self.style)


        #Declarando as Funcoes dos Botoes da TELA
        def dialog_1():
            dialog =QtWidgets.QFileDialog(self,"Escolha as pastas  origem ou diretorio")
            dialog.setFileMode(QtWidgets.QFileDialog.Directory)
            directories=['']
            if dialog.exec_():
                directories = dialog.selectedFiles()
            self.le3.setText(directories[0])
            return
        self.button_dir.clicked.connect(dialog_1)
        def dialog_2():
            dialog =QtWidgets.QFileDialog(self,"Escolha a pasta destino ou repositorio")
            dialog.setFileMode(QtWidgets.QFileDialog.Directory)
            directories=['']
            if dialog.exec_():
                directories = dialog.selectedFiles()
            self.le4.setText(directories[0])
            return
        self.button_repo.clicked.connect(dialog_2)
        def dialog_3():
            dialog =QtWidgets.QFileDialog(self,u"Selecione o Executável do Programa")
            dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
            directories=['']
            if dialog.exec_():
                directories = dialog.selectedFiles()
            self.le5.setText(directories[0])
            return
        self.button_executavel.clicked.connect(dialog_3)
        def new_project():
            self.controlador.new_project(self.le1.text(),self.le3.text(),"1.0",self.le4.text().replace("\\","/"),self.le2.text().replace("\\","/"),self.le5.text().replace("\\","/"))
            self.popula_tray()
            self.hide()
        self.button_novoproj.clicked.connect(new_project)
        def comportamento_tray(reason):
            if reason == QtWidgets.QSystemTrayIcon.Trigger:
                self.show()
        self.tray_.activated.connect(comportamento_tray)

        def timer_tray():
            self.popula_tray()
            print "Atualizando"

        self.timer_.timeout.connect(timer_tray)
        self.timer_.start(self.controlador.t_atuali)
        #abrindo a tray
        self.tray_.setContextMenu(self.menu_tray)
        self.tray_.setToolTip(u"Você está olhando o Updater-Dev! ")
        self.tray_.show()


        self.TSpl=ThreadSplash(app_)

        self.TSpl.start()
        def emit_depois():

            self.hideSplash.connect(self.TSpl.splash.hideSplash)
            self.showSplash.connect(self.TSpl.splash.showSplash)


        QtCore.QTimer.singleShot(1, emit_depois)


    def popula_tray(self):
        #Zera toda a tray
        self.ref_tray=[]
        self.lista_projetos = self.controlador.pegar_todos_projetos()
        self.menu_tray.clear()
        if self.controlador.dbg=='ON':
            self.controlador.gm.enviar_msg_("ATUALIZACAO INICIADA, tray limpa","MAIN_WINDOW")
        #Adiciona QAction do novo projeto
        abrir_new_project = QtWidgets.QAction("Adicionar Novo Projeto",self)
        self.menu_tray.addAction(abrir_new_project)
        abrir_new_project.triggered.connect(self.janelanovoprojeto_fnc)
        #Adiciona SubMenu dos Projetos
        self.menu_tray.addSeparator()
        self.menu_projetos = self.menu_tray.addMenu("Projetos")

        for projeto in self.lista_projetos:
            if self.controlador.dbg=='ON':
                warum = "Projeto adicionado na tray: " + projeto
                self.controlador.gm.enviar_msg_(warum,"MAIN_WINDOW")
            action_= QtWidgets.QAction("Deploy ",self)
            exclude_ = QtWidgets.QAction("Editar/Excluir",self)
            instar_ = QtWidgets.QAction("Instalar/Executar",self)
            menu_ = self.menu_projetos.addMenu(projeto)
            action_.setProperty("NAME",projeto)
            exclude_.setProperty("NAME",projeto)
            instar_.setProperty("NAME",projeto)
            menu_.addAction(action_)
            menu_.addAction(exclude_)
            menu_.addAction(instar_)
            self.ref_tray.append(menu_)
            self.menu_projetos.addMenu(menu_)
            action_.triggered.connect(self.predeploy_fnc)
            exclude_.triggered.connect(self.preedit_fnc)
            instar_.triggered.connect(self.instar_fnc)

        #Adciona QAction Saida do Sistema
        self.menu_tray.addSeparator()
        quit_action = QtWidgets.QAction("Sair",self)
        self.menu_tray.addAction(quit_action)
        quit_action.triggered.connect(self.app.quit)


class janela_edicao(QtWidgets.QMainWindow):
    def __init__(self,app_,mainw):

        super(janela_edicao,self).__init__()
        self.parentwindow = mainw
        self.controlador = controlador()

        #Desenhando a TELA2
        self.lay2 =  QVBoxLayout()
        self.lay_nomeprod2 = QHBoxLayout()
        self.label_nomeprod2 = QLabel('Nome do Projeto')
        self.le_nomeprod2 = QLineEdit()
        self.le_nomeprod2.setReadOnly(True)
        self.lay_nomeprod2.addWidget(self.label_nomeprod2)
        self.lay_nomeprod2.addWidget(self.le_nomeprod2)
        self.lay_tiporepo2 = QHBoxLayout()
        self.label_tiporepo2 = QLabel('Tipo do Repositorio')
        self.le_tiporepo2 = QLineEdit()
        self.lay_tiporepo2.addWidget(self.label_tiporepo2)
        self.lay_tiporepo2.addWidget(self.le_tiporepo2)
        self.lay_dire2 = QHBoxLayout()
        self.label_dire2 = QLabel(u'Endereço do Diretório')
        self.le_dire2 = QLineEdit()
        self.button_dire2 = QPushButton("...")
        self.lay_dire2.addWidget(self.label_dire2)
        self.lay_dire2.addWidget(self.le_dire2)
        self.lay_dire2.addWidget(self.button_dire2)
        self.lay_repo2 = QHBoxLayout()
        self.label_repo2 = QLabel(u'Endereço do Repositório')
        self.le_repo2= QLineEdit()
        self.lay_repo2.addWidget(self.label_repo2)
        self.lay_repo2.addWidget(self.le_repo2)
        self.button_repo2 = QPushButton("...")
        self.lay_repo2.addWidget(self.button_repo2)
        self.lay_executavel2 = QHBoxLayout()
        self.label_executavel2 = QLabel(u'Endereço do Executavel')
        self.le_executavel2 = QLineEdit()
        self.lay_executavel2.addWidget(self.label_executavel2)
        self.lay_executavel2.addWidget(self.le_executavel2)
        self.button_executavel2 = QPushButton("...")
        self.lay_executavel2.addWidget(self.button_executavel2)
        self.lay2.addLayout(self.lay_nomeprod2)
        self.lay2.addLayout(self.lay_tiporepo2)
        self.lay2.addLayout(self.lay_dire2)
        self.lay2.addLayout(self.lay_repo2)
        self.lay2.addLayout(self.lay_executavel2)
        self.button_editarproj = QPushButton('Atualizar')
        self.lay2.addWidget(self.button_editarproj)
        self.button_excluirproj=QPushButton('Excluir')
        self.lay2.addWidget(self.button_excluirproj)

        #Declarando as Funcoes do Botoes da TELA2
        def dialog_1():
            dialog =QtWidgets.QFileDialog(self,"Escolha as pastas  origem ou diretorio")
            dialog.setFileMode(QtWidgets.QFileDialog.Directory)
            directories=['']
            if dialog.exec_():
                directories = dialog.selectedFiles()
            self.le_dire2.setText(directories[0])
            return
        self.button_dire2.clicked.connect(dialog_1)
        def dialog_2():
            dialog =QtWidgets.QFileDialog(self,"Escolha a pasta destino ou repositorio")
            dialog.setFileMode(QtWidgets.QFileDialog.Directory)
            directories=['']
            if dialog.exec_():
                directories = dialog.selectedFiles()
            self.le_repo2.setText(directories[0])
            return
        self.button_repo2.clicked.connect(dialog_2)
        def dialog_3():
            dialog =QtWidgets.QFileDialog(self,u"Selecione o Executável do Programa")
            dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
            directories=['']
            if dialog.exec_():
                directories = dialog.selectedFiles()
            self.le_executavel2.setText(directories[0])
            return
        self.button_executavel2.clicked.connect(dialog_3)
        def atualizar_projeto():
            self.controlador.atualizar(self.le_nomeprod2.text(),self.le_dire2.text().replace("\\","/"),self.le_repo2.text().replace("\\","/"),self.le_tiporepo2.text().replace("\\","/"),self.le_executavel2.text().replace("\\","/"))
            self.hide()
        self.button_editarproj.clicked.connect(atualizar_projeto)
        def excluir_projeto():
            self.controlador.excluir(self.le_nomeprod2.text())
            self.parentwindow.popula_tray()
            self.hide()
        self.button_excluirproj.clicked.connect(excluir_projeto)

        #Setando STYLE DA TELA2 e NOME
        self.setWindowTitle("UPDATER-DEV Atualizar/Excluir Projetos")
        self.diretorio = self.controlador.get_main_dir()
        self.arquivo = open(self.diretorio+'/stylesheet2.txt','r')
        self.style = self.arquivo.read()
        self.setStyleSheet(self.style)
        widgetfinal = QtWidgets.QWidget()
        widgetfinal.setLayout(self.lay2)
        self.setCentralWidget(widgetfinal)

app = QtWidgets.QApplication([])
app.setQuitOnLastWindowClosed(False)
x = tela_inicial(app)
#x.show()
app.exec_()