# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 15:11:25 2024

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
        
        # Initialize lists to store cubes and LCDs
        self.cubes = []
        self.angle_lcds = []
        
        # Connected Thorlabs kinesis/APT devices
        self.devices = Thorlabs.list_kinesis_devices()
        
        # Attempt to initialize cubes and associated UI components
        for idx, device in enumerate(self.devices):
            try:
                cube = Thorlabs.KinesisMotor(device[0])
                self.cubes.append(cube)
                self.angle_lcds.append(getattr(self.ui, f"lcdNumber{idx+1}"))
                
                # Initialize UI components for this cube
                self.init_ui(idx)
            except Exception as e:
                print(f"Error initializing cube {idx+1}: {e}")
        
    def init_ui(self, idx):
        # Connect buttons for this cube
        home_button = getattr(self.ui, f"pushButton_home{idx+1}")
        home_button.clicked.connect(lambda: self.home_and_zero(idx))
        
        jog_up_button = getattr(self.ui, f"pushButton_jogup{idx+1}")
        jog_up_button.clicked.connect(lambda: self.move_by(idx, 5))
        
        jog_down_button = getattr(self.ui, f"pushButton_jogdown{idx+1}")
        jog_down_button.clicked.connect(lambda: self.move_by(idx, -5))
        
        jog_up_fine_button = getattr(self.ui, f"pushButton_jogupf{idx+1}")
        jog_up_fine_button.clicked.connect(lambda: self.move_by(idx, 1))
        
        jog_down_fine_button = getattr(self.ui, f"pushButton_jogdownf{idx+1}")
        jog_down_fine_button.clicked.connect(lambda: self.move_by(idx, -1))
        
        # Connect set power button
        self.ui.pushButton_setpower.clicked.connect(self.set_power)
        
        # Set initial position for this cube
        init_pos = self.cubes[idx].get_position(channel=None, scale=True)
        init_angle = self.steps_to_deg(init_pos)
        self.update_angle_display(init_angle, idx)
        
    def home_and_zero(self, idx):
        self.cubes[idx].home(sync=True, force=False, channel=None, timeout=None)
        self.cubes[idx].move_to(0, scale=True)
        self.update_angle_display(0, idx)
        
    def deg_to_steps(self, deg):
        return 1923 * deg
    
    def steps_to_deg(self, steps):
        return steps / 1923
    
    def get_pos(self, idx):
        return self.cubes[idx].get_position(channel=None, scale=True)
        
    def move_to(self, idx, angle):
        self.cubes[idx].move_to(self.deg_to_steps(angle), scale=True)
        self.update_angle_display(angle, idx)

    def move_by(self, idx, angle_change):
        current_pos = self.get_pos(idx)
        current_angle = self.steps_to_deg(current_pos)
        new_angle = current_angle + angle_change
        self.update_angle_display(new_angle, idx)
        self.move_to(idx, new_angle)

    def update_angle_display(self, angle, idx):
        self.angle_lcds[idx].display(angle)
        
    def set_power(self):
        power = float(self.ui.lineEdit_setpower.text())
        for idx, cube in enumerate(self.cubes):
            angle = self.pow_to_ang(power)
            self.move_to(idx, angle)
            self.update_angle_display(angle, idx)
        
    def closeEvent(self, event):
        for idx, cube in enumerate(self.cubes):
            self.move_to(idx, 0)
        app.quit()

if __name__ == '__main__':
    app = QApplication([])
    app.setStyleSheet("QMainWindow {background-color: #333333; color: #ffffff;} "
                      "QPushButton {background-color: #555555; color: #ffffff;} "
                      "QLCDNumber {background-color: #222222; color: #00ff00;}")

    win = PowerControl()
    win.show()
    app.exec_()

