from flask import Flask, render_template, session, request, redirect
app = Flask(__name__)
app.secret_key = "itsnosecret"
@app.route('/')
def index():
    import random
    if 'random_num' not in session:
        session['random_num'] = random.randrange(1,101)
    return render_template('index.html')
@app.route('/guess', methods=['POST'])
def guess():
    guess = int(request.form['guess'])
    print session['random_num']
    print guess
    if  guess == session['random_num']:
        session['status']='winner'
    elif  guess > session['random_num']:
        session['status']='toohigh'
    else:
        session['status']='toolow'
    return redirect('/')
@app.route('/start_over')
def start_over():
    session['status'] = 'none'
    del session['random_num']
    return redirect('/')
app.run(debug=True)
