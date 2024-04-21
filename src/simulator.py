from sim.UI.ViewClass import View
from sim.model.ModelClass import SystemModel
from sim.controller.ControllerClass import Controller
import sim.sim_global_vars as sg


def main():
    # Intialize simulator global variables
    sg.init()

    # Create Model
    systemModel = SystemModel()

    # Create Controller
    controller = Controller(systemModel)

    # Create View
    view = View(controller)

    # Set the View in Controller
    controller.setView(view)

    # Start the View Window
    view.startWindow()

if __name__ == "__main__":
    main()
