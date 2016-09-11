# robot-env

Controlling a simple robot arm with python and arduino, with the goal of
using it as a machine learning platform.

Robot: Snapper Arm from RobotGeek
http://www.robotgeek.com/robotgeek-snapper-robotic-arm

## Basic protocol

There's 5 joints on the robot arm.  They are in order:
Base, Shoulder, Elbow, Wrist, Grip.

Commands are given as lines (end in a newline character):

    W90,102,80,47,95\n

They begin with a 'W' and are a comma-separated list of servo commanded angles.
Commanded angles should be between 0 and 180 (inclusive).

The arm echo's received commands with the exact same line format,
but prefixed with an 'E' instead.

    E90,102,80,47,95\n

The arm also reads its potentiometer values and prints those in a similar line:

    R501,511,499,597,587,0,0\n

The potentiometer values range from 0 to 1024, and the order corresponds to the
servo command ordering (base, shoulder, elbow, wrist, grip).

The two extra values at the end are buttons (capture and playback respectively),
and are either 0 (not pressed) or 1 (pressed).
