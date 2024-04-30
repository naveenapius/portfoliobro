import portfolio_beta_calculator as pbc

def simulate(portfolio, stock_code, volume, flag):

    # convert portfolio as list of tuples into list of lists
    new_portfolio = [list(item) for item in portfolio]

    beta = []

    # if stock already exists
    if any(stock_code == stock[0] for stock in new_portfolio):
        for stock in new_portfolio:
            if stock_code == stock[0]:
                if flag == 0: # addition
                    stock[1] += volume
                else: # subtraction
                    if volume <= stock[1]:
                        stock[1] -= volume
                    else:
                        print("Error: not enough volume of stock to be deleted")
                        return
                break

    # if stock does not exist
    else:
        if flag == 0:
            new_portfolio.append([stock_code,volume])
        else:
            print("Error: stock does not exist in portfolio")
            return
        
    # convert new_portfolio as list of lists into list of tuples
    portfolio_ret = [tuple(item) for item in new_portfolio]
    beta.append(pbc.calcPortfolioBeta(portfolio))
    beta.append(pbc.calcPortfolioBeta(portfolio_ret))

    return beta
    # return portfolio_ret, new_beta