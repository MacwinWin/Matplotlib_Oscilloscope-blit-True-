#! /usr/bin/env python3
# codint: utf-8

import sys, time

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QMessageBox

from main import ApplicationWindow
from modual import initUi, read

class initFrom(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = initUi.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.open_pushButton.clicked.connect(self.init_device)

    def init_device(self):
        self.init = read.readClass(self.ui)
        self.open_flag = self.init.init_device()
        if self.open_flag:
            self.run()
        else:
            QMessageBox.information(None, '警告', '未开启CAN', QMessageBox.Ok)
    
    def run(self):
        self.close()
        self.main = ApplicationWindow()
        self.main.showMaximized()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    w = initFrom()
    w.show()
    app.exec_()
