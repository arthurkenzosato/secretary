# -*- coding: utf-8 -*-

from controlador import *
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QEventLoop
from Configer import configer
from signalControl import *
from tela_progbar import *
from tela_progbar_up import *
from secretary import *
from authenticator import *
import os,sys,imp,getpass

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
        self.sc = gestor_signal()
        self.progbar = tela_progbar()
        self.sc.seta.connect(self.progbar.seta)
        self.sc.set_range.connect(self.progbar.set_range)
        self.sc.hide_janela.connect(self.progbar.hide_window)
        self.sc.show_janela.connect(self.progbar.show_window)
        self.sc.incrementa.connect(self.progbar.incrementa)
        self.sc.menssagem.connect(self.progbar.receive_msg)
        self.app = app_

        if self.cfg.dictado['MODO']=='DEV':
            self.app2_= QtWidgets.QApplication([])
            self.app2_.setQuitOnLastWindowClosed(False)
            self.y = janela_dev(self.app2_,self,signalcontrol_= self.sc)

        elif self.cfg.dictado['MODO']=='CLIENT':
            self.app2_= QtWidgets.QApplication([])
            self.app2_.setQuitOnLastWindowClosed(False)
            self.y = tela_cliente(self.app2_,self,signalcontrol_= self.sc)

class tela_cliente(QtWidgets.QMainWindow):
    def __init__(self,app_,mainw,signalcontrol_):
        super(tela_cliente,self).__init__()
        self.parentwindow = mainw
        self.sc = signalcontrol_
        self.controlador = controlador(signalcontrol_= self.sc,app_=self.parentwindow.app,configer_=self.parentwindow.cfg)
        #setando icone da tray
        icon_path =self.controlador.get_main_dir() + "/im/suits_icon.png"
        icon = QtGui.QIcon(icon_path)
        ok_path = self.controlador.get_main_dir() + "/im/green_light-icon.png"
        self.icon_green = QtGui.QIcon(ok_path)
        down_path = self.controlador.get_main_dir() + "/im/download-icon.png"
        self.icon_down = QtGui.QIcon(down_path)
        refresh_path = self.controlador.get_main_dir() + "/im/refresh-icon.png"
        self.icon_refresh = QtGui.QIcon(refresh_path)
        programs_path = self.controlador.get_main_dir() + "/im/programs-icon.png"
        self.icon_programs = QtGui.QIcon(programs_path)
        uninstall_path = self.controlador.get_main_dir() + "/im/delete-icon.png"
        self.icon_uninstall = QtGui.QIcon(uninstall_path)
        run_path = self.controlador.get_main_dir() +"/im/run-icon.png"
        self.icon_run = QtGui.QIcon(run_path)
        yellow_path = self.controlador.get_main_dir() + "/im/yellow_light-icon.png"
        self.icon_yellow =QtGui.QIcon(yellow_path)
        white_path = self.controlador.get_main_dir() +"/im/white_light-icon.png"
        self.icon_white = QtGui.QIcon(white_path)
        alert_path = self.controlador.get_main_dir() + "/im/alert_icon.png"
        self.icon_alert = QtGui.QIcon(alert_path)
        self.tray_cliente = QtWidgets.QSystemTrayIcon(icon)
        self.menu_tray = QtWidgets.QMenu()
        self.tray_cliente.setContextMenu(self.menu_tray)
        nome=getpass.getuser()
        nome = " ".join(nome.split("."))
        self.tray_cliente.setToolTip("Ola {0} ".format(nome))
        self.tray_cliente.show()

        #acrescentar funcao de abrir programa
        def abrir_progama():
            objeto_ = self.sender()
            nome =objeto_.property("NAME")
            self.controlador.instalar_executar_projeto(nome)
            self.popula_tray()
        self.abrirprograma_fnc = abrir_progama
        def uninstall_projeto():
            objeto_ = self.sender()
            nome =objeto_.property("NAME")
            choice=QMessageBox.question(self,"Desinstalar", u"Você está certo que quer Desinstalar o projeto {0}?".format(nome))
            if choice == QMessageBox.Yes:
                print('DELETANDO')
                self.controlador.uninstall_programa(nome)
            else:
                pass
            self.popula_tray()
        self.uninstall_fnc = uninstall_projeto
        self.popula_tray()

    def fecha_tudo(self):
        self.tray_cliente.hide()
        self.parentwindow.app.quit()

    def popula_tray(self):
        #força reabrir a conneccao
        db = QtSqlConnector.sgetDB("mysql")
        try:
            db.close()
        except:
            pass
        db.open()
        self.controlador.atualizar_list_programas()

        #Zera toda a tray
        self.ref_tray=[]
        self.lista_projetos = self.controlador.pegar_todos_projetos()
        self.menu_tray.clear()
        if self.controlador.dbg=='ON':
            self.controlador.gm.enviar_msg_("ATUALIZACAO INICIADA, tray limpa","JANELA_CLIENT")
        #Adiciona QAction do novo projeto
        #atualizar_reload = QtWidgets.QAction("Atualizar Tray",self)
        #self.menu_tray.addAction(atualizar_reload)
        atualizar_reload = self.menu_tray.addAction(self.icon_refresh,"Atualizar Tray")
        atualizar_reload.triggered.connect(self.popula_tray)

        #Adiciona SubMenu dos Projetos
        self.menu_tray.addSeparator()
        for projeto in self.lista_projetos:
            if self.controlador.dbg=='ON':
                warum = "Projeto adicionado na tray: " + projeto
                self.controlador.gm.enviar_msg_(warum,"JANELA_CLIENT")

            if projeto not in self.controlador.list_programas.keys():
                menu_ = self.menu_tray.addMenu(self.icon_white,projeto)
                instar_ = menu_.addAction(self.icon_down,"Instalar ")
                instar_.setProperty("NAME",projeto)
            else:
                menu_ = self.menu_tray.addMenu(self.icon_green,projeto)
                instar_ = menu_.addAction(self.icon_run,"Executar")
                instar_.setProperty("NAME",projeto)
                report_bug = menu_.addAction(self.icon_alert,"Reportar BUG")
                uninstall_ = menu_.addAction(self.icon_uninstall,"Desinstalar")
                uninstall_.setProperty("NAME",projeto)
                uninstall_.triggered.connect(self.uninstall_fnc)


            self.ref_tray.append(menu_)
            instar_.triggered.connect(self.abrirprograma_fnc)


        #Adciona QAction Saida do Sistema
        self.menu_tray.addSeparator()
        quit_action = QtWidgets.QAction("Sair",self)
        self.menu_tray.addAction(quit_action)
        quit_action.triggered.connect(self.fecha_tudo)

