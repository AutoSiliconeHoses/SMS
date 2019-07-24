import sys, time, string, os, yaml
import socket
from PyQt5 import QtCore, QtGui, QtWidgets
#from Server.configedit import update

with open("config.yml", 'r') as cfg:
    config = yaml.load(cfg, Loader=yaml.FullLoader)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        MainWindow.setStyleSheet("background-color: rgb(46, 52, 54);\n"
"color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1000, 600))
        self.tabWidget.setObjectName("tabWidget")

        for suppliers in config['suppliers']:
            self.tab = QtWidgets.QWidget()
            self.tab.setObjectName("tab_"+suppliers)
            self.tabWidget.currentChanged['int'].connect(self.setSupplier)

            self.lbl_s = QtWidgets.QLabel(self.tab)
            self.lbl_s.setGeometry(QtCore.QRect(10, 10, 161, 21))
            font = QtGui.QFont()
            font.setPointSize(16)
            self.lbl_s.setFont(font)
            self.lbl_s.setObjectName("lbl_supplier")

            self.lbl_supplier = QtWidgets.QLabel(self.tab)
            self.lbl_supplier.setGeometry(QtCore.QRect(120, 10, 161, 21))
            font = QtGui.QFont()
            font.setPointSize(16)
            self.lbl_supplier.setFont(font)
            self.lbl_supplier.setObjectName("lbl_supplier")

            self.time_schedule = QtWidgets.QTimeEdit(self.tab)
            self.time_schedule.setGeometry(QtCore.QRect(350, 50, 161, 26))
            self.time_schedule.setObjectName("time_schedule")

            self.lbl_max = QtWidgets.QLabel(self.tab)
            self.lbl_max.setGeometry(QtCore.QRect(10, 110, 31, 21))
            self.lbl_max.setObjectName("lbl_max")

            self.spn_max = QtWidgets.QSpinBox(self.tab)
            self.spn_max.setGeometry(QtCore.QRect(220, 110, 51, 26))
            self.spn_max.setObjectName("spn_max")
            self.spn_max.setValue(config['suppliers'][suppliers]['max'])

            self.lbl_min = QtWidgets.QLabel(self.tab)
            self.lbl_min.setGeometry(QtCore.QRect(10, 140, 31, 21))
            self.lbl_min.setObjectName("lbl_min")

            self.spn_min = QtWidgets.QSpinBox(self.tab)
            self.spn_min.setGeometry(QtCore.QRect(220, 140, 51, 26))
            self.spn_min.setObjectName("spn_min")
            self.spn_min.setValue(config['suppliers'][suppliers]['min'])

            self.lbl_t = QtWidgets.QLabel(self.tab)
            self.lbl_t.setGeometry(QtCore.QRect(10, 50, 67, 21))
            self.lbl_t.setObjectName("lbl_t")

            self.lbl_type = QtWidgets.QLabel(self.tab)
            self.lbl_type.setGeometry(QtCore.QRect(200, 50, 67, 21))
            self.lbl_type.setObjectName("lbl_type")
            self.lbl_type.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)

            self.btn_submit = QtWidgets.QPushButton(self.tab)
            self.btn_submit.setGeometry(QtCore.QRect(430, 230, 80, 25))
            self.btn_submit.setObjectName("btn_submit")

            self.lbl_enabled = QtWidgets.QLabel(self.tab)
            self.lbl_enabled.setGeometry(QtCore.QRect(10, 80, 67, 21))
            self.lbl_enabled.setObjectName("lbl_enabled")

            self.chk_supplier_enabled = QtWidgets.QCheckBox(self.tab)
            self.chk_supplier_enabled.setGeometry(QtCore.QRect(250, 80, 16, 23))
            self.chk_supplier_enabled.setObjectName("chk_supplier_enabled")
            self.chk_supplier_enabled.setChecked(config['suppliers'][suppliers]['enabled'])
            self.checked = config['suppliers'][suppliers]['enabled']
            self.chk_supplier_enabled.stateChanged.connect(self.clickBox)

            self.lbl_time = QtWidgets.QLabel(self.tab)
            self.lbl_time.setGeometry(QtCore.QRect(290, 50, 51, 21))
            self.lbl_time.setObjectName("lbl_time")

            self.time_repeat = QtWidgets.QTimeEdit(self.tab)
            self.time_repeat.setGeometry(QtCore.QRect(350, 80, 161, 25))
            self.time_repeat.setObjectName("time_repeat")

            if (config['suppliers'][suppliers]['type'] == 'ftp'):
                self.lbl_user = QtWidgets.QLabel(self.tab)
                self.lbl_user.setGeometry(QtCore.QRect(10, 170, 41, 21))
                self.lbl_user.setObjectName("lbl_user")

                self.lne_user = QtWidgets.QLineEdit(self.tab)
                self.lne_user.setGeometry(QtCore.QRect(110, 170, 161, 25))
                self.lne_user.setObjectName("lne_user")
                self.lne_user.setPlaceholderText(config['suppliers'][suppliers]['user'])

                self.lbl_passwd = QtWidgets.QLabel(self.tab)
                self.lbl_passwd.setGeometry(QtCore.QRect(10, 200, 71, 21))
                self.lbl_passwd.setInputMethodHints(QtCore.Qt.ImhNone)
                self.lbl_passwd.setObjectName("lbl_passwd")

                self.lne_passwd = QtWidgets.QLineEdit(self.tab)
                self.lne_passwd.setGeometry(QtCore.QRect(110, 200, 161, 25))
                self.lne_passwd.setInputMethodHints(QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
                self.lne_passwd.setObjectName("lne_passwd")
                self.lne_passwd.setPlaceholderText(config['suppliers'][suppliers]['passwd'])

                self.lbl_file = QtWidgets.QLabel(self.tab)
                self.lbl_file.setGeometry(QtCore.QRect(10, 230, 71, 21))
                self.lbl_file.setObjectName("lbl_file")

                self.lne_file = QtWidgets.QLineEdit(self.tab)
                self.lne_file.setGeometry(QtCore.QRect(110, 230, 161, 25))
                self.lne_file.setObjectName("lne_file")
                self.lne_file.setPlaceholderText(config['suppliers'][suppliers]['file'])

            elif(config['suppliers'][suppliers]['type'] == 'email'):
                None
            elif(config['suppliers'][suppliers]['type'] == 'http'):
                self.lbl_http = QtWidgets.QLabel(self.tab)
                self.lbl_http.setGeometry(QtCore.QRect(10, 170, 75, 21))
                self.lbl_http.setObjectName("lbl_http")

                self.lne_http = QtWidgets.QLineEdit(self.tab)
                self.lne_http.setGeometry(QtCore.QRect(110, 170, 161, 25))
                self.lne_http.setObjectName("lne_user")
                self.lne_http.setPlaceholderText(config['suppliers'][suppliers]['url'])

            self.tabWidget.addTab(self.tab, "")

            MainWindow.setCentralWidget(self.centralwidget)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)

            self.retranslateUi(MainWindow, suppliers)
            self.tabWidget.setCurrentIndex(0)

            # self.btn_submit.clicked.connect(self.clickBox)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setSupplier(self):
        tabname = self.tabWidget.widget(self.tabWidget.currentIndex()).objectName()
        self.supplier = tabname.replace("tab_","")
        self.checked = config['suppliers'][self.supplier]['enabled']
        # NOTE: Will need to reload values here-
        return self.supplier

    def clickBox(self, state):
        self.checked = config['suppliers'][self.supplier]['enabled']
        if state == QtCore.Qt.Checked:
            self.checked = True
        else:
            self.checked = False
        self.editconfig(self.supplier,"enabled", self.checked)

    def editconfig(self, supplier, attribute, value):
        print("Update", supplier, attribute, "to", value)

    def retranslateUi(self, MainWindow, supplier):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_s.setText(_translate("MainWindow", "Supplier:"))
        self.lbl_supplier.setText(_translate("MainWindow", supplier))
        self.lbl_t.setText(_translate("MainWindow", "Type: "))
        self.lbl_type.setText(_translate("MainWindow", config['suppliers'][supplier]['type']))
        self.lbl_enabled.setText(_translate("MainWindow", "Enabled"))
        self.lbl_max.setText(_translate("MainWindow", "Max"))
        self.lbl_min.setText(_translate("MainWindow", "Min"))
        self.btn_submit.setText(_translate("MainWindow", "Submit"))
        self.lbl_time.setText(_translate("MainWindow", "Time"))
        try:
            self.lbl_file.setText(_translate("MainWindow", "FTP Path"))
            self.lbl_user.setText(_translate("MainWindow", "User"))
            self.lbl_passwd.setText(_translate("MainWindow", "Password"))
        except:
            None
        try:
            self.lbl_http.setText(_translate("MainWindow", "HTTP Link:"))
        except:
            None

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", supplier))
