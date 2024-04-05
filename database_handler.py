import mysql.connector 
from hashlib import sha256
import pandas as pd

conn = mysql.connector.connect(
host="localhost",
user="root",
password="",
database="portfoliobro_test",
port="3307",
buffered=True
)
cur = conn.cursor()



def cursorDestroy(cur):
    '''
    destroys a cursor object
    params:
        cur: cursor object
    return: null
    '''
    cur.close()

# user db operations

def userCreate(uname, legal_name, passwd, phone):
    '''
    params: 
        uname: username that will uniquely identify the user and their portfolio
        legal_name: legal name for aesthetic reasons
        phone: also for aesthetic reasons
        passwd: password accepted and converted to sha256 hash to store
    returns:
        1 - user created successfully
        0 - unable to create user - username already exists
    '''
    hashed_passwd = sha256(passwd.encode()).hexdigest()
    user_create = 'INSERT INTO users VALUES("{}", "{}", "{}", "{}")'.format(uname, legal_name, hashed_passwd, phone)
    try:
        cur.execute(user_create)
        print("user added")
        conn.commit()
        return 1
    except:
        print("Unable to add user. Please try again.")
        return 0


def userLogin(uname, passwd):
    '''
    params: username, password
    returns:
        1 - Login successful
        0 - Unable to login
    '''
    
