# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from video_detection import *

class Ui_MainWindow(object):

    def __init__(self):
        self.detection = ModulesDetection()



    # define callbacks
    def setVideoFeedSource(self, index):
        print(self.feed_source.itemText(index))
        self.detection.setVideoSource(self.feed_source.itemText(index).lower())

    def setNbrOfModules(self):
        print "You are now in the sub function.", self.nbr_of_modules.value()
        self.detection.setNbrOfModules(self.nbr_of_modules.value())

    def getFrameForInterface(self):
        self.getFrame("interface")

    def getFrameForModules(self):
        self.getFrame("module")

    def getFrameForModulesStatus(self):
        self.getFrame("status")

    def getFrame(self,area_to_detect):
        print "getting frame"
        self.detection.showFrame(area_to_detect)

    def testInterfaceDetection(self):
        self.detection.testDetection("interface")

    def testModulesDetection(self):
        self.detection.testDetection("module")

    def testModulesStatusDetection(self):
        print "nbr of modules ", self.nbr_of_modules.value()
        self.detection.testDetection("status")

    def closeVideoFeed(self):
        self.detection.video.stopVideoFeed()

    def runDetection(self):
        self.detection.runDetection()
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(951, 509)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # # # 1st row: video feed source #
        # Label
        self.label_set_video_feed = QtWidgets.QLabel(self.centralwidget)
        self.label_set_video_feed.setObjectName("label_set_video_feed")
        self.gridLayout.addWidget(self.label_set_video_feed, 0, 0, 1, 1)

        # video feed source comboBox
        self.feed_source = QtWidgets.QComboBox(self.centralwidget)
        self.feed_source.setObjectName("feed_source")
        self.feed_source.addItem("")
        self.feed_source.addItem("")
        self.feed_source.addItem("")
        self.feed_source.activated.connect(self.setVideoFeedSource)
        self.gridLayout.addWidget(self.feed_source, 0, 2, 1, 1)

        # add seperation
        self.sep_1 = QtWidgets.QFrame(self.centralwidget)
        self.sep_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.sep_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.sep_1.setObjectName("sep_1")
        self.gridLayout.addWidget(self.sep_1, 1, 0, 1, 6)

        # # # 2nd row: Main interface detection #
        # add label
        self.label_main_interface_detection = QtWidgets.QLabel(self.centralwidget)
        self.label_main_interface_detection.setObjectName("label_main_interface_detection")
        self.gridLayout.addWidget(self.label_main_interface_detection, 2, 0, 1, 1)

        # add push button: get frame to select the interface's color to be detected
        self.get_interface_color = QtWidgets.QPushButton(self.centralwidget)
        self.get_interface_color.setObjectName("get_interface_color")
        self.get_interface_color.clicked.connect(self.getFrameForInterface)
        self.gridLayout.addWidget(self.get_interface_color, 2, 2, 1, 1)

        # add push button: test if the interface is detected
        self.test_interface_detection = QtWidgets.QPushButton(self.centralwidget)
        self.test_interface_detection.setObjectName("test_interface_detection")
        self.test_interface_detection.clicked.connect(self.testInterfaceDetection)
        self.gridLayout.addWidget(self.test_interface_detection, 2, 5, 1, 1)

        # add seperation
        self.sep_2 = QtWidgets.QFrame(self.centralwidget)
        self.sep_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.sep_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.sep_2.setObjectName("sep_2")
        self.gridLayout.addWidget(self.sep_2, 3, 0, 1, 6)

        # # # 3rd row: Modules detection
        # add label
        self.label_module_detection = QtWidgets.QLabel(self.centralwidget)
        self.label_module_detection.setObjectName("label_module_detection")
        self.gridLayout.addWidget(self.label_module_detection, 4, 0, 1, 1)

        # add push button: get frame to select the modules' color to be detected
        self.getModulesColor = QtWidgets.QPushButton(self.centralwidget)
        self.getModulesColor.setObjectName("getModulesColor")
        self.getModulesColor.clicked.connect(self.getFrameForModules)
        self.gridLayout.addWidget(self.getModulesColor, 4, 2, 1, 1)

        # add a layout containing a label and a spinbox for the nbr od modules to be detected
        self.h_l_nrb_modules = QtWidgets.QHBoxLayout()
        self.h_l_nrb_modules.setObjectName("h_l_nrb_modules")

        # label
        self.label_nbr_modules = QtWidgets.QLabel(self.centralwidget)
        self.label_nbr_modules.setObjectName("label_nbr_modules")
        self.h_l_nrb_modules.addWidget(self.label_nbr_modules)

        #spinBox
        self.nbr_of_modules = QtWidgets.QSpinBox(self.centralwidget)
        self.nbr_of_modules.setObjectName("nbr_of_modules")
        self.nbr_of_modules.valueChanged.connect(self.setNbrOfModules)
        self.h_l_nrb_modules.addWidget(self.nbr_of_modules)

        self.gridLayout.addLayout(self.h_l_nrb_modules, 5, 2, 1, 1)

        # add push button: test if the selected nbr of modules is detected
        self.test_modules_detection = QtWidgets.QPushButton(self.centralwidget)
        self.test_modules_detection.setObjectName("test_modules_detection")
        self.test_modules_detection.clicked.connect(self.testModulesDetection)
        self.gridLayout.addWidget(self.test_modules_detection, 5, 5, 1, 1)

        # add seperation
        self.sep_3 = QtWidgets.QFrame(self.centralwidget)
        self.sep_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.sep_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.sep_3.setObjectName("sep_3")
        self.gridLayout.addWidget(self.sep_3, 7, 0, 1, 6)

        # # # 4th row: Modules status detection
        # add label
        self.label_modules_st_detection = QtWidgets.QLabel(self.centralwidget)
        self.label_modules_st_detection.setObjectName("label_modules_st_detection")
        self.gridLayout.addWidget(self.label_modules_st_detection, 8, 0, 1, 1)

        # add push button: get frame to select the modules' status color to be detected
        self.getStatusColor = QtWidgets.QPushButton(self.centralwidget)
        self.getStatusColor.setObjectName("getStatusColor")
        self.getStatusColor.clicked.connect(self.getFrameForModulesStatus)
        self.gridLayout.addWidget(self.getStatusColor, 8, 2, 1, 1)

        # add a layout containing a label and a spinbox for the nbr od modules to be detected
        self.h_l_nrb_modules_s = QtWidgets.QHBoxLayout()
        self.h_l_nrb_modules_s.setObjectName("h_l_nrb_modules_s")

        # label
        self.label_nbr_modules_st = QtWidgets.QLabel(self.centralwidget)
        self.label_nbr_modules_st.setObjectName("label_nbr_modules_st")
        self.h_l_nrb_modules_s.addWidget(self.label_nbr_modules_st)

        # spinBox
        self.nbr_of_modules_s = QtWidgets.QSpinBox(self.centralwidget)
        self.nbr_of_modules_s.setObjectName("nbrOfModules_S")
        self.nbr_of_modules_s.valueChanged.connect(self.setNbrOfModules)
        self.h_l_nrb_modules_s.addWidget(self.nbr_of_modules_s)

        self.gridLayout.addLayout(self.h_l_nrb_modules_s, 9, 2, 1, 1)

        # add push button: test if the status of the selected nbr of modules is detected
        self.test_status_detection = QtWidgets.QPushButton(self.centralwidget)
        self.test_status_detection.setObjectName("test_status_detection")
        self.test_status_detection.clicked.connect(self.testModulesStatusDetection)
        self.gridLayout.addWidget(self.test_status_detection, 9, 5, 1, 1)

        # add separation
        self.sep_4 = QtWidgets.QFrame(self.centralwidget)
        self.sep_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.sep_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.sep_4.setObjectName("sep_4")
        self.gridLayout.addWidget(self.sep_4, 11, 0, 1, 6)

        # # # 5th row
        # add push button to launch the video feed with detection
        self.launchDetection = QtWidgets.QPushButton(self.centralwidget)
        self.launchDetection.setObjectName("launchDetection")
        self.launchDetection.clicked.connect(self.runDetection)
        self.gridLayout.addWidget(self.launchDetection, 12, 2, 1, 1)

        # add a push button to close the video feed
        self.closeFeed = QtWidgets.QPushButton(self.centralwidget)
        self.closeFeed.setObjectName("closeFeed")
        self.closeFeed.clicked.connect(self.closeVideoFeed)
        self.gridLayout.addWidget(self.closeFeed, 12, 3, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_nbr_modules_st.setText(_translate("MainWindow", "Nbr of modules"))
        self.label_nbr_modules.setText(_translate("MainWindow", "Nbr of modules"))
        self.feed_source.setItemText(0, _translate("MainWindow", "-"))
        self.feed_source.setItemText(1, _translate("MainWindow", "KinectV1"))
        self.feed_source.setItemText(2, _translate("MainWindow", "KinectV2"))
        self.label_main_interface_detection.setText(_translate("MainWindow", "II. Main interface detection"))
        self.getModulesColor.setText(_translate("MainWindow", "Get frame"))
        self.test_interface_detection.setText(_translate("MainWindow", "Test the interface detection"))
        self.label_module_detection.setText(_translate("MainWindow", "III. Modules detection"))
        self.label_modules_st_detection.setText(_translate("MainWindow", "VI. Modules status detection"))
        self.getStatusColor.setText(_translate("MainWindow", "Get frame"))
        self.launchDetection.setText(_translate("MainWindow", "Launch detection"))
        self.closeFeed.setText(_translate("MainWindow", "Close video feed"))
        self.label_set_video_feed.setText(_translate("MainWindow", "I. Set video feed source"))
        self.get_interface_color.setText(_translate("MainWindow", "Get frame"))
        self.test_modules_detection.setText(_translate("MainWindow", "Test modules detection"))
        self.test_status_detection.setText(_translate("MainWindow", "Test status detection"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

