from flask import Flask, render_template, request, redirect
from mysqlconnection import MySQLConnector
import datetime
app = Flask(__name__)
mysql = MySQLConnector(app,'semi-restful-users')
@app.route('/')
def index():
    return redirect('/users')
@app.route('/users')
def index_users():
    query = "SELECT * FROM users"
    users = mysql.query_db(query)
    print users
    return render_template("index_users.html", users = users)
@app.route('/users/new')
def new_user():
    return render_template("create_user.html")
@app.route('/users/create', methods = ["POST"])
def create_user():
    print request.form
    query = "INSERT INTO users (first_name, last_name, email, created_at, modified_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
    values = {'first_name': request.form['first_name'],'last_name': request.form['last_name'],'email': request.form['email']}
    user_id =  mysql.query_db(query,values)
    return redirect('/users/'+str(user_id))
@app.route('/users/<user_id>')
@app.route('/users/<user_id>', methods = ['POST'])
def show_user(user_id):
    if request.form:
        update_user(user_id)
    info = show_user_by_id(user_id)[0]
    return render_template('show_user.html', info = info)
def show_user_by_id(user_id):
    query = "SELECT * FROM users WHERE id = :user_id"
    values = {'user_id': user_id}
    return mysql.query_db(query,values)
def update_user(user_id):
    query = "UPDATE users SET first_name = :first_name, last_name = :last_name, email = :email, modified_at = NOW() WHERE id = :id"
    values = {'first_name': request.form['first_name'],'last_name': request.form['last_name'],'email': request.form['email'],'id':user_id}
    mysql.query_db(query,values)
    return redirect('/users/'+user_id)
@app.route('/users/<user_id>/edit')
def edit_user(user_id):
    info = show_user_by_id(user_id)[0]
    return render_template('edit_user.html', info = info)
@app.route('/users/<user_id>/destroy')
def destroy_user(user_id):
    query = "DELETE FROM users WHERE id = :id"
    values = {'id': user_id}
    mysql.query_db(query,values)
    return redirect('/users')
app.run(debug=True)
