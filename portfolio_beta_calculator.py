import mysql.connector


# def is_list_of_tuples(data):
#     if isinstance(data, list):
#         return all(isinstance(item, list) for item in data)
#     return False


def getStockPrices(portfolio):
    """
    updates portfolio items with the corresponding real-time stock price
    """
    #Database connection parameters
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="portfoliobro_test",
        port="3307",
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

    # if not is_list_of_tuples(portfolio):
    #     print("Error: Expected <type list of tuples> for portfolio, received ", type(portfolio))
    #     return False
    
    priced_portfolio = getStockPrices(portfolio)

    # calculate portfolio beta using weighted averages
    weighted_sum = 0
    total_weight = 0
    for stock_data in priced_portfolio:
        weighted_sum += stock_data[3]*stock_data[1] 
        total_weight += stock_data[1]

    beta = weighted_sum/total_weight
    beta = round(beta, 2)

    return beta



