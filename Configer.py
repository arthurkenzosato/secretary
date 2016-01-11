# -*- coding: utf-8 -*-

#a classe configer precisa ser inicializada com o path do seu txt

class configer():

    def __init__(self,path_txt):
        self.path_src = unicode(path_txt.replace("\\","/"))
        self.dictado = {}

    def read(self):
        leitura = open(self.path_src,'r')
        ler = leitura.read()
        lista_colunas=ler.split("\n")
        lista_colunas = lista_colunas #corrigir o fato que ele cria um elemento que eh so espaco
        self.dictado = {}
        for x in lista_colunas:
            key_value = x.split("|")
            if (x == '') :
                pass
            else:
                self.dictado.update({key_value[0].strip() : key_value[1].strip()})
            #self.listdict.append(dictado)
        print self.dictado
        leitura.close()

    #recebe um dict de dicts, faz o append no txt
    def write(self,dicts_dicts):
        arquivo = open(self.path_src,'a')
        escrita = ""
        for y in dicts_dicts.keys():
            escrita=escrita + y.strip() + "|" + dicts_dicts[y].strip() + "\n"

        arquivo.write(escrita)
        arquivo.close()
