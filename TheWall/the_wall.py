from flask import Flask, render_template, request, redirect, session,flash
from mysqlconnection import MySQLConnector
import re, datetime, time
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)(.{8,})$')
from flask.ext.bcrypt import Bcrypt
from datetime import date
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
        flash(u'Cannot be empty!','login_email_error')
        errors = 1
    elif not EMAIL_REGEX.match(request.form['email']):
        flash(u"Invalid Email Address!",'login_email_error')
        errors = 1
    if len(request.form['password'])< 1:
        flash(u'Cannot be empty!','login_password_error')
        errors = 1
    if errors > 0:
        return redirect('/')
    else:
        db = show_by_email()
        if(db):
            match = bcrypt.check_password_hash(db[0]['password'], request.form['password'])
            if(match):
                session['active_id'] = db[0]['id']
                session['active_name'] = db[0]['first_name']
                return redirect('/wall')
        flash(u'Email/password not valid!','login_password_error')
        return redirect('/')
def show_by_email():
    query = "SELECT id, password, first_name FROM users WHERE email = :email"
    data = {'email' : request.form['email']}
    return mysql.query_db(query,data)
@app.route('/register', methods=['POST'])
def registration_form():
    errors = 0
    if len(request.form['fname'])< 2:
        flash(u'Cannot be empty!','fname_error')
        errors = 1
    elif not NAME_REGEX.match(request.form['fname']):
        flash(u"Invalid First Name!",'fname_error')
        errors = 1
    if len(request.form['lname'])< 2:
        flash(u'Cannot be empty!','lname_error')
        errors = 1
    elif not NAME_REGEX.match(request.form['lname']):
        flash(u"Invalid Last Name!",'lname_error')
        errors = 1
    if len(request.form['email'])< 1:
        flash(u'Cannot be empty!','email_error')
        errors = 1
    elif not EMAIL_REGEX.match(request.form['email']):
        flash(u"Invalid!",'email_error')
        errors = 1
    if len(request.form['password'])< 1:
        flash(u'Cannot be empty!','password_error')
        errors = 1
    elif not PASSWORD_REGEX.match(request.form['password']):
        flash(u"Password must be at least 8 characters,and contain at least 1 uppercase letter and one number!",'password_error')
        errors = 1
    if len(request.form['password_conf'])< 1:
        flash(u'Cannot be empty!','password_conf_error')
        errors = 1
    if not request.form['password_conf'] == request.form['password']:
        flash(u'Password and Confirmation must match!','password_conf_error')
        errors = 1
    if(show_by_email()):
        flash(u'Email already exists!','password_conf_error')
    if errors > 0:
        return redirect('/')
    add()
    db = show_by_email()
    session['active_id'] = db[0]['id']
    session['active_name'] = db[0]['first_name']
    return redirect('/wall')
@app.route('/logoff')
def logoff():
    session.clear()
    return redirect('/')
def add():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    query = "INSERT INTO users (first_name, last_name, email, password, created_on, modified_on) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
    data = {'first_name' : request.form['fname'],'last_name' : request.form['lname'],'email' : request.form['email'],'password' : pw_hash}
    mysql.query_db(query,data)
@app.route('/wall')
def wall_page():
    if 'active_id' not in session:
        print 'not in session'
        return redirect('/logoff')
    messages = get_messages()
    comments = {}
    for message in messages:
        print message['message_id']
        comment = get_comment_by_message(message['message_id'])
        comments[message['message_id']] = comment
    return render_template("wall.html", messages = messages, comments = comments)
def get_messages():
    query = "SELECT messages.id AS message_id, first_name, last_name, message, messages.created_on, messages.users_id AS messages_users_id FROM messages LEFT JOIN users ON users.id = messages.users_id ORDER BY created_on DESC"
    return mysql.query_db(query)
def get_message_by_id(message_id):
    query = "SELECT messages.created_on FROM messages WHERE id = :id"
    data = {'id' : message_id}
    return mysql.query_db(query,data)
def get_comment_by_id(comment_id):
    query = "SELECT comments.created_on FROM comments WHERE id = :id"
    data = {'id' : comment_id}
    return mysql.query_db(query,data)
def get_comment_by_message(messages_id):
    query = "SELECT comments.id AS 	comment_id, comments.users_id AS comment_user_id, first_name, last_name, comment, comments.created_on, messages_users_id, messages_id  FROM comments   LEFT JOIN users   ON users.id = comments.users_id WHERE messages_id = :messages_id"
    data = {'messages_id' : messages_id}
    return mysql.query_db(query,data)
def can_delete(type,id,user_id):
    now = datetime.datetime.now()
    if type == "message":
        time_dif = now - get_message_by_id(id)[0]['created_on']
    elif type == "comment":
        time_dif = now - get_comment_by_id(id)[0]['created_on']
    if time_dif > datetime.timedelta(minutes=30):
        return False
    if int(user_id) != session['active_id']:
        return False
    return True
@app.route('/add_message',methods=['POST'])
def add_message():
    query = "INSERT INTO messages (message, created_on, modified_on, users_id) VALUES (:message, NOW(), NOW(), :active_id)"
    data = {'message' : request.form['post_message'],'active_id' : session['active_id']}
    mysql.query_db(query,data)
    return redirect('/wall')
@app.route('/delete_message/<message_id>/<messages_user_id>')
def delete_message(message_id, messages_user_id):
    if not (can_delete('message',message_id,messages_user_id)):
        return redirect('/wall')
    query1 = "DELETE FROM comments WHERE comments.messages_users_id = :messages_user_id"
    data1 = {'messages_user_id':messages_user_id}
    mysql.query_db(query1,data1)
    query2 = "DELETE FROM messages WHERE messages.id = :message_id"
    data2 = {'message_id':message_id}
    mysql.query_db(query2,data2)
    return redirect('/wall')
@app.route('/add_comment',methods=['POST'])
def add_comment():
    query = "INSERT INTO comments (comment, created_on, modified_on, users_id, messages_id, messages_users_id) VALUES (:comment, NOW(), NOW(), :active_id,:message_id, :message_users_id)"
    data = {'comment' : request.form['post_comment'],'active_id' : session['active_id'], 'message_id' : request.form['message_id'],'message_users_id' : request.form['message_users_id']}
    mysql.query_db(query,data)
    return redirect('/wall')
@app.route('/delete_comment/<comment_id>/<comment_user_id>')
def delete_comment(comment_id, comment_user_id):
    if not (can_delete('comment',comment_id,comment_user_id)):
        return redirect('/wall')
    query = "DELETE FROM comments WHERE comments.id = :comment_id"
    data = {'comment_id':comment_id}
    mysql.query_db(query,data)
    return redirect('/wall')
app.run(debug=True)
