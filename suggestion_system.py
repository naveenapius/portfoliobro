import mysql.connector

import portfolio_beta_calculator as pbc
import beta_calculator as bc
from configparser import ConfigParser as cp
CONFIGS = cp()
CONFIGS.read('portfoliobro.conf')


def getVolatilityClass(volatility, risk_apt):
    """
    compares current volatility level of the portfolio with the target volatility level i.e. risk appetite of the user
    and suggests a volatility class for suggestions
    """
    classes = ["very low", "low", "medium", "high", "very high"]
    if not (volat_index := classes.index(volatility.lower().strip())):
        print("Error: invalid volatility value: ", volatility)
        return False
    if not (risk_index := classes.index(risk_apt.lower().strip())):
        print("Error: invalid risk appetite value: ", risk_apt)
        return False
    
    index_diff = risk_index - volat_index
    tgt_index = risk_index + index_diff
    if tgt_index < 0: tgt_index = 0
    elif tgt_index > 4: tgt_index = 4
    # print(tgt_index)
    return classes[tgt_index]


def getStocks(volatility_class):
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

    #fetching stocks of desired class and positive beta from nifty_500 table
    fetch_stocks = f'SELECT * FROM nifty_500 WHERE Volatility = "{volatility_class}" AND Beta >= 0 ORDER BY Beta'
    cursor.execute(fetch_stocks)
    stocks=cursor.fetchall()

    return stocks


def suggestStocks(stocks, beta, risk_apt):
    # check if more than 15 suggested stocks exist in this class
    if len(stocks) > 15:

        # assign target beta value depending on risk appetite
        if risk_apt == "very low":
            tgt_beta = 0
        elif risk_apt == "low":
            tgt_beta = 0.51
        elif risk_apt == "medium":
            tgt_beta = 1.01
        elif risk_apt == "high":
            tgt_beta = 1.51
        elif risk_apt == "very high":
            tgt_beta = 2.01
        else:
            pass

        # create a stocks list with just the symbol and stock beta
        stocks_list = [(stock[2], float(stock[6])) for stock in stocks]


        # sort the stocks list in ascending order of absolute difference of stock beta from the target beta value
        closest_stocks = sorted(stocks_list, key=lambda x: abs(x[1] - tgt_beta))


        temp = [stock[0] for stock in closest_stocks]
        # get top 15 stocks from original stocks list by symbol from top 15 stocks from closest_stocks
        top15_stocks = [stock for stock in stocks if stock[2] in temp]
        # sort stocks by price
        sorted_stocks = sorted(top15_stocks, key= lambda x: x[5])

        # divide 15 stocks into 3 categories
        suggested_stocks = {
            "Low Cost": [sorted_stocks[:5]],
            "Medium Cost": [sorted_stocks[5:10]],
            "Hgh Cost": [sorted_stocks[10:15]]
        }

    # divide the stocks without checking for beta range if less than 15 
    else:

        # sort stocks by price
        sorted_stocks = sorted(stocks, key= lambda x: x[5])

        # divide the stocks into 3 approximately equal parts
        num = len(stocks) // 3
        rem = num % 3
        if rem == 2:
            num1 = num
            num2 = (2*num) + 1
        else:
            num1 = num
            num2 = 2*num

        suggested_stocks = {
            "Low Cost": [sorted_stocks[:num1]],
            "Medium Cost": [sorted_stocks[num1:num2]],
            "Hgh Cost": [sorted_stocks[num2:]],
        }
    return suggested_stocks


def suggestions(portfolio, risk_apt):
    """
    :params
        portfolio: list of tuples containing the user's portfolio data
        risk_apt: user's risk appetite
    """

    # calculate portfolia beta and volatility level
    portfolio_beta = pbc.calcPortfolioBeta(portfolio)
    volatility = bc.checkVolatility(portfolio_beta)
    # print(f"current portfolio (beta, volatility) = ({portfolio_beta},{volatility})")


    # obtain target volatility class for suggested stocks
    volatility_class = getVolatilityClass(volatility, risk_apt)
    stocks = getStocks(volatility_class)
    suggested_stocks = suggestStocks(stocks, portfolio_beta, risk_apt)
    
    return suggested_stocks

# suggestions([('AAVAS', 6), ('CELLO', 2), ('ENGINERSIN', 4), ('GLAXO', 10), ('IRCTC', 9), ('JBMA', 6), ('LXCHEM', 8)], "very high")
