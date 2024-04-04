import json
import mysql.connector

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
        database="portfoliobroTest"
        )
    
    #Connecting to database
    try :
        cursor = db.cursor()
        print("Connected to Database succesfully")
    except :
        print("An error occured while connecting to the database. \nPlease ensure username, password and database name fields are entered correctly")

    try :
        #Update server with updated beta values
        sql = "UPDATE nifty_500 SET Beta = %s, Volatility = %s WHERE symbol = %s"
        val = ((float(Company["Beta"]),Company["Volatility"],Company["Symbol"],) for Company in listing )
        cursor.executemany(sql, val)
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