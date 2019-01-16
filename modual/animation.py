#! /usr/bin/env python3
# coding: utf-8

'''
    dynamic update 3 plots
'''

import sys
import os

from PyQt5.QtCore import QThread
import matplotlib
from matplotlib.animation import FuncAnimation
import numpy as np
 
class animation1Class(QThread):
    def __init__(self, canvas, ui):
        super(animation1Class, self).__init__()
        self.ui = ui
        self.canvas = canvas
        #self.y_voltage = np.array([],dtype = 'i1')
        self.y_voltage = []
        self.y_current = []
        self.y_power = []
        #self.x_time = np.array([], dtype='i1')
        self.x_time = []
        self.line1, = self.canvas.ax1.plot([], [])
        #self.line2, = self.canvas.ax2.plot([], [])
        #self.line3, = self.canvas.ax3.plot([], [])
        self.on_start()

    def update_line(self, i):
        try:
            with open('data0.txt', 'r') as f:
                data = f.read()
                lines = data.split('\n')
                for line in lines:
                    if len(line) > 1:
                        voltage, current, power, _, i = line.split(',')
                        #self.y_voltage = np.append(self.y_voltage, float(voltage))
                        self.y_voltage.append(float(voltage))
                        #self.y_current.append(float(current))
                        #self.y_power.append(float(power))
                        self.x_time.append(float(i))
                        #self.x_time = np.append(self.x_time, float(i))
        except:
            print('no .txt file!')
        self.line1.set_data(self.x_time, self.y_voltage)
        #self.line2.set_data(self.x_time, self.y_current)
        #self.line3.set_data(self.x_time, self.y_power)
        return self.line1,
 
    def on_start(self):
        self.ani = FuncAnimation(self.canvas.figure, self.update_line, blit = True, interval = 40, repeat = False)

class animation2Class(QThread):
    def __init__(self, canvas, ui):
        super(animation2Class, self).__init__()
        self.ui = ui
        self.canvas = canvas
        #self.y_voltage = []
        self.y_current = []
        self.y_power = []
        self.x_time = []
        #self.line1, = self.canvas.ax1.plot([], [])
        self.line2, = self.canvas.ax2.plot([], [])
        #self.line3, = self.canvas.ax3.plot([], [])
        self.on_start()
    def update_line(self, i):
        try:
            with open('data0.txt', 'r') as f:
                data = f.read()
                lines = data.split('\n')
                for line in lines:
                    if len(line) > 1:
                        voltage, current, power, _, i = line.split(',')
                        #self.y_voltage.append(float(voltage))
                        self.y_current.append(float(current))
                        #self.y_power.append(float(power))
                        self.x_time.append(float(i))
        except:
            print('no .txt file!')
        #self.line1.set_data(self.x_time, self.y_voltage)
        self.line2.set_data(self.x_time, self.y_current)
        #self.line3.set_data(self.x_time, self.y_power)
        return self.line2,
 
    def on_start(self):
        self.ani = FuncAnimation(self.canvas.figure, self.update_line, blit = True, interval = 40, repeat = False)
    
class animation3Class(QThread):
    def __init__(self, canvas, ui):
        super(animation3Class, self).__init__()
        self.ui = ui
        self.canvas = canvas
        #self.y_voltage = []
        self.y_current = []
        self.y_power = []
        self.x_time = []
        #self.line1, = self.canvas.ax1.plot([], [])
        #self.line2, = self.canvas.ax2.plot([], [])
        self.line3, = self.canvas.ax3.plot([], [])
        self.on_start()
    def update_line(self, i):
        try:
            with open('data0.txt', 'r') as f:
                data = f.read()
                lines = data.split('\n')
                for line in lines:
                    if len(line) > 1:
                        voltage, current, power, _, i = line.split(',')
                        #self.y_voltage.append(float(voltage))
                        #self.y_current.append(float(current))
                        self.y_power.append(float(power))
                        self.x_time.append(float(i))
        except:
            print('no .txt file!')
        #self.line1.set_data(self.x_time, self.y_voltage)
        #self.line2.set_data(self.x_time, self.y_current)
        self.line3.set_data(self.x_time, self.y_power)
        return self.line3,
 
    def on_start(self):
        self.ani = FuncAnimation(self.canvas.figure, self.update_line, blit = True, interval = 40, repeat = False)


