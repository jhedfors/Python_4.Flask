from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = 'secretisnone'
@app.route('/')
def index():
    if 'name_error' not in session:
        session['name_error'] = ''
    if 'comment_error' not in session:
        session['comment_error'] = ''    
    return render_template("index.html")
@app.route('/result', methods=['POST'])
def survey_form():
    del session['name_error']
    del session['comment_error']
    errors = 0
    if len(request.form['name'])< 1:
        session['name_error'] = "Name cannot be empty!"
        errors = 1
    if len(request.form['comment'])< 1:
        session['comment_error']="Comment cannot be empty!"
        errors = 1
    if len(request.form['comment'])> 120:
        session['comment_error']="Comments cannot be longer than 120 characters!"
        errors = 1
    if errors > 0:
        return redirect('/')
    info = {'name' : request.form['name'],
    'location' : request.form['location'],
    'language' : request.form['language'],
    'comment' : request.form['comment']}
    return render_template("result.html",info = info)
app.run(debug=True)
