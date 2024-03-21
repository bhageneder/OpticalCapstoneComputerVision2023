from sim.UI.ViewClass import View
from sim.model.ModelClass import Model
from sim.controller.ControllerClass import Controller

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
