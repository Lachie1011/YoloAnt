# Form implementation generated from reading ui file 'yoloAnt.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(862, 682)
        MainWindow.setIconSize(QtCore.QSize(30, 30))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setStyleSheet("*{\n"
"    color: rgb(255, 255, 255);\n"
"    border: none;\n"
"    background-colour: transparent;\n"
"    background: none;\n"
"    padding: 0;\n"
"    margin: 0;\n"
"    colour: #ffffff;\n"
"}\n"
"\n"
"#centralwidget{\n"
"    background-color: rgb(45, 45, 45);\n"
"}\n"
"\n"
"#leftMenuSubContainer{\n"
"    background-color: #282828;\n"
"}\n"
"\n"
"#topMenuContainer{\n"
"    background-color: #282828;\n"
"}\n"
"\n"
"\n"
"#stageWidget{\n"
"    background-color: rgb(55, 55, 55);\n"
"}\n"
"\n"
"QPushButton{\n"
"    padding: 2px 5px;\n"
"}\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.stageWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.stageWidget.setGeometry(QtCore.QRect(50, 20, 811, 661))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stageWidget.sizePolicy().hasHeightForWidth())
        self.stageWidget.setSizePolicy(sizePolicy)
        self.stageWidget.setStyleSheet("")
        self.stageWidget.setObjectName("stageWidget")
        self.topMenuContainer = QtWidgets.QWidget(parent=self.centralwidget)
        self.topMenuContainer.setGeometry(QtCore.QRect(0, 0, 861, 21))
        self.topMenuContainer.setObjectName("topMenuContainer")
        self.menuWidget = QtWidgets.QWidget(parent=self.topMenuContainer)
        self.menuWidget.setGeometry(QtCore.QRect(0, 0, 51, 21))
        self.menuWidget.setObjectName("menuWidget")
        self.label = QtWidgets.QLabel(parent=self.menuWidget)
        self.label.setGeometry(QtCore.QRect(10, 0, 31, 21))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("icons/ant_image.jpg"))
        self.label.setObjectName("label")
        self.frame = QtWidgets.QFrame(parent=self.topMenuContainer)
        self.frame.setGeometry(QtCore.QRect(49, -1, 811, 21))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.leftMenuSubContainer = QtWidgets.QWidget(parent=self.centralwidget)
        self.leftMenuSubContainer.setGeometry(QtCore.QRect(0, 21, 51, 661))
        self.leftMenuSubContainer.setStyleSheet("border-right-color: rgb(90, 90, 90);\n"
"border-top-color: rgb(90, 90, 90);\n"
"")
        self.leftMenuSubContainer.setObjectName("leftMenuSubContainer")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.leftMenuSubContainer)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.selectorsWidget = QtWidgets.QFrame(parent=self.leftMenuSubContainer)
        self.selectorsWidget.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.selectorsWidget.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.selectorsWidget.setObjectName("selectorsWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.selectorsWidget)
        self.verticalLayout_3.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.mousePointer = QtWidgets.QPushButton(parent=self.selectorsWidget)
        self.mousePointer.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/selector.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.mousePointer.setIcon(icon)
        self.mousePointer.setIconSize(QtCore.QSize(30, 30))
        self.mousePointer.setObjectName("mousePointer")
        self.verticalLayout_3.addWidget(self.mousePointer, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.moveTool = QtWidgets.QPushButton(parent=self.selectorsWidget)
        self.moveTool.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/movetoolicon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.moveTool.setIcon(icon1)
        self.moveTool.setIconSize(QtCore.QSize(30, 30))
        self.moveTool.setObjectName("moveTool")
        self.verticalLayout_3.addWidget(self.moveTool, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout.addWidget(self.selectorsWidget, 0, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.shapeSelectWidget = QtWidgets.QFrame(parent=self.leftMenuSubContainer)
        self.shapeSelectWidget.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.shapeSelectWidget.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.shapeSelectWidget.setObjectName("shapeSelectWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.shapeSelectWidget)
        self.verticalLayout_4.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.rectangleSelect = QtWidgets.QPushButton(parent=self.shapeSelectWidget)
        self.rectangleSelect.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/rectangleicon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.rectangleSelect.setIcon(icon2)
        self.rectangleSelect.setIconSize(QtCore.QSize(30, 30))
        self.rectangleSelect.setObjectName("rectangleSelect")
        self.verticalLayout_4.addWidget(self.rectangleSelect)
        self.verticalLayout.addWidget(self.shapeSelectWidget)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.infoWidget = QtWidgets.QFrame(parent=self.leftMenuSubContainer)
        self.infoWidget.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.infoWidget.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.infoWidget.setObjectName("infoWidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.infoWidget)
        self.verticalLayout_5.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.infoButton = QtWidgets.QPushButton(parent=self.infoWidget)
        self.infoButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/infoicon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.infoButton.setIcon(icon3)
        self.infoButton.setIconSize(QtCore.QSize(30, 30))
        self.infoButton.setObjectName("infoButton")
        self.verticalLayout_5.addWidget(self.infoButton)
        self.verticalLayout.addWidget(self.infoWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.mousePointer.setToolTip(_translate("MainWindow", "Selection tool to select annotation"))
        self.moveTool.setToolTip(_translate("MainWindow", "Move tool to select and move annotation"))
        self.rectangleSelect.setToolTip(_translate("MainWindow", "draw rectanglular shaped annotation"))
        self.infoButton.setToolTip(_translate("MainWindow", "Get more info on annotator "))
