import json
import mysql.connector

def initialiseTable(listing) : 
  
  """
  Note :
      server is hosted on the users local machine. 
      username considered has default value of 'root' and is accessed by used of password 'password'
      User must have an existing database named portfoliobroTest. 

      values can be altered as per user needs.

      code assumes that the database named portfoliobroTest and the table nifty_500 have already been created in the users system. 
  """
  
  #Database connection parameters
  db = mysql.connector.connect(
      host="localhost",
      user="root",
      password="password",
      database="portfoliobroTest",
      buffered=True
      )
  
  #Connecting to database
  try :
      cursor = db.cursor()
      print("Connected to Database succesfully")
  except :
      print("An error occured while connecting to the database. \nPlease ensure username, password and database name fields are entered correctly")


  #check if table exists in database
  sql="SELECT * FROM nifty_500"
  try :
     cursor.execute(sql)
     table_exists=1
  except :
     print("Table does not exist")
     table_exists=0
  
  #if table exists insert values into it if empty. if table already populated display message
  if table_exists :
    # Insert Dataframe into SQL Server:
    sql1 = "INSERT INTO nifty_500 (companyName, industry, symbol, series, ISINCode, Beta, Volatility ) values(%s,%s,%s,%s,%s,%s,%s)"
    val = ((Company["Company Name"], Company["Industry"], Company["Symbol"], Company["Series"], Company["ISIN Code"], Company["Beta"], Company["Volatility"],) for Company in listing)
    try :
      cursor.executemany(sql1,val)
    except mysql.connector.errors.IntegrityError :
      print("Table population failed as table already populated with values")
    
   #if table does not exist, create table and populate it. 
  else :
      print("Creating table...")
      sql2="CREATE TABLE nifty_500 (companyName varchar(250), industry varchar(50), symbol varchar(15), series varchar(5),  ISINCode varchar(20), Beta decimal(4,2), Volatility varchar(15), CONSTRAINT pk_nifty PRIMARY KEY(symbol))"
      try :
        cursor.execute(sql2)
        print("Table created successfully")
      except : 
         print("Table could not be created")

      sql1 = "INSERT INTO nifty_500 (companyName, industry, symbol, series, ISINCode, Beta, Volatility ) values(%s,%s,%s,%s,%s,%s,%s)"
      val = ((Company["Company Name"], Company["Industry"], Company["Symbol"], Company["Series"], Company["ISIN Code"], Company["Beta"], Company["Volatility"],) for Company in listing)
      cursor.executemany(sql1,val)
      
  db.commit()
  cursor.close()

with open('database.json', 'r') as f:
    listing = json.load(f)
initialiseTable(listing)