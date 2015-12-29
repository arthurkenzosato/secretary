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
        self.menu_tray = QtWidgets.QMenu()


        #menu Add Projeto

        abrir_new_project = QtWidgets.QAction("Adicionar Novo Projeto",self)
        self.menu_tray.addAction(abrir_new_project)
        abrir_new_project.triggered.connect(self.show)
        self.menu_tray.addSeparator()



        #projetos existentes
        self.ref_tray=[]
        def pre_deploy():
            objeto_ = self.sender()
            nome =objeto_.property("NAME")
            self.controlador.deploy(nome)

        self.menu_projetos = self.menu_tray.addMenu("Projetos")

        for projeto in lista_projetos:

            action_= QtWidgets.QAction(projeto,self)
            action_.setProperty("NAME",projeto)

            self.ref_tray.append(action_)

            self.menu_projetos.addAction(action_)


            action_.triggered.connect(pre_deploy)



        #menu saida sistema
        self.menu_tray.addSeparator()
        quit_action = QtWidgets.QAction("Sair",self)
        self.menu_tray.addAction(quit_action)
        quit_action.triggered.connect(app.quit)
        #copiar backuper

        #exec_action = QtWidgets.QAction("Deploy",self)



        self.app=app_
        self.setWindowTitle("UPDATER_DEV")
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

        #add botao

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

        #add botao

        self.lay1.addLayout(self.lay_nomeprod)
        self.lay1.addLayout(self.lay_tiporepo)
        self.lay1.addLayout(self.lay_dire)
        self.lay1.addLayout(self.lay_repo)
        self.lay1.addLayout(self.lay_executavel)
        self.lay_repo.addWidget(self.button_repo)
        self.lay_executavel.addWidget(self.button_executavel)


        self.diretorio = self.controlador.get_main_dir()
        self.arquivo = open(self.diretorio+'/stylesheet.txt','r')
        self.style = self.arquivo.read()
        self.setStyleSheet(self.style)

        self.button_novoproj = QPushButton('Novo Projeto')
        self.lay1.addWidget(self.button_novoproj)

        widgetfinal = QtWidgets.QWidget()
        widgetfinal.setLayout(self.lay1)
        self.setCentralWidget(widgetfinal)





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
            dialog.setFileMode(QtWidgets.QFileDialog.Directory)
            directories=['']
            if dialog.exec_():
                directories = dialog.selectedFiles()
            self.le5.setText(directories[0])
            return
        self.button_executavel.clicked.connect(dialog_3)

        def new_project():
            self.controlador.new_project(self.le1.text(),self.le3.text(),"1.0",self.le4.text().replace("\\","/"),self.le2.text().replace("\\","/"),self.le5.text().replace("\\","/"))
            criar = QtWidgets.QAction(self.le1.text(),self)
            criar.setProperty("NAME",self.le1.text())
            self.ref_tray.append(criar)
            self.menu_projetos.addAction(criar)
            criar.triggered.connect(pre_deploy)
            self.hide()




        self.button_novoproj.clicked.connect(new_project)

        #menu_tray.addAction(exec_action)
        self.tray_.setContextMenu(self.menu_tray)
        self.tray_.setToolTip("Updater")

        def comportamento_tray(reason):

            if reason == QtWidgets.QSystemTrayIcon.Trigger:
                self.show()


        self.tray_.activated.connect(comportamento_tray)
        self.tray_.show()




app = QtWidgets.QApplication([])
app.setQuitOnLastWindowClosed(False)
x = main_window(app)
x.show()
app.exec_()