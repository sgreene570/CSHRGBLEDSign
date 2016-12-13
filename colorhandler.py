"""
colorhandler.py
A flask script that handles http requests to change GPIO PWN duty cycle
with the pi-blaster library.
Author: Stephen Greene
"""
from flask import Flask, redirect, request, render_template, jsonify
from flask_restful import Resource, Api
from pathlib import Path
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from colour import Color
import time, hashlib, os


app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address)


REDPIN = 22
GREENPIN = 23
BLUEPIN = 24
currColor = Color("#000")


@app.route("/set", methods=["POST", "GET"])
@limiter.limit("4 per second")
def parseColor():
    color = request.form["color"]
    try:
        setColor(color)
    except ValueError:
        color = "C1007C"
        setColor(color)
        return jsonify({"Input error" : "Default color used"},
                {"Color" : color})

    return jsonify({"Function" : "Set color"},
        {"Color" : color})


@app.route("/setOff")
def turnOutputOff():
    setColor("#000");
    return jsonify({"Function" : "Set lights to OFF"})


@app.route("/")
def index():
    #basic instructions for connection to /
    return jsonify({"/" : "MOLS Help Request"},
        {"/set" : "Color=#FFFFFF (Hex color code or english name allowed)"},
        {"/setOff" : "No params: turns lights off"},
        {"Current color" : currColor.hex})

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error="ratelimit exceeded %s" % e.description)


def setColor(color):
    global currColor
    currColor = Color(color)
    red = str(REDPIN) + "=" + "%.3f" % (currColor.red)
    green = str(GREENPIN) + "=" + "%.3f" % (currColor.green)
    blue = str(BLUEPIN) + "=" + "%.3f" % (currColor.blue)
    os.system("echo " + red + " >> /dev/pi-blaster")
    os.system("echo " + green + " >> /dev/pi-blaster")
    os.system("echo " + blue + " >> /dev/pi-blaster")


if __name__ == "__main__":
   app.run()
