
# -*- coding: utf-8 -*-


import PyQt5.QtCore
from  PyQt5.QtCore import QObject
from PyQt5 import QtCore,QtWidgets, QtSql
from PyQt5.QtCore import Qt
from os import walk,stat
import os

import shutil



class delivery_files(QObject):

    def __init__(self, parent=None):
        super(delivery_files,self).__init__(parent)
        self.entregador_diretorio = wraper_de_diretorio()

    #mesma coisa que repositorio_base, so q ele consegue copiar para o repositorio
class wraper_de_entrega(QObject):

    def __init__(self,parent=None):
        super(wraper_de_entrega,self).__init__(parent)
        self.mytipe =""


    def sendFiles(self,lista_de_files,endereco_diretorio):
        print "sendFiles"

class wraper_de_diretorio(wraper_de_entrega):
    def __init__(self,parent=None):
        super(wraper_de_entrega,self).__init__(parent)
        self.mytipe="diretorio"

    def sendFiles(self,lista_de_files,endereco_repositorio,endereco_origem=""):

        endereco_repositorio = endereco_repositorio.replace("\\","/")
        endereco_origem = endereco_origem.replace("\\","/")

        for i in lista_de_files:

            i = i.replace("\\","/")
            #endereco_repositorio_mod = endereco_repositorio +  i.replace(endereco_origem.replace('\\','/'),"").replace(endereco_origem.replace('/','\\'),"")
            endereco_repositorio_mod = endereco_repositorio +  i.replace(endereco_origem,"")


            if "/".join(i.split("/")[:-1]) == "/".join(endereco_repositorio_mod.split("/")[:-1]) :
                print u"O endereço de origem e o repositório devem ser diferentes ... file {0} não foi copiado".format(i.split("/")[-1])
            else:

                if not os.path.exists("/".join(endereco_repositorio_mod.split("/")[:-1])):
                    os.makedirs("/".join(endereco_repositorio_mod.split("/")[:-1]))

                shutil.copy2(i,endereco_repositorio_mod)



        return True


#a=delivery_files()
#print a.entregador_diretorio.sendFiles(['C:/Users/arthur.sato/Desktop/KondorPythonProjects-master/BACKUP/config.txt'],'C:/Users/arthur.sato/Desktop')
