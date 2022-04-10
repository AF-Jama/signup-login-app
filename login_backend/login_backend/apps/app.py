from flask import Flask, flash, redirect, render_template, request,g,session
from flask_restful import Resource, Api,reqparse,abort
import bcrypt
import logic as l
from flask_sqlalchemy import SQLAlchemy
import os


password = os.environ["SECRET"]

app = Flask(__name__,template_folder='templates',static_folder='static')
# api = Api(app)

app.secret_key = 'vegnthubggvgtgknringtbjjvbungtt;hv'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://root:{password}@localhost/pracDatabase'

db = SQLAlchemy(app)


# def connection():
#     '''creates connection to mysql server'''
#     return mysql.connection

# @app.before_request
# def before_request():
#     g.db = connection()
#     '''triggers method before every request
#         Opens database'''

# @app.teardown_request
# def teardown_exception(exception):
#     g.db.close() # closes connection to database
#     print("DATABSE CLOSED")

@app.route("/",methods = ["GET","POST"])
def signup():
    '''triggered when a GET or POST request is sent to "/signup" endpoint'''
    print("TRIGGERED1")
    if request.method == "GET":
        print("TRIGGERED")
        if "user" in session:
            '''meaning user is logged in and in a session'''
            return redirect('/front')


        '''triggered when GET request is sent to endpoint at renders login page'''    
        return render_template("signup.html",greeting = "Hi,please signup") # why wont you render
        
        '''triggered if POST request'''
    elif request.method == "POST":
        print("POST RUESTED")
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form['confirm_password'] 
        if password == confirm_password and l.is_userName_valid(username) and l.check_if_password_is_valid(password):
            '''triggered if form data is all valid'''
            # area to commit user to user database
            hashed_passwd = l.hashpassword(password)
            new_user = l.make_user(username,hashed_passwd) # creates new_user object that follows Model schema
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html",login_greeting = "Welcome,Please log in") # redirects to login page 
        else:
            return render_template('signup.html',error_message = "Username or Password are not valid") 

@app.route('/login',methods = ["GET","POST"])
def login():
    '''login''' 
    if request.method == "GET":
        if "user" in session:
            return redirect('/front')

        else:
            return render_template('login.html',login_message = "Please log in") # renders login page if there is no user session


    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = l.get_user_password(username)
        if user is None:
            '''if object returned is None it means particlar username is not in database table and login page is re rendered'''
            return redirect('/login')

        else:
            # hashed_password = str(user.password)
            if user.is_password_valid(password):
                '''triggered is userpassword imatches hash password in database'''
                session['user'] = username
                session['logged_in']  =True
                return redirect("/front")

            else:
                return render_template("login.html")


# @app.route('/')
# def index():
#     if "user" in session:
#         return "SUCCESFUL"

#     return render_template("login_page.html")     

@app.route('/front',methods = ["GET","POST"])
def front():
    if request.method == "GET":    
        if "user" in session:
            '''triggered if user is in session meaning they are logged in'''
            return render_template('front_page.html',username = session['user'])

        else:
            return redirect('/login')

    elif request.method == "POST":
        '''if method is a post request(ie:user presses logout button which triggers to "/front" end point)'''
        session.pop('user',None)
        return render_template("login.html",logged_out_message = "You have been logged out, please log in again")



@app.errorhandler(404)
def page_not_found():
    return render_template('server_error.html')



@app.errorhandler(500)
def server_error():
    return render_template('not_found.html')






if __name__ == "__main__":
    app.run(debug=True)