class janela_dev(QtWidgets.QMainWindow):
    def __init__(self,app_,mainw,signalcontrol_):
        super(janela_dev,self).__init__()
        self.parentwindow = mainw
        self.sc=signalcontrol_
        self.progbar_up_ = tela_progbar_up()
        self.sc.seta_up.connect(self.progbar_up_.seta)
        self.sc.set_range_up.connect(self.progbar_up_.set_range)
        self.sc.hide_janela_up.connect(self.progbar_up_.hide_window)
        self.sc.show_janela_up.connect(self.progbar_up_.show_window)
        self.sc.incrementa_up.connect(self.progbar_up_.incrementa)
        self.sc.menssagem_up.connect(self.progbar_up_.receive_msg)
        self.controlador = controlador(signalcontrol_= self.sc,app_=self.parentwindow.app,configer_=self.parentwindow.cfg)
        icon_path =self.controlador.get_main_dir()  + "/im/Updater-icon.png"
        icon = QtGui.QIcon(icon_path)
        ok_path = self.controlador.get_main_dir() + "/im/green_light-icon.png"
        self.icon_green = QtGui.QIcon(ok_path)
        down_path = self.controlador.get_main_dir() + "/im/download-icon.png"
        self.icon_down = QtGui.QIcon(down_path)
        config_path = self.controlador.get_main_dir()+"/im/config-icon.png"
        self.icon_config = QtGui.QIcon(config_path)
        deploy_path = self.controlador.get_main_dir()+"/im/upload-icon.png"
        self.icon_deploy = QtGui.QIcon(deploy_path)
        run_path = self.controlador.get_main_dir() +"/im/run-icon.png"
        self.icon_run = QtGui.QIcon(run_path)
        refresh_path = self.controlador.get_main_dir()+"/im/refresh-icon.png"
        self.icon_refresh = QtGui.QIcon(refresh_path)
        plus_path = self.controlador.get_main_dir() + "/im/plus-icon.png"
        self.icon_plus = QtGui.QIcon(plus_path)
        program_path = self.controlador.get_main_dir() + "/im/programs-icon.png"
        self.icon_programs = QtGui.QIcon(program_path)
        uninstall_path = self.controlador.get_main_dir() + "/im/delete-icon.png"
        self.icon_uninstall = QtGui.QIcon(uninstall_path)
        yellow_path = self.controlador.get_main_dir() + "/im/yellow_light-icon.png"
        self.icon_yellow =QtGui.QIcon(yellow_path)
        check_path = self.controlador.get_main_dir() +"/im/check-icon.png"
        self.icon_check = QtGui.QIcon(check_path)
        white_path = self.controlador.get_main_dir() + "/im/white_light-icon.png"
        self.icon_white = QtGui.QIcon(white_path)
        alert_path = self.controlador.get_main_dir() + "/im/alert_icon.png"
        self.icon_alert = QtGui.QIcon(alert_path)
        self.usuario_pc = getpass.getuser()
        self.tray_ = QtWidgets.QSystemTrayIcon(icon)
        self.app = app_
        #inicializando a janela de edicao
        self.app2= QtWidgets.QApplication([])
        self.app2.setQuitOnLastWindowClosed(False)
        self.y = janela_edicao(self.app2,self)
        self.timer_ = QtCore.QTimer()
        #Declarando as funcoes de que as trays contem
        def janela_novo_projeto():
            widgetfinal.setLayout(self.lay1)
            self.setCentralWidget(widgetfinal)
            self.show()
        self.janelanovoprojeto_fnc = janela_novo_projeto
        def pre_deploy():
            objeto_ = self.sender()
            nome = objeto_.property("NAME")
            self.controlador.deploy(nome)
            self.popula_tray()
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
            self.y.le_config2.setText(dict_dados['LISTA_CONFIGS'])
            self.y.show()
        self.preedit_fnc = pre_edit
        def abrir_progama():
            objeto_ = self.sender()
            nome =objeto_.property("NAME")
            self.controlador.instalar_executar_projeto(nome)
            self.popula_tray()
        self.instar_fnc = abrir_progama

        def report_bug():
            objeto_ = self.sender()
            nome_projeto =objeto_.property("NAME")
            #self.usuario_pc
            '''caixa_texto = QInputDialog()
            caixa_texto.resize(1000, 1000)
            texto,ok = caixa_texto.getText(self,'BUG report','Descreva o Bug: ')
            '''
            dlg =  QInputDialog(self)
            dlg.setInputMode( QInputDialog.TextInput)
            dlg.setLabelText("Descreva o Bug:")
            dlg.resize(500,200)
            ok = dlg.exec_()
            texto = dlg.textValue()
            if ok:
                self.controlador.reportar_bug(nome_projeto,self.usuario_pc,texto)
                print texto

            else:
                print "erro"
            #self.controlador.
        self.reportbug_fnc = report_bug
        def uninstall_projeto():
            objeto_ = self.sender()
            nome =objeto_.property("NAME")
            choice=QMessageBox.question(self,"Desinstalar", u"Você está certo que quer Desinstalar o projeto {0}?".format(nome))
            if choice == QMessageBox.Yes:
                print('DELETANDO')
                self.controlador.uninstall_programa(nome)
            else:
                pass
            self.popula_tray()
        self.uninstall_fnc = uninstall_projeto

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
        self.lay_repo.addWidget(self.button_repo)
        self.lay_executavel = QHBoxLayout()
        self.label5 = QLabel(u'Endereço do Executavel')
        self.le5 = QLineEdit()
        self.lay_executavel.addWidget(self.label5)
        self.lay_executavel.addWidget(self.le5)
        self.button_executavel = QPushButton("...")
        self.lay_executavel.addWidget(self.button_executavel)
        self.lay_config = QHBoxLayout()
        self.label6 = QLabel(u"Arquivos configuração")
        self.le6 = QLineEdit()
        self.lay_config.addWidget(self.label6)
        self.lay_config.addWidget(self.le6)
        self.button_config = QPushButton("...")
        self.lay_config.addWidget(self.button_config)
        self.lay1.addLayout(self.lay_nomeprod)
        self.lay1.addLayout(self.lay_tiporepo)
        self.lay1.addLayout(self.lay_dire)
        self.lay1.addLayout(self.lay_executavel)
        self.lay1.addLayout(self.lay_config)
        self.lay1.addLayout(self.lay_repo)

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
        def dialog_4():
            var_di = str(self.le6.text())
            dialog = QtWidgets.QFileDialog(self,u"Selecione os configs do Programa")
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
            #dialog.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
            directories=['']
            if dialog.exec_():
                directories = dialog.selectedFiles()
            self.le6.setText(str(self.le6.text()) + ('|' if str(self.le6.text())!='' else '')+ directories[0])
            return
        self.button_config.clicked.connect(dialog_4)
        def new_project():
            self.controlador.new_project(self.le1.text(),self.le3.text(),"1.0",self.le4.text().replace("\\","/"),self.le2.text().replace("\\","/"),self.le5.text().replace("\\","/"),self.le6.text().replace("\\","/").strip(" "))
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

        nome = " ".join(self.usuario_pc.split("."))
        self.tray_.setToolTip("Ola {0}, eu sou o UPDATER".format(nome))
        self.tray_.show()

    def fecha_tudo(self):
        self.tray_.hide()
        self.parentwindow.app.quit()

    def popula_tray(self):
        #força reabrir a conneccao
        db = QtSqlConnector.sgetDB("mysql")
        try:
            db.close()
        except:
            pass
        db.open()
        self.controlador.atualizar_list_programas()

        #Zera toda a tray
        self.ref_tray=[]
        self.lista_projetos = self.controlador.pegar_todos_projetos()
        self.menu_tray.clear()
        if self.controlador.dbg=='ON':
            self.controlador.gm.enviar_msg_("ATUALIZACAO INICIADA, tray limpa","JANELA_DEV")
        atualizar_reload = self.menu_tray.addAction(self.icon_refresh, "Atualizar Tray")
        self.menu_tray.addSeparator()
        abrir_new_project = self.menu_tray.addAction(self.icon_plus, "Adicionar Novo Projeto")
        atualizar_reload.triggered.connect(self.popula_tray)
        abrir_new_project.triggered.connect(self.janelanovoprojeto_fnc)

        #Adiciona SubMenu dos Projetos
        self.menu_tray.addSeparator()
        #self.menu_projetos = self.menu_tray.addMenu(self.icon_programs, "Projetos")


        for projeto in self.lista_projetos:
            ''' if self.controlador.dbg=='ON':
                warum = "Projeto adicionado na tray: " + projeto
                self.controlador.gm.enviar_msg_(warum,"JANELA_DEV")'''

            verifi = self.controlador.secretaria.tem_diferenca_projeto(projeto)

            if projeto not in self.controlador.list_programas.keys() and verifi==True:
                menu_ = self.menu_tray.addMenu(self.icon_white,projeto)
                action_ = menu_.addAction(self.icon_deploy,"Fazer Deploy")
                action_.setProperty("NAME",projeto)
                instar_ = menu_.addAction(self.icon_down,"Instalar ")
                instar_.setProperty("NAME",projeto)
                exclude_ = menu_.addAction(self.icon_config,"Editar/Excluir")

            elif projeto in self.controlador.list_programas.keys() and  verifi==True:
                menu_ = self.menu_tray.addMenu(self.icon_yellow,projeto)
                action_ = menu_.addAction(self.icon_deploy,"Fazer Deploy")
                action_.setProperty("NAME",projeto)
                instar_ = menu_.addAction(self.icon_run,"Executar")
                instar_.setProperty("NAME",projeto)
                exclude_ = menu_.addAction(self.icon_config,"Editar/Excluir")
                report_bug = menu_.addAction(self.icon_alert,"Reportar BUG")
                uninstall_ = menu_.addAction(self.icon_uninstall,"Desinstalar")
                uninstall_.setProperty("NAME",projeto)
                uninstall_.triggered.connect(self.uninstall_fnc)
            elif projeto not in self.controlador.list_programas.keys() and verifi==False:
                menu_ = self.menu_tray.addMenu(self.icon_white,projeto)
                action_ = menu_.addAction(self.icon_check,"Deploy Feito")
                action_.setProperty("NAME",projeto)
                instar_ = menu_.addAction(self.icon_down,"Instalar ")
                instar_.setProperty("NAME",projeto)
                exclude_ = menu_.addAction(self.icon_config,"Editar/Excluir")

            else:
                #menu_ = self.menu_projetos.addMenu(self.icon_green,projeto)
                menu_ = self.menu_tray.addMenu(self.icon_green,projeto)
                action_ = menu_.addAction(self.icon_check,"Deploy")
                action_.setProperty("NAME",projeto)
                instar_ = menu_.addAction(self.icon_run,"Executar")
                instar_.setProperty("NAME",projeto)
                exclude_ = menu_.addAction(self.icon_config,"Editar/Excluir")
                report_bug = menu_.addAction(self.icon_alert,"Reportar BUG")
                report_bug.setProperty("NAME",projeto)
                report_bug.triggered.connect(self.reportbug_fnc)
                uninstall_ = menu_.addAction(self.icon_uninstall,"Desinstalar")
                uninstall_.setProperty("NAME",projeto)
                uninstall_.triggered.connect(self.uninstall_fnc)


            #instar_ = menu_.addAction(self.icon_run,"Instalar/Executar")
            #exclude_ = menu_.addAction(self.icon_config,"Editar/Excluir")
            exclude_.setProperty("NAME",projeto)
            #instar_.hovered.connect(QToolTip.showText("TESTE"))

            self.ref_tray.append(menu_)
            action_.triggered.connect(self.predeploy_fnc)
            exclude_.triggered.connect(self.preedit_fnc)
            instar_.triggered.connect(self.instar_fnc)


        #Adciona QAction Saida do Sistema
        self.menu_tray.addSeparator()
        quit_action = QtWidgets.QAction("Sair",self)
        self.menu_tray.addAction(quit_action)
        quit_action.triggered.connect(self.fecha_tudo)


