"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  This code is the delegate for handling messages from the shared GUI.

  Author:  Your professors (for the framework)
    and PUT_YOUR_NAMES_HERE.
  Winter term, 2018-2019.
"""

import rosebot



class Delegate(object):
    def __init__(self, robot):
        """
        :type robot: rosebot.RoseBot
        :type stop_holder: StopHolder
        """
        self.robot = robot
        self.stop = False

    def go(self, left_motor_speed, right_motor_speed):
        print("Delegate receives go", left_motor_speed, right_motor_speed)
        left = int(left_motor_speed)
        right = int(right_motor_speed)
        self.robot.drive_system.go(left, right)

    def stop(self):
        print("Delegate receives stop")
        self.robot.drive_system.stop()

    def raise_arm(self):
        print("Delegate receives raise_arm")
        self.robot.arm_and_claw.raise_arm()

    def lower_arm(self):
        print("Delegate receives lower_arm")
        self.robot.arm_and_claw.lower_arm()

    def calibrate_arm(self):
        print("Delegate receives calibrate_arm")
        self.robot.arm_and_claw.calibrate_arm()

    def move_arm_to_position(self, desired_arm_position):
        print("Delegate receives move_arm_to_position")
        self.robot.arm_and_claw.move_arm_to_position(int(desired_arm_position))

    def quit(self):
        print("Delegate receives quit")
        self.stop = True

    def drive_until_closer(self, distance, speed):
        print("Delegate receives drive_until_closer", distance, speed)
        self.robot.drive_system.go_forward_until_distance_is_less_than(
            int(distance),
            int(speed))

    def drive_until_farther(self, distance, speed):
        print("Delegate receives drive_until_farther", distance, speed)
        self.robot.drive_system.go_backward_until_distance_is_greater_than(
            int(distance),
            int(speed))

    def drive_until_there(self, distance, speed):
        print("Delegate receives drive_until_there", distance, speed)
        self.robot.drive_system.go_until_distance_is_within(
            int(distance),
            int(speed))

    def show_camera_blob(self):
        print("Delegate receives show_camera_blob")
        self.robot.drive_system.display_camera_data()

    def spin_clockwise_until_see(self, speed, blob):
        print("Delegate receives spin_clockwise_until_see")
        self.robot.drive_system.spin_clockwise_until_sees_object(int(speed), int(blob))

    def handle_spin_counterclockwise_until_see(self, speed, blob):
        print("Delegate receives spin_counterclockwise_until_see")
        self.robot.drive_system.spin_counterclockwise_until_sees_object(int(speed), int(blob))


