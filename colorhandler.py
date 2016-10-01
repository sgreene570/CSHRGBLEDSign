from flask import Flask, redirect, request
app = Flask(__name__)


@app.route('/set', methods=['GET', 'POST'])
def colorhandler():
    print(request.form['redval'])
    print(request.form['greenval'])
    print(request.form['blueval'])

    return redirect('/')


if __name__ == '__main__':
   app.run(debug=True)