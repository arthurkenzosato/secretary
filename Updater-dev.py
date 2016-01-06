# -*- coding: utf-8 -*-


from controlador import *
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import *

from Templates import *




class main_window(QtWidgets.QMainWindow):


    def __init__(self,app_):

        super(main_window,self).__init__()
        self.controlador = controlador()
        lista_projetos = self.controlador.pegar_todos_projetos() #lista com o nome de todos os projetos
        icon_path =self.controlador.get_main_dir()  + "/Updater-icon.png"
        icon = QtGui.QIcon(icon_path)
        self.tray_ = QtWidgets.QSystemTrayIcon(icon)
        self.app = app_

        #inicializando a janela de edicao
        self.app2= QtWidgets.QApplication([])
        self.app2.setQuitOnLastWindowClosed(False)
        self.y = janela_edicao(self.app2,self)

        #Declarando as funcoes de que as trays contem
        def janela_novo_projeto():
            widgetfinal.setLayout(self.lay1)
            self.setCentralWidget(widgetfinal)
            self.show()
        self.janelanovoprojeto_fnc = janela_novo_projeto
        def pre_deploy():
            objeto_ = self.sender()
            nome =objeto_.property("NAME")
            self.controlador.deploy(nome)
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

        #abrindo a tray
        self.tray_.setContextMenu(self.menu_tray)
        self.tray_.setToolTip(u"Você está olhando o Updater-Dev! ")
        self.tray_.show()


    def popula_tray(self):
        #Zera toda a tray
        self.ref_tray=[]
        self.lista_projetos = self.controlador.pegar_todos_projetos()
        self.menu_tray.clear()
        #Adiciona QAction do novo projeto
        abrir_new_project = QtWidgets.QAction("Adicionar Novo Projeto",self)
        self.menu_tray.addAction(abrir_new_project)
        abrir_new_project.triggered.connect(self.janelanovoprojeto_fnc)
        #Adiciona SubMenu dos Projetos
        self.menu_tray.addSeparator()
        self.menu_projetos = self.menu_tray.addMenu("Projetos")
        for projeto in self.lista_projetos:
            action_= QtWidgets.QAction("Deploy ",self)
            exclude_ = QtWidgets.QAction("Atualizar/Excluir",self)
            menu_ = self.menu_projetos.addMenu(projeto)
            action_.setProperty("NAME",projeto)
            exclude_.setProperty("NAME",projeto)
            menu_.addAction(action_)
            menu_.addAction(exclude_)
            self.ref_tray.append(menu_)
            self.menu_projetos.addMenu(menu_)
            action_.triggered.connect(self.predeploy_fnc)
            exclude_.triggered.connect(self.preedit_fnc)

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
x = main_window(app)
x.show()
app.exec_()