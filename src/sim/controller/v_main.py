import threading
import queue
from sim.controller.config.v_global_vars import vGlobals
from sim.controller.classes.vDetectorClass import vDetector
from sim.controller.threads.v_new_visible import v_new_visible
from sim.controller.threads.v_new_lost import v_new_lost
from sim.controller.threads.v_link_receive import v_link_receive
from sim.controller.threads.v_link_send import v_link_send
from sim.controller.threads.v_send_manager import v_send_manager
from sim.controller.threads.v_receive_manager import v_receive_manager

def v_main(params):
    robotModel = params[0]
    systemModel = params[1]

    # initialize virtual globals
    vg = vGlobals()
    vg.init(robotModel.ip)

    # Initialize Detector
    vg.detector = vDetector(robotModel, systemModel, vg.debug_detector)

    # Initialize Detector Thread
    vg.detector_thread = threading.Thread(target = vg.detector.detect, args=[vg] ,daemon=True, name="Virtual_Detect")

    vg.new_visible_thread = threading.Thread(target=v_new_visible, args=[vg], daemon=True, name="Virtual_New_Visible")

    vg.new_lost_thread = threading.Thread(target=v_new_lost, args=[vg], daemon=True, name="Virtual_New_Lost")

    vg.send_manager_thread = threading.Thread(target=v_send_manager, args=[vg], daemon=True, name="Virtual_Send_Manager")

    vg.receive_manager_thread = threading.Thread(target=v_receive_manager, args=[vg], daemon=True, name="Virtual_Receive_Manager")

    # Start Threads
    vg.detector_thread.start()
    vg.new_visible_thread.start()
    vg.new_lost_thread.start()
    vg.send_manager_thread.start()
    vg.receive_manager_thread.start()

    # Store Thread Number
    thread_number = 0

    while robotModel.robotItem.isActive():
        # Blocking Call to Get New Robot
        try:
            robot = vg.newRobotQ.get(timeout=0.5)

            # Create and Start Link Send Thread
            link_send_thread = threading.Thread(target=v_link_send, args=[robot, vg], daemon=True, name=f"Link_Send_{thread_number}")
            link_send_thread.start()

            # Create and Start Link Receive Thread
            link_receive_thread = threading.Thread(target=v_link_receive, args=[robot, vg], daemon=True, name=f"Link_Receive_{thread_number}")
            link_receive_thread.start()

            # Increase Thread Number
            thread_number += 1
        except queue.Empty:
            # No robot available
            print("exception")
            pass