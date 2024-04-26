import mysql.connector 
from hashlib import sha256
import pandas as pd
from configparser import ConfigParser as cp
CONFIGS = cp()
CONFIGS.read('portfoliobro.conf')


conn = mysql.connector.connect(
host=CONFIGS.get('mysql', 'host'),
user=CONFIGS.get('mysql', 'user'),
password=CONFIGS.get('mysql', 'password'),
database=CONFIGS.get('mysql', 'database'),
port=CONFIGS.get('mysql', 'port'),
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

def userCreate(uname, legal_name, passwd, phone, risk_app):
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
    user_create = 'INSERT INTO users VALUES("{}", "{}", "{}", "{}", "{}")'.format(uname, legal_name, hashed_passwd, phone, risk_app)
    user_portfolio_create = "CREATE TABLE {}(symbol varchar(255), shares int, CONSTRAINT primary key(symbol), CHECK (shares>=0));".format(uname)
    try:
        cur.execute(user_create)
        cur.execute(user_portfolio_create)
        conn.commit()
        print("User added.")
        return 1
    except:
        print("Unable to add user. Please try a different username.")
        return 0


def userLogin(uname, passwd):
    '''
    params: username, password
    returns:
        1 - if login successful
        status - error message if login unsuccessful    
    '''
    try:
        login_check = 'SELECT uname, passwd FROM users WHERE uname="{}"'.format(uname)
        cur.execute(login_check)
        data = cur.fetchall()
    except:
        print("Unable to execute fetch query. Check database connection")
    
    #confirms that user exists
    if len(data) == 0:
        return "User does not exist. Please signup or check username for typos."
    
    #password matching
    hashed_passwd = data[0][1]
    entered_passwd_hashed = sha256(passwd.encode()).hexdigest()

    if hashed_passwd == entered_passwd_hashed:
        return 1
    else:
        return "Incorrect password entered. Please try again."
    

# user portfolio operations

def getPortfolio(uname):
    query = 'SELECT * FROM {}'.format(uname)
    try:
        cur.execute(query)
        portfolio = cur.fetchall()
        return portfolio
    except:
        return 0

def getLegalName(uname):
    query = 'SELECT legal_name FROM users WHERE uname="{}"'.format(uname)
    try:
        cur.execute(query)
        return cur.fetchall()[0][0]
    except:
        return "Unable to retrieve legal name for this user"

def addStock(uname, stock, shares):
    check_exists = 'SELECT * FROM {} WHERE symbol="{}"'.format(uname, stock)
    cur.execute(check_exists)
    flag = len(cur.fetchall())
    try: 
        if flag==0:
            query = 'INSERT INTO {} values("{}", {})'.format(uname, stock, shares)
            cur.execute(query)
            print("New stock added to portfolio")
        else:
            query = 'UPDATE {} SET shares = shares + {} WHERE symbol = "{}"' .format(uname, shares, stock)
            cur.execute(query)
            print("Share volume updated")
        conn.commit()
        return 1
    except:
        print("Unable to update portfolio. Check configuration.")

def removeStock(uname, stock, shares):
    check_exists = 'SELECT * FROM {} WHERE symbol="{}"'.format(uname, stock)
    cur.execute(check_exists)
    flag = len(cur.fetchall())
    try: 
        if flag==0:
            print("This stock does not exist in your portfolio")
        else:
            query = 'UPDATE {} SET shares = shares - {} WHERE symbol = "{}"' .format(uname, shares, stock)
            cur.execute(query)
            print("Share volume updated")
        conn.commit()
        return 1
    except:
        print("Number of shares to remove exceeds total number of shares bought.")

def getRiskAppetite(uname):
    query = 'SELECT risk_app FROM users WHERE uname="{}"'.format(uname)
    try:
        cur.execute(query)
        return cur.fetchall()[0][0]
    except:
        return "Unable to retrieve risk appetite for this user"
    


############TESTING CODE##################
# print(getPortfolio('olivertwist'))
########END OF TESTING CODE##############