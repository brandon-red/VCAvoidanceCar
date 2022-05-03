VCAvoidanceCar
==============

Overview
--------
Software for a system that will control an obstacle avoidant vehicle using voice commands.

**Planned Features:**
- Navigation to preset beacon points from any area in a given space
- Execute voice commands detailing actions to take
- Avoid visible obstacles (at least the same elevation)
- Avoid drops in elevation
- Statistics and readings being sent to computer for verification of functionality

Project Structure
-----------------
**Client Directory**
- Contains voice command handling
- Contains logic for basic vehicle functions
- Contains libraries for sensors
- Contains algorithms for Navigation and Obstacle Avoidance Features
- Contains main python file to run system and send data to the server displaying outputs

**Server Directory**
- Contains python file to host server and display information being sent from client
    
Hardware Set Up
---------------
- Raspberry Pi 
- 4x Ultrasonic Ranger Sensor
- 2x Infrared Sensor
- 1x Electronic Compass
- Google Home Mini
- Computer to run server

How to Run
----------
- Set up server on computer listening on port of choice
- Start client by running `python client.py`
- Speak commands to Google Home Mini in one of 3 ways:
    - "Go to Location (A, B, C)" 
    - "Drive (forward, backward) for # seconds"
    - "Turn (right, left)