
# -*- coding: utf-8 -*-
import time
import datetime
#Formata o DATE do pc para o DATE do SQL

print(datetime.datetime.fromtimestamp(int("1284101485")).strftime('%Y-%m-%d %H:%M:%S'))
print time.localtime()
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

#codigo para gerar o time de agora:
time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())