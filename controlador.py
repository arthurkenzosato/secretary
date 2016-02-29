# -*- coding: utf-8 -*-
import PyQt5.QtCore
from  PyQt5.QtCore import QObject
from PyQt5 import QtCore,QtWidgets, QtSql
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QProcess
from Configer import configer
from secretary import *
from entregador import *
from authenticator import *
import os,imp,sys,socket,getpass,shutil,errno,stat
import datetime

class gestor_de_log(QtCore.QObject):
    def main_is_frozen(self):
        return (hasattr(sys, "frozen") or # new py2exe
                hasattr(sys, "importers") # old py2exe
                or imp.is_frozen("__main__")) # tools/freeze
    def get_main_dir(self):
        if self.main_is_frozen():
            return os.path.dirname(sys.executable)
        return os.path.dirname(sys.argv[0])


    def __init__(self, obj_ = "/LOGS.txt",modo_op_=  "FILE",connect_print = False,parent=None, debug_ = 0):
        super(gestor_de_log, self).__init__(parent)

        self.user=socket.gethostname()
        self.diretorio = self.get_main_dir()


        self.obj_ = obj_
        self.modo_op_ = modo_op_
        self.debug = debug_

        if self.modo_op_=="CONSOLE" and connect_print:

            def append_(str_):
                self.obj_.append(str_)
                self.obj_.moveCursor(QtGui.QTextCursor.End)

            XStream.stdout().messageWritten.connect(append_)
            XStream.stderr().messageWritten.connect(append_)


    def escrever_log(self,msg_, sender,escopo_ = "Normal", fprint = True,cor=""):
        if self.user=="":
            self.user =self.get_pc_name()

        reload(sys)
        sys.setdefaultencoding("latin-1")

        hora_ = datetime.datetime.now()
        hora = hora_.strftime('%H:%M:%S')
        sender  = str(sender)




        if (self.debug==0 and (escopo_ =="DEBUG" or escopo_== "DEBUG_EXTRA")) or (self.debug==1 and escopo_=="DEBUG_EXTRA"):
            return

        if cor<>"":
            msg ='<font color="{0}">'.format(cor)+ "<b>"+sender+r"</b>"+ r"</font>" + " : "+hora+": "+ ('<font color="red">' if escopo_.upper()=="ERRO" else ('<font color="green">' if escopo_.upper()=="FUNCAO" else "")) + escopo_  + (r'</font>' if escopo_.upper()=="ERRO" or escopo_.upper()=="FUNCAO" else "")  +": "+ str(msg_)+ "\n"
        else:
            msg = "<b>"+sender+r"</b>"+" : "+hora+": "+ ('<font color="red">' if escopo_.upper()=="ERRO" else ('<font color="green">' if escopo_.upper()=="FUNCAO" else "")) + escopo_ + (r'</font>' if escopo_.upper()=="ERRO" or escopo_.upper()=="FUNCAO" else "") +": "+ str(msg_)+ "\n"



        if self.modo_op_ =="FILE":

            logs = open(self.diretorio +"/"+ self.obj_,'a')
            logs.write(msg)
            logs.close()

        if self.modo_op_ == "CONSOLE":
            self.obj_.append(msg)
            self.obj_.moveCursor(QtGui.QTextCursor.End)


        if fprint:
            print (msg)


    def set_debug(self,value_debug):
        self.debug = value_debug
class gestor_mensageiro(QtCore.QObject):

    mensagem_sn = QtCore.pyqtSignal(str, str, str,int)

    def enviar_msg_(self, msg_,sender , escopo_="Normal",debug_ = 0):

        self.mensagem_sn.emit(msg_, str(sender), escopo_, debug_)


    def __init__(self):
        super(gestor_mensageiro, self).__init__(parent=None)


