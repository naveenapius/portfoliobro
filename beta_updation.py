import yfinance as yf
import json
import beta_calc as beta

f = open('stocks.json')

Listing = json.load(f)

#define the index to compare all stock to (NSE)
print("Fetching index data from API, please wait...")

try:
    index_df=yf.download("^NSEI", period ='4y')
except:
    exit("Error occured in fetching index data, please try again.")

for Company in Listing:
    stock_name=Company["Symbol"]
    stock_name = f"{stock_name}.NS" if ".NS" not in stock_name else stock_name
    print("Fetching data for stock : ",stock_name)
    Company['Beta'] = beta.calcBeta(stock_name,index_df) 

for Company in Listing:
	print(Company['Company Name'], " - ", Company["Symbol"], " - ", Company["Beta"])

#push to database
f.close()
