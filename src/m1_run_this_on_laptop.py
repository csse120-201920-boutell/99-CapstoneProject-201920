"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Displays the Graphical User Interface (GUI) and communicates with the robot.

  Authors:  Your professors (for the framework)
    and PUT_YOUR_NAME_HERE.
  Winter term, 2018-2019.
"""

import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk
import shared_gui


def main():
    """
    This code, which must run on a LAPTOP:
      1. Constructs a GUI for my part of the Capstone Project.
      2. Communicates via MQTT with the code that runs on the EV3 robot.
    """
    # -------------------------------------------------------------------------
    # Construct and connect the MQTT Client:
    # -------------------------------------------------------------------------
    mqtt_sender = com.MqttClient()
    # TODO: Uncomment
    #mqtt_sender.connect_to_ev3()

    # -------------------------------------------------------------------------
    # The root TK object for the GUI:
    # -------------------------------------------------------------------------
    root = tkinter.Tk()
    root.title("Matts Robot GUI")

    # -------------------------------------------------------------------------
    # The main frame, upon which the other frames are placed.
    # -------------------------------------------------------------------------
    main_frame = ttk.Frame(
        root, padding=10, borderwidth=5, relief="groove", width=100, height=100)
    main_frame.grid()

    # -------------------------------------------------------------------------
    # Sub-frames for the shared GUI that the team developed:
    # -------------------------------------------------------------------------
    teleop_frame, arm_frame, control_frame = get_shared_frames(
        main_frame,
        mqtt_sender)

    # -------------------------------------------------------------------------
    # Frames that are particular to my individual contributions to the project.
    # -------------------------------------------------------------------------
    # DONE: Implement and call get_my_frames(...)
    sensor_drive_frame, drive_system_frame, sound_system_frame = get_my_frames(main_frame, mqtt_sender)

    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------
    grid_frames([teleop_frame, arm_frame, sensor_drive_frame,
                 drive_system_frame, sound_system_frame, control_frame])

    # -------------------------------------------------------------------------
    # The event loop:
    # -------------------------------------------------------------------------
    root.mainloop()


def get_shared_frames(main_frame, mqtt_sender):
    teleop_frame = shared_gui.get_teleoperation_frame(main_frame, mqtt_sender)
    arm_frame = shared_gui.get_arm_frame(main_frame, mqtt_sender)
    control_frame = shared_gui.get_control_frame(main_frame, mqtt_sender)
    return teleop_frame, arm_frame, control_frame


def grid_frames(frames):
    for k in range(len(frames)):
        frames[k].grid(row=k, column=0)


def get_my_frames(main_frame, mqtt_sender):
    sensor_drive_frame = shared_gui.get_sensor_drive_frame(main_frame, mqtt_sender)
    drive_system_frame = shared_gui.get_drive_system_frame(main_frame, mqtt_sender)
    sound_system_frame = shared_gui.get_sound_system_frame(main_frame, mqtt_sender)
    return sensor_drive_frame, drive_system_frame, sound_system_frame


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()