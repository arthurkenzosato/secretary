# -*- coding: utf-8 -*-
from PyQt5 import QtCore,QtWidgets, QtSql
from PyQt5.QtWidgets import *
from QtCore import QObject
import sys,os,imp



class QtSqlConnector(QtCore.QObject):

    list_dbs={}
    def __init__(self,database=None,tipoDB="MYSQL",parconnections={},nameConnection ="default",parent=None, menssageiro_= None):
        super(QtSqlConnector, self).__init__(parent)

        self.gm  =menssageiro_
        if self.gm!=None:
            self.gm.enviar_msg_('Inicializando QtSqlConnector',str(self),"DEBUG")

        if database ==None:
            self.db = self.createConnection(tipoDB,nameConnection,parconnections)

        else:
            self.db = database
            try:
                self.db.open()
            except:
                pass


        QtSqlConnector.list_dbs[nameConnection]=self.db

    @staticmethod
    def sgetDB(name):
        if not name in QtSqlConnector.list_dbs:
            db=QtSql.QSqlDatabase.database(name)
            try:
                db.open()
            except:
                pass
            QtSqlConnector.list_dbs[name]=db
        else:
            db = QtSqlConnector.list_dbs[name]
        #warnings.warn(db.databaseName(),RuntimeWarning)
        return db

    @staticmethod
    def setDB(name,db):
        QtSqlConnector.list_dbs[name] = db

    def getDB(self,name='default',tipoDB='mysql'):

        if self.gm!=None:
            self.gm.enviar_msg_('Iniciando funcao getDB',str(self),"DEBUG")
        try:
            if not name in QtSqlConnector.list_dbs:
                db = self.createConnection(tipoDB,name,{})
                QtSqlConnector.list_dbs[name] =db
            else:
                return QtSqlConnector.list_dbs[name]
            return db
        except:
            if self.gm!=None:
                self.gm.enviar_msg_('Erro na funcao getDB '+str(sys.exc_info()[1]),str(self),"ERRO")
            else:
                pass

    def createConnection(self,tipoDB='MYSQL',name='default',parametros={}):
        if self.gm!=None:
            self.gm.enviar_msg_('Criando conexao com MYSQL',str(self),"DEBUG")
        c_name = name if name !="default" else tipoDB.lower()
        nameConnection=name

        db=QtSql.QSqlDatabase.database(c_name)
        if not db.isValid():
            if tipoDB=="MYSQL":
                if len(parametros)>0:
                    db=QtSql.QSqlDatabase.addDatabase("QMYSQL","mysql" if nameConnection=="default" else nameConnection)
                    db.setHostName(parametros["host"])
                    db.setDatabaseName(parametros["schema"])
                    db.setUserName(parametros["user"])
                    db.setPassword(parametros["password"])
                else:
                    db=QtSql.QSqlDatabase.addDatabase("QMYSQL","mysql" if nameConnection=="default" else nameConnection)
                    db.setHostName("192.168.180.249")
                    db.setDatabaseName("python")
                    db.setUserName("root")
                    db.setPassword("marisco")
            else:
                if len(parametros)>0:
                    db=QtSql.QSqlDatabase.addDatabase("QSQLITE","sqlite" if nameConnection=="default" else nameConnection)
                    db.setDatabaseName(parametros["db"])
                else:
                    db=QtSql.QSqlDatabase.addDatabase("QSQLITE","sqlite" if nameConnection=="default" else nameConnection)
                    db.setDatabaseName(":memory:")

        try:
            db.open()
        except:
            if self.gm!=None:
                self.gm.enviar_msg_('Erro na abertura da Conexao'+str(sys.exc_info()[1]),str(self),"ERRO")
            pass
        return db

    def __del__(self):
        try:
            self.db.close()
        except:
            if self.gm!=None:
                self.gm.enviar_msg_('Erro no fechamento da Conexao'+str(sys.exc_info()[1]),str(self),"ERRO")

            pass