class controlador(QObject):
    def __init__(self,parent=None,signalcontrol_=None,app_ = None,configer_=None):
        super(controlador,self).__init__(parent)
        self.app_ =app_
        self.sc = signalcontrol_
        self.cfg = configer_
        self.authenticator = gestor_autenticador()
        self.nome_pc = self.authenticator.get_pc_name()
        self.nome_user = getpass.getuser()

        self.user_diretorio = self.cfg.dictado["DIRETORIO"] # VEM O C:\\
        self.user_diretorio = self.user_diretorio.replace('\\','/')
        self.user_modo = self.cfg.dictado["MODO"] #VEM DEV OU CLIENT
        self.dbg = self.cfg.dictado["DEBUG"] #VEM ON OU OFF
        self.t_atuali = self.cfg.dictado["T_ATUALIZACAO"] #VEM EM ms
        self.t_atuali = int(self.t_atuali)
        self.gm= gestor_mensageiro()
        self.gl = gestor_de_log(obj_='logs.txt',modo_op_ = "FILE")
        def msg_(msg_, sender_, escopo_, debug_):
            self.gl.escrever_log(msg_,sender_,escopo_,debug_,"")
        self.gm.mensagem_sn.connect(msg_)
        self.gm.enviar_msg_("UPDATER INICIADO","CONTROLADOR")
        self.secretaria =secretary(self, menssageiro_ = self.gm, debug_=self.dbg,signalcontrol_=self.sc,app_=self.app_ )
        self.list_programas = self.secretaria.autent_user(self.nome_pc)
        self.entregador = wraper_de_diretorio(self, menssageiro_ = self.gm, debug_=self.dbg,signalcontrol_=self.sc,app_=self.app_ )

    #Utilidade interna
    def main_is_frozen(self):
        return (hasattr(sys, "frozen") or # new py2exe
                hasattr(sys, "importers") # old py2exe
                or imp.is_frozen("__main__")) # tools/freeze
    def get_main_dir(self):
        if self.main_is_frozen():
            return os.path.dirname(sys.executable)
        return os.path.dirname(sys.argv[0])

    #Fornece informacoes pra TELA
    def pegar_todos_projetos(self):
        lista =  self.secretaria.get_all_projects()
        return [x['PROJETO'] for x in lista]
    def pegar_dados_projeto(self,nomeproj):
        return self.secretaria.get_project_info(nomeproj)

    #Comandos TELA sem botao
    def atualizar_list_programas(self):
        self.list_programas = self.secretaria.autent_user(self.nome_pc)

    #Botoes TELA
    #exclui o projeto do db, tanto do project quanto do file
    def excluir(self,nome_projeto):
        self.secretaria.excluir_so_db(nome_projeto)
        #muda os dados em python.updater_project_version
    def atualizar(self,nome_projeto,diretorio,repositorio,tiporepositorio,executavel,configs):
        list_configs = configs.strip(" ").split("|")
        new_configs=[x.replace(diretorio ,"") for x in list_configs]
        self.secretaria.atualizar_configs(nome_projeto,new_configs)
        self.secretaria.modificar_dados_projeto(nome_projeto,diretorio,repositorio,tiporepositorio,executavel,new_configs)

    def reportar_bug(self,nome_projeto,usuario,text_descricao):
        self.secretaria.reportar_bug(nome_projeto,usuario,text_descricao)

    def deploy(self,nome_projeto):
        verifica = self.secretaria.tem_projeto(nome_projeto)
        if(verifica==False):
            print "projeto nao existe ainda"
            if self.dbg == 'ON':
                warum = "Tentativa de deploy, projeto nao existente no db: " + nome_projeto
                self.gm.enviar_msg_(warum,"Controlador")
            return False

        else:
            lista_files_modificados = self.secretaria.comparar_arquivos_projeto(nome_projeto)
            if len(lista_files_modificados)==0:
                print "Sem arquivos modificados"
                return True

            self.sc.setv_up_(0)
            self.sc.show_janela_up_()
            dados_projeto= self.secretaria.get_project_info(nome_projeto)
            lista_de_files = [x['FILE'] for x in lista_files_modificados]
            if len(lista_de_files)>0:
                self.sc.setr_up_(len(lista_de_files))
                verifi2 = self.entregador.sendFiles(lista_de_files, dados_projeto['REPOSITORIO'], dados_projeto['DIRETORIO'])
                self.sc.hide_janela_up_()
                if verifi2 == True:
                    self.secretaria.registra_deploy(nome_projeto)
                    self.secretaria.atualizar_configs(nome_projeto,dados_projeto['LISTA_CONFIGS'].split("|"))

                    if self.dbg == 'ON':
                        warum = "deploy feito com sucesso: " + nome_projeto
                        self.gm.enviar_msg_(warum,"Controlador")

                return True

            else:
                if self.dbg == 'ON':
                    warum = "Tentativa de deploy, sem nenhum arquivo modificado, projeto: " + nome_projeto
                    self.gm.enviar_msg_(warum,"Controlador")
                self.sc.hide_janela_up_()
                return True

    def new_project(self,nome_projeto,diretorio,versao,repositorio,tiporepositorio,executavel,configs):
        self.sc.setv_up_(0)
        self.sc.show_janela_up_()
        datamod = self.secretaria.data_agora()
        list_new_configs = configs.split('|')
        list_new_configs = [x.replace(diretorio,"") for x in list_new_configs]
        configs_limpo = "|".join(list_new_configs)
        lista_files_novos = self.secretaria.cadastra_projeto(nome_projeto,{'DIRETORIO':diretorio,'VERSAO':versao,'REPOSITORIO':repositorio,'TIPOREPOSITORIO':tiporepositorio,'DATAMOD':datamod,'EXECUTAVEL':executavel,'CONFIG':configs_limpo})
        lista_files_novos = [x['FILE'] for x in lista_files_novos]
        self.sc.setr_up_(len(lista_files_novos))
        if self.entregador.sendFiles(lista_files_novos, repositorio,diretorio) :
            print "projeto criado"
            if self.dbg == 'ON':
                warum = "Projeto criado: " + nome_projeto
                self.gm.enviar_msg_(warum,"Controlador")
        else:
            print u"Falha na criação do Projeto"
            if self.dbg == 'ON':
                warum = "Falha na criacao do Projeto: " + nome_projeto
                self.gm.enviar_msg_(warum,"Controlador")
        self.sc.hide_janela_up_()
        return True

    def instalar_executar_projeto(self,nome_projeto):
        #verifica se esse projeto ja foi instalado
        if nome_projeto not in self.list_programas.keys() :
            path_updater_projeto=self.instalar_programa(nome_projeto)
            self.secretaria.insert_projeto(self.nome_pc,nome_projeto,path_updater_projeto,self.nome_user)
            self.list_programas = self.secretaria.autent_user(self.nome_pc)
            self.executar_programa(path_updater_projeto,nome_projeto)
        else:
            path_exec=self.list_programas[nome_projeto]
            self.executar_programa(path_exec,nome_projeto)

    #faz o shutil do updater-client
    def instalar_programa(self,nome_projeto):
        #cria pasta do novo projeto
        self.sc.setv_(0)
        self.sc.show_janela_()
        path_pasta_install = self.user_diretorio + "/" + nome_projeto
        if not os.path.exists(path_pasta_install):
            os.makedirs(path_pasta_install)
        #envia o updater-client pra pasta do novo projeto
        self.secretaria.instalar_projeto(path_pasta_install,"Z:/TI/QtApps/NewUpdaterClient")
        #edita o config.txt
        path_config = path_pasta_install + "/config.txt"
        arquivo = open(path_config,'w')
        escrita = 'PROJETO|' + nome_projeto
        arquivo.write(escrita)
        arquivo.close()
        path_executavel_updater = path_pasta_install + "/Controlador.exe"
        self.sc.hide_janela_()
        return path_executavel_updater.replace("\\","/")

    def executar_programa(self,path_projeto,nome_projeto):
        self.gm.enviar_msg_("INICIANDO EXECUCAO "+ nome_projeto,"CONTROLADOR")
        process = QProcess()
        if process.startDetached(path_projeto):
            self.gm.enviar_msg_(u"Programa aberto com sucesso! "+ nome_projeto,"CONTROLADOR")
        else:
            self.gm.enviar_msg_(u"Programa não foi aberto com sucesso"+ nome_projeto,"CONTROLADOR")

    def uninstall_programa(self,nome_projeto):
        self.secretaria.uninstall_projeto(self.nome_pc,nome_projeto)
        path_programa = self.user_diretorio +"/"+nome_projeto
        #os.remove(unicode(path_programa))
        shutil.rmtree(path_programa, ignore_errors=False, onerror=self.handleRemoveReadonly)

    def handleRemoveReadonly(self,func, path, exc):
      excvalue = exc[1]
      if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
          os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
          func(path)
      else:
          raise