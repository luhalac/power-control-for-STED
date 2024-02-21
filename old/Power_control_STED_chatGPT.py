# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:46:38 2024

@author: Lucía Lopez
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
        
        # Initialize UI components
        self.init_ui()
        
    def init_ui(self):
        # Rename devices
        self.angle_lcd1 = self.ui.lcdNumber1
        self.angle_lcd2 = self.ui.lcdNumber2
        self.angle_lcd3 = self.ui.lcdNumber3
        
        
        # Connect buttons
        self.ui.pushButton_home1.clicked.connect(self.home_and_zero)
        self.ui.pushButton_jogup1.clicked.connect(lambda: self.move_by(5))
        self.ui.pushButton_jogupf1.clicked.connect(lambda: self.move_by(1))
        self.ui.pushButton_jogd1.clicked.connect(lambda: self.move_by(-5))
        self.ui.pushButton_jogdf1.clicked.connect(lambda: self.move_by(-1))
        self.ui.pushButton_setpower.clicked.connect(self.set_power)
        
        # Set initial position
        init_pos = self.cube1.get_position(channel=None, scale=True)
        init_angle = self.steps_to_deg(init_pos)
        self.update_angle_display(init_angle)
        
    def home_and_zero(self):    
        self.cube1.home(sync=True, force=False, channel=None, timeout=None)
        self.cube1.move_to(0, scale=True)
        self.update_angle_display(0)
            
    def deg_to_steps(self, deg):
        return 1923 * deg
    
    def steps_to_deg(self, steps):
        return steps / 1923
    
    def pow_to_ang(self, power):
        return power
    
    def ang_to_pow(self, angle):
        return angle
    
    def get_pos(self, cube):
        return self.cube1.get_position(channel=None, scale=True)
        
    def move_to(self, cube, angle):
        cube.move_to(self.deg_to_steps(angle), scale=True)
        self.update_angle_display(angle)

    def move_by(self, angle):
        current_pos = self.get_pos(self.cube1) 
        current_angle = self.steps_to_deg(current_pos)
        new_angle = current_angle + angle
        self.update_angle_display(new_angle)
        self.move_to(self.cube1, new_angle)

        
    def update_angle_display(self, angle):
        self.angle_lcd1.display(angle)
        
    def set_power(self, power):
        power = float(self.ui.lineEdit_setpower.text())
        angle = self.pow_to_ang(power)
        self.move_to(self.cube1, angle)
        self.update_angle_display(angle)
        
        
    def closeEvent(self, event):
        # Execute command upon closing the main window
        
        self.move_to(self.cube1, 0)
        # self.move_to(self.cube2, 0)
        # self.move_to(self.cube3, 0)
        # event.accept()  # Accept the event to close the window
        app.quit()  # Close the entire application process

if __name__ == '__main__':
    app = QApplication([])
    app.setStyleSheet("QMainWindow {background-color: #333333; color: #ffffff;} "
                      "QPushButton {background-color: #555555; color: #ffffff;} "
                      "QLCDNumber {background-color: #222222; color: #00ff00;}")

    win = PowerControl()
    win.show()
    app.exec_()
