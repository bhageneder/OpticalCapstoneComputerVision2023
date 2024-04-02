import sim.controller.config.global_sim_vars as vg
from sim.UI.ViewClass import View
from sim.model.ModelClass import Model
from sim.controller.ControllerClass import Controller


def main():

    # initialize virtual globals
    vg.init() 

    # Create Model
    model = Model()

    # Create Controller
    controller = Controller(model, vg)

    # Create View
    view = View(controller)

    # Set the View in Controller
    controller.setView(view)

    # Start the View Window
    view.startWindow()

if __name__ == "__main__":
    main()
