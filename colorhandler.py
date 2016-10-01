from flask import Flask, request
app = Flask(__name__)


@app.route("/", methods=['POST'])
def color():
    test = request.form['redval'] + " " + request.form['greeneval'] + " " + request.form['blueval']
    f = open("/dev/pi-blaster")
    print(test)
    print('echo"22=' + str(request.form['redval'] / 1.0)) >> f
    print('echo"23=' + str(request.form['greenval'] / 1.0)) >> f
    print('echo"24=' + str(request.form['blueval'] / 1.0)) >> f


if __name__ == "__main__":
    app.run()
