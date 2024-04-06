def is_list_of_lists(data):
    if isinstance(data, list):
        return all(isinstance(item, list) for item in data)
    return False


def get_stock_prices(portfolio_data):
    """
    Algorithm :-
    step 1: create database connection with nifty500
    step 2: iterate through portfoliod_data as stock_data
    step 3: use the stock_code to obtain the real-time price from nifty500 database
    step 4: append the stock_price to end to the stock_data
    step 5: return stock_data
    """


def portfolio_beta(portfolio_data):
    """
    :param portfolio_data: list of lists of type [stock_code, volume]
    """

    if not is_list_of_lists(portfolio_data):
        print("Error: Expected <type list of lists> for portfolio_data, received ", type(portfolio_data))
        return False
    
    get_stock_prices(portfolio_data)

    weighted_sum = 0
    total_weight = 0

    for stock_data in portfolio_data:
        # assuming that stock_data is of order [stock_code, volume, current_price]
        weighted_sum += stock_data[2]*stock_data[1] 
        total_weight += stock_data[1]

    beta = weighted_sum/total_weight

    return beta