class Easy_Query(QObject):

    mensagem_ = QtCore.pyqtSignal(str)

    def  __init__(self,mysqldatabase, parent=None,menssageiro_=None, sender_ ="",debug_ = 'OFF'):
        super(Easy_Query,self).__init__(parent)

        self.gm  = menssageiro_
        self.dbg = debug_
        self.sender_=sender_
        #self.gm.enviar_msg_('Inicializando Easy_Query',self.sender,"DEBUG")


        self.mysql =mysqldatabase
        self.types={}

        try:
            self.mysql.open()
        except:
            #self.gm.enviar_msg_('Erro na abertura da conexao '+str(sys.exc_info()[1]),self.sender_,"ERRO")
            pass

    def Query_no_Result(self,query_):
        #self.gm.enviar_msg_('Iniciando funcao Query_no_Result com a Query: {0}'.format(query_),self.sender_,"DEBUG")
        query=QtSql.QSqlQuery(self.mysql)

        mquery = query_.split(";")

        for q_ in mquery:
            query.prepare(q_)


            if not query.exec_():
                print query.lastError().text()
                #print u"Erro na execução da query : " + q_
                self.mensagem_.emit(u"Erro na execucao da query : " + q_)
                if self.dbg == 'ON':
                    warum = "Erro na execucao da query: " + q_
                    self.gm.enviar_msg_(warum,"Easy_Query")
                #self.gm.enviar_msg_('Erro na execucao da Query, '+query.lastError().text(),self.sender_,"ERRO")
            else:
                if self.dbg == 'ON':
                    warum = "Query executada: " + q_
                    self.gm.enviar_msg_(warum,"Easy_Query")
        return 1

    def Query_Result(self,query_,column_types={},auto=[]):
        #self.gm.enviar_msg_('Iniciando funcao Query_Result com a Query: {0}'.format(query_),self.sender_,"DEBUG")

        respo=[]
        query=QtSql.QSqlQuery(self.mysql)
        query.prepare(query_)


        if not query.exec_():
            #warnings.warn(query.lastError().text())
            #print query.lastError().text()
            #print "Erro na execução da query : " + query_
            self.mensagem_.emit("Erro na execução da query : " + query_)
            if self.dbg == 'ON':
                warum = "Erro na execucao da query: " + query_
                self.gm.enviar_msg_(warum,"Easy_Query")
            #self.gm.enviar_msg_('Erro na execucao da Query, '+query.lastError().text(),self.sender_,"ERRO")
        else:
            if self.dbg == 'ON':
                warum = "Query executada: " + query_
                self.gm.enviar_msg_(warum,"Easy_Query")


        rec = query.record()

        fields={}

        col_n=rec.count()

        for i in range(col_n):
            fields[i]=str(rec.fieldName(i)).upper()

        def converte_qvariant(key,value,col_types):

            if key.upper() in col_types.keys():
                if col_types[key].upper()=="STRING":
                    return unicode(value)
                elif col_types[key].upper()=="INT":
                    return int(value)
                elif col_types[key].upper()=="DOUBLE":
                    return float(value)
                elif col_types[key].upper()=="BOOL":
                    return int(value)
                elif col_types[key].upper()=="DATE":
                    return value.toString("yyyy-MM-dd")
                else:
                    return value
            else:
                if type(value)==QtCore.QDate:
                    if not key in self.types:
                        self.types[key]="DATE"
                    return value.toString("yyyy-MM-dd")
                else:
                    if not key in self.types:
                        if type(value)==str or type(value) == unicode :
                            self.types[key]="TEXT"
                        else:
                            self.types[key]="REAL"
                    return value
                    '''
                    if value.replace(".","").replace("-","").replace(",","").replace("(","").replace(")","").isdigit():
                        return float(value)
                    else:
                        return value
                    '''
        if len(auto)>0 and len(column_types)==0:
            query_2=QtSql.QSqlQuery(self.mysql)
            if len(auto)==1:
                metaquery= "select column_name,data_type from information_schema.columns where table_name='{0}'".format(auto[0])
            else:
                metaquery= "select column_name,data_type from information_schema.columns where table_name='{0}' and table_schema='{1}'".format(auto[0],auto[1])

            query_2.prepare(metaquery)
            if not query_2.exec_():
                print query_2.lastError().text()
                #print "Erro na execução da query de metadata  : " + metaquery
                self.mensagem_.emit("Erro na execução da query de metadata: " + metaquery)

                self.gm.enviar_msg_('Erro na execucao da Query de metadata: {0}, erro: {1} '.format(metaquery, str(sys.exc_info()[1])),self.sender_,"ERRO")

            column_types={}

            def colum_selector(col):
                if col.upper() in ["VARCHAR","TEXT","STRING"]:
                    return "STRING"
                elif col.upper() in ["INT","INTEGER"]:
                    return "INT"
                elif col.upper() in ["DOUBLE","FLOAT"]:
                    return "DOUBLE"
                elif col.upper() in ["BOOL","BOOLEAN"]:
                    return "BOOL"
                elif col.upper() in ["DATE"]:
                    return "DATE"
                else:
                    return "STRING"


            while query_2.next():
                column_types[str(query_2.value(0)).upper()]=colum_selector(str(query_2.value(1))).upper()


        while query.next():
            ll={}
            for k in range(col_n):
               ll[fields[k].upper()]=converte_qvariant(fields[k].upper(),query.value(k),column_types)
            respo.append(ll)

        return respo

