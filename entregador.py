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


#mesma coisa que repositorio_base, so q ele consegue copiar para o repositorio
class delivery_files(QObject):
    def __init__(self, parent=None,menssageiro_=None,debug_='OFF'):
        super(delivery_files,self).__init__(parent)
        self.gm = menssageiro_
        self.dbg = debug_
        self.entregador_diretorio = wraper_de_diretorio(menssageiro_=self.gm,debug_=self.dbg)



class wraper_de_entrega(QObject):

    def __init__(self,parent=None, menssageiro_=None,debug_='OFF'):
        super(wraper_de_entrega,self).__init__(parent)
        self.mytipe =""

    def sendFiles(self,lista_de_files,endereco_diretorio):
        print "sendFiles"
class wraper_de_diretorio(wraper_de_entrega):
    def __init__(self,parent=None, menssageiro_=None,debug_='OFF'):
        super(wraper_de_diretorio,self).__init__(parent)
        self.gm=menssageiro_
        self.dbg=debug_
        self.mytipe="diretorio"

    def getFiles(self,instrucao_endereco,lista_saida=[]):
        instrucao_endereco=instrucao_endereco.replace("\\","/")
        for (dirpath, dirnames, filenames) in walk(instrucao_endereco):
            dirpath = dirpath.replace("\\","/")
            for subel in  [dirpath+ "/" +x  for x in filenames]:
                dicionario = {'FILE':subel.replace(instrucao_endereco,""),'DATEMODIFICATION':datetime.datetime.fromtimestamp(os.stat(subel).st_mtime).strftime('%Y-%m-%d %H:%M:%S')}
                lista_saida.append(dicionario)
        #entrega FILE do jeito certo ex: /.idea/misc.xml
        return lista_saida

    def sendFiles(self,lista_de_files,endereco_repositorio,endereco_origem=""):

        endereco_repositorio = endereco_repositorio.replace("\\","/")
        endereco_origem = endereco_origem.replace("\\","/")
        if self.dbg == 'ON':
            warum = " Inicio do envio de arquivos \n Endereco repositorio:{0} \n Endereco diretorio(origem):{1}".format(endereco_repositorio,endereco_origem)
            self.gm.enviar_msg_(warum,"sendFiles")

        for i in lista_de_files:
            i = i.replace("\\","/")
            endereco_repositorio_mod = endereco_repositorio +  i.replace(endereco_origem,"")

            if "/".join(i.split("/")[:-1]) == "/".join(endereco_repositorio_mod.split("/")[:-1]) :
                warum = u"O endereço de origem e o repositório devem ser diferentes ... file {0} não foi copiado".format(i.split("/")[-1])
                print warum
                if self.dbg == 'ON':
                    self.gm.enviar_msg_(warum,"sendFiles")
            else:
                if not os.path.exists("/".join(endereco_repositorio_mod.split("/")[:-1])):
                    os.makedirs("/".join(endereco_repositorio_mod.split("/")[:-1]))
                    if self.dbg == 'ON':
                        warum = "criou o diretorio {0}".format("/".join(endereco_repositorio_mod.split("/")[:-1]))
                        self.gm.enviar_msg_(warum,"sendFiles")

                shutil.copy2(i,endereco_repositorio_mod)
                if self.dbg == 'ON':
                    warum = "copiou o arquivo {0}".format(i)
                    self.gm.enviar_msg_(warum,"sendFiles")

        return True

    #envia os arquivos dada a pasta de origem e de destino com uma lista dos arquivos ja limpos
    def Update_files(self,lista_de_files,endereco_diretorio,pasta_repositorio):
        #lista_de_files é só o "/teste.py ou .idea/teste.py" NAO EH O PATH TOtal!!
        for i in lista_de_files:
            i = i.replace("\\","/")
            endereco_repositorio = pasta_repositorio + i
            endereco_diretorio_mod = endereco_diretorio +  i


            if not os.path.exists("/".join(endereco_diretorio_mod.split("/")[:-1])):
                os.makedirs("/".join(endereco_diretorio_mod.split("/")[:-1]))

            shutil.copy2(endereco_repositorio,endereco_diretorio_mod)