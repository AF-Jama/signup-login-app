import bcrypt
from password_strength import PasswordPolicy
from model import User
import os


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
    data = User.query.filter_by(userName = userName).first() # returns first User object as one unique username should be in database table
    if data == None and len(userName)>=6:
        '''if query returns nothing means username is not in database and userName is greater than 6. then username is valid'''
        return True

    else:
       return False
        
def hashpassword(password:str):
    '''takes in valid password and hashes using bcrpyt'''
    PASSWORD = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(PASSWORD,bcrypt.gensalt()) # hashed password with salt
    return hashed_password # returns hashed password

def make_user(username,password):
    new_user = User(userName = username,password = password)
    return new_user

def check_hashed_password(password:str,hash_password):
    '''triggered to check actual password to hashed password when logging in'''
    PASSWORD = password.encode('utf-8')
    return bcrypt.checkpw(PASSWORD,hash_password)

def get_user_password(username = ''):
    '''queries database for usernames password and returns None if it does not exist and an object if it does'''
    user_obj = User.query.filter_by(userName = username).first() 
    return user_obj 

PASSWORD = "Testpassword123." # test password

hashed_password = hashpassword(PASSWORD) #  return salted+hashed password from password string

print("Hashed password:",hashed_password)

# is_password_legit = check_hashed_password(PASSWORD,hashed_password)

# print(is_password_legit)

# print("IS:",is_userName_valid("James123."))

# get_user_password("CaliforniaDreamer256.")