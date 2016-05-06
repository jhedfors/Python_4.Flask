# import Flask
from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnector
# the "re" module will let us perform some regular expression operations
import re
# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
mysql = MySQLConnector(app,'email_addresses')
@app.route('/', methods=['GET'])
def index():
  return render_template("index.html")
@app.route('/success')
def success():
    query = "SELECT * FROM users" # define your query
    users = mysql.query_db(query) # run the query with the query_db method
    return render_template('success.html', all_users=users) # pass the data to our template
@app.route('/process', methods=['POST'])
def submit():
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
    else:
        add()
        session['email'] = request.form['email']
        return redirect('/success')
    return redirect('/')
def add():
    query = "INSERT INTO users (email, created_at, modified_at) VALUES (:email, NOW(), NOW())"
    # we'll then create a dictionary of data from the POST data received
    data = {
           'email': request.form['email']
           }
    # run the query with the dictionary values injected into the query
    mysql.query_db(query, data)
@app.route('/delete/<id>')
def delete(id):
    query = "DELETE FROM users WHERE users.id = :id"
    # we'll then create a dictionary of data from the POST data received
    data = {
           'id': id
           }
    # run the query with the dictionary values injected into the query
    mysql.query_db(query, data)
    return redirect('/success')
app.run(debug=True)
