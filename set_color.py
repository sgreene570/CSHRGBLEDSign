"""
set_color.py
Takes RGB values over the command line along with a timer length
Implements argparse and GPIO
"""


import argparse
import RPi.GPIO as GPIO
import time

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("r", help="Enter r value(0-255)")
    parser.add_argument("g", help="Enter g value(0-255)")
    parser.add_argument("b", help="Enter b value(0-255)")
    parser.add_argument("time", help="Enter a time length");
    args = parser.parse_args()
    set_color(int(args.r), int(args.g), int(args.b), int(args.time))

def set_color(redval, greenval, blueval, timer):
    # LED pin mapping.
    red = 18
    green = 23
    blue = 24

    # GPIO Setup.
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(red, GPIO.OUT)
    GPIO.setup(green, GPIO.OUT)
    GPIO.setup(blue, GPIO.OUT)

    red = GPIO.PWM(red, 100)
    green = GPIO.PWM(green, 100)
    blue = GPIO.PWM(blue, 100)
    red.start(0)
    green.start(0)
    blue.start(0)
    red.ChangeDutyCycle((redval / 255.0) * 100)
    green.ChangeDutyCycle((greenval / 255.0) * 100)
    blue.ChangeDutyCycle((blueval / 255.0) * 100)

    time.sleep(timer)
    GPIO.cleanup()

if __name__ == '__main__':
    main()
