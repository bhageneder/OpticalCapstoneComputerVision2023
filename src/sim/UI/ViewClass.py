import sys
import time
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from screeninfo import get_monitors
import sim.sim_global_vars as sg

class View():
    def __init__(self, controller):
        self.__app = QApplication([])
        self.__window = QWidget()
        self.__controller = controller
        self.__threadPool = QThreadPool()
        self.__commsRadiusList = list()
        self.__detectionRadiusList = list()

        #self.__window.setStyleSheet("background-color: black; border: 5px solid green; color: white;")
        #self.__window.setStyleSheet("background-color: black; border: 2px solid white; color: white;")
        m = self.__getMainMonitor()
        self.__window.setGeometry(m.height_mm, m.width_mm, 1000, 500) 
        self.__window.setWindowTitle("Optical Wireless Communications Simulator")

        # Set Default States
        self.__xRobotVal = 0
        self.__yRobotVal = 0
        self.__blockerVals = [0, 0, 10, 100] # x, y, width, height

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
        xRobot = QLineEdit()
        xRobot.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        xRobot.textChanged.connect(self.__xRobotHandler)
        xLayout.addWidget(xRobot)
        
        # New Robot Y Coordinates
        yLayout = QHBoxLayout()
        yLabel = QLabel('Y: ')
        yLayout.addWidget(yLabel)
        yRobot = QLineEdit()
        yRobot.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        yRobot.textChanged.connect(self.__yRobotHandler)
        yLayout.addWidget(yRobot)

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
        widthTextbox.textChanged.connect(self.__widthBTextboxHandler)
        widthLayout.addWidget(widthTextbox)
        
        # New Blocker Height
        heightLayout = QHBoxLayout()
        heightLabel = QLabel('Height: ')
        heightLayout.addWidget(heightLabel)
        heightTextbox = QLineEdit()
        heightTextbox.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        heightTextbox.textChanged.connect(self.__heightBTextboxHandler)
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

        # Make Remove Items Push Button
        removeItemsButton = QPushButton("Remove Items")
        settingsLayout.addWidget(removeItemsButton)
        removeItemsButton.clicked.connect(self.__deleteItemsButtonClicked)

        # Add Settings and New Robot Sections to Top Layout
        topLayout.addLayout(settingsLayout, 0, 0, 0, 1)
        topLayout.addLayout(newRobotLayout, 0, 1, 0, 1)
        topLayout.addLayout(newBlockerLayout, 0, 2, 0, 1)

        # Set Top Layout Properties
        topLayout.setSpacing(5)

        # Create Graphics Widget
        self.graphicsScene = QGraphicsScene()
        self.graphicsScene.selectionChanged.connect(self.__selectHandler)

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
        self.__controller.addNewRobot(self.__xRobotVal, self.__yRobotVal)


    def __deleteItemsButtonClicked(self):
        worker = Worker(self.__controller.deleteItems, (self.graphicsScene.selectedItems()))
        self.__threadPool.start(worker)


    def __selectHandler(self):
        try:
            self.__handleSelectionChanged()
        except RuntimeError:
            # View has been closed via select, skip this
            pass


    def __handleSelectionChanged(self):
        # parse thread args
        
        selectedItemsList = self.graphicsScene.selectedItems()
        itemsList = self.graphicsScene.items()
        remainingItemList = [x for x in itemsList if x not in set(selectedItemsList)]
        
        # For all selected robots, draw radii
        for item in selectedItemsList:
            # selected robot radii already exists
            if len(item.childItems()) > 1:
                pass
            else:
                self.__drawRadius(item) if type(item) is QGraphicsEllipseItem else None
        
        worker = Worker(self.__clearRadius, (remainingItemList))
        self.__threadPool.start(worker)
        # For all remaining robots (if permitting) clear radii
        remainingItemList = [x for x in itemsList if x not in set(selectedItemsList)]


    def __xRobotHandler(self, text):
        try:
            self.__xRobotVal = int(text)
        except:
            self.__xRobotVal = 0


    def __yRobotHandler(self, text):
        try:
            self.__yRobotVal = int(text)
        except:
            self.__yRobotVal = 0


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
    
    def __widthBTextboxHandler(self, text):
        try:
            newVal = int(text)
            if newVal > 0:
                self.__blockerVals[2] = newVal
        except:
            self.__blockerVals[2] = 10
    
    def __heightBTextboxHandler(self, text):
        try:
            newVal = int(text)
            if newVal > 0:
                self.__blockerVals[3] = newVal
        except:
            self.__blockerVals[3] = 100


    def __settingHandler(self):
        print("Setting1 Changed")


    def __radioHandler(self):
        print("Radio1 Changed")


    ### Private Methods ###
    def __clearRadius(self, nonSelectedItemList):
        for remainingItem in nonSelectedItemList:
            # Clear any child ellipse items that may be attached
            for childItem in remainingItem.childItems():
                # Avoid grabbing text box
                self.graphicsScene.removeItem(childItem) if type(childItem) is QGraphicsEllipseItem else None


    def __drawRadius(self, selectedItem):
        # Create Comms Ring
        commsEllipse = QGraphicsEllipseItem((selectedItem.boundingRect().center().x()-(sg.commsThreshold/2)), (selectedItem.boundingRect().center().y()-(sg.commsThreshold/2)), sg.commsThreshold, sg.commsThreshold, parent=selectedItem)
        commsEllipse.setZValue(-10) # set this to be behind robot item
        commsEllipse.setBrush(QBrush(QColor(128, 128, 128, 77))) # gray at 30% opacity (r, g, b, opacity % (#/255))

        # Create Detection Rings
        detectionEllipse = QGraphicsEllipseItem((selectedItem.boundingRect().center().x()-(sg.detectionThreshold/2)), (selectedItem.boundingRect().center().y()-(sg.detectionThreshold/2)), sg.detectionThreshold, sg.detectionThreshold, parent=selectedItem)
        detectionEllipse.setZValue(-20) # set this to be behind first two ellipse items
        detectionEllipse.setBrush(QBrush(QColor(144, 238, 144, 77))) # Light green at 30% opacity (r, g, b, opacity % (#/255))


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
    
                    