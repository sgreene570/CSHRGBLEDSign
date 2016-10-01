from flask import Flask, redirect, request, render_template
app = Flask(__name__)


@app.route('/set', methods=['GET', 'POST'])
def colorhandler():
    with open("/dev/pi-blaster") as f:
        print("22=" + str(request.form['redval'] / 255.0), f)
        print("23=" + str(request.form['greenval'] / 255.0), f)
        print("24=" + str(request.form['blueval'] / 255.0), f)
    return redirect('/')


@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
   app.run(debug=True)