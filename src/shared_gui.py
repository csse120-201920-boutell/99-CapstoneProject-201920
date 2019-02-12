"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Constructs and returns Frame objects for the basics:
  -- teleoperation
  -- arm movement
  -- stopping the robot program

  This code is SHARED by all team members.  It contains both:
    -- High-level, general-purpose methods for a Snatch3r EV3 robot.
    -- Lower-level code to interact with the EV3 robot library.

  Author:  Your professors (for the framework and lower-level code)
    and Matt Boutell.
  Winter term, 2018-2019.
"""

import tkinter
from tkinter import ttk
import time


def get_teleoperation_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Entry and Button objects that control the EV3 robot's motion
    by passing messages using the given MQTT Sender.
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Teleoperation")
    left_speed_label = ttk.Label(frame, text="Left wheel speed (0 to 100)")
    right_speed_label = ttk.Label(frame, text="Right wheel speed (0 to 100)")

    left_speed_entry = ttk.Entry(frame, width=8)
    left_speed_entry.insert(0, "100")
    right_speed_entry = ttk.Entry(frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "100")

    forward_button = ttk.Button(frame, text="Forward")
    backward_button = ttk.Button(frame, text="Backward")
    left_button = ttk.Button(frame, text="Left")
    right_button = ttk.Button(frame, text="Right")
    stop_button = ttk.Button(frame, text="Stop")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    left_speed_label.grid(row=1, column=0)
    right_speed_label.grid(row=1, column=2)
    left_speed_entry.grid(row=2, column=0)
    right_speed_entry.grid(row=2, column=2)

    forward_button.grid(row=3, column=1)
    left_button.grid(row=4, column=0)
    stop_button.grid(row=4, column=1)
    right_button.grid(row=4, column=2)
    backward_button.grid(row=5, column=1)

    # Set the button callbacks:
    forward_button["command"] = lambda: handle_forward(
        left_speed_entry, right_speed_entry, mqtt_sender)
    backward_button["command"] = lambda: handle_backward(
        left_speed_entry, right_speed_entry, mqtt_sender)
    left_button["command"] = lambda: handle_left(
        left_speed_entry, right_speed_entry, mqtt_sender)
    right_button["command"] = lambda: handle_right(
        left_speed_entry, right_speed_entry, mqtt_sender)
    stop_button["command"] = lambda: handle_stop(mqtt_sender)

    return frame


def get_arm_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Entry and Button objects that control the EV3 robot's Arm
    by passing messages using the given MQTT Sender.
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Arm and Claw")
    position_label = ttk.Label(frame, text="Desired arm position:")
    position_entry = ttk.Entry(frame, width=8)

    raise_arm_button = ttk.Button(frame, text="Raise arm")
    lower_arm_button = ttk.Button(frame, text="Lower arm")
    calibrate_arm_button = ttk.Button(frame, text="Calibrate arm")
    move_arm_button = ttk.Button(frame,
                                 text="Move arm to position (0 to 5112)")
    blank_label = ttk.Label(frame, text="")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    position_label.grid(row=1, column=0)
    position_entry.grid(row=1, column=1)
    move_arm_button.grid(row=1, column=2)

    blank_label.grid(row=2, column=1)
    raise_arm_button.grid(row=3, column=0)
    lower_arm_button.grid(row=3, column=1)
    calibrate_arm_button.grid(row=3, column=2)

    # Set the Button callbacks:
    move_arm_button["command"] = lambda: handle_move_arm_to_position(position_entry, mqtt_sender)
    raise_arm_button["command"] = lambda: handle_raise_arm(mqtt_sender)
    lower_arm_button["command"] = lambda: handle_lower_arm(mqtt_sender)
    calibrate_arm_button["command"] = lambda: handle_calibrate_arm(mqtt_sender)

    return frame


def get_sensor_drive_frame(window, mqtt_sender):
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()
    frame_label = ttk.Label(frame, text="Sensor Drive")
    frame_label.grid(row=0, column=0)

    label1 = ttk.Label(frame, text="Distance (inches):")
    label1.grid(row=1, column=0)
    entry1 = ttk.Entry(frame, width=8)
    entry1.grid(row=1, column=1)

    label2 = ttk.Label(frame, text="Speed (0 to 100):")
    label2.grid(row=2, column=0)
    entry2 = ttk.Entry(frame, width=8)
    entry2.grid(row=2, column=1)

    label3 = ttk.Label(frame, text="Area of blob:")
    label3.grid(row=3, column=0)
    entry3 = ttk.Entry(frame, width=8)
    entry3.grid(row=3, column=1)

    drive_until_close_button = ttk.Button(frame, text="Drive forward until closer")
    drive_until_close_button.grid(row=4, column=0)
    drive_until_close_button["command"] = lambda: handle_drive_until_closer(
        mqtt_sender, entry1, entry2)

    drive_until_farther_button = ttk.Button(frame, text="Drive backward until farther")
    drive_until_farther_button.grid(row=5, column=0)
    drive_until_farther_button["command"] = lambda: handle_drive_until_farther(
        mqtt_sender, entry1, entry2)

    drive_until_there_button = ttk.Button(frame, text="Drive until close")
    drive_until_there_button.grid(row=6, column=0)
    drive_until_there_button["command"] = lambda: handle_drive_until_there(
        mqtt_sender, entry1, entry2)

    # TODO: Add driving using color sensor



    show_camera_blob_button = ttk.Button(frame, text="Show camera blob on robot")
    show_camera_blob_button.grid(row=7, column=0)
    show_camera_blob_button["command"] = lambda: handle_show_camera_blob(
        mqtt_sender)

    spin_clockwise_until_see_button= ttk.Button(frame, text="Spin clockwise until see blob")
    spin_clockwise_until_see_button.grid(row=8, column=0)
    spin_clockwise_until_see_button["command"] = lambda: handle_spin_clockwise_until_see(
        mqtt_sender, entry2, entry3)

    spin_counter_clockwise_until_see_button= ttk.Button(frame, text="Spin counterclockwise until see blob")
    spin_counter_clockwise_until_see_button.grid(row=9, column=0)
    spin_counter_clockwise_until_see_button["command"] = lambda: handle_spin_counterclockwise_until_see(
        mqtt_sender, entry2, entry3)

    return frame


def get_drive_system_frame(window, mqtt_sender):
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()
    frame_label = ttk.Label(frame, text="Drive System")
    frame_label.grid(row=0, column=0)
    label1 = ttk.Label(frame, text="Time (seconds):")
    label1.grid(row=1, column=0)
    entry1 = ttk.Entry(frame, width=8)
    entry1.grid(row=1, column=1)
    label2 = ttk.Label(frame, text="Speed (0-100):")
    label2.grid(row=2, column=0)
    entry2 = ttk.Entry(frame, width=8)
    entry2.grid(row=2, column=1)
    label3 = ttk.Label(frame, text="Distance (inches):")
    label3.grid(row=3, column=0)
    entry3 = ttk.Entry(frame, width=8)
    entry3.grid(row=3, column=1)

    drive_for_time_button = ttk.Button(frame, text="Go for time")
    drive_for_time_button.grid(row=4, column=0)
    drive_for_time_button["command"] = lambda: handle_drive_for_time(
        mqtt_sender, entry1, entry2)

    drive_for_inches_using_time_button = ttk.Button(frame, text="Go distance using time")
    drive_for_inches_using_time_button.grid(row=5, column=0)
    drive_for_inches_using_time_button["command"] = lambda: handle_drive_for_inches_using_time(
        mqtt_sender, entry2, entry3)

    drive_for_inches_using_encoder_button = ttk.Button(frame, text="Go distance using encoder")
    drive_for_inches_using_encoder_button.grid(row=5, column=0)
    drive_for_inches_using_encoder_button["command"] = lambda: handle_drive_for_inches_using_encoder(
        mqtt_sender, entry2, entry3)
    return frame


def get_sound_system_frame(window, mqtt_sender):
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()
    frame_label = ttk.Label(frame, text="Sound System")
    frame_label.grid(row=0, column=1)
    # label1 = ttk.Label(frame, text="Seconds:")
    # label1.grid(row=1, column=0)
    # entry1 = ttk.Entry(frame, width=8)
    # entry1.grid(row=1, column=1)
    # label2 = ttk.Label(frame, text="Speed:")
    # label2.grid(row=2, column=0)
    # entry2 = ttk.Entry(frame, width=8)
    # entry2.grid(row=2, column=1)
    # label3 = ttk.Label(frame, text="Distance:")
    # label3.grid(row=3, column=0)
    # entry3 = ttk.Entry(frame, width=8)
    # entry3.grid(row=3, column=1)
    #
    # drive_for_time_button = ttk.Button(frame, text="Go for time")
    # drive_for_time_button.grid(row=4, column=0)
    # drive_for_time_button["command"] = lambda: handle_drive_for_time(mqtt_sender, entry1, entry2)
    #
    # drive_for_inches_using_time_button = ttk.Button(frame, text="Go distance using time")
    # drive_for_inches_using_time_button.grid(row=5, column=0)
    # drive_for_inches_using_time_button["command"] = lambda: handle_drive_for_inches_using_time(mqtt_sender, entry2, entry3)
    #
    # drive_for_inches_using_encoder_button = ttk.Button(frame, text="Go distance using encoder")
    # drive_for_inches_using_encoder_button.grid(row=5, column=0)
    # drive_for_inches_using_encoder_button["command"] = lambda: handle_drive_for_inches_using_encoder(mqtt_sender, entry2, entry3)
    return frame


def get_line_following_frame(window, mqtt_sender):
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()
    frame_label = ttk.Label(frame, text="Line following")
    frame_label.grid(row=0, column=0)
    # label1 = ttk.Label(frame, text="Seconds:")
    # label1.grid(row=1, column=0)
    # entry1 = ttk.Entry(frame, width=8)
    # entry1.grid(row=1, column=1)
    # label2 = ttk.Label(frame, text="Speed:")
    # label2.grid(row=2, column=0)
    # entry2 = ttk.Entry(frame, width=8)
    # entry2.grid(row=2, column=1)
    # label3 = ttk.Label(frame, text="Distance:")
    # label3.grid(row=3, column=0)
    # entry3 = ttk.Entry(frame, width=8)
    # entry3.grid(row=3, column=1)
    #
    bang_bang_button = ttk.Button(frame, text="Bang-bang drive")
    bang_bang_button.grid(row=4, column=0)
    bang_bang_button["command"] = lambda: handle_bang_bang(mqtt_sender)

    p_control_button = ttk.Button(frame, text="P-control drive")
    p_control_button.grid(row=5, column=0)
    p_control_button["command"] = lambda: handle_p_control(mqtt_sender)

    pd_control_button = ttk.Button(frame, text="PD-control drive")
    pd_control_button.grid(row=6, column=0)
    pd_control_button["command"] = lambda: handle_pd_control(mqtt_sender)
    return frame

def get_control_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame has
    Button objects to exit this program and/or the robot's program (via MQTT).
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Control")
    quit_robot_button = ttk.Button(frame, text="Stop the robot's program")
    exit_button = ttk.Button(frame, text="Stop this and the robot's program")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    quit_robot_button.grid(row=1, column=0)
    exit_button.grid(row=1, column=2)

    # Set the Button callbacks:
    quit_robot_button["command"] = lambda: handle_quit(mqtt_sender)
    exit_button["command"] = lambda: handle_exit(mqtt_sender)

    return frame

###############################################################################
###############################################################################
# The following specifies, for each Button,
# what should happen when the Button is pressed.
###############################################################################
###############################################################################


###############################################################################
# Handlers for Buttons in the Teleoperation frame.
###############################################################################
def handle_forward(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    with the speeds used as given.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """
    print("gui forward handler", left_entry_box.get(), right_entry_box.get())
    mqtt_sender.send_message("go", [left_entry_box.get(), right_entry_box.get()])


