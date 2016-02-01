# -*- coding: utf-8 -*-
import socket,os,getpass

class gestor_autenticador():

    def get_pc_name(self):
        return socket.gethostname()
    def get_pc_ip(self):
        return gethostbyname(gethostname())


nome=getpass.getuser()
nome = " ".join(nome.split("."))
print u"Olá "+unicode(nome)+ u" seu ip é:" + socket.gethostbyname(socket.gethostname())


