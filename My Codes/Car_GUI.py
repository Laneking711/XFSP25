# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'Car_GUI.ui'
# Created by: PyQt5 UI code generator 5.15.4

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1143, 959)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # === Input Group ===
        self.grp_Inputs = QtWidgets.QGroupBox(Form)
        self.grp_Inputs.setMaximumSize(QtCore.QSize(600, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.grp_Inputs.setFont(font)
        self.grp_Inputs.setTitle("Model Inputs")
        self.gridLayout = QtWidgets.QGridLayout(self.grp_Inputs)

        def add_labeled_edit(row, label_text, name, default_text):
            label = QtWidgets.QLabel(self.grp_Inputs)
            label.setText(label_text)
            edit = QtWidgets.QLineEdit(self.grp_Inputs)
            edit.setObjectName(name)
            edit.setText(default_text)
            edit.setMinimumSize(QtCore.QSize(75, 0))
            edit.setMaximumSize(QtCore.QSize(150, 16777215))
            edit.setFont(font)
            self.gridLayout.addWidget(label, row, 0, alignment=QtCore.Qt.AlignRight)
            self.gridLayout.addWidget(edit, row, 1)
            setattr(self, name, edit)

        add_labeled_edit(0, "Car body mass (m1, kg)", "le_m1", "450")
        add_labeled_edit(1, "Car Speed (kph)", "le_v", "120")
        add_labeled_edit(2, "Suspension Spring (k1, N/m)", "le_k1", "15000")
        add_labeled_edit(3, "Suspension Shock Absorber (c1, N*s/m)", "le_c1", "4500")
        add_labeled_edit(4, "Wheel mass (m2, kg)", "le_m2", "20")
        add_labeled_edit(5, "Tire spring constant (k2, N/m)", "le_k2", "90000")
        add_labeled_edit(6, "Ramp Angle (deg)", "le_ang", "45")
        add_labeled_edit(7, "t, max plot (s)", "le_tmax", "3")

        self.chk_LogX = QtWidgets.QCheckBox("log scale t", self.grp_Inputs)
        self.chk_LogY = QtWidgets.QCheckBox("log scale Y", self.grp_Inputs)
        self.chk_LogAccel = QtWidgets.QCheckBox("log scale Y''", self.grp_Inputs)
        hlog = QtWidgets.QHBoxLayout()
        hlog.addWidget(self.chk_LogX)
        hlog.addWidget(self.chk_LogY)
        hlog.addWidget(self.chk_LogAccel)
        self.gridLayout.addLayout(hlog, 9, 0, 1, 2)

        self.chk_ShowAccel = QtWidgets.QCheckBox("Plot Car Accel.", self.grp_Inputs)
        self.gridLayout.addWidget(self.chk_ShowAccel, 11, 0, 1, 2, alignment=QtCore.Qt.AlignRight)

        self.chk_IncludeAccel = QtWidgets.QCheckBox("Include Accel in Opt.", self.grp_Inputs)
        self.gridLayout.addWidget(self.chk_IncludeAccel, 12, 0, 1, 2, alignment=QtCore.Qt.AlignRight)

        self.lbl_MaxMinInfo = QtWidgets.QLabel("TextLabel", self.grp_Inputs)
        self.gridLayout.addWidget(self.lbl_MaxMinInfo, 14, 0, 1, 2, alignment=QtCore.Qt.AlignRight)

        self.gv_Schematic = QtWidgets.QGraphicsView(self.grp_Inputs)
        self.gv_Schematic.setMinimumSize(QtCore.QSize(500, 500))
        self.gv_Schematic.setMaximumSize(QtCore.QSize(600, 600))
        self.gridLayout.addWidget(self.gv_Schematic, 15, 0, 1, 2)

        self.btn_calculate = QtWidgets.QPushButton("Calculate", self.grp_Inputs)
        self.pb_Optimize = QtWidgets.QPushButton("Optimize Suspension", self.grp_Inputs)
        hbtn = QtWidgets.QHBoxLayout()
        hbtn.addWidget(self.btn_calculate)
        hbtn.addWidget(self.pb_Optimize)
        self.gridLayout.addLayout(hbtn, 8, 0, 1, 2)

        self.horizontalLayout.addWidget(self.grp_Inputs)

        # === Plot Layout ===
        self.layout_Plot = QtWidgets.QVBoxLayout()
        self.layout_Plot.setObjectName("layout_Plot")
        self.horizontalLayout.addLayout(self.layout_Plot)
        QtCore.QMetaObject.connectSlotsByName(Form)
