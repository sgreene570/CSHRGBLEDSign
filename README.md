# cshrgbledsign

WIP Networked RGB LEDs using the Python Flask Library.  Prints out to the pi-blaster library with RGB Leds connected to GPIO pins 22, 23, and 24 in that respective order.  See the sample HTML website to see what form data is being sent over HTTP.  Feel free to work code however you would like or to contact me with questions.
=======
Networked RGB LEDs. Work in progress. Implemented using pi-blaster library on a raspberry pi running the python flask library.
Uses software pwm pins 22,23, and 24 for respective RGB values.  Tip 120 transistors connect LEDS to the pi.  Index.html uses the jscolor.js script to generate a color picker box that live updates.  Right now, supports blinking abilities with a specified timer within a 100 count for loop in the flask python file.

