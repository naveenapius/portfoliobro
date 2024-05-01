import mysql.connector
import random
import math

import portfolio_beta_calculator as pbc
import beta_calculator as bc
from configparser import ConfigParser as cp
CONFIGS = cp()
CONFIGS.read('portfoliobro.conf')

RISK_CLASSES = ["very low", "low", "medium", "high", "very high"]
RISK_RANGES = [0, 0.5, 1.0, 1.5, 2, 100]

port_beta = float()
port_vol = str()
port_vol_index = int()
risk_apt = str()
risk_apt_index = int()


def getIndices():
    # get index for portfolio volatility and risk appetite values from RISK_CLASSES
    global port_vol_index
    global risk_apt_index
    if not (port_vol_index := RISK_CLASSES.index(port_vol)) and port_vol_index != 0:
        exit(f"Error: invalid volatility value: {port_vol}")
    if not (risk_apt_index := RISK_CLASSES.index(risk_apt)) and risk_apt_index != 0:
        exit(f"Error: invalid risk appetite value: {risk_apt}")


def getPosPortfolioClasses():
    """
    for a portfolio with positive portfolio beta value, suggest two risk classes for generating suggestions
    - suggesting stocks with positive beta for diversification
    - suggesting stocks with negative beta for hedging
    """

    def positiveSuggestionClass():
        """
        compares current portfolio volatility class to the risk appetite class to get the class for positive beta stock suggestions
        """

        # compute the index of volatility class from which stocks will be suggested
        index_diff = risk_apt_index - port_vol_index
        class_index = risk_apt_index + index_diff
        if class_index < 0: class_index = 0
        elif class_index > 4: class_index = 4

        return RISK_CLASSES[class_index]
    
    def negativeSuggestionClass():
        """
        compares current portfolio beta to the risk appetite range limit to get the class for negative beta stock suggestions
        """

        # get lower limit beta value of the risk appetite class from RISK_RANGES
        risk_apt_limit = RISK_RANGES[risk_apt_index]

        # find difference between current portfolio beta and target portfolio beta i.e. risk_apt_limit
        beta_diff = port_beta - risk_apt_limit

        # if difference is negative, moving from lower portfolio beta to higher risk appetite level while hedging is not possible
        # if difference does not cause change in class then no hedging is required
        if beta_diff < 0.5:
            return None
        
        # compute index of risk class within which the difference falls
        for i in range(0, 5):
            if beta_diff >= RISK_RANGES[i] and beta_diff < RISK_RANGES[i+1]:
                class_index = i
                break

        return RISK_CLASSES[class_index]

    return positiveSuggestionClass(), negativeSuggestionClass()


def getNegPortfolioClasses():
    """
    for a portfolio with positive portfolio beta value, suggest two risk classes for generating suggestions
    - suggesting stocks with positive beta for hedging
    - suggesting stocks with negative beta for diversification
    """

    def positiveSuggestionClass():
        """
        compares current portfolio beta to the risk appetite range limit to get the class for positive beta stock suggestions
        """

        # get lower limit beta value of the risk appetite class from RISK_RANGES
        risk_apt_limit = RISK_RANGES[risk_apt_index]

        # find difference between current portfolio beta and target portfolio beta i.e. risk_apt_limit
        beta_diff = risk_apt_limit - port_beta
        
        # compute index of risk class within which the difference falls
        for i in range(0, 5):
            if beta_diff >= RISK_RANGES[i] and beta_diff < RISK_RANGES[i+1]:
                class_index = i
                break

        return RISK_CLASSES[class_index]

    def negativeSuggestionClass():
        """
        compares current portfolio volatility class to the risk appetite class to get the class for negative beta stock suggestions
        """

        # compute the index of volatility class from which stocks will be suggested
        index_diff = risk_apt_index - port_vol_index
        class_index = risk_apt_index + index_diff
        if class_index < 0: class_index = 0
        elif class_index > 4: class_index = 4

        return RISK_CLASSES[class_index]

    return positiveSuggestionClass(), negativeSuggestionClass()


def getStocks(pos_suggestion_class, neg_suggestion_class):
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
    fetch_stocks = f'SELECT * FROM nifty_500 WHERE Volatility in ("{pos_suggestion_class}","{neg_suggestion_class}")'
    cursor.execute(fetch_stocks)
    stocks=cursor.fetchall()

    # divide the list of stocks into two for positive and negative beta suggestions
    pos_stocks = [stock for stock in stocks if (stock[7]==pos_suggestion_class and stock[6]>=0)]
    neg_stocks = [stock for stock in stocks if (stock[7]==neg_suggestion_class and stock[6]<0)]

    return pos_stocks, neg_stocks


