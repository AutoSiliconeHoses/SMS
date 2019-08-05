import sys, time, string, os, yaml
import socket
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
sys.path.append("Client")
import client

with open("config.yml", 'r') as cfg: # open config to populate certain areas of the GUI
    config = yaml.load(cfg, Loader=yaml.FullLoader)
    cfg.close()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1144, 790)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Client/GUI/ASH-Black.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setStyleSheet("background-color: rgb(49, 49, 49);\ncolor: rgb(255, 255, 255);\n")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")

        self.btn_run = QtWidgets.QPushButton(self.centralwidget)
        self.btn_run.setGeometry(QtCore.QRect(10, 170, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btn_run.setFont(font)
        self.btn_run.setObjectName("btn_run")

        self.lbl_sms = QtWidgets.QLabel(self.centralwidget)
        self.lbl_sms.setGeometry(QtCore.QRect(30, 10, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.lbl_sms.setFont(font)
        self.lbl_sms.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_sms.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_sms.setObjectName("lbl_sms")

        self.btn_config = QtWidgets.QPushButton(self.centralwidget)
        self.btn_config.setGeometry(QtCore.QRect(10, 240, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btn_config.setFont(font)
        self.btn_config.setObjectName("btn_config")

        self.btn_zero = QtWidgets.QPushButton(self.centralwidget)
        self.btn_zero.setGeometry(QtCore.QRect(10, 310, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btn_zero.setFont(font)
        self.btn_zero.setObjectName("btn_zero")

        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(0, 710, 181, 81))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("Client/GUI/ashlogo.png"))
        self.logo.setObjectName("logo")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(190, 0, 951, 791))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_token = QtWidgets.QWidget()
        self.tab_token.setObjectName("tab_token")

        self.lbl_amazon = QtWidgets.QLabel(self.tab_token)
        self.lbl_amazon.setGeometry(QtCore.QRect(10, 10, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lbl_amazon.setFont(font)
        self.lbl_amazon.setObjectName("lbl_amazon")

        self.lbl_tok = QtWidgets.QLabel(self.tab_token)
        self.lbl_tok.setGeometry(QtCore.QRect(30, 150, 51, 17))
        self.lbl_tok.setObjectName("lbl_tok")

        self.label_4 = QtWidgets.QLabel(self.tab_token)
        self.label_4.setGeometry(QtCore.QRect(130, 150, 51, 17))
        self.label_4.setObjectName("label_4")

        self.lbl_shiptime = QtWidgets.QLabel(self.tab_token)
        self.lbl_shiptime.setGeometry(QtCore.QRect(30, 210, 151, 17))
        self.lbl_shiptime.setObjectName("lbl_shiptime")

        self.spn_ship = QtWidgets.QSpinBox(self.tab_token)
        self.spn_ship.setGeometry(QtCore.QRect(170, 205, 48, 26))
        self.spn_ship.setObjectName("spn_ship")
        self.spn_ship.setValue(config['amazon']['leadShipping'])

        self.listView = QtWidgets.QListView(self.tab_token)
        self.listView.setGeometry(QtCore.QRect(290, 60, 256, 192))
        self.listView.setObjectName("listView")

        self.tabWidget.addTab(self.tab_token, "")

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
            self.spn_max.valueChanged.connect(self.maxSpin)

            self.lbl_min = QtWidgets.QLabel(self.tab)
            self.lbl_min.setGeometry(QtCore.QRect(10, 140, 31, 21))
            self.lbl_min.setObjectName("lbl_min")

            self.spn_min = QtWidgets.QSpinBox(self.tab)
            self.spn_min.setGeometry(QtCore.QRect(220, 140, 51, 26))
            self.spn_min.setObjectName("spn_min")
            self.spn_min.setValue(config['suppliers'][suppliers]['min'])
            self.spn_min.valueChanged.connect(self.minSpin)

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
            self.enabled = config['suppliers'][suppliers]['enabled']
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

            self.retranslateUi(MainWindow, suppliers)
            self.btn_submit.clicked.connect(self.editconfig)
            self.tabWidget.setCurrentIndex(0)

        self.btn_config.clicked.connect(self.tabWidget.show)
        self.btn_run.clicked.connect(self.tabWidget.hide)
        self.btn_zero.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def setSupplier(self):
        tabname = self.tabWidget.widget(self.tabWidget.currentIndex()).objectName()
        self.supplier = tabname.replace("tab_","")
        try:
            self.enabled = config['suppliers'][self.supplier]['enabled']
            self.max = config['suppliers'][self.supplier]['max']
            self.min = config['suppliers'][self.supplier]['min']

            if config['suppliers'][self.supplier]['type'] is "ftp":
                self.user = config['suppliers'][self.supplier]['user']
                self.passwd = config['suppliers'][self.supplier]['passwd']
                self.file = config['suppliers'][self.supplier]['file']
            elif config['suppliers'][self.supplier]['type'] is "http":
                self.url = config['suppliers'][self.supplier]['url']
            # NOTE: Will need to reload values here-
            return self.supplier
        except:
            None

    def clickBox(self, state):
        self.enabled = config['suppliers'][self.supplier]['enabled']
        if state == QtCore.Qt.Checked:
            self.enabled = True
        else:
            self.enabled = False
        #self.editconfig(self.supplier,"enabled", self.enabled)

    def maxSpin(self, number):
        self.max = number

    def minSpin(self, number):
        self.min = number

    def timeRepeat():
        None # tbc

    def timeSchedule():
        None # tbc

    def editconfig(self, supplier):
        updateType = ['enabled', 'max', 'min', 'user', 'passwd', 'file', 'url']
        with open("config.yml", 'r') as cfg: # open config to populate certain areas of the GUI
            config = yaml.load(cfg, Loader=yaml.FullLoader)
            cfg.close()
        for value in updateType:
            try:
                selfval = eval("self." + value)
                if config['suppliers'][self.supplier][value] is not selfval:
                    updateStr = "CNFED ['suppliers']['"+self.supplier+"']['"+value+"'] "+str(selfval)
                    client.runClient(ipaddr="192.168.1.99", args=updateStr)
            except:
               None
        client.runClient(ipaddr="192.168.1.99", args="UPDATE")

    def retranslateUi(self, MainWindow, supplier):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SMS"))
        self.lbl_s.setText(_translate("MainWindow", "Supplier:"))
        self.lbl_supplier.setText(_translate("MainWindow", supplier))
        self.lbl_t.setText(_translate("MainWindow", "Type: "))
        self.lbl_type.setText(_translate("MainWindow", config['suppliers'][supplier]['type']))
        self.lbl_enabled.setText(_translate("MainWindow", "Enabled"))
        self.lbl_max.setText(_translate("MainWindow", "Max"))
        self.lbl_min.setText(_translate("MainWindow", "Min"))
        self.btn_submit.setText(_translate("MainWindow", "Submit"))
        self.lbl_time.setText(_translate("MainWindow", "Time"))
        self.btn_run.setText(_translate("MainWindow", "Run"))
        self.lbl_sms.setText(_translate("MainWindow", "SMS"))
        self.btn_config.setText(_translate("MainWindow", "Config"))
        self.btn_zero.setText(_translate("MainWindow", "Zero"))
        try:
            self.lbl_amazon.setText(_translate("MainWindow", "Amazon"))
            self.lbl_tok.setText(_translate("MainWindow", "Token:"))
            self.label_4.setText(_translate("MainWindow", "Token:"))
            self.lbl_shiptime.setText(_translate("MainWindow", "Lead Shipping Time:"))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_token), _translate("MainWindow", "tokens"))
        except:
            None
        try:
            self.lbl_file.setText(_translate("MainWindow", "FTP Path"))
            self.lbl_user.setText(_translate("MainWindow", "User"))
            self.lbl_passwd.setText(_translate("MainWindow", "Password"))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", supplier))
        except:
            None
        try:
            self.lbl_http.setText(_translate("MainWindow", "HTTP Link:"))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", supplier))
        except:
            None
        try:
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", supplier))
        except:
            None
        self.tabWidget.setHidden(True)

class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
