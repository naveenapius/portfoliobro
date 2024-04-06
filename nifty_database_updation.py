import json
import mysql.connector
import nifty500_db_init as init

#purpose of program is to extract instances of updated values from the json file to maintain in the database

def updateDatabase(listing) :

    """
    Note :
        server is hosted on the users local machine. 
        username considered has default value of 'root' and is accessed by used of password 'password'
        User must have an existing database named portfoliobroTest. 

        values can be altered as per user needs.
        variable 'listing' refers to the dataframe that holds values of all equity shares listed in the nifty_500

        code assumes that the database portfoliobroTest and the table nifty_500 already exist in the users sysstem 
            where nifty_500 has already been populated with necessary values. purpose of this function is to simply 
            update the database with relevant data changes
    """
    
    #Database connection parameters
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="portfoliobro_test",
        #port="3307",
        buffered=True
        )
    
    #Connecting to database
    try :
        cursor = db.cursor()
        print("Connected to Database succesfully")
    except :
        print("An error occured while connecting to the database. \nPlease ensure username, password and database name fields are entered correctly")

    #check if table exists, if not, create table and initialise table
    table_exists=0
    
    sql="SELECT * FROM nifty_500"
    try :
        cursor.execute(sql)
        table_exists=1
    except :
        print("Table does not exist")
    
    if table_exists==0 :
        init.initialiseTable(listing)
    
    try :
        #Update server with updated beta values
        print("Attempting updation of database...")
        for Company in listing :
            row_update = "UPDATE nifty_500 SET Price = '{}', Beta = '{}', Volatility = '{}' WHERE symbol = '{}'".format(float(Company["Price"]),float(Company["Beta"]),Company["Volatility"],Company["Symbol"])
            cursor.execute(row_update)
        print("Table updated succesfully")
    except :
        print("Error. Table could not be updated.")
        
    #committing changes to the database and closing cursor
    db.commit()
    cursor.close()
        
#opening json file to read and update database
with open('database.json', 'r') as f:
    listing = json.load(f)

updateDatabase(listing)    