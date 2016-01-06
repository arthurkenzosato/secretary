# -*- coding: utf-8 -*-
import PyQt5.QtCore
from  PyQt5.QtCore import QObject
from PyQt5 import QtCore,QtWidgets, QtSql
from PyQt5.QtCore import Qt

from secretary import *
from entregador import *
import os,imp,sys
import datetime


class controlador(QObject):
    def __init__(self,parent=None):
        super(controlador,self).__init__(parent)
        self.secretaria =secretary(self)
        self.entregador = delivery_files(self)

    #Funcoes usadas por TELA e TELA2
    def pegar_todos_projetos(self):
        lista =  self.secretaria.get_all_projects()
        return [x['PROJETO'] for x in lista]
    def pegar_dados_projeto(self,nomeproj):
        return self.secretaria.get_project_info(nomeproj)
    def main_is_frozen(self):
        return (hasattr(sys, "frozen") or # new py2exe
                hasattr(sys, "importers") # old py2exe
                or imp.is_frozen("__main__")) # tools/freeze
    def get_main_dir(self):
        if self.main_is_frozen():
            return os.path.dirname(sys.executable)
        return os.path.dirname(sys.argv[0])

    #Funcoes usadas pela TELA2
    def excluir(self,nome_projeto):
        self.secretaria.excluir_so_db(nome_projeto)
    def atualizar(self,nome_projeto,diretorio,repositorio,tiporepositorio,executavel):
        self.secretaria.atualizar_dados_projeto(nome_projeto,diretorio,repositorio,tiporepositorio,executavel)

    #Funcoes usadas pela TELA
    def deploy(self,nome_projeto):
        verifica = self.secretaria.verifica_deploy(nome_projeto)
        if(verifica==False):
            print "projeto nao existe ainda"
            return False
        else:
            diretorio_projeto= self.secretaria.get_project_info(nome_projeto )
            lista_de_files = [x['PATH'] for x in verifica]
            #verifi2 = self.entregador.entregador_diretorio.sendFiles(lista_de_files, diretorio_projeto['DIRETORIO'])
            if len(lista_de_files)>0:
                verifi2 = self.entregador.entregador_diretorio.sendFiles(lista_de_files, diretorio_projeto['REPOSITORIO'], diretorio_projeto['DIRETORIO'])
            else:
                return True

            if verifi2 == True:
                self.secretaria.registra_deploy(nome_projeto)
                print "deploy feito com sucesso"
            return True
    def new_project(self,nome_projeto,diretorio,versao,repositorio,tiporepositorio,executavel):
        datamod = self.secretaria.data_agora()
        lista_files_novos = self.secretaria.verifica_deploy(nome_projeto,{'DIRETORIO':diretorio,'VERSAO':versao,'REPOSITORIO':repositorio,'TIPOREPOSITORIO':tiporepositorio,'DATAMOD':datamod,'EXECUTAVEL':executavel})

        lista_files_novos = [x['PATH'] for x in lista_files_novos]
        if self.entregador.entregador_diretorio.sendFiles(lista_files_novos, repositorio,diretorio) :
            print "projeto criado"
        else:
            print "Falha na criação do Projeto"

        return True


