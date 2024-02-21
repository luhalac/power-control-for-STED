# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 12:40:33 2024

@author: Lucía Lopez

GUI for MPS x,y,z data exploration and quick analysis

conda command for converting QtDesigner file to .py:
pyuic5 -x power_control_GUI.ui -o power_control_GUI.py

"""

from pylablib.devices import Thorlabs
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

import pyqtgraph as pg
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets


import os
cdir = os.getcwd()
os.chdir(cdir)
import power_control_GUI




class power_control(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        
        self.ui = power_control_GUI.Ui_MainWindow()
        self.ui.setupUi(self)
        
        # connected Thorlabs kinesis/APT devices
        self.devices = Thorlabs.list_kinesis_devices()
        # number of connected devices
        N = len(self.devices)
        print(N)
        
          
        
        # rename devices
        self.cube1 = Thorlabs.KinesisMotor(self.devices[0][0])
        # self.cube2 = Thorlabs.KinesisMotor(self.devices[0][1])
        # self.cube3 = Thorlabs.KinesisMotor(self.devices[0][2])
        
        # get initial positions
        initpos1 = self.cube1.get_position(channel=None, scale=True)
        initangle1 = self.steps_to_deg(initpos1)
        
        # display angles
        self.angle_lcd1 = self.ui.lcdNumber1
        self.update_angle_display(initangle1)
        
        
        
        # home devices (go to 0 degrees)
        
        self.home1 = self.ui.pushButton_home1
        self.home1.clicked.connect(self.home_and_zero)
        
        angleu = 5
        self.jogup1 = self.ui.pushButton_jogup1
        self.jogup1.clicked.connect(lambda: self.move_by(angleu))
        angleuf = 1
        self.jogupf1 = self.ui.pushButton_jogupf1
        self.jogupf1.clicked.connect(lambda: self.move_by(angleuf))
        
        
        angled = -5
        self.jogd1 = self.ui.pushButton_jogd1
        self.jogd1.clicked.connect(lambda: self.move_by(angled))
        angledf = -1
        self.jogdf1 = self.ui.pushButton_jogdf1
        self.jogdf1.clicked.connect(lambda: self.move_by(angledf))
        
        
        
    def home_and_zero(self):    
        
        #home devices 
        self.cube1.home(sync=True, force=False, channel=None, timeout=None)
        #go to 0 position
        self.cube1.move_to(0, scale=True)
        # Update angle display
        self.update_angle_display(0)
            
        
    def deg_to_steps(self,deg):
        
        #scale steps to deg
        
        steps = 1923*deg
        
        return steps
    
    def steps_to_deg(self,steps):
        
        #scale steps to deg
        
        deg = steps/1923
        
        return deg
    
    def pow_to_ang(self, power):
        
        angle = power
        
        return angle
    
    def ang_to_pow(self, angle):
        
        power = angle
        
        return power
    
    def get_pos(self,cube):
        
        pos = self.cube1.get_position(channel=None, scale=True)
        
        return pos
        
        
    def move_to(self,cube, angle):
        
        # Move to specified angle
        cube.move_to(self.deg_to_steps(angle), scale=True)
        # Update angle display
        self.update_angle_display(angle)

        
    def move_by(self, angle):
        
        # Move by specified angle
        current_pos = self.get_pos(self.cube1) 
        current_angle = self.steps_to_deg(current_pos)
        new_angle = current_angle + angle
        self.move_to(self.cube1, new_angle)
        
        # self.cube1.move_by(self.steps_to_deg(angle))
        # Update angle display
        self.update_angle_display(new_angle)
        
        
        
    def update_angle_display(self, angle):
        # Update angle display
        self.angle_lcd1.display(angle)
        
    def set_power(self, power):
        
        angle = self.pow_to_ang(power)
        self.move_to(self.cube1, angle)
        
        # self.cube1.move_by(self.steps_to_deg(angle))
        # Update angle display
        self.update_angle_display(angle)
        

        
        
            
            
if __name__ == '__main__':
    
    app = QtWidgets.QApplication([])
    # app = QtGui.QApplication([])
    app.setStyleSheet("QMainWindow {background-color: #333333; color: #ffffff;} "
                  "QPushButton {background-color: #555555; color: #ffffff;} "
                  "QLCDNumber {background-color: #222222; color: #00ff00;}")

    win = power_control()
    win.show()
    app.exec_()           
            
                       
        

















