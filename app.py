from flask import Flask, render_template, request, redirect, url_for
from main import loop


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ndays = request.form['ndays']
        return redirect(url_for('success', ndays=ndays))
    else:
        return render_template('index.html')

@app.route('/success/<ndays>', methods=['GET'])
def success(ndays):
    return render_template('success.html', ndays=ndays)
