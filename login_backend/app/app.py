from wsgiref import validate
from flask import Flask, flash, redirect, render_template, render_template_string, request,g,session
from flask_restful import Resource, Api,reqparse,abort
from flask_mysqldb import MySQL
from matplotlib.style import context
from logic import hashpassword,check_if_password_is_valid,check_hashed_password,is_userName_valid   
import os

app = Flask(__name__)
api = Api(app)
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = os.environ["SECRET"]
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_DB"] = "theDatabase"

mysql = MySQL(app)

def connection():
    '''creates connection to mysql server'''
    return mysql.connection

@app.before_request
def before_request():
    g.db = connection()
    '''triggers method before every request
        Opens database'''

@app.route('/signup',methods = ["GET","POST"])
def signup():
    '''triggered when a GET or POST request is sent to "/signup" endpoint'''
    c = g.db.cursor()
    if request.method == "GET":
        if "user" in session:
            '''meaning user is logged in and in a session'''
            return redirect('/front')

        '''triggered when GET request is sent to endpoint at renders login page'''
        return render_template("sign_up.html") # why wont you render
    
    '''triggered if POST request'''
    username = request.form["username"]
    password = request.form["password"]
    confirm_password = request.form['confirm_password'] 
    if password == confirm_password and is_userName_valid(username) and check_if_password_is_valid(password):
        '''triggered if form data is all valid'''
        c.execute("INSERT INTO users(userName,password) VALUES(%s,%s)",(username,hashpassword(password))) # inserts user into user table
        g.db.commit() # commmits user into table
        return redirect('/login') # redirects to login page 
    else:
        return render_template('sign_up.html',context={"message":"Username or Password are not valid"}) 


@app.route('/login',methods = ["GET","POST"])
def login():
    c = g.db.cursor()
    if request.method == "GET":
        if "user" in session:
            return redirect('/front')

        else:
            return render_template('login_page.html')

    '''triggered if request method is post'''
    username = request.form["username"] # gets username submitted
    password = request.form["password"] # gets password submitted
    c.execute("SELECT password FROM users WHERE userName = %s",(username,)) # selects password hash from database
    hashed_password = c.fetchone()[0]
    if check_hashed_password(password,hashed_password):
        session['user'] = username # creating session dict with user key and username value
        session['logged_in'] = True # creating session dict with user key and logged in value set to true 
        return render_template('front_page.html')

    else:
        return render_template('sign_up.html',context={'message':"Username or password is wrong. You may not have an account"})

@app.route('/')
def index():
    if "user" in session:
        return redirect('/front')

    return render_template('login_page.html')

@app.route('/front')
def front():
    if "user" in session:
        '''triggered if user is in session meaning they are logged in'''
        return render_template('front_page.html')

    else:
        return render_template('login_page.html')















if __name__ == "__main__":
    app.run(debug=True)
