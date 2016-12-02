"""
colorhandler.py
A flask script that handles http requests to change GPIO PWN duty cycle
with the pi-blaster library.
Author: Stephen Greene
"""
from __future__ import print_function
from flask import Flask, redirect, request, render_template, jsonify
from pathlib import Path
import time, hashlib
from flask_restful import Resource, Api


app = Flask(__name__)


REDPIN = 22
GREENPIN = 23
BLUEPIN = 24
f = open(str(Path("/dev/pi-blaster").absolute()), "w", 0)


@app.route("/set", methods=["POST", "GET"])
def parseColor():
    color = request.form["color"]
    try:
        setColor(color)
    except ValueError:
        color = stringColor(color)
        setColor(color)

    return jsonify({"Function" : "Set color"},
        {"Color" : str(color)})


@app.route("/setOff")
def turnOutputOff():
    setColor("000000");
    return jsonify({"Function" : "Set lights to OFF"})


@app.route("/")
def index():
    #basic instructions for connection to /
    return jsonify({"/" : "MOLS Help Request"},
        {"/set" : "Color=FFFFFF (6 digit hex format, no # sign)"},
        {"/setOff" : "No params: turns lights off (hex value 000000)"})


def setColor(color):
    red = str(REDPIN) + "=" + "%.3f" % (int(color[:2], 16) / 255.0)
    green = str(GREENPIN) + "=" + "%.3f" % (int(color[2:4], 16) / 255.0)
    blue = str(BLUEPIN) + "=" + "%.3f" % (int(color[4:], 16) / 255.0)
    print(red, file=f)
    print(green, file=f)
    print(blue, file=f)


def setFade(colorOne, colorTwo):
    colorOneVals = [int(colorOne[:2], 16), int(colorOne[2:4], 16),
    int(colorOne[4:], 16)]

    colorTwoVals = [int(colorTwo[:2], 16), int(colorTwo[2:4], 16),
    int(colorTwo[4:], 16)]

    while ((colorOneVals[0] != colorTwoVals[0])
        or (colorOneVals[1] != colorTwoVals[1])
        or (colorOneVals[2] != colorTwoVals[2])):
        hexColor = ""
        for x in range(0, 3):
            if colorOneVals[x] > colorTwoVals[x]:
                colorOneVals[x] -= 1
            elif colorOneVals[x] < colorTwoVals[x]:
                colorOneVals[x] += 1
            if colorOneVals[x] < 10:      #format hex digits in string correctly
                hexColor += "0"
            #remove front 2 chars of hex value
            hexColor += str(hex(colorOneVals[x]))[2:]
        setColor(hexColor)


#Hash a given string to a 6 digit hex color
def stringColor(string):
    h = hashlib.md5(string)
    n = int(h.hexdigest(), 16)
    n = n % (256 ** 3)
    return "%06x" % n


if __name__ == "__main__":
   app.run()

