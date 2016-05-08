from flask import Flask, render_template, request, redirect
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'semi-restful')
@app.route('/')
def index():
    return redirect('/users')
@app.route('/users')
def index_users():
    return render_template("index_users.html")
@app.route('/users/new')
def new_user():
    return render_template("create_user.html")
@app.route('/users/create', methods = ["POST"])
def create_user():
    user_id = 1
    return redirect('/users/'+str(user_id))
@app.route('/users/<user_id>')
def show_user(user_id = None):
    info = {'user_id' : 1}
    return render_template('show_user.html', info = info)
@app.route('/users/<user_id>', methods = ['POST'])
def update_user():
    user_id = 1
    return redirect('/users/'+user_id)
@app.route('/users/<user_id>/edit')
def edit_user(user_id):
    info = {'user_id' : user_id}
    return render_template('edit_user.html', info = info)
@app.route('/users/<user_id>/destroy')
def destroy_user(user_id):
    info = {'user_id' : user_id}
    return redirect('/users')
app.run(debug=True)
