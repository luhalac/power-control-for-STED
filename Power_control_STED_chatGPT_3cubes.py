# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 14:43:01 2024

@author: Lucía Lopez


TO DO:
- try with 3rd cube
- calibrate with powermeter
- define low and high values for fast switch
"""

from pylablib.devices import Thorlabs
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLCDNumber
import os
import power_control_GUI

class PowerControl(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.ui = power_control_GUI.Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connected Thorlabs kinesis/APT devices
        self.devices = Thorlabs.list_kinesis_devices()
        self.cube1 = Thorlabs.KinesisMotor(self.devices[0][0])
        self.cube2 = Thorlabs.KinesisMotor(self.devices[1][0])
        # self.cube3 = Thorlabs.KinesisMotor(self.devices[2][0])
        
        # Initialize UI components
        self.init_ui()
        
    def init_ui(self):
        # Connect home buttons for each cube
        self.ui.pushButton_home1.clicked.connect(self.home_and_zero_cube1)
        self.ui.pushButton_home2.clicked.connect(self.home_and_zero_cube2)
        self.ui.pushButton_home3.clicked.connect(self.home_and_zero_cube3)

        
        # Connect jog buttons for each cube
        self.ui.pushButton_jogup1.clicked.connect(lambda: self.move_by(1, 5))
        self.ui.pushButton_jogdown1.clicked.connect(lambda: self.move_by(1, -5))
        
        self.ui.pushButton_jogupf1.clicked.connect(lambda: self.move_by(1, 1))
        self.ui.pushButton_jogdownf1.clicked.connect(lambda: self.move_by(1, -1))
        
        self.ui.pushButton_jogup2.clicked.connect(lambda: self.move_by(2, 5))
        self.ui.pushButton_jogdown2.clicked.connect(lambda: self.move_by(2, -5))
        
        self.ui.pushButton_jogupf2.clicked.connect(lambda: self.move_by(2, 1))
        self.ui.pushButton_jogdownf2.clicked.connect(lambda: self.move_by(2, -1))
        
        self.ui.pushButton_jogup3.clicked.connect(lambda: self.move_by(3, 5))
        self.ui.pushButton_jogdown3.clicked.connect(lambda: self.move_by(3, -5))
        
        self.ui.pushButton_jogupf3.clicked.connect(lambda: self.move_by(3, 1))
        self.ui.pushButton_jogdownf3.clicked.connect(lambda: self.move_by(3, -1))

        
        # Connect set power button
        self.ui.pushButton_setpower.clicked.connect(self.set_power)
        
        # Set initial position for each cube
        init_pos1 = self.cube1.get_position(channel=None, scale=True)
        init_angle1 = self.steps_to_deg(init_pos1)
        self.update_angle_display(init_angle1, 1)
        
        init_pos2 = self.cube2.get_position(channel=None, scale=True)
        init_angle2 = self.steps_to_deg(init_pos2)
        self.update_angle_display(init_angle2, 2)
        
        init_pos3 = self.cube3.get_position(channel=None, scale=True)
        init_angle3 = self.steps_to_deg(init_pos3)
        self.update_angle_display(init_angle3, 3)
        
    def home_and_zero_cube1(self):    
        self.cube1.home(sync=True, force=False, channel=None, timeout=None)
        self.cube1.move_to(0, scale=True)
        self.update_angle_display(0, 1)
            
    def home_and_zero_cube2(self):    
        self.cube2.home(sync=True, force=False, channel=None, timeout=None)
        self.cube2.move_to(0, scale=True)
        self.update_angle_display(0, 2)
            
    def home_and_zero_cube3(self):    
        self.cube3.home(sync=True, force=False, channel=None, timeout=None)
        self.cube3.move_to(0, scale=True)
        self.update_angle_display(0, 3)
            
    def deg_to_steps(self, deg):
        return 1923 * deg
    
    def steps_to_deg(self, steps):
        return steps / 1923
    
    def get_pos(self, cube):
        return cube.get_position(channel=None, scale=True)
        
    def move_to(self, cube, angle):
        cube.move_to(self.deg_to_steps(angle), scale=True)
        self.update_angle_display(angle)

    def move_by(self, cube_num, angle_change):
        if cube_num == 1:
            cube = self.cube1
        elif cube_num == 2:
            cube = self.cube2
        elif cube_num == 3:
            cube = self.cube3
            
        current_pos = self.get_pos(cube) 
        current_angle = self.steps_to_deg(current_pos)
        new_angle = current_angle + angle_change
        self.update_angle_display(new_angle, cube_num)
        self.move_to(cube, new_angle)


    def update_angle_display(self, angle, cube_num):
        if cube_num == 1:
            self.ui.lcdNumber1.display(angle)
        elif cube_num == 2:
            self.ui.lcdNumber2.display(angle)
        elif cube_num == 3:
            self.ui.lcdNumber3.display(angle)
        
    def set_power(self):
        power = float(self.ui.lineEdit_setpower.text())
        angle = self.pow_to_ang(power)
        self.move_to(self.cube1, angle)
        self.update_angle_display(angle, 1)
        self.move_to(self.cube2, angle)
        self.update_angle_display(angle, 2)
        self.move_to(self.cube3, angle)
        self.update_angle_display(angle, 3)
        
    def closeEvent(self, event):
        self.move_to(self.cube1, 0)
        self.move_to(self.cube2, 0)
        self.move_to(self.cube3, 0)
        app.quit()

if __name__ == '__main__':
    app = QApplication([])
    app.setStyleSheet("QMainWindow {background-color: #333333; color: #ffffff;} "
                      "QPushButton {background-color: #555555; color: #ffffff;} "
                      "QLCDNumber {background-color: #222222; color: #00ff00;}")

    win = PowerControl()
    win.show()
    app.exec_()
