from flask import Flask, render_template, request, redirect, session,flash
app = Flask(__name__)
app.secret_key = 'secretisnone'
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/register', methods=['POST'])
def registration_form():
    errors = 0
    if len(request.form['fname'])< 1:
        flash(u'First Name cannot be empty!','fname_error')
        errors = 1
    if len(request.form['fname'])< 1:
        flash(u'Last Name cannot be empty!','lname_error')
        errors = 1
    if len(request.form['email'])< 1:
        flash(u'Email cannot be empty!','email_error')
        errors = 1
    if len(request.form['password'])< 1:
        flash(u'Password cannot be empty!','password_error')
        errors = 1
    if len(request.form['password_conf'])< 1:
        flash(u'Password Confirmation cannot be empty!','password_conf_error')
        errors = 1
    if errors > 0:
        return redirect('/')
    info = {'fname' : request.form['fname'],
    'lname' : request.form['lname'],
    'email' : request.form['email'],
    'password' : request.form['password'],
    'password_conf' : request.form['password_conf']}
    return render_template("result.html",info = info)
app.run(debug=True)
