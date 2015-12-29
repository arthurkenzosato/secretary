# -*- coding: utf-8 -*-
import time
import datetime


import PyQt5.QtCore
from  PyQt5.QtCore import QObject
from PyQt5 import QtCore,QtWidgets, QtSql
from PyQt5.QtCore import Qt

import os
from os import walk,stat

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

    def  __init__(self,mysqldatabase, parent=None,menssageiro_=None, sender_ =""):
        super(Easy_Query,self).__init__(parent)

        self.gm  =menssageiro_

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

                #self.gm.enviar_msg_('Erro na execucao da Query, '+query.lastError().text(),self.sender_,"ERRO")
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
            #self.gm.enviar_msg_('Erro na execucao da Query, '+query.lastError().text(),self.sender_,"ERRO")


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

class secretary(QObject):

    def data_agora(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


    def __init__(self,parent=None):
        super(secretary,self).__init__(parent)

        self.eq_ =Easy_Query(QtSqlConnector.sgetDB("mysql"))
        self.repo =respositorio_diretorio(self)

    def get_project_info(self,nome_projeto):
        query_table_projeto = "select * from python.updater_project_version where projeto = '{0}' ;".format(nome_projeto)
        lista_dados_projeto = self.eq_.Query_Result(query_table_projeto)
        return lista_dados_projeto[0]


    #parametros_projeto -> parametros_projeto
    #{'VERSAO':'11234','DATAMOD':'2015-11-11 16:04:51','DIRETORIO':'C:\Users/User/Desktop/KondorPythonProjects-master/BACKUP','REPOSITORIO':'C:\Users\User\Desktop\KondorPythonProjects-master\BACKUP','TIPOREPOSITORIO':'ASDF'},{'projeto':'testando_registra_deploy','file':'arquivo1','datamod':'2015-12-15 17:23:51'},{'projeto':'testando_registra_deploy','file':'arquivo2','datamod':'2015-12-15 17:23:51'},{'projeto':'testando_registra_deploy','file':'arquivo3','datamod':'2015-12-15 17:23:51'}

    def verifica_deploy(self,nome_projeto,parametros_projeto={}):

        if len(parametros_projeto)>0:

            #primeiro acesso cadastrar no bd
            parametros_projeto['DIRETORIO'] = parametros_projeto['DIRETORIO'].replace("\\","/")
            parametros_projeto['REPOSITORIO'] = parametros_projeto['REPOSITORIO'].replace("\\","/")
            parametros_projeto['EXECUTAVEL'] = parametros_projeto['EXECUTAVEL'].replace("\\","/")

            query_criacao1 = "REPLACE INTO python.updater_project_version VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}') ".format(unicode(nome_projeto),parametros_projeto['VERSAO'],parametros_projeto['DATAMOD'],unicode(parametros_projeto['DIRETORIO']),unicode(parametros_projeto['REPOSITORIO']),unicode(parametros_projeto['TIPOREPOSITORIO']),unicode(parametros_projeto['EXECUTAVEL']))
            self.eq_.Query_no_Result(query_criacao1)

            lista_files = self.repo.getFiles(parametros_projeto['DIRETORIO'])
            query_criacao2 = "REPLACE INTO python.updater_files_version (projeto,file,datamod) values "
            for elemento in lista_files:
                query_criacao2 = query_criacao2 + unicode("('{0}','{1}','{2}'),").format(unicode(nome_projeto),unicode(elemento['PATH'].replace("\\","/")),elemento['DATEMODIFICATION'])
            query_criacao2 = query_criacao2[:-1] + ";"
            self.eq_.Query_no_Result(query_criacao2)

            return lista_files

        else:
            #so recebi o nome .. verificar contra o bs
            query_verification = "select * from python.updater_project_version where projeto = '{0}' ;".format(nome_projeto)
            list_verification = self.eq_.Query_Result(query_verification)
            pasta_diretorio = list_verification[0]['DIRETORIO']
            pasta_repositorio = list_verification[0]['REPOSITORIO']
            #olha os arquivos no diretorio
            lista_files = self.repo.getFiles(list_verification[0]['DIRETORIO'])
            #olha os arquivos no db
            query_verification2 = "select * from python.updater_files_version where projeto = '{0}' ;".format(nome_projeto)
            list_verification2 = self.eq_.Query_Result(query_verification2)
            lista_files_nomes  = [x_['FILE'] for x_ in list_verification2]
            lista_arquivos_nodir = [x['PATH'] for x in lista_files]
            #deleta o que ta no repositorio mas nao esta no diretorio
            for y in lista_files_nomes:
                if y not in lista_arquivos_nodir:
                    query_deletar = u"delete from python.updater_files_version where file = '{0}' ;".format(unicode(y))
                    self.eq_.Query_no_Result(query_deletar)
                    end_rem_file = pasta_repositorio + unicode(y.replace(pasta_diretorio,""))
                    os.remove(unicode(end_rem_file))


            if len(list_verification)>0 :
                #procegue com  amlogica de  verificacao
                #print lista_files

                lista_dict_modificar=[]
                lista_files_modificar=[]



                for x in lista_files:
                    for y in list_verification2:
                        if((datetime.datetime.strptime(x['DATEMODIFICATION'],'%Y-%m-%d %H:%M:%S')>y['DATAMOD'].toPyDateTime() and x['PATH']==y['FILE']) or (x['PATH'] not in lista_files_nomes and x['PATH'] not in lista_files_modificar)):
                            #substitui
                            #query_substituicao = " python.updater_files_version where projeto = '{0}'".format()
                            lista_dict_modificar.append(x)
                            lista_files_modificar.append(x['PATH'])



                return lista_dict_modificar
            else:
                #retorna false .. nao tem cadastro desse projeto
                print"NAO TEM"
                return False

    def registra_deploy(self,nome_projeto,lista_dict_dados=[]):
        #faz query dos dados do projeto
        query_table_projeto = "select * from python.updater_project_version where projeto = '{0}' ;".format(nome_projeto)
        lista_dados_projeto = self.eq_.Query_Result(query_table_projeto)

        # atualiza versao
        nova_versao = float(lista_dados_projeto[0]['VERSAO'])+0.1

        #pega lista de files a serem mudados
        lista_files_mudados=self.verifica_deploy(nome_projeto)
        if len(lista_files_mudados)==0:
            return True

        #calcula nova data de modificacao do projeto
        data_mudanca =  self.data_agora()

        #faz a atualizacao da table update_project_version
        query_update1="REPLACE INTO python.updater_project_version  VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}') ;".format(unicode(nome_projeto) ,unicode(nova_versao) ,unicode(data_mudanca),unicode(lista_dados_projeto[0]['DIRETORIO']),unicode(lista_dados_projeto[0]['REPOSITORIO']),unicode(lista_dados_projeto[0]['TIPOREPOSITORIO']),unicode(lista_dados_projeto[0]['EXECUTAVEL']))
        self.eq_.Query_no_Result(query_update1)

        #faz a atualizacao da table update_files_version PARA CADA FILE
        query_update2 = "REPLACE INTO python.updater_files_version (projeto,file,datamod) values "
        for i in lista_files_mudados:
            query_update2= query_update2 + unicode("('{0}','{1}','{2}'),").format(nome_projeto,i['PATH'],i['DATEMODIFICATION'])

        query_update2 = query_update2[:-1] + ";"

        if query_update2 != "REPLACE INTO python.updater_files_version (projeto,file,datamod) values;":
            self.eq_.Query_no_Result(query_update2)

        return True

    def get_all_projects(self):
        query_projetos = "Select * from python.updater_project_version ;"
        lista_projetos = self.eq_.Query_Result(query_projetos)
        return lista_projetos
class repositorio_base(QObject):

    def __init__(self,parent=None):
        super(repositorio_base,self).__init__(parent)
        self.mytipe =""

    def getFiles(self,instrucao_endereco):
        print "getFiles"

    def sendFiles(self,instrucao_endereco):
        print "sendFiles"

class respositorio_diretorio(repositorio_base) :


    def __init__(self,parent=None):
        super(respositorio_diretorio,self).__init__(parent)
        self.mytipe="diretorio"

    def getFiles(self,instrucao_endereco,lista_saida=[]):
        lista_saida = []
        #{"PATH":'C:/Users/User/Desktop/KondorPythonProjects-master/BACKUP/backup.png',"DATACREATION":"2012-01-01",,"DATAMODIFICATION":"2012-01-01"}
        for (dirpath, dirnames, filenames) in walk(instrucao_endereco):

            dirpath = dirpath.replace("\\","/")
            for subel in  [dirpath+"/"+x  for x in filenames]:
                dicionario = {'PATH':subel,'DATEMODIFICATION':datetime.datetime.fromtimestamp(os.stat(subel).st_mtime).strftime('%Y-%m-%d %H:%M:%S')}
                lista_saida.append(dicionario)

        #[datetime.datetime.fromtimestamp(os.stat(y).st_mtime).strftime('%Y-%m-%d %H:%M:%S') for y in lista_saida]
        return lista_saida








#a1 = respositorio_diretorio()


r1=QtSqlConnector(None,"MYSQL",{"host":"192.168.180.249","schema":"python","user":"root","password":"marisco"},nameConnection="mysql")
r2=QtSqlConnector(None,"SQLITE",{"db":":memory:"},nameConnection="memory")