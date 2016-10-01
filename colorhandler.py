from flask import Flask, redirect, request, render_template
app = Flask(__name__)


@app.route('/set', methods=['GET', 'POST'])
def colorhandler():
    print(request.form['redval'])
    print(request.form['greenval'])
    print(request.form['blueval'])

    return redirect('/')


@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
   app.run(debug=True)