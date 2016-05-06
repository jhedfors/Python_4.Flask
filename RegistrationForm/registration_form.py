from flask import Flask, render_template, request, redirect, session,flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)(.{8,})$')
app = Flask(__name__)
app.secret_key = 'secretisnone'
mysql = MySQLConnector(app,'mydb')
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/register', methods=['POST'])
def registration_form():
    errors = 0
    if len(request.form['fname'])< 1:
        flash(u'First Name cannot be empty!','fname_error')
        errors = 1
    elif not NAME_REGEX.match(request.form['fname']):
        flash(u"Invalid First Name!",'fname_error')
        errors = 1
    if len(request.form['lname'])< 1:
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
    elif not PASSWORD_REGEX.match(request.form['password']):
        flash(u"Password must be at least 8 characters,and contain at least 1 uppercase letter and one number!",'password_error')
        errors = 1
    if len(request.form['password_conf'])< 1:
        flash(u'Password Confirmation cannot be empty!','password_conf_error')
        errors = 1
    if not request.form['password_conf'] == request.form['password']:
        flash(u'Password and Confirmation must match!','password_conf_error')
        errors = 1
    if errors > 0:
        return redirect('/')
    else:
        add()
        return render_template("result.html")
def add():
    print request.form
    query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
    data = {'first_name' : request.form['fname'],'last_name' : request.form['lname'],'email' : request.form['email'],'password' : request.form['password']}
    print query
    print data
    mysql.query_db(query,data)
    return redirect("/")

app.run(debug=True)
