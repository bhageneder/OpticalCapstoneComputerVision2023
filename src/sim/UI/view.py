import sys
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore 
from PyQt5.QtGui import * 
from screeninfo import get_monitors

class MainWindow():
    def __init__(self, monitorSize, windowTitle="Default"):
        print("Initializing main window")
        self.__app = QApplication([])
        self.__window = QWidget() 
        self.__title = windowTitle

        self.__window.setStyleSheet("background-color: green; border: 5px solid black;")
        self.__window.setGeometry(monitorSize[0], monitorSize[1], 1000, 500) 
        self.__window.setWindowTitle(self.__title)

        self.initUI()

    def initUI(self):

        # create layouts for main window
        top_layout = QHBoxLayout()
        radio_layout = QHBoxLayout()
        checkbox_layout = QHBoxLayout()
        bottom_layout = QVBoxLayout()
        main_layout = QVBoxLayout()

        # create widgets for layout
        self.openGrid = QLabel('This is where grid goes')
        self.openGrid.setAlignment(QtCore.Qt.AlignCenter) 
        self.openGrid.setFixedSize(1000, 450)
        self.openGrid.setStyleSheet("background-color: white;")
        self.radbtn_1 = QRadioButton('Radio1', self.__window)
        self.radbtn_1.setStyleSheet("color: white;")
        self.radbtn_2 = QRadioButton('Radio2', self.__window)
        self.radbtn_2.setStyleSheet("color: white;")
        self.radbtn_3 = QRadioButton('Radio3', self.__window)
        self.radbtn_3.setStyleSheet("color: white;")
        self.radbtn_4 = QRadioButton('Radio4', self.__window)
        self.radbtn_4.setStyleSheet("color: white;")
        self.chkbtn_1 = QCheckBox('Check1', self.__window)
        self.chkbtn_1.setStyleSheet("color: white;")
        self.chkbtn_2 = QCheckBox('Check2', self.__window)
        self.chkbtn_2.setStyleSheet("color: white;")
        self.chkbtn_3 = QCheckBox('Check3', self.__window)
        self.chkbtn_3.setStyleSheet("color: white;")

        # Connected radio buttons to their corresponding action functions
        self.radbtn_1.clicked.connect(self.radioButton1)
        self.radbtn_2.clicked.connect(self.radioButton2)
        self.radbtn_3.clicked.connect(self.radioButton3)
        self.radbtn_4.clicked.connect(self.radioButton4)

        # Connected check boxes to their corresponding action functions
        self.chkbtn_1.clicked.connect(self.checkBox1)
        self.chkbtn_2.clicked.connect(self.checkBox2)
        self.chkbtn_3.clicked.connect(self.checkBox3)

        # add radio widgets to radio layout
        radio_layout.addWidget(self.radbtn_1)
        radio_layout.addWidget(self.radbtn_2)
        radio_layout.addWidget(self.radbtn_3)
        radio_layout.addWidget(self.radbtn_4)
        radio_layout.addStretch(5)
        radio_layout.setSpacing(10)
        radio_widget = QWidget()
        radio_widget.setLayout(radio_layout)
        radio_widget.setStyleSheet("background-color: black;")  # Set background color
        radio_widget.setFixedHeight(50)

        
        # add checkbox widgets to checkbox layout
        checkbox_layout.addWidget(self.chkbtn_1)
        checkbox_layout.addWidget(self.chkbtn_2)
        checkbox_layout.addWidget(self.chkbtn_3)
        checkbox_layout.addStretch(5)
        checkbox_layout.setSpacing(10)
        checkbox_widget = QWidget()
        checkbox_widget.setLayout(checkbox_layout)
        checkbox_widget.setStyleSheet("background-color: black;")  # Set background color
        checkbox_widget.setFixedHeight(50)

        
        # append radio & checkbox layouts to top layout
        top_layout.addWidget(radio_widget)
        top_layout.addWidget(checkbox_widget)


        # append grid layout to bottom layout
        bottom_layout.addWidget(self.openGrid)

        
        # append top_layout and bottom_layout to a main_layout
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        # set the main layout as the window layout
        self.__window.setLayout(main_layout)

    # ----------------- 
    # radio buttons
    # -----------------

    def radioButton1(self):
        print("Radio Button 1 is clicked!")
        # do something here

    def radioButton2(self):
        print("Radio Button 2 is clicked!")
        # do something here

    def radioButton3(self):
        print("Radio Button 3 is clicked!")
        # do something here

    def radioButton4(self):
        print("Radio Button 4 is clicked!")
        # do something here

    # -----------------
    # check boxes
    # -----------------
    def checkBox1(self):
        print("Check Box 1 is clicked!")
        # do something here

    def checkBox2(self):
        print("Check Box 2 is clicked!")
        # do something here

    def checkBox3(self):
        print("Check Box 3 is clicked!")
        # do something here

    def startWindow(self):
        self.__window.show()
        sys.exit(self.__app.exec())

    def __del__(self):
        print("Decontructing Main Window Object")
        
def view():
    for monitor in get_monitors():
        if monitor.is_primary:
            m = monitor
            break
    view = MainWindow([m.height_mm,m.width_mm], "SIMDEV Main")
    view.startWindow()


if __name__ == "__main__":
    for monitor in get_monitors():
        if monitor.is_primary:
            m = monitor
            break
    view = MainWindow([m.height_mm,m.width_mm], "SIMDEV Main")
    view.startWindow()
    

