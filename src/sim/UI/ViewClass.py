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

        # Make Push Button
        newRobotButton = QPushButton("Add Robot")

        # Bind Push Button to Event Handler
        newRobotButton.clicked.connect(self.__addRobotButtonClicked)

        # Add New Robot Button to Top Layout
        topLayout.addWidget(newRobotButton)

        # Set Top Layout Properties
        topLayout.setSpacing(5)

        # Create Graphics Widget
        graphicsScene = QGraphicsScene()
        graphicsScene.addText("Graphics Go Here")
        graphicsView = QGraphicsView(graphicsScene)
        graphicsView.show()

        # Append Graphics Widget to the Bottom Layout
        bottomLayout.addWidget(graphicsView)

        # Append Top and Bottom Layouts to the Main Layout
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(bottomLayout)

        # Set the Window Layout to Main Layout
        self.__window.setLayout(mainLayout)

    def startWindow(self):
        self.__window.show()
        sys.exit(self.__app.exec())

    def updateUI(self):
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