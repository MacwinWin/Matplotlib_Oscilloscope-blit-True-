#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    init CAN device
    read data thread
    read data0, save data0 at data0.txt
    read data1, save data1 at data1.txt
'''

import struct

from PyQt5.QtCore import QThread, pyqtSignal
from ctypes import *

class _VCI_INIT_CONFIG(Structure):
    _fields_ = [('AccCode', c_ulong),
                ('AccMask', c_ulong),
                ('Reserved', c_ulong),
                ('Filter', c_ubyte),
                ('Timing0', c_ubyte),
                ('Timing1', c_ubyte),
                ('Mode', c_ubyte)]

class _VCI_CAN_OBJ(Structure):
    _fields_ = [('ID', c_uint),
                ('TimeStamp', c_uint),
                ('TimeFlag', c_ubyte),
                ('SendType', c_ubyte),
                ('RemoteFlag', c_ubyte),
                ('ExternFlag', c_ubyte),
                ('DataLen', c_ubyte),
                ('Data', c_ubyte*8),
                ('Reserved', c_ubyte*3)]

class readClass(QThread):
    trigger = pyqtSignal()
    def __init__(self, mainWindow):
        super(readClass, self).__init__()
        self.mainWindow = mainWindow
        self.canLib = windll.LoadLibrary('./ControlCAN.dll')
        self.vic = _VCI_INIT_CONFIG()
        self.vic.AccCode = 0x00000000
        self.vic.AccMask = 0xffffffff
        self.vic.Filter = 0
        self.vic.Timing0 = 0x01
        self.vic.Timing1 = 0x1c
        self.vic.Mode = 0 
        self.vco = _VCI_CAN_OBJ()
        self.bandRateList = {'1000K':0x060003,\
                         '800K':0x060004, \
                         '500K':0x060007, \
                         '250K':0x1C0008, \
                         '125K':0x1C0011, \
                         '100K':0x160023}
        self.timingList = {'1000K':(0x00, 0x14), \
                           '800K':(0x00, 0x16), \
                           '500K':(0x00, 0x1C), \
                           '250K':(0x01, 0x1C), \
                           '125K':(0x03, 0x1C), \
                           '100K':(0x04, 0x1C)}
        # this program only receiving data, so send type not using
        #self.sendTypeList = {'正常发送': 0, \
        #                     '单次发送': 1, \
        #                     '自发自收': 2, \
        #                     '单次自发自收': 3}

    def init_device(self):
        if self.mainWindow.type_comboBox.currentText() == 'USBCAN-2E-U':
            self.deviceType = 21
        else:
            self.deviceType = 3
        self.bandRate = self.bandRateList[self.mainWindow.rate_comboBox.currentText()]
        self.vic.Timing0 = self.timingList[self.mainWindow.rate_comboBox.currentText()][0]
        self.vic.Timing1 = self.timingList[self.mainWindow.rate_comboBox.currentText()][1]
        self.open_flag = self.canLib.VCI_OpenDevice(self.deviceType, 0, 0)
        print('打开设备: {}'.format(self.open_flag))
        print('设置波特率: {}'.format(self.canLib.VCI_SetReference(self.deviceType, 0, 0, 0, \
                                pointer(c_int(self.bandRate)))))
        print('初始化: {}'.format(self.canLib.VCI_InitCAN(self.deviceType, 0, 0, pointer(self.vic))))
        print('启动: {}'.format(self.canLib.VCI_StartCAN(self.deviceType, 0, 0)))
        print('清空缓冲区: {}'.format(self.canLib.VCI_ClearBuffer(self.deviceType, 0, 0)))
        return self.open_flag

    def run(self):
        i = 0
        while True:
            num = self.canLib.VCI_GetReceiveNum(21, 0, 0)
            #print(num)
            if num:
                flag = self.canLib.VCI_Receive(21, 0, 0, pointer(self.vco), 1, 0)
                #print(flag)
                if flag <= 0:
                    print('调用 VCI_Receive 出错\r\n')
                    self.mainWindow.ui.read_textBrowser.append('调用 VCI_Receive 出错')
                elif flag > 0:
                    if self.vco.ID == 0x0701:
                        self.id = hex(self.vco.ID)
                        self.frame = list(self.vco.Data)
                        self.voltage = float((self.frame[0] * 256 + self.frame[1]) / 10)
                        self.current = float((self.frame[2] * 256 + self.frame[3]) / 10)
                        self.power = int(self.frame[4] * 256 + self.frame[5])
                        self.time = float((self.frame[6] * 256 + self.frame[7]) / 10)
                        self.mainWindow.textBrowser.append('ID:{}  帧:{}<br>电压:{}  电流:{}  功率:{}  时间:{}<br>'.format(\
                                                            self.id, self.frame, self.voltage, self.current, self.power, self.time))
                        with open('data1.txt', 'a') as f:
                            #print('write')
                            f.write('{},{},{},{}\n'.format(self.voltage,self.current,self.power,self.time))
                    elif self.vco.ID == 0x0700:
                        self.Id = hex(self.vco.ID)
                        self.Frame = list(self.vco.Data)
                        self.Voltage = float((self.Frame[0] * 256 + self.Frame[1]) / 10)
                        self.Current = float((self.Frame[2] * 256 + self.Frame[3]) / 10)
                        self.Power = int(self.Frame[4] * 256 + self.Frame[5])
                        self.time = float((self.Frame[6] * 256 + self.Frame[7]) / 10)
                        with open('data0.txt', 'a') as f:
                            #print('write')
                            f.write('{},{},{},{},{}\n'.format(self.Voltage,self.Current,self.Power,self.time,i))
                            i = i+1
                            #f.write('{},{}\n'.format(list(self.vco.Data)[7], list(self.vco.Data)[1]))
                    else:
                        pass
    #def closeFile(self):
        

            elif num == 0:
                pass
                #self.trigger.emit()