import sys, string, os, yaml, tkinter, numpy, scipy
from PySide2.QtWidgets import *
from PySide2.QtQuick import *
from PySide2.QtCore import *

with open("config.yml", 'r') as cfg:
    config = yaml.load(cfg, Loader=yaml.FullLoader)

suppliersList = []
for s in config['suppliers']:
    suppliersList.append(s)

class Pages(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)

        count = 0
        tab = QTabWidget()
        list = QListWidget()

        for supplier in suppliersList:
            content = QLabel(str(config['suppliers'][supplier]))
            tab.addTab(content, str(supplier))
            layout.addWidget(tab, 0, 0)
            count +=1

    def populateTab(supplier):
        tablayout = QGridLayout()
        supplierDeatails = []
        for s in config['suppliers'][supplier]:
            supplierDetails.append(s)

        label = QLabel("label works 2222")
        tablayout.addWidget(label, 0 , 0)



        # label1 = QLabel("Widget in Tab 1.")
        # tabwidget = QTabWidget()
        # tabwidget.addTab(label1, "Tab 1")
        #
        # layout.addWidget(tabwidget, 0, 0)
        #
        # label2 = QLabel("Widget in Tab 2.")
        # tabwidget.addTab(label2, "Tab 2")
        # layout.addWidget(tabwidget, 0, 0)

app = QApplication(sys.argv)
screen = Pages()
screen.show()
sys.exit(app.exec_())


#
# class Widget(QWidget):
#     def __init__(self, parent=None):
#         QWidget.__init__(self, parent)
#         self.setLayout(QGridLayout())
#         for i in range(20):
#             letter = chr(ord('a') + i)
#             checkBox = QCheckBox('{}'.format(i+1), self)
#             self.layout().addWidget(checkBox, i, 0)
#
#             btna = QPushButton("{}1".format(letter), self)
#             btnb = QPushButton("{}2".format(letter), self)
#
#             self.layout().addWidget(btna, i, 1)
#             self.layout().addWidget(btnb, i, 2)
#
#
# class Tab1(QWidget):
#     def __init__(self, parent=None):
#         QWidget.__init__(self, parent)
#         self.setLayout(QGridLayout())
#
#         self.group = Widget(self)
#         scroll = QScrollArea(self)
#         scroll.setWidget(self.group)
#         scroll.setWidgetResizable(True)
#
#         self.layout().addWidget(scroll)
#         self.runBtn = QPushButton("Run", self)
#         self.layout().addWidget(self.runBtn)
#
#
# class Page1(QTabWidget):
#     def __init__(self, parent=None):
#         super(Page1, self).__init__(parent)
#         self.tab1 = Tab1()
#         self.tab2 = QWidget()
#         self.tab3 = QWidget()
#         self.addTab(self.tab1, "Tab1")
#         self.addTab(self.tab2, "Tab2")
#         self.addTab(self.tab3, "Tab3")
#         self.tab2_initUI()
#         self.tab3_initUI()
#
#     def tab2_initUI(self):
#         grid = QGridLayout()
#         self.tab2.setLayout(grid)
#
#     def tab3_initUI(self):
#         grid = QGridLayout()
#         self.tab3.setLayout(grid)
#
# class MainWindow(QMainWindow):
#     def __init__(self, parent=None):
#         super(MainWindow, self).__init__(parent)
#         self.setGeometry(300, 200, 600, 370)
#         self.startPage1()
#
#     def startPage1(self):
#         x = Page1(self)
#         self.setWindowTitle("Auto Benchmark")
#         self.setCentralWidget(x)
#         self.show()
#
# def main():
#     app = QApplication(sys.argv)
#     main = MainWindow()
#     main.show()
#     sys.exit(app.exec_())
#
#
# if __name__ == '__main__':
# main()
