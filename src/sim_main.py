import threading
from sim.UI.view import View
from sim.ModelClass import Model
from sim.controller.ControllerClass import Controller
#from sim.controller.v_main import v_main

def main():
    # Create Model
    model = Model()

    # Create Controller
    controller = Controller(model)

    # Create View
    view = View(controller)

    # Start the View Window
    view.startWindow()

if __name__ == "__main__":
    main()
