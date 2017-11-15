from flask import Flask, render_template, redirect, request, flash
from mysqlconnection import MySQLConnector
from SLList  import SLList, UserNode

app = Flask(__name__)
mysql = MySQLConnector(app, 'friends')
app.secret_key = 'thisismysupersecretkey'

def listToFriendString(arr):
    nstr = ''
    for friend in arr:
        nstr += friend['first_name'] + ' ' + friend['last_name'] + ', '
    return nstr

class FlashMessage(object):
    def __init__(self, message, status):
        self.message = message
        self.status = status

@app.route('/')
def index():
    user_query = """
    SELECT
        users.id AS id, 
        CONCAT(users.first_name, ' ', users.last_name) AS name,
        GROUP_CONCAT(' ', friend.first_name, ' ', friend.last_name) AS friends
    FROM 
        users
    LEFT JOIN friendships ON users.id = friendships.user_id
    LEFT JOIN users AS friend ON friendships.friend_id = friend.id
    GROUP BY users.id;
    """
    users = mysql.query_db(user_query.strip())
    print "******"*2
    print users
    print "******"*2
    return render_template('index.html', users=users)

@app.route('/addUser', methods=["POST"])
def create():
    create_query = """
    INSERT INTO users (first_name, last_name, created_at, updated_at)
    VALUES (:first_name, :last_name, NOW(), NOW())
    """

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name']
    }

    mysql.query_db(create_query.strip(), data)

    return redirect('/')

@app.route('/friendship', methods=["POST"])
def friendify():
    friend_query = """
    INSERT INTO friendships (user_id, friend_id, created_at, updated_at)
    VALUES (:user_id, :friend_id, NOW(), NOW())
    """
    
    data = {
        "user_id": request.form['user_id'],
        "friend_id": request.form['friend_id'],
    }

    reverse_data = {
        "user_id": request.form['friend_id'],
        "friend_id": request.form['user_id'],
    }

    mysql.query_db(friend_query.strip(), data)
    mysql.query_db(friend_query.strip(), reverse_data)

    return redirect('/')

app.run(debug=True)