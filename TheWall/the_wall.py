from flask import Flask, render_template, request, redirect, session,flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)(.{8,})$')
from flask.ext.bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'secretisnone'
mysql = MySQLConnector(app,'the_wall')
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/login', methods=['POST'])
def login_form():
    errors = 0
    if len(request.form['email'])< 1:
        flash(u'Email cannot be empty!','login_email_error')
        errors = 1
    elif not EMAIL_REGEX.match(request.form['email']):
        flash(u"Invalid Email Address!",'login_email_error')
        errors = 1
    if len(request.form['password'])< 1:
        flash(u'Password cannot be empty!','login_password_error')
        errors = 1
    if errors > 0:
        return redirect('/')
    else:
        db = login()
        match = bcrypt.check_password_hash(db[0]['password'], request.form['password'])
        if(db):
            if(match):
                session['active_id'] = db[0]['id']
                return redirect('/wall')
            return redirect('/')
        else:
            flash(u'Email/password not valid!','login_password_error')
            return redirect('/')
def login():
    query = "SELECT id, password FROM users WHERE email = :email"
    data = {'email' : request.form['email']}
    return mysql.query_db(query,data)
@app.route('/register', methods=['POST'])
def registration_form():
    errors = 0
    if len(request.form['fname'])< 2:
        flash(u'First Name cannot be empty!','fname_error')
        errors = 1
    elif not NAME_REGEX.match(request.form['fname']):
        flash(u"Invalid First Name!",'fname_error')
        errors = 1
    if len(request.form['lname'])< 2:
        flash(u'Last Name cannot be empty!','lname_error')
        errors = 1
    elif not NAME_REGEX.match(request.form['lname']):
        flash(u"Invalid Last Name!",'lname_error')
        errors = 1
    if len(request.form['email'])< 1:
        flash(u'Email cannot be empty!','email_error')
        errors = 1
    elif not EMAIL_REGEX.match(request.form['email']):
        flash(u"Invalid Email Address!",'email_error')
        errors = 1
    if len(request.form['password'])< 1:
        flash(u'Password cannot be empty!','password_error')
        errors = 1
    # elif not PASSWORD_REGEX.match(request.form['password']):
    #     flash(u"Password must be at least 8 characters,and contain at least 1 uppercase letter and one number!",'password_error')
    #     errors = 1
    if len(request.form['password_conf'])< 1:
        flash(u'Password Confirmation cannot be empty!','password_conf_error')
        errors = 1
    if not request.form['password_conf'] == request.form['password']:
        flash(u'Password and Confirmation must match!','password_conf_error')
        errors = 1
    if(login()):
        flash(u'Email already exists!','password_conf_error')
    if errors > 0:
        return redirect('/')
    add()
    return redirect('/wall')
def add():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    query = "INSERT INTO users (first_name, last_name, email, password, created_on, modified_on) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
    data = {'first_name' : request.form['fname'],'last_name' : request.form['lname'],'email' : request.form['email'],'password' : pw_hash}
    mysql.query_db(query,data)
@app.route('/wall')
def wall_page():
    messages = get_messages()
    print messages
    return render_template("wall.html")
def get_messages():
    active_id = session['active_id']
    query = "SELECT messages.id AS message_id, first_name, last_name, message, messages.created_on, messages.users_id AS messages_users_id FROM messages LEFT JOIN users ON users.id = :id"
    data = {'id' : active_id}
    return mysql.query_db(query,data)
def add_message(message,active_id):
    active_id = session['active_id']
    query = "INSERT INTO messages (message, created_on, modified_on, users_id) VALUES (:message, NOW(), NOW(), :active_id)"
    data = {'message' : message,'active_id' : active_id}
@app.route('/logoff')
def logoff():
    session.clear()
    return redirect
    ('/')
app.run(debug=True)
