# cshrgbledsign
Networked RGB LEDs. Work in progress. Implemented using pi-blaster library on a raspberry pi running the python flask library.
Uses software pwm pins 22,23, and 24 for respective RGB values.  Tip 120 transistors connect LEDS to the pi.  Index.html uses the jscolor.js script to generate a color picker box that live updates.  Right now, supports blinking abilities with a specified timer within a 100 count for loop in the flask python file.