def formatSuggestions(suggestion_stocks, new_portfolio):

    # stocks are not suggested only for negative suggestions
    if not suggestion_stocks:
        if port_beta>0:
            if port_vol_index < risk_apt_index:
                return "No suggestions for hedging since risk appetite is greater than portfolio volatility"
            elif port_vol_index == risk_apt_index:
                return "No suggestions for hedging since risk appetite is same as portfolio volatility"
            else:
                return "No suggestions available"
        else:
            return "No suggestions available"
        return None
    
    # get target risk appetite value based on kind of suggestions

    tgt_risk_apt = None

    # portfolio with positive weighted beta value
    if port_beta >= 0:
        # suggesting stocks with positive beta
        if suggestion_stocks[0][6]>=0:
            if port_vol_index < risk_apt_index:
                tgt_risk_apt = RISK_RANGES[risk_apt_index]
            elif port_vol_index > risk_apt_index:
                tgt_risk_apt = RISK_RANGES[risk_apt_index+1] - 0.01
            else:
                pass # volume for each suggestion will be 1
        # suggesting stocks with negative beta
        else:
            if port_vol_index < risk_apt_index:
                pass
            elif port_vol_index > risk_apt_index:
                tgt_risk_apt = tgt_risk_apt = RISK_RANGES[risk_apt_index+1] - 0.01
            else:
                pass
    # portfolio with negative weighted beta value
    else:
        # suggesting stocks with positive beta
        if suggestion_stocks[0][6]>=0:
            tgt_risk_apt = RISK_RANGES[risk_apt_index]
        # suggesting stocks with negative beta
        else:
            if port_vol_index < risk_apt_index:
                tgt_risk_apt = RISK_RANGES[risk_apt_index] * (-1)
            elif port_vol_index > risk_apt_index:
                tgt_risk_apt = (RISK_RANGES[risk_apt_index+1] - 0.01) * (-1)
            else:
                pass # volume for each suggestion will be 1

    weighted_sum = 0
    total_weight = 0
    for stock_data in new_portfolio:
        weighted_sum += float(stock_data[3])*stock_data[1] 
        total_weight += stock_data[1]

    # print("ra = ", tgt_risk_apt) if tgt_risk_apt else print("no ra")
    # print("Ef = ", total_weight)
    # print("Exf = ", weighted_sum)

    updated_stocks = []
    for stock in suggestion_stocks:
        # print("sb = ", stock[6])
        if port_vol == risk_apt and (port_beta>=0 and suggestion_stocks[0][6]>=0) or (port_beta<=0 and suggestion_stocks[0][6]<=0):
            volume = 1
        else:
            try:
                volume = math.ceil((tgt_risk_apt*total_weight - weighted_sum)/(float(stock[6])-tgt_risk_apt))
            except ZeroDivisionError:
                volume = 0
        # print("vol = ", volume)
        updated_stocks.append([stock[2], float(stock[5]), volume, round(float(stock[5])*volume,2)])
        
    return updated_stocks


def suggestStocks(stocks, new_portfolio):

    mid_stocks = []
    large_stocks = []

    # divide the suggested stocks into mid cap and large cap lists, trimmed to stock code and price
    for stock in stocks:
        if stock[8] == "mid":
            mid_stocks.append(stock)
        elif stock[8] == "large":
            large_stocks.append(stock)
        else:
            pass

    # choose 5 random stocks from each list of suggestions 
    mid_suggestions = random.sample(mid_stocks, 5) if len(mid_stocks)>5 else mid_stocks.copy()
    large_suggestions = random.sample(large_stocks, 5) if len(large_stocks)>5 else large_stocks.copy()

    suggestion = {
        "mid cap": formatSuggestions(mid_suggestions, new_portfolio),
        "large cap": formatSuggestions(large_suggestions, new_portfolio),
    }

    return suggestion


def suggestions(portfolio, risk_appetite):
    """
    :params
        portfolio: list of tuples containing the user's portfolio data
        risk_apt: user's risk appetite
    """

    global port_beta
    global port_vol
    global risk_apt

    # calculate portfolia beta and volatility level
    new_portfolio = pbc.getStockPrices(portfolio)
    port_beta = float(pbc.calcPortfolioBeta(portfolio))
    port_vol = bc.checkVolatility(port_beta).lower().strip()
    risk_apt = risk_appetite.lower().strip()
    getIndices()

    # print(f"current portfolio (beta, volatility, risk appetite) = ({port_beta}, {port_vol}, {risk_apt})")

    # calculate risk classes for suggestions based on current portfolio beta value
    if port_beta >= 0:
        pos_suggestion_class, neg_suggestion_class = getPosPortfolioClasses()
    else:
        pos_suggestion_class, neg_suggestion_class = getNegPortfolioClasses()

    pos_stocks, neg_stocks = getStocks(pos_suggestion_class, neg_suggestion_class)

    pos_suggestions = suggestStocks(pos_stocks, new_portfolio)
    neg_suggestions = suggestStocks(neg_stocks, new_portfolio)

    if port_beta >= 0:
        suggested_stocks = {
            "diversification": pos_suggestions,
            "beta hedging": neg_suggestions
        }
    else:
        suggested_stocks = {
            "diversification": neg_suggestions,
            "beta hedging": pos_suggestions
        }
    
    return suggested_stocks


# if __name__ == "__main__":
    # print(suggestions(
    #     [
    #         ('BANKINDIA', 6),
    #     ], 
    #     "low"))
    
    # print(suggestions(
    #     [
    #         ('AAVAS', 6), 
    #         ('CELLO', 2), 
    #         ('ENGINERSIN', 4), 
    #         ('GLAXO', 10), 
    #         ('IRCTC', 9), 
    #         ('JBMA', 6), 
    #         ('LXCHEM', 8)
    #     ], 
    #     "medium"))

    # print(suggestions(
    #     [
    #         ('PAYTM', 89),
    #         ('IRFC', 55),
    #         ('ZOMATO', 36),
    #         ('MANKIND', 60),
    #         ('DOMS', 42),
    #         ('MSUMI', 15)
    #     ],
    #     "very low"
    # ))
