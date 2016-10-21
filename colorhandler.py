"""
colorhandler.py
A flask script that handles requests to change GPIO PWN duty cycle 
with the pi-blaster library.
Change pin numbers at the top of the setColor function 
to change which pinouts of the raspi are used
Author: sgreene570
"""
from __future__ import print_function
from flask import Flask, redirect, request, render_template, jsonify
from pathlib import Path
import time, hashlib
from flask_restful import Resource, Api


app = Flask(__name__)


@app.route('/set', methods=['POST'])
def parseColor():
    color = request.form['color']
    timer = int(request.form['timer'])
    loop = int(request.form['loop'])
    setColor(color, timer, loop)
    return jsonify({"Function" : "Set color"}, 
        {"Color" : str(color)}, 
        {"Timer" : str(timer)}, 
        {"Loop" : str(loop)})


@app.route('/setFade', methods=['POST'])
def parseFade():
    timer = int(request.form['timer'])
    loop = int(request.form['loop'])
    colorOne = request.form['colorOne']
    colorTwo = request.form['colorTwo']
    setFade(colorOne, colorTwo, timer, loop)
    return jsonify({"Function" : "Fade"}, 
        {"Starting color" : str(colorOne)},
        {"Ending color" : str(colorTwo)}, 
        {"Timer" : str(timer)}, 
        {"Loop" : str(loop)})


@app.route('/setString', methods=['POST'])
def parseString():
    color = stringColor(request.form['string'])
    setColor(color, 0, 0)
    return jsonify({"Function" : "Set color with string"}, 
        {"Color" : str(color)})


@app.route('/setStringFade', methods=['POST'])
def praseStringFade():
    timer = int(request.form['timer'])
    loop = int(request.form['loop'])
    colorOne = stringColor(request.form['stringOne'])
    colorTwo = stringColor(request.form['stringTwo'])
    setFade(colorOne, colorTwo, timer, loop)
    return jsonify({"Function" : "Fade from Strings"}, 
        {"Starting color" : str(colorOne)},
        {"Ending color" : str(colorTwo)}, 
        {"Timer" : str(timer)}, 
        {"Loop" : str(loop)})


@app.route('/')
def index():
    #basic instructions for connection to wrong url rather than 404
    return """/set: color, timer, and loop \n /set2: colorOne, colorTwo, timer, 
        and loop \n /setFade colorOne, colorTwo, timer, and loop"""


def setColor(color, timer, loop):
    f = openFile()
    red = "22=" + "%.3f" % (int(color[:2], 16) / 255.0)
    green = "23=" + "%.3f" % (int(color[2:4], 16) / 255.0)
    blue = "24=" + "%.3f" % (int(color[4:], 16) / 255.0)
    print(red, file=f)
    print(green, file=f)
    print(blue, file=f)

    if timer > 0 and loop > 0:
        for x in range(0, loop):
            time.sleep(timer / 100.0)  #convert time to milliseconds for blinks
            print("22=0", file=f)
            print("23=0", file=f)
            print("24=0", file=f)
            time.sleep(timer / 100.0)
            print(red, file=f)
            print(green, file=f)
            print(blue, file=f)
            x += 1


def setFade(colorOne, colorTwo, timer, loop):
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
        setColor(hexColor, timer, loop)


def stringColor(string):
    h = hashlib.md5(string)
    n = int(h.hexdigest(), 16)
    n = n % (256 ** 3)
    return "%06x" % n


def openFile():
    #open file with write premissions and instant flushing
    f = open(str(Path("/dev/pi-blaster").absolute()), "w", 0)
    return f


if __name__ == '__main__':
   app.run()