r1=QtSqlConnector(None,"MYSQL",{"host":"192.168.180.249","schema":"python","user":"root","password":"marisco"},nameConnection="mysql")
r2=QtSqlConnector(None,"SQLITE",{"db":":memory:"},nameConnection="memory")

eq_ = Easy_Query(QtSqlConnector.sgetDB("mysql"))
lista_ = eq_.Query_Result("select * from python.updater_users ;")
print lista_

class tela_cliente(QtWidgets.QMainWindow):
    def __init__(self,app_,mainw,signalcontrol_):
        super(tela_cliente,self).__init__()
        self.parentwindow = mainw
        self.sc = signalcontrol_
        self.controlador = controlador(signalcontrol_= self.sc,app_=self.parentwindow.app,configer_=self.parentwindow.cfg)
        #setando icone da tray
        icon_path =self.controlador.get_main_dir() + "/im/suits_icon.png"
        icon = QtGui.QIcon(icon_path)
        self.tray_cliente = QtWidgets.QSystemTrayIcon(icon)
        self.menu_tray = QtWidgets.QMenu()
        self.tray_cliente.setContextMenu(self.menu_tray)
        nome=getpass.getuser()
        nome = " ".join(nome.split("."))
        self.tray_cliente.setToolTip("Ola {0}, eu sou o UPDATER".format(nome))
        self.tray_cliente.show()

        #acrescentar funcao de abrir programa
        def abrir_progama():
            objeto_ = self.sender()
            nome =objeto_.property("NAME")
            self.controlador.instalar_executar_projeto(nome)
        self.abrirprograma_fnc = abrir_progama
        self.popula_tray()


    def fecha_tudo(self):
        self.tray_cliente.hide()
        self.parentwindow.app.quit()

    def popula_tray(self):
        #Zera toda a tray
        self.ref_tray=[]
        self.lista_projetos = self.controlador.pegar_todos_projetos()
        self.menu_tray.clear()
        if self.controlador.dbg=='ON':
            self.controlador.gm.enviar_msg_("ATUALIZACAO INICIADA, tray limpa","JANELA_CLIENT")
        #Adiciona QAction do novo projeto
        #abrir_new_project.triggered.connect(self.janelanovoprojeto_fnc)
        #Adiciona SubMenu dos Projetos
        #self.menu_tray.addSeparator()
        atualizar_reload = QtWidgets.QAction("Atualizar Tray",self)
        self.menu_tray.addAction(atualizar_reload)
        atualizar_reload.triggered.connect(self.popula_tray)
        self.menu_projetos = self.menu_tray.addMenu("Projetos")

        for projeto in self.lista_projetos:
            if self.controlador.dbg=='ON':
                warum = "Projeto adicionado na tray: " + projeto
                self.controlador.gm.enviar_msg_(warum,"JANELA_CLIENT")

            aba_project = QtWidgets.QAction(projeto,self)
            aba_project.setProperty("NAME",projeto)
            self.ref_tray.append(aba_project)
            self.menu_projetos.addAction(aba_project)
            aba_project.triggered.connect(self.abrirprograma_fnc)
        #Adciona QAction Saida do Sistema
        self.menu_tray.addSeparator()
        quit_action = QtWidgets.QAction("Sair",self)
        self.menu_tray.addAction(quit_action)
        quit_action.triggered.connect(self.fecha_tudo)
