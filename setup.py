from distutils.core import setup
import py2exe
import os,os.path
import sys
#from C:\Users\felipe.kuratomi\.PyCharm40\system\python_stubs\-762174762\numpy import *
#from pykondoraux.RPCClient import *
import numpy
#import enum

sys.setrecursionlimit(5000)

datafiles = [("platforms", ["C:\\Python27\\Lib\\site-packages\\PyQt5\\plugins" +
                            "\\platforms\\qwindows.dll"]),
				("sqldrivers",["C:\\Python27\\Lib\\site-packages\\PyQt5\\plugins\\sqldrivers\\qsqlmysql.dll"])]



#includess=['PyQt5','PyQt5.QtWidgets', 'PyQt5.QtSql','PyQt5.QtWebKitWidgets']
includess=['PyQt5','PyQt5.QtWidgets', 'PyQt5.QtSql','PyQt5.QtWebKit','PyQt5.QtPrintSupport']


setup(data_files=datafiles,windows=[{"script" : 'C:\\py_workspace\\KondorPythonProjects\\Updater-dev\\Updater-dev.py'}], options={"py2exe" : {"skip_archive": True,"includes" : includess ,"packages":["MySQLdb"],"ascii": 0}})

