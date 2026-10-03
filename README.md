# Autonomous-Raspberry-PI-Car

This is a Raspberry Pi controlled car that uses real time object avoidance to avoid and navigate obstacles by itself.

## Demo
https://youtu.be/WJqAy8MjAcs


## How it works
- The car uses a single ultrasonic sensor to gather the data in front of it. When it senses it is too close to an object it runs a function checking how much distance is on its left and right. It then compares the distance and procedes to choose the way with more free space.
- Steering is controlled by a servo with a custom designed steering rack.
- Moves via two micro dc gear motors in the rear

## Hardware
- Ultrasonic sensor
- Raspberry PI
- Motor Shield
- Micro gear DC motors
- 18650 battery pack
- Mini Servo

## Software
- Python

## Development Setup
Developed via SSH from a laptop into the Raspberry PI, using VS Code's Remote-SSH extension to edit and run code directly on the PI.

## Challenges
- Fusion 360 design procsses
- Powering Raspberry Pi
- WIFI connection with the Pi from laptop

## Future Improvments
- More effort into steering system 
