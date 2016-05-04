from flask import Flask, render_template, request, redirect, session
import random
import datetime
app = Flask(__name__)
app.secret_key = 'secretisnone'
@app.route('/')
def index():
    if 'score' not in session:
        session['score'] = 0
    if 'actions' not in session:
        session['actions'] = []
    return render_template("index.html")
@app.route('/process_money', methods=['POST'])
def process_money():
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %I:%M %p")
    print current_time
    print datetime.datetime.now()
    if request.form['building'] == 'farm':
        randNum = random.randrange(10,21)
        session['score'] += randNum
        session['actions'].insert(0,"Earned " + str(randNum)+ " golds from the farm! ("+current_time+")")
    if request.form['building'] == 'cave':
        randNum = random.randrange(5,11)
        session['score'] += randNum
        session['actions'].insert(0,"Earned " + str(randNum)+ " golds from the cave! ("+current_time+")")
    if request.form['building'] == 'house':
        randNum = random.randrange(2,6)
        session['score'] += randNum
        session['actions'].insert(0,"Earned " + str(randNum)+ " golds from the house! ("+current_time+")")
    if request.form['building'] == 'casino':
        if random.randrange(0,2) == 1:
            randNum = random.randrange(0,51)
            session['score'] += randNum
            session['actions'].insert(0,"Earned " + str(randNum)+ " golds from the casino! ("+current_time+")")
        else:
            randNum = random.randrange(0,51)
            session['score'] -= randNum
            session['actions'].insert(0,"Lost " + str(randNum)+ " golds from the casino! ("+current_time+")")
    return redirect('/')
@app.route('/reset')
def reset():
    del session['actions']
    del session['score']
    return redirect('/')
app.run(debug=True)
