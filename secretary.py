# -*- coding: utf-8 -*-
import time
import datetime
import PyQt5.QtCore
from  PyQt5.QtCore import QObject
from PyQt5 import QtCore,QtWidgets, QtSql
from PyQt5.QtCore import Qt
import os
from entregador import wraper_de_diretorio
from controlador import *
from os import walk,stat

#Classes de Acesso ao DB
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

#Classe que arruma tudo no DB
class secretary(QObject):
    def __init__(self ,parent=None ,menssageiro_=None ,debug_='OFF' ,signalcontrol_=None ,app_=None):
        super(secretary,self).__init__(parent)
        self.gm = menssageiro_
        self.dbg = debug_
        self.sc = signalcontrol_
        self.eq_ = Easy_Query(QtSqlConnector.sgetDB("mysql"),menssageiro_=self.gm,debug_=self.dbg)
        self.app_ = app_
        self.entregador = wraper_de_diretorio(menssageiro_=self.gm ,debug_=self.dbg, signalcontrol_=self.sc,app_=self.app_)

    #Utilidade interna
    def data_agora(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    #Fornece informações pra TELA
    def get_all_projects(self):
        query_projetos = "Select * from python.updater_project_version ;"
        lista_projetos = self.eq_.Query_Result(query_projetos)
        return lista_projetos
    def get_project_info(self,nome_projeto):
        query_table_projeto = "select * from python.updater_project_version where projeto = '{0}' ;".format(nome_projeto)
        lista_dados_projeto = self.eq_.Query_Result(query_table_projeto)
        return lista_dados_projeto[0]

    def reportar_bug(self,nome_projeto,usuario,texto) :
		query_inserir_bug = u"REPLACE INTO python.updater_bugs VALUES ('{0}','{1}','{2}','{3}');".format(unicode(nome_projeto),unicode(self.data_agora()),unicode(usuario),unicode(texto))
		self.eq_.Query_no_Result(query_inserir_bug)

    #VERIFICA se projeto ja existe ou Faz o CADASTRO do projeto(NEW)
    def verifica_deploy(self,nome_projeto,parametros_projeto={}):
        #CADASTRA projeto
        if len(parametros_projeto)>0:
            parametros_projeto['DIRETORIO'] = parametros_projeto['DIRETORIO'].replace("\\","/")
            parametros_projeto['REPOSITORIO'] = parametros_projeto['REPOSITORIO'].replace("\\","/")
            parametros_projeto['EXECUTAVEL'] = parametros_projeto['EXECUTAVEL'].replace("\\","/")
            query_criacao1 = "REPLACE INTO python.updater_project_version VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}') ".format(unicode(nome_projeto),parametros_projeto['VERSAO'],parametros_projeto['DATAMOD'],unicode(parametros_projeto['DIRETORIO']),unicode(parametros_projeto['REPOSITORIO']),unicode(parametros_projeto['TIPOREPOSITORIO']),unicode(parametros_projeto['EXECUTAVEL']))
            self.eq_.Query_no_Result(query_criacao1)
            lista_files = self.entregador.getFiles(parametros_projeto['DIRETORIO'],[])
            #coloca no db
            query_criacao2 = "REPLACE INTO python.updater_files_version (projeto,file,datamod) values "
            for elemento in lista_files:
                query_criacao2 = query_criacao2 + unicode("('{0}','{1}','{2}'),").format(unicode(nome_projeto),unicode(elemento['FILE'].replace("\\","/")),elemento['DATEMODIFICATION'])
            query_criacao2 = query_criacao2[:-1] + ";"
            self.eq_.Query_no_Result(query_criacao2)
            return lista_files

        #VERIFICA se projeto ja existe
        else:
            #so recebi o nome .. verificar contra o bs
            query_verification = "select * from python.updater_project_version where projeto = '{0}' ;".format(nome_projeto)
            list_verification = self.eq_.Query_Result(query_verification)
            pasta_diretorio = list_verification[0]['DIRETORIO']
            pasta_repositorio = list_verification[0]['REPOSITORIO']
            #olha os arquivos no diretorio
            lista_files = self.entregador.getFiles(list_verification[0]['DIRETORIO'],[])
            #olha os arquivos no DB
            query_verification2 = "select * from python.updater_files_version where projeto = '{0}' ;".format(nome_projeto)
            list_verification2 = self.eq_.Query_Result(query_verification2)
            lista_files_nomes  = [x_['FILE'] for x_ in list_verification2]
            lista_arquivos_nodir = [x['FILE'] for x in lista_files]

            #deleta o que ta no repositorio mas nao esta no diretorio
            for y in lista_files_nomes:
                if y not in lista_arquivos_nodir:
                    query_deletar = u"delete from python.updater_files_version where file = '{0}' ;".format(unicode(y))
                    self.eq_.Query_no_Result(query_deletar)
                    end_rem_file = pasta_repositorio + unicode(y.replace(pasta_diretorio,""))
                    os.remove(unicode(end_rem_file))

            if len(list_verification)>0 :
                #procegue com  a logica de  verificacao
                #print lista_files

                index_lista_files =dict((x['DATEMODIFICATION']+x['FILE'],x) for x in  lista_files)
                index_list_verification2 = dict((str(x['DATAMOD'].toPyDateTime())+x['FILE'],x) for x in list_verification2)
                result_diff = set.difference(set(index_lista_files.keys()),set(index_list_verification2.keys()))
                return [index_lista_files[y] for y in result_diff ]

            else:
                #retorna false .. nao tem cadastro desse projeto
                print"NAO TEM"
                return False

    def tem_projeto(self,nome_projeto):
        query_verification = "select * from python.updater_project_version where projeto = '{0}' ;".format(nome_projeto)
        list_verification = self.eq_.Query_Result(query_verification)
        if len(list_verification)>0:
            return True
        else:
            return False
    def cadastra_projeto(self,nome_projeto,parametros_projeto={}):
        query_criacao1 = "REPLACE INTO python.updater_project_version VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}') ".format(unicode(nome_projeto),parametros_projeto['VERSAO'],parametros_projeto['DATAMOD'],unicode(parametros_projeto['DIRETORIO']),unicode(parametros_projeto['REPOSITORIO']),unicode(parametros_projeto['TIPOREPOSITORIO']),unicode(parametros_projeto['EXECUTAVEL']),unicode(parametros_projeto['CONFIG']))
        self.eq_.Query_no_Result(query_criacao1)
        lista_files_dir = self.entregador.getFiles(parametros_projeto['DIRETORIO'],[])
        lista_files_config = parametros_projeto['CONFIG'].split("|")
        lista_files_config = [x.replace(parametros_projeto['DIRETORIO'],"") for x in lista_files_config]
        #coloca no db
        query_criacao2 = "REPLACE INTO python.updater_files_version (projeto,file,datamod,tipo) values "
        for elemento in lista_files_dir:
            if elemento['FILE'] not in lista_files_config:
                query_criacao2 = query_criacao2 + unicode("('{0}','{1}','{2}','{3}'),").format(unicode(nome_projeto),unicode(elemento['FILE'].replace("\\","/")),elemento['DATEMODIFICATION'],u'normal')
            else:
                query_criacao2 = query_criacao2 + unicode("('{0}','{1}','{2}','{3}'),").format(unicode(nome_projeto),unicode(elemento['FILE'].replace("\\","/")),elemento['DATEMODIFICATION'],u'config')

        query_criacao2 = query_criacao2[:-1] + ";"
        self.eq_.Query_no_Result(query_criacao2)
        return lista_files_dir


    def tem_diferenca_projeto(self,nome_projeto):
        dict_dados_projeto = self.get_project_info(nome_projeto)
        pasta_diretorio = dict_dados_projeto['DIRETORIO']
        lista_files_dir =  self.entregador.getFiles(pasta_diretorio,[])
        query_files_repo = "select * from python.updater_files_version where projeto = '{0}' ;".format(nome_projeto)
        list_files_db = self.eq_.Query_Result(query_files_repo)

        index_lista_files_dir =dict((x['DATEMODIFICATION']+x['FILE'],x) for x in  lista_files_dir)
        index_list_files_db = dict((str(x['DATAMOD'].toPyDateTime())+x['FILE'],x) for x in list_files_db)
        result_diff  =  set.difference(set(index_lista_files_dir.keys()),set(index_list_files_db.keys()))
        dict_diff = [index_lista_files_dir[y] for y in result_diff ]

        if len(dict_diff)>0:
            print "teve mudanca no projeto"
            return True

        else:
            print "nao teve mudanca no projeto"
            return False

    def comparar_arquivos_projeto(self,nome_projeto):
        #pega dados do projeto e deixa facil de ler
        dict_dados_projeto = self.get_project_info(nome_projeto)
        pasta_diretorio = dict_dados_projeto['DIRETORIO']
        pasta_repositorio = dict_dados_projeto['REPOSITORIO']
        lista_files_dir =  self.entregador.getFiles(pasta_diretorio,[])

        query_files_repo = "select * from python.updater_files_version where projeto = '{0}' ;".format(nome_projeto)
        list_files_db = self.eq_.Query_Result(query_files_repo)

        #lista os arquivos mudados/novos
        index_lista_files_dir =dict((x['DATEMODIFICATION']+x['FILE'],x) for x in  lista_files_dir)
        index_list_files_db = dict((str(x['DATAMOD'].toPyDateTime())+x['FILE'],x) for x in list_files_db)
        result_diff = set.difference(set(index_lista_files_dir.keys()),set(index_list_files_db.keys()))
        dict_diff = [index_lista_files_dir[y] for y in result_diff ]

        #Tira do DB os arquivos que estao no DB mas nao estao no Diretorio
        lista_so_files_repo  = [x_['FILE'] for x_ in list_files_db]
        lista_so_files_dir = [x['FILE'] for x in lista_files_dir]
        for y in lista_so_files_repo:
            if y not in lista_so_files_dir:
                query_deletar = u"delete from python.updater_files_version where file = '{0}' ;".format(unicode(y))
                self.eq_.Query_no_Result(query_deletar)
                end_rem_file = pasta_repositorio + unicode(y)
                os.remove(unicode(end_rem_file))

        if len(dict_diff)>0:
            print "teve mudanca no projeto"
            return dict_diff

        else:
            print "nao teve mudanca no projeto"
            return []

    #Funcoes DEV oficializar deploy/edicao/exclusao de Projetos
    def registra_deploy(self,nome_projeto,lista_dict_dados=[]):
        #faz query dos dados do projeto
        query_table_projeto = "select * from python.updater_project_version where projeto = '{0}' ;".format(nome_projeto)
        lista_dados_projeto = self.eq_.Query_Result(query_table_projeto)
        nova_versao = float(lista_dados_projeto[0]['VERSAO'])+0.1
        #pega lista de files a serem mudados
        lista_files_mudados=self.verifica_deploy(nome_projeto)
        if len(lista_files_mudados)==0:
            return True
        #calcula nova data de modificacao do projeto
        data_mudanca =  self.data_agora()

        query_update1="REPLACE INTO python.updater_project_version  VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}') ;".format(unicode(nome_projeto) ,unicode(nova_versao) ,unicode(data_mudanca),unicode(lista_dados_projeto[0]['DIRETORIO']),unicode(lista_dados_projeto[0]['REPOSITORIO']),unicode(lista_dados_projeto[0]['TIPOREPOSITORIO']),unicode(lista_dados_projeto[0]['EXECUTAVEL']))
        self.eq_.Query_no_Result(query_update1)
        #faz a atualizacao da table update_files_version PARA CADA FILE
        query_update2 = "REPLACE INTO python.updater_files_version (projeto,file,datamod,tipo) values "

        for i in lista_files_mudados:
            query_update2= query_update2 + unicode("('{0}','{1}','{2}','{3}'),").format(nome_projeto,i['FILE'],i['DATEMODIFICATION'],'normal')
        #tira a virgula
        query_update2 = query_update2[:-1] + ";"
        if query_update2 != "REPLACE INTO python.updater_files_version (projeto,file,datamod) values;":
            self.eq_.Query_no_Result(query_update2)

        return True
    def modificar_dados_projeto(self,nome_projeto,diretorio,repositorio,tiporeposirotio,executavel,configs):
        query_atualizar = "UPDATE python.updater_project_version SET DIRETORIO ='{0}', REPOSITORIO='{1}',TIPOREPOSITORIO='{2}',EXECUTAVEL='{3}',LISTA_CONFIGS='{5}' WHERE PROJETO='{4}' ;".format(diretorio,repositorio,tiporeposirotio,executavel,nome_projeto,configs)
        self.eq_.Query_no_Result(query_atualizar)

    def excluir_so_db(self,nome_projeto):
        query_deletar_project='delete from python.updater_project_version where projeto="{0}";'.format(nome_projeto)
        query_deletar_files = "delete from python.updater_files_version where projeto='{0}';".format(nome_projeto)
        query_deletar_users = "delete from python.updater_users where projeto = '{0}' ;".format(nome_projeto)
        self.eq_.Query_no_Result(query_deletar_project)
        self.eq_.Query_no_Result(query_deletar_files)
        self.eq_.Query_no_Result(query_deletar_users)

    def atualizar_configs(self,nome_projeto,lista_configs):
        for x in lista_configs:
            if x != '':
                query_update2= "UPDATE python.updater_files_version SET TIPO='{0}' WHERE PROJETO ='{1}' AND FILE='{2}' ;".format('config',nome_projeto,x)
                self.eq_.Query_no_Result(query_update2)

    #Faz o shutil pro controlador
    def instalar_projeto(self,path_novo_projeto,path_updaterclient):
        lista_arquivos=self.entregador.getFiles(path_updaterclient,[])
        lista_files = [x['FILE'] for x in lista_arquivos]
        self.sc.setr_(len(lista_files))
        self.entregador.Update_files(lista_files,path_novo_projeto,path_updaterclient)

    #Pega dados dos programas instalados pelo usuario
    def autent_user(self,usuario):
        query_user = "select * from python.updater_users where nomepc = '{0}';".format(usuario)
        asdfasdf = self.eq_.Query_Result(query_user)
        dict_projeto = {}
        for x in asdfasdf:
            dict_projeto[x['PROJETO']] =  x['EXECUTAVEL']
        dict_projeto = dict((x['PROJETO'],x['EXECUTAVEL']) for x in asdfasdf)
        return dict_projeto

    def insert_projeto(self,usuario,nome_projeto,executavel,nome_user):
        query_inserir_programa = u"INSERT INTO python.updater_users VALUES ('{0}','{1}','{2}','{3}');".format(unicode(usuario),unicode(nome_projeto),unicode(executavel),unicode(nome_user))
        return self.eq_.Query_no_Result(query_inserir_programa)

    def uninstall_projeto(self,usuario,nome_projeto):
        query_deletar_projeto = u"DELETE FROM python.updater_users where NOMEPC = '{0}' and PROJETO = '{1}' ;".format(unicode(usuario),unicode(nome_projeto))
        return self.eq_.Query_no_Result(query_deletar_projeto)