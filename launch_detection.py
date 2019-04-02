#!/usr/bin/env python

# Author       : Yaakoubi Oussama
# Organism     : Amac-Isir (In the scoop of the Dream project)
# Description  : This node is used to launch the detection of the interfaces

from PyQt5 import QtCore, QtGui, QtWidgets
from video_detection import *
import roslib
import rospy

class Ui_MainWindow(object):

    def __init__(self):
        self.detection = None
        self.translate = QtCore.QCoreApplication.translate
        self.buttons = ["greenButton", "redButton", "yellowButton", "blueButton"]


    # define callbacks

    def setVideoFeedSource(self, index):
        video_feed = self.feed_source.itemText(index)
        print(video_feed)
        self.detection.setVideoSource(video_feed.lower())

    def setInterface(self, index):
        interface = self.main_interface.itemText(index).lower()
        print interface
        if interface == "buttons interface":
            self.area_to_detect.addItem("")
            self.area_to_detect.setItemText(3, self.translate("MainWindow", "reward status area"))
            index = 1
            for button in self.buttons:
                self.area_to_detect.addItem("")
                self.area_to_detect.setItemText(3 + index, self.translate("MainWindow", button + " area"))
                index += 1
            self.detection = ButtonsDetection()
        else:
            self.area_to_detect.addItem("")
            self.area_to_detect.setItemText(3, self.translate("MainWindow", "status  area"))
            if interface == "modules interface":
                self.detection = ModulesDetection()
            elif interface == "box interface":
                self.detection = BoxDetection()

    def getFrame(self):
        area_to_detect = str(self.area_to_detect.currentText()).split(" ")[0]
        print "getting frame for", area_to_detect
        self.detection.showFrame(area_to_detect)

    def testDetection(self):
        area_to_detect = str(self.area_to_detect.currentText()).split(" ")[0]
        print "testing frame for", area_to_detect
        self.detection.testDetection(area_to_detect)

    def closeVideoFeed(self):
        self.detection.video.stopVideoFeed()

    def runDetection(self):
        self.detection.runDetection()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(951, 509)

        # central widget and grid layout
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.gridLayout = QtWidgets.QGridLayout(self.central_widget)
        self.gridLayout.setObjectName("gridLayout")

        # first row
        self.label_set_main_interface = QtWidgets.QLabel(self.central_widget)
        self.label_set_main_interface.setObjectName("label_set_main_interface")
        self.gridLayout.addWidget(self.label_set_main_interface, 0, 0, 1, 1)

        self.main_interface = QtWidgets.QComboBox(self.central_widget)
        self.main_interface.setObjectName("main_interface")
        self.main_interface.addItem("")
        self.main_interface.addItem("")
        self.main_interface.addItem("")
        self.main_interface.addItem("")
        self.gridLayout.addWidget(self.main_interface, 0, 2, 1, 1)
        self.main_interface.activated.connect(self.setInterface)

        # separation
        self.first_row_sep = QtWidgets.QFrame(self.central_widget)
        self.first_row_sep.setFrameShape(QtWidgets.QFrame.HLine)
        self.first_row_sep.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.first_row_sep.setObjectName("first_row_sep")
        self.gridLayout.addWidget(self.first_row_sep, 1, 0, 1, 5)

        # second row
        self.label_set_video_feed = QtWidgets.QLabel(self.central_widget)
        self.label_set_video_feed.setObjectName("label_set_video_feed")
        self.gridLayout.addWidget(self.label_set_video_feed, 2, 0, 1, 2)

        self.feed_source = QtWidgets.QComboBox(self.central_widget)
        self.feed_source.setObjectName("feed_source")
        self.feed_source.addItem("")
        self.feed_source.addItem("")
        self.feed_source.addItem("")
        self.gridLayout.addWidget(self.feed_source, 2, 2, 1, 1)
        self.feed_source.activated.connect(self.setVideoFeedSource)

        # separation
        self.second_row_sep = QtWidgets.QFrame(self.central_widget)
        self.second_row_sep.setFrameShape(QtWidgets.QFrame.HLine)
        self.second_row_sep.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.second_row_sep.setObjectName("second_row_sep")
        self.gridLayout.addWidget(self.second_row_sep, 3, 0, 1, 5)


        # third row
        self.label_set_area_to_detect = QtWidgets.QLabel(self.central_widget)
        self.label_set_area_to_detect.setObjectName("label_set_area_to_detect")
        self.gridLayout.addWidget(self.label_set_area_to_detect, 4, 0, 1, 1)

        self.area_to_detect = QtWidgets.QComboBox(self.central_widget)
        self.area_to_detect.setObjectName("area_to_detect")
        self.area_to_detect.addItem("")
        self.area_to_detect.addItem("")
        self.area_to_detect.addItem("")
        self.gridLayout.addWidget(self.area_to_detect, 4, 2, 1, 1)
        self.get_frame = QtWidgets.QPushButton(self.central_widget)
        self.get_frame.setObjectName("get_frame")
        self.gridLayout.addWidget(self.get_frame, 5, 2, 1, 1)
        self.get_frame.clicked.connect(self.getFrame)

        self.b_test_detection = QtWidgets.QPushButton(self.central_widget)
        self.b_test_detection.setObjectName("b_test_detection")
        self.gridLayout.addWidget(self.b_test_detection, 4, 4, 1, 1)
        self.b_test_detection.clicked.connect(self.testDetection)

        # separation
        self.third_row_sep = QtWidgets.QFrame(self.central_widget)
        self.third_row_sep.setFrameShape(QtWidgets.QFrame.HLine)
        self.third_row_sep.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.third_row_sep.setObjectName("third_row_sep")
        self.gridLayout.addWidget(self.third_row_sep, 7, 0, 1, 5)

        #forth row
        self.b_launch_detection = QtWidgets.QPushButton(self.central_widget)
        self.b_launch_detection.setObjectName("b_launch_detection")
        self.gridLayout.addWidget(self.b_launch_detection, 11, 1, 1, 1)
        self.b_launch_detection.clicked.connect(self.runDetection)

        self.b_close_feed = QtWidgets.QPushButton(self.central_widget)
        self.b_close_feed.setObjectName("b_close_feed")
        self.gridLayout.addWidget(self.b_close_feed, 11, 3, 1, 1)
        self.b_close_feed.clicked.connect(self.closeVideoFeed)

        #
        MainWindow.setCentralWidget(self.central_widget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(self.translate("MainWindow", "MainWindow"))
        self.b_launch_detection.setText(self.translate("MainWindow", "Launch detection"))
        self.b_test_detection.setText(self.translate("MainWindow", "Test  detection"))
        self.feed_source.setItemText(0, self.translate("MainWindow", "-"))
        self.feed_source.setItemText(1, self.translate("MainWindow", "KinectV1"))
        self.feed_source.setItemText(2, self.translate("MainWindow", "KinectV2"))
        self.label_set_video_feed.setText(self.translate("MainWindow", "I. Select video feed source"))
        self.label_set_area_to_detect.setText(self.translate("MainWindow", "III. Select area to be detected"))
        self.label_set_main_interface.setText(self.translate("MainWindow", "II. Select interface"))
        self.main_interface.setItemText(0, self.translate("MainWindow", "-"))
        self.main_interface.setItemText(1, self.translate("MainWindow", "Modules interface"))
        self.main_interface.setItemText(2, self.translate("MainWindow", "Buttons interface"))
        self.main_interface.setItemText(3, self.translate("MainWindow", "Box interface"))
        self.b_close_feed.setText(self.translate("MainWindow", "Close video feed"))
        self.area_to_detect.setItemText(0, self.translate("MainWindow", "-"))
        self.area_to_detect.setItemText(1, self.translate("MainWindow", "interface area"))
        self.area_to_detect.setItemText(2, self.translate("MainWindow", "modules area"))
        self.get_frame.setText(self.translate("MainWindow", "Get frame"))


if __name__ == "__main__":
    rospy.init_node('launchDetection', anonymous=True)
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())