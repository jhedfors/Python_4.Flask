from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'friendsdb')
@app.route('/')
def index():
    query = "SELECT * FROM users" # define your query
    users = mysql.query_db(query) # run the query with the query_db method
    return render_template('index.html', all_friends=friends) # pass the data to our template
@app.route('/friends', methods=['POST'])
def create():
    print request.form['first_name']
    # write our query as a string, notice how we have multiple values we want to
    # insert into our query
    query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (:firstname, :lastname, :occupation, NOW(), NOW())"
    # we'll then create a dictionary of data from the POST data received
    data = {
           'firstname': request.form['first_name'],
           'lastname':  request.form['last_name'],
           'occupation': request.form['occupation']
           }
    print data
    # run the query with the dictionary values injected into the query
    mysql.query_db(query, data)
    return redirect('/')
@app.route('/friends/<friend_id>')
def index_friends(friend_id):
    # write a query to select a specific user by id at every point where
    # we want to insert data we will write a ":" and a some variable name
    query = "SELECT * FROM friends WHERE id = :specific_id"
    # then we define a dictionary that has a key that matches the :variable_name in our query
    data = {'specific_id': friend_id}
    # run the query with inserted data
    friends = mysql.query_db(query, data)
    # friends should be a list with a single object
    # so we will pass the value that the zero index to our template under
    # the alias one_friend
    return render_template('index.html', one_friend=friends[0])
@app.route('/update_friend/<friend_id>', methods=['POST'])
def update(friend_id):
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, occupation = :occupation WHERE id = :id"
    data = {
           'first_name': request.form['first_name'],
           'last_name':  request.form['last_name'],
           'occupation': request.form['occupation'],
           'id': friend_id
           }
    mysql.query_db(query, data)
    return redirect('/')
@app.route('/remove_friend/<friend_id>', methods=['POST'])
def update2(friend_id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': friend_id}
    mysql.query_db(query, data)
app.run(debug=True)
