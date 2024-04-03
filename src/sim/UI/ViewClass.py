import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from screeninfo import get_monitors

class View():
    def __init__(self, controller):
        self.__app = QApplication([])
        self.__window = QWidget()
        self.__controller = controller
        self.__threadPool = QThreadPool()

        #self.__window.setStyleSheet("background-color: black; border: 5px solid green; color: white;")
        #self.__window.setStyleSheet("background-color: black; border: 2px solid white; color: white;")
        m = self.__getMainMonitor()
        self.__window.setGeometry(m.height_mm, m.width_mm, 1000, 500) 
        self.__window.setWindowTitle("Optical Wireless Communications Simulator")

        # Set Default States
        self.__xTextboxVal = 0
        self.__yTextboxVal = 0
        self.__blockerVals = [0, 0, 10, 100]

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
        xTextbox.textChanged.connect(self.__xTextboxHandler)
        xLayout.addWidget(xTextbox)
        
        # New Robot Y Coordinates
        yLayout = QHBoxLayout()
        yLabel = QLabel('Y: ')
        yLayout.addWidget(yLabel)
        yTextbox = QLineEdit()
        yTextbox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        yTextbox.textChanged.connect(self.__yTextboxHandler)
        yLayout.addWidget(yTextbox)

        # Add Coordinates to New Robot Layout
        newRobotLayout.addLayout(xLayout)
        newRobotLayout.addLayout(yLayout)

        # Make New Robot Push Button
        newRobotButton = QPushButton("Add Robot")

        # Add New Robot Push Button to New Robot Layout
        newRobotLayout.addWidget(newRobotButton)

        # Bind New Robot Push Button to Event Handler
        newRobotButton.clicked.connect(self.__addRobotButtonClicked)

        # New Blocker Layout
        newBlockerLayout = QVBoxLayout()
        newBlockerLabel = QLabel('Configure New Blocker')
        newBlockerLayout.addWidget(newBlockerLabel)

        # New Blocker X Coordinates
        xBLayout = QHBoxLayout()
        xBLabel = QLabel('X: ')
        xBLayout.addWidget(xBLabel)
        xBTextbox = QLineEdit()
        xBTextbox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        xBTextbox.textChanged.connect(self.__xBTextboxHandler)
        xBLayout.addWidget(xBTextbox)
        
        # New Blocker Y Coordinates
        yBLayout = QHBoxLayout()
        yBLabel = QLabel('Y: ')
        yBLayout.addWidget(yBLabel)
        yBTextbox = QLineEdit()
        yBTextbox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        yBTextbox.textChanged.connect(self.__yBTextboxHandler)
        yBLayout.addWidget(yBTextbox)

        # New Blocker Width
        widthLayout = QHBoxLayout()
        widthLabel = QLabel('Width: ')
        widthLayout.addWidget(widthLabel)
        widthTextbox = QLineEdit()
        widthTextbox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        widthTextbox.textChanged.connect(self.__widthTextboxHandler)
        widthLayout.addWidget(widthTextbox)
        
        # New Blocker Height
        heightLayout = QHBoxLayout()
        heightLabel = QLabel('Height: ')
        heightLayout.addWidget(heightLabel)
        heightTextbox = QLineEdit()
        heightTextbox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        heightTextbox.textChanged.connect(self.__heightTextboxHandler)
        heightLayout.addWidget(heightTextbox)

        # Add Coordinates and Size to New Blocker Layout
        newBlockerLayout.addLayout(xBLayout)
        newBlockerLayout.addLayout(yBLayout)
        newBlockerLayout.addLayout(widthLayout)
        newBlockerLayout.addLayout(heightLayout)

        # Make New Blocker Push Button
        newBlockerButton = QPushButton("Add Blocker")
        newBlockerLayout.addWidget(newBlockerButton)
        newBlockerButton.clicked.connect(self.__addBlockerButtonClicked)

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

        # Make Remove Robots Push Button
        removeRobotsButton = QPushButton("Remove Robots")
        settingsLayout.addWidget(removeRobotsButton)
        removeRobotsButton.clicked.connect(self.__deleteRobotsButtonClicked)

        # Add Settings and New Robot Sections to Top Layout
        topLayout.addLayout(settingsLayout, 0, 0, 0, 1)
        topLayout.addLayout(newRobotLayout, 0, 1, 0, 1)
        topLayout.addLayout(newBlockerLayout, 0, 2, 0, 1)

        # Set Top Layout Properties
        topLayout.setSpacing(5)

        # Create Graphics Widget
        self.graphicsScene = QGraphicsScene()
        #graphicsScene.addText("Graphics Go Here")
        graphicsView = QGraphicsView(self.graphicsScene)
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
        sys.exit(self.__appExec())

    def __appExec(self):
        # Run the app
        self.__app.exec()
        
        # Cleanup (executes when window closes)
        self.__controller.cleanupThreads()

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
        self.__controller.addNewRobot(self.__xTextboxVal, self.__yTextboxVal)

    def __deleteRobotsButtonClicked(self):
        worker = Worker(self.__controller.deleteRobots, (self.graphicsScene.selectedItems()))
        self.__threadPool.start(worker)

    def __xTextboxHandler(self, text):
        try:
            self.__xTextboxVal = int(text)
        except:
            self.__xTextboxVal = 0

    def __yTextboxHandler(self, text):
        try:
            self.__yTextboxVal = int(text)
        except:
            self.__yTextboxVal = 0

    def __addBlockerButtonClicked(self):
        self.__controller.addNewBlocker(self.__blockerVals[0], self.__blockerVals[1], self.__blockerVals[2], self.__blockerVals[3])

    def __xBTextboxHandler(self, text):
        try:
            self.__blockerVals[0] = int(text)
        except:
            self.__blockerVals[0] = 0

    def __yBTextboxHandler(self, text):
        try:
            self.__blockerVals[1] = int(text)
        except:
            self.__blockerVals[1] = 0
    
    def __widthTextboxHandler(self, text):
        try:
            self.__blockerVals[2] = int(text)
        except:
            self.__blockerVals[2] = 0
    
    def __heightTextboxHandler(self, text):
        try:
            self.__blockerVals[3] = int(text)
        except:
            self.__blockerVals[3] = 0

    def __settingHandler(self):
        print("Setting1 Changed")

    def __radioHandler(self):
        print("Radio1 Changed")

    ### Public Methods ###
    def drawRobot(self, robotModel, x, y):
        # Create an Ellipse
        ellipse = QGraphicsEllipseItem(0, 0, 100, 100)
        ellipse.setPos(x,y) # Must set position seperately (or the QPointF data gets screwed)

        # Make Ellipse Moveable
        ellipse.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

        # Add Text Item to the Ellipse (Display the IP in the Ellipse)
        text = QGraphicsTextItem(robotModel.ip, ellipse)
        text.setPos(20, 35)

        # Render
        self.graphicsScene.addItem(ellipse)

        # Return the ellipse
        return ellipse
    
    def eraseRobot(self, robotItem):
        # Remove the robotItem
        self.graphicsScene.removeItem(robotItem)

    def drawBlocker(self, x, y, width, height):
        # Create a Rectangle
        rect = QGraphicsRectItem(0, 0, width, height)
        rect.setPos(x,y) # Must set position seperately (or the QPointF data gets screwed)

        # Make Rectangle Moveable
        rect.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

        # Render
        self.graphicsScene.addItem(rect)

        # Return the rectangle
        return rect
    
    def eraseBlocker(self, blockerItem):
        # Remove the robotItem
        self.graphicsScene.removeItem(blockerItem)


# Worker Thread Class
class Worker(QRunnable):
    def __init__(self, target, args):
        self.__target = target
        self.__args = args

        super().__init__()

    @pyqtSlot()
    def run(self):
        self.__target(self.__args)