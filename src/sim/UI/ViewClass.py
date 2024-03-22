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

        #self.__window.setStyleSheet("background-color: black; border: 5px solid green; color: white;")
        #self.__window.setStyleSheet("background-color: black; border: 2px solid white; color: white;")
        m = self.__getMainMonitor()
        self.__window.setGeometry(m.height_mm, m.width_mm, 1000, 500) 
        self.__window.setWindowTitle("Optical Wireless Communications Simulator")

        self.initUI()

    def initUI(self):
        # create layouts for main window
        topLayout = QGridLayout()
        bottomLayout = QVBoxLayout()
        mainLayout = QVBoxLayout()

        # New Robot Layout
        newRobotLayout = QVBoxLayout()
        newRobotLabel = QLabel('Configure New Robot')
        newRobotLayout.addWidget(newRobotLabel)

        # New Robot X Coordinates
        xLayout = QHBoxLayout()
        xLabel = QLabel('X: ')
        xLayout.addWidget(xLabel)
        xTextbox = QLineEdit()
        xTextbox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        xLayout.addWidget(xTextbox)
        
        # New Robot Y Coordinates
        yLayout = QHBoxLayout()
        yLabel = QLabel('Y: ')
        yLayout.addWidget(yLabel)
        yTextbox = QLineEdit()
        yTextbox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        yLayout.addWidget(yTextbox)

        # Add Coordinates to New Robot Layout
        newRobotLayout.addLayout(xLayout)
        newRobotLayout.addLayout(yLayout)

        # Make Push Button
        newRobotButton = QPushButton("Add Robot")

        # Add Push Button to New Robot Layout
        newRobotLayout.addWidget(newRobotButton)

        # Bind Push Button to Event Handler
        newRobotButton.clicked.connect(self.__addRobotButtonClicked)

        # Simulator Settings
        settingsLayout = QVBoxLayout()
        settingsLabel = QLabel('Simulator Settings')
        settingsLayout.addWidget(settingsLabel)
        
        radio1 = QRadioButton('Radio1')
        settingsLayout.addWidget(radio1)
        radio1.clicked.connect(self.__radioHandler)

        setting1 = QCheckBox('Test Setting')
        settingsLayout.addWidget(setting1)
        setting1.clicked.connect(self.__settingHandler)

        # Add Settings and New Robot Sections to Top Layout
        topLayout.addLayout(settingsLayout, 0, 0, 0, 2)
        topLayout.addLayout(newRobotLayout, 0, 2, 0, 1)

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

    def __settingHandler(self):
        print("Setting1 Changed")

    def __radioHandler(self):
        print("Radio1 Changed")