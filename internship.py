# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form1.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


import cv2
import numpy as np
import argparse
from matplotlib import pyplot as plt
import imutils
from PyQt5 import QtCore, QtGui, QtWidgets
import sysv_ipc as ipc
import sys
import polling2
import threading
import os


# GLOBAL VARS
speck_size = 0
threshold = 0
specks_selected = False
holes_selected = False
fibers_selected = False
all_selected = False
specks_craft_selected = False
camera_resolution = 0.076
#current_image_index = 0
#files = []
size = int(11000*4096*3)  #134217728 #122884000  #61440000
key = None #for shared memory
shm = None # for shared memory
is_valid_image = 48
img_size = 6000*4096*3
t1 = None #thread
capture_flag = False # High when capture button is clicked
first_live = True
#FOR STORING THE CAPTURED IMAGE
temp_img = np.zeros([10000, 4096, 3], dtype=np.uint8)
temp_img_bin = np.zeros([10000, 4096, 3], dtype=np.uint8)
app_closed = False


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1850, 900)
        MainWindow.setGeometry(0,0,1850,900)
        MainWindow.setStyleSheet("background-color: rgb(14, 19, 122);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.liveFeed = QtWidgets.QLabel(self.centralwidget)
        self.liveFeed.setGeometry(QtCore.QRect(80, 200, 1281, 511))
        self.liveFeed.setStyleSheet("background: #000000\n"
"")
        self.liveFeed.setText("")
        self.liveFeed.setObjectName("liveFeed")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(1400, 150, 371, 561))
        self.frame.setStyleSheet("background-color: rgb(14, 19, 122);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.update_push_button = QtWidgets.QPushButton(self.frame)
        self.update_push_button.setGeometry(QtCore.QRect(20, 280, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.update_push_button.setFont(font)
        self.update_push_button.setStyleSheet("background: rgb(114, 159, 207)")
        self.update_push_button.setObjectName("update_push_button")
        self.inspection_settings_label = QtWidgets.QLabel(self.frame)
        self.inspection_settings_label.setGeometry(QtCore.QRect(90, 20, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.inspection_settings_label.setFont(font)
        self.inspection_settings_label.setObjectName("inspection_settings_label")
        self.run_push_button = QtWidgets.QPushButton(self.frame)
        self.run_push_button.setGeometry(QtCore.QRect(20, 370, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.run_push_button.setFont(font)
        self.run_push_button.setStyleSheet("background-color: rgb(115, 210, 22);")
        self.run_push_button.setObjectName("run_push_button")
        self.stop_push_button = QtWidgets.QPushButton(self.frame)
        self.stop_push_button.setGeometry(QtCore.QRect(20, 460, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.stop_push_button.setFont(font)
        self.stop_push_button.setStyleSheet("background-color: rgb(204, 0, 0);")
        self.stop_push_button.setObjectName("stop_push_button")
        self.defect_list = QtWidgets.QComboBox(self.frame)
        #items_defect_list = self.defect_list.lineEdit()
        #items_defect_list.setAlignment(Qt.AlignCenter)
        self.defect_list.setEditable(True)
        self.defect_list.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.defect_list.lineEdit().setReadOnly(True)
        self.defect_list.setGeometry(QtCore.QRect(20, 100, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.defect_list.lineEdit().setFont(font)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.defect_list.setFont(font)
        self.defect_list.setStyleSheet("selection-background-color: rgb(114, 159, 207);\n"
"background-color: rgb(114, 159, 207);\n"
"")
        self.defect_list.setObjectName("defect_list")
        self.defect_list.addItem("")
        self.defect_list.addItem("")
        self.defect_list.addItem("")
        self.defect_list.addItem("")
        self.defect_list.addItem("")
        self.defect_list.addItem("")
        self.speck_size_label = QtWidgets.QLabel(self.frame)
        self.speck_size_label.setGeometry(QtCore.QRect(10, 170, 100, 16)) #position_x , y width, height
        self.speck_size_label.setStyleSheet("background-color: rgb(114, 159, 207);")
        self.speck_size_label.setTextFormat(QtCore.Qt.RichText)
        self.speck_size_label.setObjectName("speck_size_label")
        self.speck_size_slider = QtWidgets.QSlider(self.frame)
        self.speck_size_slider.setGeometry(QtCore.QRect(10, 190, 331, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.speck_size_slider.setPalette(palette)
        self.speck_size_slider.setMouseTracking(True)
        self.speck_size_slider.setTabletTracking(False)
        self.speck_size_slider.setStyleSheet("background-color: rgb(114, 159, 207);")
        self.speck_size_slider.setMinimum(100)
        self.speck_size_slider.setMaximum(2000)
        self.speck_size_slider.setOrientation(QtCore.Qt.Horizontal)
        self.speck_size_slider.setObjectName("speck_size_slider")
        self.threshold_label = QtWidgets.QLabel(self.frame)
        self.threshold_label.setGeometry(QtCore.QRect(10, 220, 100, 16))
        self.threshold_label.setStyleSheet("background-color: rgb(114, 159, 207);")
        self.threshold_label.setObjectName("threshold_label")
        self.threshold_slider = QtWidgets.QSlider(self.frame)
        self.threshold_slider.setGeometry(QtCore.QRect(10, 240, 331, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(196, 225, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(155, 192, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(57, 79, 103))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 106, 138))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(184, 207, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(196, 225, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(155, 192, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(57, 79, 103))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 106, 138))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(184, 207, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(57, 79, 103))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(196, 225, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(155, 192, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(57, 79, 103))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 106, 138))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(57, 79, 103))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(57, 79, 103))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.threshold_slider.setPalette(palette)
        self.threshold_slider.setMouseTracking(True)
        self.threshold_slider.setTabletTracking(False)
        self.threshold_slider.setStyleSheet("background-color: rgb(114, 159, 207);\n"
"font: 11pt \"Ubuntu\";")
        self.threshold_slider.setMaximum(99)
        self.threshold_slider.setOrientation(QtCore.Qt.Horizontal)
        self.threshold_slider.setObjectName("threshold_slider")
        # Enbale this after figuring out threshold function
        self.threshold_slider.setEnabled(False)
        self.speck_size = QtWidgets.QLabel(self.frame)
        self.speck_size.setGeometry(QtCore.QRect(330, 190, 33, 21))
        self.speck_size.setStyleSheet("background-color: rgb(114, 159, 207);")
        self.speck_size.setObjectName("speck_size")
        self.threshold = QtWidgets.QLabel(self.frame)
        self.threshold.setGeometry(QtCore.QRect(330, 240, 33, 21))
        self.threshold.setStyleSheet("background-color: rgb(114, 159, 207);")
        self.threshold.setObjectName("threshold")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(10, 70, 1801, 851))
        self.frame_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.inspection_report_button = QtWidgets.QPushButton(self.frame_2)
        self.inspection_report_button.setGeometry(QtCore.QRect(1420, 670, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.inspection_report_button.setFont(font)
        self.inspection_report_button.setStyleSheet("background-color: rgb(78, 154, 6);")
        self.inspection_report_button.setObjectName("inspection_report_button")
        self.layoutWidget = QtWidgets.QWidget(self.frame_2)
        self.layoutWidget.setGeometry(QtCore.QRect(71, 670, 1281, 60))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.web_speed_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.web_speed_label.setFont(font)
        self.web_speed_label.setStyleSheet("background:rgb(255,255,255)")
        self.web_speed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.web_speed_label.setObjectName("web_speed_label")
        self.verticalLayout.addWidget(self.web_speed_label)
        self.web_speed_count = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.web_speed_count.setFont(font)
        self.web_speed_count.setStyleSheet("background:rgb(114, 159, 207)")
        self.web_speed_count.setAlignment(QtCore.Qt.AlignCenter)
        self.web_speed_count.setObjectName("web_speed_count")
        self.verticalLayout.addWidget(self.web_speed_count)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.specks_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.specks_label.setFont(font)
        self.specks_label.setStyleSheet("background:rgb(255,255,255)")
        self.specks_label.setAlignment(QtCore.Qt.AlignCenter)
        self.specks_label.setObjectName("specks_label")
        self.verticalLayout_2.addWidget(self.specks_label)
        self.specks_count = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.specks_count.setFont(font)
        self.specks_count.setStyleSheet("background:rgb(114, 159, 207)")
        self.specks_count.setAlignment(QtCore.Qt.AlignCenter)
        self.specks_count.setObjectName("specks_count")
        self.verticalLayout_2.addWidget(self.specks_count)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.holes_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.holes_label.setFont(font)
        self.holes_label.setStyleSheet("background:rgb(255,255,255)")
        self.holes_label.setAlignment(QtCore.Qt.AlignCenter)
        self.holes_label.setObjectName("holes_label")
        self.verticalLayout_3.addWidget(self.holes_label)
        self.holes_count = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.holes_count.setFont(font)
        self.holes_count.setStyleSheet("background:rgb(114, 159, 207)")
        self.holes_count.setAlignment(QtCore.Qt.AlignCenter)
        self.holes_count.setObjectName("holes_count")
        self.verticalLayout_3.addWidget(self.holes_count)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.fibers_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.fibers_label.setFont(font)
        self.fibers_label.setStyleSheet("background:rgb(255,255,255)")
        self.fibers_label.setAlignment(QtCore.Qt.AlignCenter)
        self.fibers_label.setObjectName("fibers_label")
        self.verticalLayout_4.addWidget(self.fibers_label)
        self.fibers_count = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.fibers_count.setFont(font)
        self.fibers_count.setStyleSheet("background:rgb(114, 159, 207)")
        self.fibers_count.setAlignment(QtCore.Qt.AlignCenter)
        self.fibers_count.setObjectName("fibers_count")
        self.verticalLayout_4.addWidget(self.fibers_count)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.brightness_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.brightness_label.setFont(font)
        self.brightness_label.setStyleSheet("background:rgb(255,255,255)")
        self.brightness_label.setAlignment(QtCore.Qt.AlignCenter)
        self.brightness_label.setObjectName("brightness_label")
        self.verticalLayout_5.addWidget(self.brightness_label)
        self.brightness_count = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.brightness_count.setFont(font)
        self.brightness_count.setStyleSheet("background:rgb(114, 159, 207)")
        self.brightness_count.setAlignment(QtCore.Qt.AlignCenter)
        self.brightness_count.setObjectName("brightness_count")
        self.verticalLayout_5.addWidget(self.brightness_count)
        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.speck_density_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.speck_density_label.setFont(font)
        self.speck_density_label.setStyleSheet("background:rgb(255,255,255)")
        self.speck_density_label.setAlignment(QtCore.Qt.AlignCenter)
        self.speck_density_label.setObjectName("speck_density_label")
        self.verticalLayout_6.addWidget(self.speck_density_label)
        self.speck_density_count = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.speck_density_count.setFont(font)
        self.speck_density_count.setStyleSheet("background:rgb(114, 159, 207)")
        self.speck_density_count.setAlignment(QtCore.Qt.AlignCenter)
        self.speck_density_count.setObjectName("speck_density_count")
        self.verticalLayout_6.addWidget(self.speck_density_count)
        self.horizontalLayout.addLayout(self.verticalLayout_6)

        self.layoutWidget1 = QtWidgets.QWidget(self.frame_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(70, 60, 451, 71))  # (70, 60, 751, 71) if previous and next butttons are present
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.live_feed = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.live_feed.setFont(font)
        self.live_feed.setStyleSheet("background: rgb(114, 159, 207)")
        self.live_feed.setObjectName("live_feed")
        self.horizontalLayout_4.addWidget(self.live_feed)
        self.capture_button = QtWidgets.QPushButton(self.layoutWidget1)

        font = QtGui.QFont()
        font.setPointSize(15)
        self.capture_button.setFont(font)
        self.capture_button.setStyleSheet("background: rgb(114, 159, 207)")
        self.capture_button.setObjectName("capture_button")
        self.horizontalLayout_4.addWidget(self.capture_button)


        """self.previous_image = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.previous_image.setFont(font)
        self.previous_image.setStyleSheet("background: rgb(114, 159, 207)")
        self.previous_image.setObjectName("previous_image")
        self.horizontalLayout_4.addWidget(self.previous_image)
        self.current_image_label = QtWidgets.QLabel(self.layoutWidget1)
        self.current_image_label.setObjectName("current_image_label")
        self.horizontalLayout_4.addWidget(self.current_image_label)
        self.next_image = QtWidgets.QPushButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.next_image.setFont(font)
        self.next_image.setStyleSheet("background: rgb(114, 159, 207)")
        self.next_image.setObjectName("next_image")
        self.horizontalLayout_4.addWidget(self.next_image) """



        self.company_logo = QtWidgets.QLabel(self.centralwidget)
        self.company_logo.setGeometry(QtCore.QRect(1600, 10, 131, 41))
        self.company_logo.setObjectName("company_logo")
        self.frame_2.raise_()
        self.liveFeed.raise_()
        self.frame.raise_()
        self.company_logo.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.speck_size_slider.valueChanged['int'].connect(self.speck_size.setNum)
        self.threshold_slider.valueChanged['int'].connect(self.threshold.setNum)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.update_push_button.setText(_translate("MainWindow", "UPDATE"))
        self.inspection_settings_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">INSPECTION SETTINGS</span></p></body></html>"))
        self.run_push_button.setText(_translate("MainWindow", "RUN"))
        self.stop_push_button.setText(_translate("MainWindow", "STOP"))
        self.defect_list.setCurrentText(_translate("MainWindow", "DEFECT LIST"))
        self.defect_list.setItemText(0, _translate("MainWindow", "DEFECT LIST"))
        self.defect_list.setItemText(1, _translate("MainWindow", "SPECKS"))
        self.defect_list.setItemText(2, _translate("MainWindow", "HOLES"))
        self.defect_list.setItemText(3, _translate("MainWindow", "FIBER"))
        self.defect_list.setItemText(4, _translate("MainWindow", "ALL"))
        self.defect_list.setItemText(5, _translate("MainWindow", "SPECKS(KRAFT)"))
        self.speck_size_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">SIZE (microns)</span></p></body></html>"))
        self.threshold_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">THRESHOLD</span></p></body></html>"))
        self.speck_size.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">0</p></body></html>"))
        self.threshold.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">0</p></body></html>"))
        #self.current_image_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">CURRENT IMAGE</p></body></html>"))
        #self.previous_image.setText(_translate("MainWindow", "PREVIOUS"))
        #self.next_image.setText(_translate("MainWindow", "NEXT"))
        self.inspection_report_button.setText(_translate("MainWindow", "INSPECTION REPORT"))
        self.web_speed_label.setText(_translate("MainWindow", "WEB SPEED"))
        self.web_speed_count.setText(_translate("MainWindow", "NA"))
        self.specks_label.setText(_translate("MainWindow", "SPECKS"))
        self.specks_count.setText(_translate("MainWindow", "0"))
        self.holes_label.setText(_translate("MainWindow", "HOLES"))
        self.holes_count.setText(_translate("MainWindow", "0"))
        self.fibers_label.setText(_translate("MainWindow", "FIBERS"))
        self.fibers_count.setText(_translate("MainWindow", "0"))
        self.brightness_label.setText(_translate("MainWindow", "BRIGHTNESS LEVEL"))
        self.brightness_count.setText(_translate("MainWindow", "NA"))
        self.speck_density_label.setText(_translate("MainWindow", "SPECK DENSITY"))
        self.speck_density_count.setText(_translate("MainWindow", "0"))
        self.live_feed.setText(_translate("MainWindow", "LIVE FEED"))
        self.capture_button.setText(_translate("MainWindow", "CAPTURE"))
        """self.image_selector.setCurrentText(_translate("MainWindow", "IMAGE SELECTOR"))
        self.image_selector.setItemText(0, _translate("MainWindow", "/home/srikar/paper/CAM0/imageCaptureCAM0_0.bmp"))
        self.image_selector.setItemText(1, _translate("MainWindow", "/home/srikar/paper/CAM0/imageCaptureCAM0_1.bmp"))
        self.image_selector.setItemText(2, _translate("MainWindow", "/home/srikar/paper/CAM0/imageCaptureCAM0_2.bmp"))
        self.image_selector.setItemText(3, _translate("MainWindow", "/home/srikar/paper/CAM0/imageCaptureCAM0_3.bmp"))
        self.image_selector.setItemText(4, _translate("MainWindow", "/home/srikar/paper/CAM0/imageCaptureCAM0_4.bmp"))
        """
        #self.company_logo.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; color:#ffffff;\">YantraVision</span></p></body></html>"))
        self.company_logo.setPixmap(QtGui.QPixmap("YVlogo.png"))
        self.company_logo.setScaledContents(True)
        #self.load_files()
        #self.current_image_label.setText("          "+files[current_image_index])
        self.capture_button.clicked.connect(self.capture_and_stop_live)
        self.update_push_button.clicked.connect(self.update_params)        
        #self.next_image.clicked.connect(self.next_file)        
        #self.previous_image.clicked.connect(self.previous_file)        
        self.live_feed.clicked.connect(self.show_live_feed)
        self.run_push_button.clicked.connect(self.start_frame_grabber)


    def start_frame_grabber(self):
        os.system('cd /home/yv/srikar/PrintInspectionTriggerDesign/frameGrabberModuleV2 && ./run.sh && cd -')
        #res = command.run(['/home/srikar/PrintInspectionTriggerDesign/frameGrabberModuleV2/run.sh'])

        #print(res.output)
 

    def show_live_feed(self):
        global t1
        global first_live
        global capture_flag
        if first_live:
            t1 = threading.Thread(target=self.start_live_feed)
            t1.start()
            first_live = False
            if capture_flag == True:
                capture_flag = False
        else:
            capture_flag = False
        global key
        global shm
        global size
        key = ipc.ftok("/tmp", 65)
        shm = ipc.SharedMemory(key, 0, ipc.IPC_CREAT, size)
        shm.attach()
        shm.write(bytes('0', 'utf-8'),img_size+4)
        print("SHM IS ATTACHED")

    def capture_and_stop_live(self):
        global capture_flag
        global t1
        #global img1
        global temp_img
        global temp_img_bin
        capture_flag = True
        #temp_img = img1
        cv2.namedWindow("captured_image", cv2.WINDOW_NORMAL)
        print("\nSHOWING CAPTURED IMAGE\n")
        cv2.resizeWindow("captured_image",800, 600)
        cv2.imshow("captured_image",temp_img)
        image1 = cv2.cvtColor(temp_img, cv2.COLOR_BGR2RGB)
        height0,width0,channel0 = image1.shape
        bytes_per_line = channel0 * width0
        qImg = QtGui.QImage(image1.data, width0, height0, bytes_per_line, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(qImg)
        self.liveFeed.setPixmap(pix)
        self.liveFeed.setScaledContents(True)

        #t1.join()
        #self.show_image(img1)

    def start_live_feed(self):      
        print("STARTING LIVE FEED")
        global capture_flag
        global is_valid_image
        global img_size
        global app_closed
        global shm
        print("validity = ", is_valid_image)
       # print("validity = ", type(is_valid_image))
        while(True):
            while(is_valid_image == 48):
                global shm
                #print("READING IMAGE FROM MEMORY")
                if(shm != None):
                    isValidImage =  shm.read(4, img_size+4) #stays here as long as valid bit = 0(ascii 48)
                    is_valid_image = int(isValidImage[0])
                #print("inner loop valid",is_valid_image)
            print("next image sent")
            self.show_image()
            if app_closed:
                print("is app closed ?",app_closed)
                if (shm != None):
                    shm.write(bytes('1', 'utf-8'),img_size+4)
                    break
            # IF SOME BUTTON PRESSED, BREAK
        print("STOPPED LIVE FEED")
        #print(app_closed)
       
     # will mark specks and holes
    def thresholding_algorithm(self , image):
        #global img1
        img1 = np.array(image, dtype=np.uint8)
        img1 = img1[0:4587, 600:3500]
        img1 = cv2.rotate(img1,cv2.ROTATE_90_CLOCKWISE)
        width = img1.shape[0]
        height = img1.shape[1]
        #print(img)
        #img1 = cv2.resize(img1, (1000, 1000),interpolation = cv2.INTER_NEAREST)
        #cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        #cv2.resizeWindow("image",800, 600)
        #cv2.imshow("image",img1)
        img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img = cv2.blur(img, (11,11),cv2.BORDER_DEFAULT) # VERY SENSITIVE
        #cv2.namedWindow("B&W", cv2.WINDOW_NORMAL)
        #cv2.resizeWindow("B&W",800, 600)
        #cv2.imshow("B&W",img)
        #THRESHOLDING
        global threshold
        const = (threshold * 2.1) / 100
        mean_threshold = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2.1)
        #DILATING
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 13))
        #th2 = mean_threshold
        th2 = cv2.bitwise_not(mean_threshold)
        th2 = cv2.dilate(th2,kernel,iterations = 1)
        th2 = cv2.bitwise_not(th2)
        #cv2.namedWindow("mean threshold", cv2.WINDOW_NORMAL)
        #cv2.resizeWindow("mean threshold",800, 600)
        #cv2.imshow("mean threshold",th2)
       
        #FINDING CONTOURS
        MAX_COUNTOUR_AREA = (width - 10) * (height - 10)
        # Page fill at least 30% of image, then saving max area found
        maxAreaFound = MAX_COUNTOUR_AREA * 0.3
        # Saving page contour
        pageContour = np.array([[[5, 5]], [[5, height-5]], [[width-5, height-5]], [[width-5, 5]]])
        doc_cnts = pageContour
        cnts1 = cv2.findContours(th2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnts1 = imutils.grab_contours(cnts1)
        cnts1 = sorted(cnts1, key=cv2.contourArea, reverse=True)
        """ for c in cnts1:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.05*peri, True) #Increase 0.05 to any other higher value for discarding even more points and make better approximations
            if len(approx) ==4 and cv2.contourArea(approx)>maxAreaFound:
                doc_cnts = approx
                break"""
        #print("paper border cordinates",doc_cnts)
        #cv2.drawContours(img1, doc_cnts, -1, (255,255,255), 100)
        speck_count = 0
        hole_count = 0
        # Change the min and max sizes to identify smaller and biggers specks
        global speck_size
        min_area_speck = speck_size
        min_area_hole = 2022
        #max_area_speck = speck_size+50
        max_area_hole = 10000
        for c in cnts1:
            if min_area_speck < cv2.contourArea(c) < min_area_hole:
                x,y,w,h = cv2.boundingRect(c)
                #if cv2.pointPolygonTest(doc_cnts,(x,y),False) == 1 and (specks_selected or all_selected):
                if (specks_selected or all_selected):
                    cv2.rectangle(img1, (x-5, y-5), (x+w+5, y+h+5), (0, 255, 0), 2)
                    speck_count += 1
            if min_area_hole<cv2.contourArea(c): #<max_area:
                x,y,w,h = cv2.boundingRect(c)
                #if cv2.pointPolygonTest(doc_cnts,(x,y),False) == 1  and (holes_selected or all_selected or fibers_selected):
                if (holes_selected or all_selected or fibers_selected):
                    cv2.rectangle(img1, (x-5, y-5), (x+w+5, y+h+5), (0, 0, 255), 2)
                    hole_count += 1
        print("number of specks = ",speck_count)
        print("number of holes = ",hole_count)
        #cv2.namedWindow("final", cv2.WINDOW_NORMAL)
        #cv2.resizeWindow("final",800, 600)
        #cv2.imshow("final",img1)
        #image1 = cv2.resize(img1, (self.liveFeed.width(),self.liveFeed.height()),interpolation = cv2.INTER_NEAREST)
        #img1 = cv2.rotate(img1, cv2.ROTATE_90_CLOCKWISE)
 
        image1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        height0,width0,channel0 = image1.shape
        bytes_per_line = channel0 * width0
        global capture_flag
        global temp_img
        if (capture_flag==False):
            temp_img = img1
            qImg = QtGui.QImage(image1.data, width0, height0, bytes_per_line, QtGui.QImage.Format_RGB888)
            pix = QtGui.QPixmap(qImg)
            self.liveFeed.setPixmap(pix)
            self.liveFeed.setScaledContents(True)
            paper_length_in_camera = max( abs(doc_cnts[1][0][1] - doc_cnts[0][0][1]) , abs(doc_cnts[2][0][1] - doc_cnts[0][0][1]) , abs(doc_cnts[2][0][1] - doc_cnts[1][0][1]) , abs(doc_cnts[3][0][1] - doc_cnts[0][0][1]) , abs(doc_cnts[3][0][1] - doc_cnts[1][0][1]) , abs(doc_cnts[3][0][1] - doc_cnts[2][0][1]))
            #paper_length = (paper_length_in_camera * camera_resolution)/1000
            paper_length = 0.15 # METERS
            print("paper length = ",paper_length*100," CM")
            speck_density = round(speck_count/paper_length,4)
            self.speck_density_count.setText(str(speck_density)+" specks/m^2")
            self.specks_count.setText(str(speck_count))
            self.holes_count.setText(str(hole_count))
            self.fibers_count.setText(str(hole_count))
        global is_valid_image
        is_valid_image = 48

    def craft_paper(self, image):
        global specks_craft_selected
        if specks_craft_selected:
            img1 = np.array(image, dtype=np.uint8)
            img1 = img1[0:4587, 600:3500]
            img1 = cv2.rotate(img1,cv2.ROTATE_90_CLOCKWISE)
            lower_black = np.array([0,0,0])
            upper_black = np.array([39,39,39]) #45,45,45 in BGR

            #FINDING A BINARY IMAGE IN WHICH VALUES WITHIN RANGE ARE 255 AND OTHERS 0
            black = cv2.inRange(img1, lower_black, upper_black)
           
            """width = img1.shape[0]
            height = img1.shape[1]
            MAX_COUNTOUR_AREA = (width - 10) * (height - 10)
            # Page fill at least 30% of image, then saving max area found
            maxAreaFound = MAX_COUNTOUR_AREA * 0.3
            # Saving page contour
            pageContour = np.array([[[5, 5]], [[5, height-5]], [[width-5, height-5]], [[width-5, 5]]])
            doc_cnts = pageContour
            black = cv2.bitwise_not(black)
            cnts1 = cv2.findContours(black,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cnts1 = imutils.grab_contours(cnts1)
            cnts1 = sorted(cnts1, key=cv2.contourArea, reverse=True)
           
            for c in cnts1:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.05*peri, True) #Increase 0.05 to any other higher value for discarding even more points and make better approximations
                if len(approx) ==4 and cv2.contourArea(approx)>maxAreaFound:
                    doc_cnts = approx
                    break
           # print("paper border cordinates",doc_cnts)
            #cv2.drawContours(img1, doc_cnts, -1, (255,255,255), 100)

            black = cv2.bitwise_not(black)"""
            #FINDING CONTOURS
            cnts1 = cv2.findContours(black,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cnts1 = imutils.grab_contours(cnts1)

            speck_count = 0
            hole_count = 0
            # Change the min and max sizes to identify smaller and biggers specks
            global speck_size
            min_area_speck = speck_size
            min_area_hole = 4500
            #max_area_speck = 90
            max_area_hole = 10000
            for c in cnts1:
                if min_area_speck < cv2.contourArea(c) < min_area_hole:
                    x,y,w,h = cv2.boundingRect(c)
                    #if cv2.pointPolygonTest(doc_cnts,(x,y),False) == 1:
                    cv2.rectangle(img1, (x-10, y-10), (x+w+10, y+h+10), (0,255, 0), 2)
                    speck_count += 1
                if min_area_hole<cv2.contourArea(c)<max_area_hole:
                    x,y,w,h = cv2.boundingRect(c)
                    #if cv2.pointPolygonTest(doc_cnts,(x,y),False) == 1:
                    cv2.rectangle(img1, (x-10, y-10), (x+w+10, y+h+10), (0, 255,0), 2)
                    hole_count += 1
            #cv2.namedWindow("final", cv2.WINDOW_NORMAL)
            #cv2.resizeWindow("final",800, 600)
            #cv2.imshow("final",img)
            #cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
            #cv2.resizeWindow("mask",800, 600)
            #cv2.imshow("mask",black)
            #paper_length = (paper_length_in_camera * camera_resolution)/1000
            #self.specks_count.setText(str(speck_count))
            #self.holes_count.setText(str(hole_count))
            #self.fibers_count.setText(str(hole_count))
            #print("PAPER LENGTH = ",paper_length*100," CM") #1.10 is to say that due to contouring and dilating 10% length might be lost
            #speck_density = round(speck_count/paper_length,4)
            #self.speck_density_count.setText(str(speck_density)+" specks/m^2")
            global capture_flag
            global temp_img
            #img1 = cv2.rotate(img1, cv2.ROTATE_90_CLOCKWISE)
            image1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            height0,width0,channel0 = image1.shape
            bytes_per_line = channel0 * width0
 
            if (capture_flag==False):
                temp_img = img1
                qImg = QtGui.QImage(image1.data, width0, height0, bytes_per_line, QtGui.QImage.Format_RGB888)
                pix = QtGui.QPixmap(qImg)
                self.liveFeed.setPixmap(pix)
                self.liveFeed.setScaledContents(True)
                paper_length_in_camera = max( abs(doc_cnts[1][0][1] - doc_cnts[0][0][1]) , abs(doc_cnts[2][0][1] - doc_cnts[0][0][1]) , abs(doc_cnts[2][0][1] - doc_cnts[1][0][1]) , abs(doc_cnts[3][0][1] - doc_cnts[0][0][1]) , abs(doc_cnts[3][0][1] - doc_cnts[1][0][1]) , abs(doc_cnts[3][0][1] - doc_cnts[2][0][1]))
                #paper_length = (paper_length_in_camera * camera_resolution)/1000
                #paper_length = 2463 * camera_resolution/1000
                paper_length = 0.15 # METERS
                print("paper length = ",paper_length*100," CM")
                speck_density = round(speck_count/paper_length,4)
                self.speck_density_count.setText(str(speck_density)+" specks/m^2")
                self.specks_count.setText(str(speck_count))
                self.holes_count.setText(str(hole_count))
                self.fibers_count.setText(str(hole_count))
            global is_valid_image
            is_valid_image = 48

 # will display image in liveFeed
    def show_image(self):
        global current_image_index
        global img_size
        global img1
        global shm
        #image_path = files[current_image_index]
        #image_path = "/home/srikar/paper/CAM1/imageCaptureCAM0_3.bmp" # CAN CHANGE
        #image_path = "/home/srikar/User_Interface_ori/Paper_insp/paper_1/imageCaptureCAM0_3.bmp" # CAN CHANGE
        #self.liveFeed.setPixmap(QtGui.QPixmap(image_path))
        #self.liveFeed.setScaledContents(True)
        #image = cv2.imread(image_path)
        if(shm != None):
           imgInfoBuff = shm.read(4)
           rows = (int( (imgInfoBuff[1] << 8) | imgInfoBuff[0]))
           cols = (int( (imgInfoBuff[3] << 8) | imgInfoBuff[2]))
           img_size = (rows *cols *3)
           imgBuff = shm.read(img_size, 4)
           img1 = np.frombuffer(imgBuff, np.uint8, img_size)
           #cv2.imwrite("after_read.bmp",img1)
           print(rows," ",cols)
        if img1 is None:
            print("No image")
        #cv2.namedWindow("image1", cv2.WINDOW_NORMAL)
        #cv2.resizeWindow("image1",800, 600)
        #cv2.imshow("image1",img)
        img1 = img1.reshape([rows, cols, 3])
        #print(int(isValidImage[0]))
        print("image is processing")
        if specks_craft_selected == True:
            self.craft_paper(img1)
        else:
            self.thresholding_algorithm(img1)
        if (shm!= None):
            shm.write(bytes('0', 'utf-8'),img_size+4)
   

    def update_params(self):
        global speck_size
        speck_size = self.speck_size_slider.value()
        global threshold
        threshold = self.threshold_slider.value()
        print("speck size selected = ", speck_size )
        print("threshold selected = ", threshold )
        global fibers_selected
        global specks_selecte
        global holes_selected
        global all_selected
        global specks_selected
        global specks_craft_selected
        if self.defect_list.currentText()=="SPECKS" :
            specks_selected =True
            holes_selected =False
            fibers_selected =False
            all_selected =False
            specks_craft_selected = False
       
        if self.defect_list.currentText()=="HOLES" :
            holes_selected =True
            specks_selected =False
            fibers_selected =False
            all_selected =False
            specks_craft_selected = False

        if self.defect_list.currentText()=="FIBER" :
            fibers_selected =True
            specks_selected =False
            holes_selected =False
            all_selected =False
            specks_craft_selected = False
       
        if self.defect_list.currentText()=="ALL" :
            all_selected =True
            holes_selected =False
            fibers_selected =False
            specks_selected =False
            specks_craft_selected = False
 
        if self.defect_list.currentText()=="SPECKS(KRAFT)" :
            all_selected = False
            holes_selected =False
            fibers_selected =False
            specks_selected =False
            specks_craft_selected = True


        if self.defect_list.currentText()=="DEFECT LIST" :
            all_selected =False
            holes_selected =False
            fibers_selected =False
            specks_selected =False
            specks_craft_selected = False
        print(self.defect_list.currentText()," \nis/are selected\n")

    """def load_files(self):
        global files
        files = ["image1.bmp", "image2.bmp", "image3.bmp", "image4.bmp", "image5.bmp", "image6.bmp"]
        if len(files) > 0:
            for file in files:
                pass
                #print(file)

    def next_file(self):
        global current_image_index
        if(current_image_index <= 4):
            current_image_index+=1
            print('next image click')
            self.current_image_label.setText("          "+files[current_image_index])
        else:
            print('end reached')

    def previous_file(self):
        global current_image_index
        if(current_image_index >= 1):
            current_image_index-=1
            print('previous image click')
            self.current_image_label.setText("          "+files[current_image_index])
        else:
            print('beginning reached')"""
