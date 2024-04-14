# This script should be run at setup to initialise all databases and user tablesimport mysql.connector 
import mysql.connector
from configparser import ConfigParser as cp
import json
CONFIGS = cp()
CONFIGS.read('portfoliobro.conf')

def createDatabase():
    """
    creates portfoliobro database if it doesn't exist
    """
    conn = mysql.connector.connect(
    host=CONFIGS.get('mysql', 'host'),
    user=CONFIGS.get('mysql', 'user'),
    password=CONFIGS.get('mysql', 'password'),
    port=CONFIGS.get('mysql', 'port'),
    buffered=True
    )
    conn
    cursor = conn.cursor()
    query = "CREATE DATABASE {}".format(CONFIGS.get('mysql', 'database'))
    try:
        cursor.execute(query)
        print("Database {} created".format(CONFIGS.get('mysql', 'database')))
    except:
        print("Unable to create database. Check configs. Is the database server online?")
        

def initNifty500(listing):
    """
    initialises nifty500 table
    """
    conn = mysql.connector.connect(
    host=CONFIGS.get('mysql', 'host'),
    user=CONFIGS.get('mysql', 'user'),
    password=CONFIGS.get('mysql', 'password'),
    database=CONFIGS.get('mysql', 'database'),
    port=CONFIGS.get('mysql', 'port'),
    buffered=True
    )
    conn
    cursor = conn.cursor()
    sql="SELECT * FROM nifty_500"
    try:
        cursor.execute(sql)
        print("Check table executed")
        table_exists=1
    except :
        print("Table does not exist")
    table_exists=0
    
    #if table exists insert values into it if empty. if table already populated display message
    if table_exists :
        # Insert Dataframe into SQL Server:  
        try :
            print("Attempting to populate table nifty_500")
            for Company in listing:
                insert_row = 'INSERT INTO nifty_500 values("{}","{}","{}","{}","{}","{}",{},"{}")'.format(Company["Company Name"], Company["Industry"], Company["Symbol"], Company["Series"], Company["ISIN Code"], Company["Price"], Company["Beta"], Company["Volatility"])
                cursor.execute(insert_row)
        except mysql.connector.errors.IntegrityError :
            print("Table population skipped. Table already populated with values")
        
    #if table does not exist, create table and populate it. 
    else :
        print("Attempting to create table")
        try :
            table_create_query="CREATE TABLE nifty_500 (companyName varchar(250), industry varchar(50), symbol varchar(15), series varchar(5),  ISINCode varchar(20), Price decimal(10,2), Beta decimal(4,2), Volatility varchar(15), CONSTRAINT pk_nifty PRIMARY KEY(symbol))"
            cursor.execute(table_create_query)
            print("Table created successfully")
        except : 
            print("Table already exists.")
        for Company in listing:
            try:
                insert_row = 'INSERT INTO nifty_500 values("{}","{}","{}","{}","{}","{}",{},"{}")'.format(Company["Company Name"], Company["Industry"], Company["Symbol"], Company["Series"], Company["ISIN Code"], Company["Price"], Company["Beta"], Company["Volatility"])
                cursor.execute(insert_row)
            except:
                print("Record already exists for listing: {}".format(Company["Symbol"]))
        
    conn.commit()
    conn.close()


def initUserTable():
    """
    initialises user table
    """
    conn = mysql.connector.connect(
    host=CONFIGS.get('mysql', 'host'),
    user=CONFIGS.get('mysql', 'user'),
    password=CONFIGS.get('mysql', 'password'),
    database=CONFIGS.get('mysql', 'database'),
    port=CONFIGS.get('mysql', 'port'),
    buffered=True
    )
    conn
    cursor = conn.cursor()

    query = "create table users(uname varchar(255), legal_name varchar(255), passwd varchar(255), phone varchar(12), risk_app varchar(255), CONSTRAINT primary key(uname));"



#INIT MAIN
with open('database.json', 'r') as f:
        listing = json.load(f)
        initNifty500(listing)
############TESTING CODE##################
# print(getCursor())
########END OF TESTING CODE##############