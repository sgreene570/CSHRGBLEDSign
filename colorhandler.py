"""
colorhandler.py
A flask script that handles requests to change GPIO PWN through the pi-blaster library
Stephen Greene
"""
from __future__ import print_function
from flask import Flask, redirect, request, render_template
from pathlib import Path
import time
app = Flask(__name__)


@app.route('/set', methods=['GET', 'POST'])
def parseColor():
    f = open(str(Path("/dev/pi-blaster").absolute()), "w", 0)       # 0 forces file flushing
    global color
    global timer
    global loop
    color = request.form['color']
    timer = int(request.form['timer'])
    loop = int(request.form['loop'])
    return setColor(color, timer, loop, f)


def setColor(color, timer, loop, f):
    red = "22=" + "%.3f" % (int(color[:2], 16) / 255.0)
    green = "23=" + "%.3f" % (int(color[2:4], 16) / 255.0)
    blue = "24=" + "%.3f" % (int(color[4:], 16) / 255.0)
    print(red, file=f)
    print(green, file=f)
    print(blue, file=f)

    if timer > 0 and loop > 0:
        for x in range(0, loop):
            time.sleep(timer / 100.0)        # convert time to milliseconds for blinks
            print("22=0", file=f)
            print("23=0", file=f)
            print("24=0", file=f)
            time.sleep(timer / 100.0)
            print(red, file=f)
            print(green, file=f)
            print(blue, file=f)
            x += 1

    return "Color: " + color + " Timer: " + str(timer) + " Loop: " + str(loop)


@app.route('/set2', methods=['GET', 'POST'])
def parseTwoColors():
    global timer
    global loop
    global color
    f = open(str(Path("/dev/pi-blaster").absolute()), "w", 0)       # 0 forces file flushing
    timer = int(request.form['timer'])
    loop = int(request.form['loop'])
    colorOne = request.form['colorOne']
    colorTwo = request.form['colorTwo']
    for x in range(0, loop):
        setColor(colorOne, 0, 0, f)
        time.sleep(timer / 100.0)
        setColor(colorTwo, 0, 0, f)
        time.sleep(timer / 100.0)
        x += 1
    color = colorOne        #colorOne will always be last color displayed
    return setColor(colorOne, 0, 0, f)


@app.route('/setFade', methods=['GET', 'POST'])
def parseFade():
    global timer
    global loop
    global color
    f = open(str(Path("/dev/pi-blaster").absolute()), "w", 0)
    timer = int(request.form['timer'])
    loop = int(request.form['loop'])
    colorOne = request.form['colorOne']
    colorTwo = request.form['colorTwo']
    for x in range(int(colorOne, 16), int(colorTwo, 16)):
        setColor(x, timer, loop, f)
        if int(colorOne, 16) > int(colorTwo, 16):
            x -= hex(1)
        else:
            x += hex(1)

    return setColor(colorTwo, 0, 0, f)

@app.route('/getLast', methods=['GET'])
def getLast():
    #returns last recieved set of instructions even if they are still running. Good for repeating
    if 'color' in globals() and 'timer' in globals() and 'loop' in globals(): 
        return "Last arguments recevied: Color: " + color + " timer: " + str(timer) + " loop: " + str(loop)

    return "no arguments have been received"


@app.route('/')
def index():
    #basic instructions for connection to wrong url rather than 404
    return "use /set with color, timer, and loop args or /set2 with colorOne, colorTwo, timer, and loop"


if __name__ == '__main__':
   app.run()

