from flask import Flask, render_template, redirect, session, flash, request
app = Flask(__name__)
app.secret_key = 'secretisnone'
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/ninja/', defaults={'name': 'all'})
@app.route('/ninja/<name>')
def ninja(name):
    if name == 'all':
        ninja = 'all'
    elif name == 'blue':
        ninja = 'blue'
    elif name == 'orange':
        ninja = 'orange'
    elif name == 'red':
        ninja = 'red'
    elif name == 'purple':
        ninja = 'purple'
    else:
        ninja = 'none'
    return render_template("ninjas.html",ninja = ninja)
app.run(debug=True)
