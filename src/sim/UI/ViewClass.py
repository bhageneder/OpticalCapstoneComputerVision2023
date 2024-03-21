import sys
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore 
from PyQt5.QtGui import * 
from screeninfo import get_monitors

class View():
    def __init__(self, controller):
        self.__app = QApplication([])
        self.__window = QWidget()
        self.__controller = controller

        #self.__window.setStyleSheet("background-color: white; border: 2px solid black;")
        m = self.__getMainMonitor()
        self.__window.setGeometry(m.height_mm, m.width_mm, 1000, 500) 
        self.__window.setWindowTitle("Optical Wireless Communications Simulator")

        self.initUI()

    def initUI(self):
        # create layouts for main window
        topLayout = QHBoxLayout()
        bottomLayout = QVBoxLayout()
        mainLayout = QVBoxLayout()

        # Create IP Label and Textbox
        ipLabel = QLabel('IP Address')
        ipTextbox = QLineEdit()

        # Make Push Button
        newRobotButton = QPushButton("Add Robot")

        # Bind Push Button to Event Handler
        newRobotButton.clicked.connect(self.__addRobotButtonClicked)

        # Add IP Label, IP Textbox, New Robot Button to Top Layout
        topLayout.addWidget(ipLabel)
        topLayout.addWidget(ipTextbox)
        topLayout.addWidget(newRobotButton)

        # Set Top Layout Properties
        topLayout.setSpacing(5)

        # Create Grid Widget
        openGrid = QLabel('This is where grid goes')
        openGrid.setAlignment(QtCore.Qt.AlignCenter) 
        openGrid.setFixedSize(1000, 450)
        openGrid.setStyleSheet("background-color: white;")

        # append grid layout to bottom layout
        bottomLayout.addWidget(openGrid)

        # append topLayout and bottomLayout to a mainLayout
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(bottomLayout)

        # set the main layout as the window layout
        self.__window.setLayout(mainLayout)

    def startWindow(self):
        self.__window.show()
        sys.exit(self.__app.exec())

    def updateUI():
        # Read from the model and update UI
        pass
        
    def __getMainMonitor(self):
        for monitor in get_monitors():
            if monitor.is_primary:
                return monitor
        return None
    
    ### Event Handlers ###
    # Add Robot Button Click Event
    def __addRobotButtonClicked(self):
        self.__controller.addNewRobot()