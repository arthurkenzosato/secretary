# -*- coding: utf-8 -*-
from PyQt5 import QtCore,QtWidgets, QtSql
from PyQt5.QtWidgets import *
from QtCore import QObject
import sys,os,imp,shutil

def handleRemoveReadonly(func, path, exc):
      excvalue = exc[1]
      if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
          os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
          func(path)
      else:
          raise

path_teste = "C:/Users/arthur.sato/Desktop/pasta_kenzo/AtuViewer"
#os.remove(path_teste)
shutil.rmtree(path_teste, ignore_errors=False, onerror=handleRemoveReadonly)

