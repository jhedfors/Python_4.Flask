from flask import Flask, render_template, session, request, redirect
app = Flask(__name__)
app.secret_key = 'secretisnone'
@app.route('/')
def index():
    if 'visits' not in session:
        session['visits']=1
        return render_template('index.html')
    else:
        session['visits']+=1
        return render_template('index.html')
@app.route('/x2')
def x2():
    session['visits']+=2
    return render_template('index.html')
@app.route('/reset')
def reset():
    session['visits']=1
    return render_template('index.html')
app.run(debug=True)