class janela_edicao(QtWidgets.QMainWindow):

    def __init__(self,app_,mainw):

        super(janela_edicao,self).__init__()
        self.parentwindow = mainw
        self.controlador = self.parentwindow.controlador

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
        self.lay_config2 = QHBoxLayout()
        self.label_config2 = QLabel(u"Arquivos configuração")
        self.le_config2 = QLineEdit()
        self.lay_config2.addWidget(self.label_config2)
        self.lay_config2.addWidget(self.le_config2)
        self.button_config2 = QPushButton("...")
        self.lay_config2.addWidget(self.button_config2)
        self.lay2.addLayout(self.lay_nomeprod2)
        self.lay2.addLayout(self.lay_tiporepo2)
        self.lay2.addLayout(self.lay_dire2)
        self.lay2.addLayout(self.lay_executavel2)
        self.lay2.addLayout(self.lay_config2)
        self.lay2.addLayout(self.lay_repo2)

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
        def dialog_4():
            dialog = QtWidgets.QFileDialog(self,u"Selecione os configs do Programa")
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
            directories=['']
            if dialog.exec_():
                directories = dialog.selectedFiles()
            self.le_config2.setText(str(self.le_config2.text()) + ('|' if str(self.le_config2.text())!='' else '')+ directories[0])
            return
        self.button_config2.clicked.connect(dialog_4)
        def atualizar_projeto():
            self.controlador.atualizar(self.le_nomeprod2.text(),self.le_dire2.text().replace("\\","/"),self.le_repo2.text().replace("\\","/"),self.le_tiporepo2.text().replace("\\","/"),self.le_executavel2.text().replace("\\","/"),self.le_config2.text().strip(" ").replace("\\","/"))
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


r1=QtSqlConnector(None,"MYSQL",{"host":"192.168.180.249","schema":"python","user":"root","password":"marisco"},nameConnection="mysql")
r2=QtSqlConnector(None,"SQLITE",{"db":":memory:"},nameConnection="memory")
app = QtWidgets.QApplication([])
app.setQuitOnLastWindowClosed(False)
x = tela_inicial(app)
app.exec_()