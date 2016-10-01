from flask import Flask, redirect, request, render_template
app = Flask(__name__)


@app.route('/set', methods=['GET', 'POST'])
def colorhandler():
    with open("/dev/pi-blaster") as f:
        red = "22=" + "%.3f" % str(int(request.form['redval']) / 255.0)
        green = "23=" + "%.3f" % str(int(request.form['greenval']) / 255.0)
        blue = "24=" + "%.3f" % str(int(request.form['blueval']) / 255.0)
        f.write(red.encode('utf8'))
        f.write(green.encode('utf8'))
        f.write(blue.encode('utf8'))

    return redirect('/')


@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
   app.run(debug=True)