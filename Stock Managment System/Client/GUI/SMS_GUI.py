import sys, time, string, os, yaml, datetime, socket
from functools import partial
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
            self.lbl_s.setGeometry(QtCore.QRect(10, 10, 161, 25))
            font = QtGui.QFont()
            font.setPointSize(16)
            self.lbl_s.setFont(font)
            self.lbl_s.setObjectName("lbl_s")

            self.lbl_supplier = QtWidgets.QLabel(self.tab)
            self.lbl_supplier.setGeometry(QtCore.QRect(120, 10, 161, 21))
            font = QtGui.QFont()
            font.setPointSize(16)
            self.lbl_supplier.setFont(font)
            self.lbl_supplier.setObjectName("lbl_supplier")

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
            self.lbl_type.setAlignment(QtCore.Qt.AlignRight)

            self.btn_save = QtWidgets.QPushButton(self.tab)
            self.btn_save.setGeometry(QtCore.QRect(90, 280, 101, 41))
            self.btn_save.setObjectName("btn_save")

            self.lbl_enabled = QtWidgets.QLabel(self.tab)
            self.lbl_enabled.setGeometry(QtCore.QRect(10, 80, 67, 21))
            self.lbl_enabled.setObjectName("lbl_enabled")

            self.chk_supplier_enabled = QtWidgets.QCheckBox(self.tab)
            self.chk_supplier_enabled.setGeometry(QtCore.QRect(250, 80, 16, 23))
            self.chk_supplier_enabled.setObjectName("chk_supplier_enabled")
            self.chk_supplier_enabled.setChecked(config['suppliers'][suppliers]['enabled'])
            self.enabled = config['suppliers'][suppliers]['enabled']
            self.chk_supplier_enabled.stateChanged.connect(self.supplierEnabled)

            self.lbl_rundays = QtWidgets.QLabel(self.tab)
            self.lbl_rundays.setGeometry(QtCore.QRect(330, 30, 151, 21))
            self.lbl_rundays.setObjectName("lbl_rundays")

            self.lbl_mon = QtWidgets.QLabel(self.tab)
            self.lbl_mon.setGeometry(QtCore.QRect(330, 80, 81, 21))
            self.lbl_mon.setObjectName("lbl_mon")
            self.lbl_fri = QtWidgets.QLabel(self.tab)
            self.lbl_fri.setGeometry(QtCore.QRect(330, 200, 81, 21))
            self.lbl_fri.setObjectName("lbl_fri")
            self.lbl_thu = QtWidgets.QLabel(self.tab)
            self.lbl_thu.setGeometry(QtCore.QRect(330, 170, 81, 21))
            self.lbl_thu.setObjectName("lbl_thu")
            self.lbl_wed = QtWidgets.QLabel(self.tab)
            self.lbl_wed.setGeometry(QtCore.QRect(330, 140, 81, 21))
            self.lbl_wed.setObjectName("lbl_wed")
            self.lbl_tue = QtWidgets.QLabel(self.tab)
            self.lbl_tue.setGeometry(QtCore.QRect(330, 110, 81, 21))
            self.lbl_tue.setObjectName("lbl_tue")
            self.lbl_sun = QtWidgets.QLabel(self.tab)
            self.lbl_sun.setGeometry(QtCore.QRect(330, 260, 81, 21))
            self.lbl_sun.setObjectName("lbl_sun")
            self.lbl_sat = QtWidgets.QLabel(self.tab)
            self.lbl_sat.setGeometry(QtCore.QRect(330, 230, 81, 21))
            self.lbl_sat.setObjectName("lbl_sat")

            self.chk_mon = QtWidgets.QCheckBox(self.tab)
            self.chk_mon.setGeometry(QtCore.QRect(440, 80, 16, 21))
            self.chk_mon.setObjectName("chk_mon")
            self.chk_mon.setChecked(config['suppliers'][suppliers]['days']['monday'])
            self.monday = config['suppliers'][suppliers]['days']['monday']
            self.chk_mon.stateChanged.connect(self.mondayEnabled)

            self.chk_tue = QtWidgets.QCheckBox(self.tab)
            self.chk_tue.setGeometry(QtCore.QRect(440, 110, 16, 21))
            self.chk_tue.setObjectName("chk_tue")
            self.chk_tue.setChecked(config['suppliers'][suppliers]['days']['tuesday'])
            self.tuesday = config['suppliers'][suppliers]['days']['tuesday']
            self.chk_tue.stateChanged.connect(self.tuesdayEnabled)

            self.chk_wed = QtWidgets.QCheckBox(self.tab)
            self.chk_wed.setGeometry(QtCore.QRect(440, 140, 16, 21))
            self.chk_wed.setObjectName("chk_wed")
            self.chk_wed.setChecked(config['suppliers'][suppliers]['days']['wednesday'])
            self.wednesday = config['suppliers'][suppliers]['days']['wednesday']
            self.chk_wed.stateChanged.connect(self.wednesdayEnabled)

            self.chk_thu = QtWidgets.QCheckBox(self.tab)
            self.chk_thu.setGeometry(QtCore.QRect(440, 170, 16, 21))
            self.chk_thu.setObjectName("chk_thu")
            self.chk_thu.setChecked(config['suppliers'][suppliers]['days']['thursday'])
            self.thursday = config['suppliers'][suppliers]['days']['thursday']
            self.chk_thu.stateChanged.connect(self.thursdayEnabled)

            self.chk_fri = QtWidgets.QCheckBox(self.tab)
            self.chk_fri.setGeometry(QtCore.QRect(440, 200, 16, 21))
            self.chk_fri.setObjectName("chk_fri")
            self.chk_fri.setChecked(config['suppliers'][suppliers]['days']['friday'])
            self.friday = config['suppliers'][suppliers]['days']['friday']
            self.chk_fri.stateChanged.connect(self.fridayEnabled)

            self.chk_sat = QtWidgets.QCheckBox(self.tab)
            self.chk_sat.setGeometry(QtCore.QRect(440, 230, 16, 21))
            self.chk_sat.setObjectName("chk_sat")
            self.chk_sat.setChecked(config['suppliers'][suppliers]['days']['saturday'])
            self.saturday = config['suppliers'][suppliers]['days']['saturday']
            self.chk_sat.stateChanged.connect(self.saturdayEnabled)

            self.chk_sun = QtWidgets.QCheckBox(self.tab)
            self.chk_sun.setGeometry(QtCore.QRect(440, 260, 16, 21))
            self.chk_sun.setObjectName("chk_sun")
            self.chk_sun.setChecked(config['suppliers'][suppliers]['days']['sunday'])
            self.sunday = config['suppliers'][suppliers]['days']['sunday']
            self.chk_sun.stateChanged.connect(self.sundayEnabled)






            self.lbl_runtimes = QtWidgets.QLabel(self.tab)
            self.lbl_runtimes.setGeometry(QtCore.QRect(520, 30, 151, 21))
            self.lbl_runtimes.setObjectName("lbl_runtimes")

            position = 80
            for runtimes in range(0, len(config['suppliers'][suppliers]['times'])):

                time1 = time.strptime(config['suppliers'][suppliers]['times'][runtimes], "%H:%M")

                self.time_schedule1 = QtWidgets.QTimeEdit(self.tab)
                self.time_schedule1.setGeometry(QtCore.QRect(520, position, 161, 26))
                self.time_schedule1.setObjectName("time_schedule1")
                self.time_schedule1.setTime(QtCore.QTime(time1[3], time1[4]))

                if runtimes > 0:
                    self.btn_remove_time1 = QtWidgets.QPushButton(self.tab)
                    self.btn_remove_time1.setGeometry(QtCore.QRect(690, position, 26, 26))
                    self.btn_remove_time1.setObjectName("btn_remove_time1")
                    self.btn_remove_time1.setText(QtCore.QCoreApplication.translate("MainWindow", "-"))
                    self.removeTime_ = partial(self.removeTime, runtimes, suppliers)
                    self.btn_remove_time1.clicked.connect(self.removeTime_)


                position += 30
            self.times = config['suppliers'][suppliers]['times']
            self.btn_add_time = QtWidgets.QPushButton(self.tab)
            self.btn_add_time.setGeometry(QtCore.QRect(520, position, 26, 26))
            self.btn_add_time.setObjectName("btn_add_time")









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
            self.btn_save.clicked.connect(self.editconfig)
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
            self.monday = config['suppliers'][self.supplier]['days']['monday']
            self.tuesday = config['suppliers'][self.supplier]['days']['tuesday']
            self.wednesday = config['suppliers'][self.supplier]['days']['wednesday']
            self.thursday = config['suppliers'][self.supplier]['days']['thursday']
            self.friday = config['suppliers'][self.supplier]['days']['friday']
            self.saturday = config['suppliers'][self.supplier]['days']['saturday']
            self.sunday = config['suppliers'][self.supplier]['days']['sunday']
            self.times = config['suppliers'][supplier]['times']

            if config['suppliers'][self.supplier]['type'] is "ftp":
                self.user = config['suppliers'][self.supplier]['user']
                self.passwd = config['suppliers'][self.supplier]['passwd']
                self.file = config['suppliers'][self.supplier]['file']
            elif config['suppliers'][self.supplier]['type'] is "http":
                self.url = config['suppliers'][self.supplier]['url']
            elif config['suppliers'][self.supplier]['type'] is "email":
                None
            # NOTE: Will need to reload values here-
            return self.supplier
        except:
            None

    def removeTime(self, n, supplier):
        self.times = config['suppliers'][supplier]['times']
        # print(self.times)
        # print(self.times[n])
        del self.times[n]
        # print(self.times)

    def supplierEnabled(self, state):
        self.enabled = config['suppliers'][self.supplier]['enabled']
        if state == QtCore.Qt.Checked:
            self.enabled = True
        else:
            self.enabled = False

    def mondayEnabled(self, state):
        self.monday = config['suppliers'][self.supplier]['days']['monday']
        if state == QtCore.Qt.Checked:
            self.monday = True
        else:
            self.monday = False

    def tuesdayEnabled(self, state):
        self.tuesday = config['suppliers'][self.supplier]['days']['tuesday']
        if state == QtCore.Qt.Checked:
            self.tuesday = True
        else:
            self.tuesday = False

    def wednesdayEnabled(self, state):
        self.wednesday = config['suppliers'][self.supplier]['days']['wednesday']
        if state == QtCore.Qt.Checked:
            self.wednesday = True
        else:
            self.wednesday = False

    def thursdayEnabled(self, state):
        self.thursday = config['suppliers'][self.supplier]['days']['thursday']
        if state == QtCore.Qt.Checked:
            self.thursday = True
        else:
            self.thursday = False

    def fridayEnabled(self, state):
        self.friday = config['suppliers'][self.supplier]['days']['friday']
        if state == QtCore.Qt.Checked:
            self.friday = True
        else:
            self.friday = False

    def saturdayEnabled(self, state):
        self.saturday = config['suppliers'][self.supplier]['days']['saturday']
        if state == QtCore.Qt.Checked:
            self.saturday = True
        else:
            self.saturday = False

    def sundayEnabled(self, state):
        self.sunday = config['suppliers'][self.supplier]['days']['sunday']
        if state == QtCore.Qt.Checked:
            self.sunday = True
        else:
            self.sunday = False

    def maxSpin(self, number):
        self.max = number

    def minSpin(self, number):
        self.min = number

    def timeSchedule():
        None # tbc

    def editconfig(self, supplier):
        updateType = ['enabled', 'max', 'min', 'user', 'passwd', 'file', 'url', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'times']
        with open("config.yml", 'r') as cfg: # open config to populate certain areas of the GUI
            config = yaml.load(cfg, Loader=yaml.FullLoader)
            cfg.close()

        for value in updateType:
            if value in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                try:
                    selfval = eval("self." + value)
                    if config['suppliers'][self.supplier]['days'][value] is not selfval:
                        updateStr = "CNFED ['suppliers']['"+self.supplier+"']['days']['"+value+"'] "+str(selfval)
                        client.runClient(ipaddr="192.168.1.99", args=updateStr)
                except:
                   None
            elif value is 'times':
                if str(config['suppliers'][self.supplier]['times']) is not str(self.times):
                    updateStr = "CNFED ['suppliers']['"+self.supplier+"']['times'] ['"+self.times[0]+"'"
                    for t in range(1, len(self.times)):
                        updateStr += ",'" + self.times[t] + "'"
                    updateStr += "]"
                    print(updateStr)
                    client.runClient(ipaddr="192.168.1.99", args=updateStr)
            else:
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
        self.btn_save.setText(_translate("MainWindow", "Save"))
        self.btn_run.setText(_translate("MainWindow", "Run"))
        self.lbl_sms.setText(_translate("MainWindow", "SMS"))
        self.btn_config.setText(_translate("MainWindow", "Config"))
        self.btn_zero.setText(_translate("MainWindow", "Zero"))
        self.lbl_mon.setText(_translate("MainWindow", "Monday"))
        self.lbl_fri.setText(_translate("MainWindow", "Friday"))
        self.lbl_thu.setText(_translate("MainWindow", "Thursday"))
        self.lbl_wed.setText(_translate("MainWindow", "Wednesday"))
        self.lbl_tue.setText(_translate("MainWindow", "Tuesday"))
        self.lbl_sun.setText(_translate("MainWindow", "Sunday"))
        self.lbl_sat.setText(_translate("MainWindow", "Saturday"))
        self.lbl_rundays.setText(_translate("MainWindow", "Scheduled Run Days"))
        self.lbl_runtimes.setText(_translate("MainWindow", "Scheduled Run Times"))
        #self.btn_remove_time1.setText(_translate("MainWindow", "-"))
        self.btn_add_time.setText(_translate("MainWindow", "+"))
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
