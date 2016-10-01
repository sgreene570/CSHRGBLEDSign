from flask import Flask, redirect, request, render_template
from pathlib import Path
app = Flask(__name__)


@app.route('/set', methods=['GET', 'POST'])
def colorhandler():
    f = open(str(Path("/dev/pi-blaster").absolute()))
    red = "22=" + "%.3f" % (int(request.form['redval']) / 255.0)
    green = "23=" + "%.3f" % (int(request.form['greenval']) / 255.0)
    blue = "24=" + "%.3f" % (int(request.form['blueval']) / 255.0)
    print(red, file=f)
    print(green, file=f)
    print(blue, file=f)

    return redirect('/')


@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
   app.run(debug=True)