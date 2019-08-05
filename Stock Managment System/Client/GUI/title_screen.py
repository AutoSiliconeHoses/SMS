import sys, time, string, os, yaml
import socket
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
sys.path.append("Client")
import client
from GUI.configwindow import Config_Window

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        MainWindow = QtWidgets.QMainWindow()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(242, 361)
        MainWindow.setStyleSheet("background-color: rgb(49, 49, 49);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")

        self.btn_run = QtWidgets.QPushButton(self.centralwidget)
        self.btn_run.setGeometry(QtCore.QRect(50, 110, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btn_run.setFont(font)
        self.btn_run.setObjectName("btn_run")

        self.lbl_sms = QtWidgets.QLabel(self.centralwidget)
        self.lbl_sms.setGeometry(QtCore.QRect(50, 30, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.lbl_sms.setFont(font)
        self.lbl_sms.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_sms.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_sms.setObjectName("lbl_sms")

        self.btn_config = QtWidgets.QPushButton(self.centralwidget)
        self.btn_config.setGeometry(QtCore.QRect(50, 160, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btn_config.setFont(font)
        self.btn_config.setObjectName("btn_config")

        self.btn_zero = QtWidgets.QPushButton(self.centralwidget)
        self.btn_zero.setGeometry(QtCore.QRect(50, 210, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btn_zero.setFont(font)
        self.btn_zero.setObjectName("btn_zero")

        self.lbl_ash = QtWidgets.QLabel(self.centralwidget)
        self.lbl_ash.setGeometry(QtCore.QRect(30, 270, 181, 81))
        self.lbl_ash.setText("")
        self.lbl_ash.setPixmap(QtGui.QPixmap("../../../../../smb-share:server=diskstation.local,share=feeds/SMS/Stock Managment System/Client/GUI/ashlogo.png"))
        self.lbl_ash.setObjectName("lbl_ash")

        self.windows = list()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.btn_config.clicked.connect(self.config_button)
        self.btn_run.clicked.connect(MainWindow.close)
        self.btn_zero.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def config_button(self):
        self.config = Config_Window()
        self.windows.append(self.config)
        self.config.setupConfig(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SMS"))
        self.btn_run.setText(_translate("MainWindow", "Run"))
        self.lbl_sms.setText(_translate("MainWindow", "SMS"))
        self.btn_config.setText(_translate("MainWindow", "Config"))
        self.btn_zero.setText(_translate("MainWindow", "Zero"))

def main():
    app = QApplication(sys.argv)
    form = Ui_MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
