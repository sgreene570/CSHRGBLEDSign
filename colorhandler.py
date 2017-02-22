"""
colorhandler.py
A flask script that handles http requests to change GPIO PWN duty cycle
with the pi-blaster library.
Author: Stephen Greene
"""
from flask import Flask, redirect, request, render_template, jsonify
from flask_restful import Resource, Api
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
default_color = "#C1007C"
current_color = Color("#000")



@app.route("/", methods=["POST"])
@limiter.limit("4 per second")
def parse_color():
    color = request.form["color"]
    if color is None:
        abort(400)

    try:
        set_color(color)
    except ValueError:
        set_color(default_color)
        return jsonify({"Input error" : "Default color used"},
                {"Current color" : current_color.hex})

    return jsonify({"Current color" : str(current_color.hex)})


@app.route("/status", methods=["GET"])
@limiter.limit("4 per second")
def get_current_color():
    return jsonify({"Current color" : str(current_color.hex)})


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error="ratelimit exceeded %s" % e.description)


def set_color(color):
    global current_color
    current_color = Color(color)
    red = str(REDPIN) + "=" + "%.3f" % (current_color.red)
    green = str(GREENPIN) + "=" + "%.3f" % (current_color.green)
    blue = str(BLUEPIN) + "=" + "%.3f" % (current_color.blue)
    #Use os.system calls to avoid opening/closing the text file
    os.system("echo " + red + " >> /dev/pi-blaster")
    os.system("echo " + green + " >> /dev/pi-blaster")
    os.system("echo " + blue + " >> /dev/pi-blaster")
