import threading
from sim.UI.view import view
from sim.controller.v_main import v_main

def main():
    # Creating View Thread 
    view_thread = threading.Thread(target=view, daemon=False, name=f'View')
    view_thread.start()

    """ IF ROBOT CREATED"""
    """ v_main() """


if __name__ == "__main__":
    main()
