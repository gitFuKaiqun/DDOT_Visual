__author__ = 'Kaiqun'

import pyodbc
import os

def connector():
	ConnInfo = open(os.path.dirname(os.path.realpath(__file__)) + '/res/DBconn', 'r').readline()
	ConnStr = 'DRIVER={SQL Server};SERVER=' + ConnInfo.split('|')[0] + ';DATABASE=' + ConnInfo.split('|')[1] + ';UID=' + ConnInfo.split('|')[2] + ';PWD=' + ConnInfo.split('|')[3]
	return pyodbc.connect(ConnStr)