# Robotics
2019-2020 Robotics projects 

We present a gesture controlled Pachinko game with auto-mated ball return. Using hand gestures players try to catch a ball witha cup. If the ball is not caught it is returned automatically to the top ofthe board using a lift. The system is build using two one-axis sliders, anUltraLeap, a Raspberry Pi and an Arduino Uno

Minimal idea           |  Final project
:-------------------------:|:-------------------------:
![Minimal idea](schematic.png) | ![Final project](final.jpg)

# Usage

## Cup slider
To set up the socket connection, set the PCs local IP in LeapMotion.py and leap_robot.py. Any free port number can be used.
LeapMotion.py has to be started first, from a PC that has a Leap connected. Afterwards run leap_robot.py from a Raspberry Pi to connect to the server.
The connection will now be established and handtracking coordinates will be send to the Raspberry Pi.

## Lift

The lift is pretty much plug and plug and as soon as the power is connected
start to loop up and down. It's important to start with the pplatform being at
the lowest possible position.

## Ball tracking
To run the experimental ball tracking feature run the following command in your teminal.

````
python ball_tracking_single_color.py
````
