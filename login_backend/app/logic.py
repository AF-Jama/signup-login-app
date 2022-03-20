import bcrypt
from password_strength import PasswordPolicy
import mysql.connector
import os

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = os.environ["SECRET"],
    database = "theDatabase"
)

c = db.cursor()

policy = PasswordPolicy.from_names( # password policy that sets password criteria
    length=6,  # min length: 6
    uppercase=1,  # need min. 1 uppercase letters
    numbers=1,  # need min. 2 digits
    special=1  # need min. 1 special characters
)


def check_if_password_is_valid(password = ''):
    '''checks if password is valid'''
    passwordtest = policy.test(password)
    if(len(passwordtest) == 0):
        return True # valid password

    else:
        return False

def is_userName_valid(userName):
    '''checks if username is not in user table'''
    c.execute("SELECT userName FROM users")
    if (userName,) not in c.fetchall() and len(userName)>=6:
        '''triggered if username is not in user table'''
        return True #  valid username

    else:
       return False
        
def hashpassword(password):
    '''takes in valid password and hashes using bcrpyt'''
    password = bytes(password,"utf-8") # constructs an array of bytes 
    hashed_password = bcrypt.hashpw(password,bcrypt.gensalt()) # hashed password with salt
    return hashed_password # returns hashed password

def check_hashed_password(password,hash_password):
    '''triggered to check actual password to hashed password when logging in'''
    return bcrypt.checkpw(password,hash_password) # returns boolean if password and hashed password match or not


print(is_userName_valid("Theddgr8"))