def handle_backward(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negatives of the speeds in the entry boxes.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """
    print("gui backward handler", left_entry_box.get(), right_entry_box.get())
    left = -int(left_entry_box.get())
    right = -int(right_entry_box.get())
    mqtt_sender.send_message("go", [str(left), str(right)])


def handle_left(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negative of the speed in the left entry box.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """
    print("gui left handler:", left_entry_box.get(), right_entry_box.get())
    left = -int(left_entry_box.get())
    right = int(right_entry_box.get())
    mqtt_sender.send_message("go", [str(left), str(right)])


def handle_right(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negative of the speed in the right entry box.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """
    print("gui right handler:", left_entry_box.get(), right_entry_box.get())
    left = int(left_entry_box.get())
    right = -int(right_entry_box.get())
    mqtt_sender.send_message("go", [str(left), str(right)])


def handle_stop(mqtt_sender):
    """
    Tells the robot to stop.
      :type  mqtt_sender:  com.MqttClient
    """
    print("gui stop")
    mqtt_sender.send_message("stop", [])


###############################################################################
# Handlers for Buttons in the ArmAndClaw frame.
###############################################################################
def handle_raise_arm(mqtt_sender):
    """
    Tells the robot to raise its Arm until its touch sensor is pressed.
      :type  mqtt_sender:  com.MqttClient
    """
    print("gui raise arm")
    mqtt_sender.send_message("raise_arm")


def handle_lower_arm(mqtt_sender):
    """
    Tells the robot to lower its Arm until it is all the way down.
      :type  mqtt_sender:  com.MqttClient
    """
    print("gui lower arm")
    mqtt_sender.send_message("lower_arm")


def handle_calibrate_arm(mqtt_sender):
    """
    Tells the robot to calibrate its Arm, that is, first to raise its Arm
    until its touch sensor is pressed, then to lower its Arm until it is
    all the way down, and then to mark taht position as position 0.
      :type  mqtt_sender:  com.MqttClient
    """
    print("gui calibrate arm")
    mqtt_sender.send_message("calibrate_arm")


def handle_move_arm_to_position(arm_position_entry, mqtt_sender):
    """
    Tells the robot to move its Arm to the position in the given Entry box.
    The robot must have previously calibrated its Arm.
      :type  arm_position_entry  ttk.Entry
      :type  mqtt_sender:        com.MqttClient
    """
    print("gui move arm to position", arm_position_entry.get())
    mqtt_sender.send_message("move_arm_to_position", [arm_position_entry.get()])


###############################################################################
# Handlers for Buttons in the Control frame.
###############################################################################
def handle_quit(mqtt_sender):
    """
    Tell the robot's program to stop its loop (and hence quit).
      :type  mqtt_sender:  com.MqttClient
    """
    mqtt_sender.send_message("quit")


def handle_exit(mqtt_sender):
    """
    Tell the robot's program to stop its loop (and hence quit).
    Then exit this program.
      :type mqtt_sender: com.MqttClient
    """
    handle_quit(mqtt_sender)
    exit(code=0)


###############################################################################
# Handlers for Buttons in the Sensor Drive frame.
###############################################################################
def handle_drive_until_closer(mqtt_sender, distance_entry, speed_entry):
    print("gui drive until closer")
    mqtt_sender.send_message(
        "drive_until_closer",
        [distance_entry.get(), speed_entry.get()])


def handle_drive_until_farther(mqtt_sender, distance_entry, speed_entry):
    print("gui drive until farther")
    mqtt_sender.send_message(
        "drive_until_farther",
        [distance_entry.get(), speed_entry.get()])


def handle_drive_until_there(mqtt_sender, distance_entry, speed_entry):
    print("gui drive until there")
    mqtt_sender.send_message(
        "drive_until_there",
        [distance_entry.get(), speed_entry.get()])


def handle_show_camera_blob(mqtt_sender):
    print("gui show_camera_blob")
    mqtt_sender.send_message("show_camera_blob")


def handle_spin_clockwise_until_see(mqtt_sender, speed_entry, blob_entry):
    print("gui handle_spin_clockwise_until_see", speed_entry.get(), blob_entry.get())
    mqtt_sender.send_message("spin_clockwise_until_see", [speed_entry.get(), blob_entry.get()])


def handle_spin_counterclockwise_until_see(mqtt_sender, speed_entry, blob_entry):
    print("gui handle_spin_counterclockwise_until_see", speed_entry.get(), blob_entry.get())
    mqtt_sender.send_message("spin_counterclockwise_until_see", [speed_entry.get(), blob_entry.get()])



###############################################################################
# Handlers for Buttons in the Drive System frame.
###############################################################################
def handle_drive_for_time(mqtt_sender, time_entry, speed_entry):
    print("gui drive for time")
    mqtt_sender.send_message(
        "drive_until_close",
        [time_entry.get(), speed_entry.get()])


def handle_drive_for_inches_using_time(mqtt_sender, speed_entry, distance_entry):
    print("gui drive for inches using time")
    mqtt_sender.send_message(
        "drive_for_inches_using_time",
        [speed_entry.get(), distance_entry.get()])


def handle_drive_for_inches_using_encoder(mqtt_sender, speed_entry, distance_entry):
    print("gui drive for inches using encoder")
    mqtt_sender.send_message(
        "drive_for_inches_using_encoder",
        [speed_entry.get(), distance_entry.get()])

def handle_bang_bang(mqtt_sender):
    print("gui bang-bang")
    mqtt_sender.send_message("bang_bang")

def handle_p_control(mqtt_sender):
    print("gui p-control")
    mqtt_sender.send_message("p_control")

def handle_pd_control(mqtt_sender):
    print("gui pd-control")
    mqtt_sender.send_message("pd_control")
