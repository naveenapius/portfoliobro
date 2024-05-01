import mysql.connector
from configparser import ConfigParser as cp
CONFIGS = cp()
CONFIGS.read('portfoliobro.conf')


def getStockPrices(portfolio):
    """
    updates portfolio items with the corresponding real-time stock price
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

    #Connecting to database
    try :
        cursor = db.cursor()
    except :
        print("An error occured while connecting to the database. \nPlease ensure username, password and database name fields are entered correctly")
        return
    
    new_portfolio_data=[]

    #iterating through portfolio_data as stock_data to append price to end of stock_data
    for stock_data in portfolio:
        fetch_price='SELECT Price, Beta FROM nifty_500 WHERE symbol = "{}"'.format(stock_data[0])
        try:
            cursor.execute(fetch_price)
            price=cursor.fetchall()
        except:
            print("Error occured in fetching price data from nifty_500")
            return
        stock_data=stock_data +(float(price[0][0]), price[0][1],)
        new_portfolio_data.append(stock_data)

    return new_portfolio_data


def calcPortfolioBeta(portfolio):
    """
    :param portfolio: list of tuples of type (stock_code, volume)
    :returns beta: list of lists 
    """
    
    priced_portfolio = getStockPrices(portfolio)

    # calculate portfolio beta using weighted averages
    weighted_sum = 0
    total_weight = 0
    for stock_data in priced_portfolio:
        weighted_sum += stock_data[3]*stock_data[1] 
        total_weight += stock_data[1]
    try:
        beta = weighted_sum/total_weight
        beta = round(beta, 2)
    except ZeroDivisionError:
        return None

    return beta



