# -*- coding: utf-8 -*-
import PyQt5.QtCore
from  PyQt5.QtCore import QObject
from PyQt5 import QtCore,QtWidgets, QtSql
from PyQt5.QtCore import Qt
from os import walk,stat
import datetime
import os
from controlador import *
import shutil

asdf='asdf'


class wraper_de_entrega(QObject):
    def __init__(self,parent=None, menssageiro_=None,debug_='OFF',signalcontrol_=None,app_ = None):
        super(wraper_de_entrega,self).__init__(parent)
        self.mytipe =""

    def sendFiles(self,lista_de_files,endereco_diretorio):
        print "sendFiles"

class wraper_de_diretorio(wraper_de_entrega):
    def __init__(self,parent=None, menssageiro_=None,debug_='OFF',signalcontrol_=None,app_ = None):
        super(wraper_de_diretorio,self).__init__(parent)
        self.gm=menssageiro_
        self.dbg=debug_
        self.sc =signalcontrol_
        self.mytipe="diretorio"
        self.app_=app_

    #faz uma lista dos arquivos na pasta instrucao_endereco
    def getFiles(self,instrucao_endereco,lista_saida=[]):
        instrucao_endereco=instrucao_endereco.replace("\\","/")
        for (dirpath, dirnames, filenames) in walk(instrucao_endereco):
            dirpath = dirpath.replace("\\","/")
            for subel in  [dirpath+ "/" +x  for x in filenames]:
                dicionario = {'FILE':subel.replace(instrucao_endereco,""),'DATEMODIFICATION':datetime.datetime.fromtimestamp(os.stat(subel).st_mtime).strftime('%Y-%m-%d %H:%M:%S')}
                lista_saida.append(dicionario)
        #entrega FILE do jeito certo ex: /.idea/misc.xml
        return lista_saida

    #faz o upload dos arquivos no deploy
    def sendFiles(self,lista_de_files,endereco_repositorio,endereco_origem=""):
        endereco_repositorio = endereco_repositorio.replace("\\","/")
        endereco_origem = endereco_origem.replace("\\","/")
        if self.dbg == 'ON':
            warum = " Inicio do UPLOAD de arquivos \n Endereco repositorio:{0} \n Endereco diretorio(origem):{1}".format(endereco_repositorio,endereco_origem)
            self.gm.enviar_msg_(warum,"sendFiles")

        for i in lista_de_files:
            i = i.replace("\\","/")
            endereco_repositorio_mod = endereco_repositorio + i
            endereco_diretorio_mod = endereco_origem +  i
            if not os.path.exists("/".join(endereco_repositorio_mod.split("/")[:-1])):
                os.makedirs("/".join(endereco_repositorio_mod.split("/")[:-1]))
            shutil.copy2(endereco_diretorio_mod,endereco_repositorio_mod)
            self.sc.incrementa_up_(1)
            self.sc.msg_up_("Uploading " + i)
            self.app_.processEvents()
        return True

    #envia os arquivos dada a pasta de origem e de destino com uma lista dos arquivos ja limpos
    def Update_files(self,lista_de_files,endereco_diretorio,pasta_repositorio):
        #lista_de_files é só o "/teste.py ou .idea/teste.py" NAO EH O PATH TOtal!!
        endereco_diretorio = endereco_diretorio.replace("\\","/")
        pasta_repositorio = pasta_repositorio.replace("\\","/")
        for i in lista_de_files:
            i = i.replace("\\","/")
            endereco_repositorio = pasta_repositorio + i
            endereco_diretorio_mod = endereco_diretorio +  i
            if not os.path.exists("/".join(endereco_diretorio_mod.split("/")[:-1])):
                os.makedirs("/".join(endereco_diretorio_mod.split("/")[:-1]))

            shutil.copy2(endereco_repositorio,endereco_diretorio_mod)
            self.sc.incrementa_(1)
            self.sc.msg("Copiando " + i)
            self.app_.processEvents()