import socket
import os
import getpass

class gestor_autenticador():

    def get_pc_name(self):
        return socket.gethostname()
nome=getpass.getuser()
nome = " ".join(nome.split("."))
print nome
