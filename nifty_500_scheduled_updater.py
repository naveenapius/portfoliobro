import yfinance as yf
import json
import beta_calculator as beta
from datetime import date
from configparser import ConfigParser as cp
import mysql.connector
CONFIGS = cp()
CONFIGS.read('portfoliobro.conf')


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
        host=CONFIGS.get('mysql', 'host'),
        user=CONFIGS.get('mysql', 'user'),
        password=CONFIGS.get('mysql', 'password'),
        database=CONFIGS.get('mysql', 'database'),
        port=CONFIGS.get('mysql', 'port'),
        buffered=True
        )
    
    cursor = db.cursor()
    
    try :
        #Update server with updated beta values
        print("Attempting updation of database...")
        for Company in listing :
            row_update = "UPDATE nifty_500 SET Price = '{}', Beta = '{}', Volatility = '{}', MarketCap ='{}' WHERE symbol = '{}'".format(float(Company["Price"]),float(Company["Beta"]),Company["Volatility"],Company["Market Cap"],Company["Symbol"])
            cursor.execute(row_update)
        print("Table updated succesfully")
    except :
        print("Error. Table could not be updated.")
        
    #committing changes to the database and closing cursor
    db.commit()
    cursor.close()




#main
f = open('database.json')

Listing = json.load(f)

#define the index to compare all stock to (NSE)
print("Fetching index data from API, please wait...")

try:
    index_df=yf.download("^NSEI", period ='4y')
except:
    exit("Error occured in fetching index data, please try again.")

today=date.today()

for Company in Listing:
    stock_name=Company["Symbol"]
    stock_name = f"{stock_name}.NS" if ".NS" not in stock_name else stock_name
    print("Fetching data for stock : ",stock_name)

    # If today is saturday or sunday -> update beta and volatility (week ends on friday so no need to update price)
    if today.weekday() == 5 or today.weekday() == 6 :
        Company['Beta'] = beta.calcBeta(stock_name,index_df) 
        Company['Volatility'] = beta.checkVolatility(Company['Beta'])
    
    # else run price updation
    else :
        stock = yf.Ticker(stock_name)
        current_price = stock.info['currentPrice']
        market_cap_value = stock.info['marketCap']
        market_cap = beta.checkMarketCap(market_cap_value)
        Company['Price'] = current_price
        Company['Market Cap'] = market_cap
    

#print updated values for debugging purposes : can remove
for Company in Listing:
	print(Company['Company Name'], " - ", Company["Symbol"], " - ",Company["Price"]," - ", Company["Beta"]," - " ,Company["Volatility"], " - " ,Company["Market Cap"])

#rewrite json with updated values
with open('database.json', 'w') as json_file:
  json_file.seek(0)
  json.dump(Listing, json_file, indent=4)

#push to database
updateDatabase(Listing)

f.close()