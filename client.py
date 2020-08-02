#coding:utf-8

import socket
import sys
import os
import random
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QFileDialog, QLineEdit, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork
import requests
import json
from PyQt5.QtCore import QByteArray

# reload(sys)
# sys.setdefaultencoding('utf-8')

class main_win(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 1000)
        self.wnd = QtWidgets.QWidget(MainWindow)
        self.wnd.setObjectName("wnd")
        self.response_text = QtWidgets.QTextEdit(self.wnd)
        self.response_text.setGeometry(QtCore.QRect(300, 400, 671, 351))
        self.response_text.setObjectName("response_text")
        self.response_text.setReadOnly(True)
        self.file_table = QtWidgets.QTableWidget(self.wnd)
        self.file_table.setGeometry(QtCore.QRect(20, 80, 951, 291))
        self.file_table.setObjectName("file_table")
        self.file_table.setColumnCount(4)
        self.file_table.setRowCount(0)
        self.file_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.file_table.setHorizontalHeaderLabels([u'合并编码',u'货物和劳务名称', u'商品和服务分类简称',u'说明'])
        
        self.layout_1 = QtWidgets.QWidget(self.wnd)
        self.layout_1.setGeometry(QtCore.QRect(20, 20, 951, 30))
        self.layout_1.setObjectName("layout_1")
        self.topbar_layout = QtWidgets.QHBoxLayout(self.layout_1)
        self.topbar_layout.setContentsMargins(0, 0, 0, 0)
        self.topbar_layout.setObjectName("topbar_layout")
        self.label_ip = QtWidgets.QLabel(self.layout_1)
        self.label_ip.setObjectName("label_ip")
        self.topbar_layout.addWidget(self.label_ip)
        self.input_ip = QtWidgets.QLineEdit(self.layout_1)
        self.input_ip.setObjectName("input_ip")
        self.topbar_layout.addWidget(self.input_ip)
        # 
        self.login_but = QtWidgets.QPushButton(self.layout_1)
        self.login_but.setObjectName("login_but")
        self.topbar_layout.addWidget(self.login_but)
        
        self.layout_2 = QtWidgets.QWidget(self.wnd)
        self.layout_2.setGeometry(QtCore.QRect(20, 400, 261, 321))
        self.layout_2.setObjectName("layout_2")
        self.grid_layout = QtWidgets.QGridLayout(self.layout_2)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setObjectName("grid_layout")
        self.grid_layout_2 = QtWidgets.QGridLayout()
        self.grid_layout_2.setObjectName("grid_layout_2")

        self.save_but = QtWidgets.QPushButton(self.layout_2)
        self.save_but.setObjectName("save_but")
        self.grid_layout_2.addWidget(self.save_but, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.wnd)

        self.rename_func(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def rename_func(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "tax project"))

        self.label_ip.setText(_translate("MainWindow", "product name"))
        self.login_but.setText(_translate("MainWindow", "search"))
        self.save_but.setText(_translate("MainWindow", "save"))





class client_func(QMainWindow):

    def __init__(self, ui:main_win):
        QMainWindow.__init__(self)
        self.ui = ui
        self.server_ip = "127.0.0.1"
        self.server_port = 8000
        self.init_ui()
        self.clickPos = ""
        self.data =  QtCore.QByteArray()


    def init_ui(self):
        self.ui.file_table.resizeColumnsToContents() 
        self.ui.login_but.clicked.connect(self.connect)
        self.ui.save_but.clicked.connect(self.insert)
        self.ui.file_table.verticalHeader().sectionClicked.connect(self.tableClick)#表头单击信号

        # self.ui.file_table.clicked.connect(self.func_test) 
        
    def tableClick(self,index):
        self.clickPos = index
        self.data = QtCore.QByteArray()

        self.data.append("code="+self.ui.file_table.item(self.clickPos,0).text()+"&")
        self.data.append("firstCategory="+self.ui.file_table.item(self.clickPos,1).text()+"&")
        self.data.append("secondCategory="+self.ui.file_table.item(self.clickPos,2).text()+"&")
        self.data.append("item="+str(self.ui.input_ip.text()))

    def print_msg(self, msg:str):
        if msg[-1] == '\r' or msg[-1] == '\n':
            msg = msg[:-1]
        self.ui.response_text.append(msg)

    def insert(self):
        try:

            url = "http://127.0.0.1:8000/insert"
            req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
            req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, 
                "application/x-www-form-urlencoded")

            self.nam = QtNetwork.QNetworkAccessManager()
            self.nam.finished.connect(self.handleResponsePost)
            self.nam.post(req, self.data)
 
        except:
            self.print_msg("Connection Error")

    def connect(self):
        try:
            url = "http://127.0.0.1:8000/search?productName="
            url +=  str(self.ui.input_ip.text())
            req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))


            self.nam = QtNetwork.QNetworkAccessManager()
            self.nam.finished.connect(self.handleResponse)
            self.nam.get(req)    
        except:
            self.print_msg("Connection Error")

    def handleResponsePost(self, reply):

        er = reply.error()

        if er == QtNetwork.QNetworkReply.NoError:

            bytes_string = reply.readAll()

            self.print_msg(json.loads(str(bytes_string, 'utf-8')).get("status"))

        else:
            print("Error occurred: ", er)
            print(reply.errorString())


    def handleResponse(self, reply):

        er = reply.error()

        if er == QtNetwork.QNetworkReply.NoError:

            bytes_string = reply.readAll()
            # print(str(bytes_string, 'utf-8'))
            self.print_msg(json.loads(str(bytes_string, 'utf-8')).get("status"))
            self.list(bytes_string)

        else:
            print("Error occured: ", er)
            print(reply.errorString())


    def list(self,jsonObj):

        t = json.loads(str(jsonObj, 'utf-8'))
        objList = t.get('objList')
        print(objList)
        print(type(objList))
        # print(t.get('objList'))

        self.ui.file_table.setRowCount(len(objList))
        for i, obj in enumerate(objList):
            newItem = QTableWidgetItem(str(obj.get('code')))
            self.ui.file_table.setItem(i, 0, newItem)
            newItem = QTableWidgetItem(str(obj.get('firstCategory')))
            self.ui.file_table.setItem(i, 1, newItem)
            newItem = QTableWidgetItem(str(obj.get('secondCategory')))
            self.ui.file_table.setItem(i, 2, newItem)
            newItem = QTableWidgetItem(str(obj.get('info')))
            self.ui.file_table.setItem(i, 3, newItem)
        self.ui.file_table.resizeColumnsToContents() 




    def quit(self):
        self.close()
        self.sk.send(bytes('QUIT' + '\r\n', encoding="utf-8"))
        self.recv_msg = str(self.sk.recv(8192), encoding="utf-8")[:-1]
        self.print_msg(self.recv_msg)
        self.sk.close()
        if self.datasocket is not None:
            self.datasocket.close()
        sys.exit(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = main_win()
    ui.setupUi(MainWindow)
    MainWindow.show()

    c = client_func(ui)
    sys.exit(app.exec_())
