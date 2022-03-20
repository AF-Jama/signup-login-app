import mysql.connector
import os

# Creation of database 

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = os.environ["SECRET"],
    database = "theDatabase"
)


c = db.cursor() # creating cursor 

c.execute("CREATE DATABASE IF NOT EXISTS theDatabase") # creates database if not exists 

c.execute('''CREATE TABLE IF NOT EXISTS users(id BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
            userName VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL
)''') # create user table containing userName and password. Using simple one to one table for brevity





