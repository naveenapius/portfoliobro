import yfinance as yf
import pandas as pd
import numpy as np 



def calcBeta(stock_name, index_df) :
    """
    Calculates the beta of the stock

    Params:
        stock_name: name of the stock for which beta needs to be calculated
        index_df: dataframe of the index
    """

    # fetch stock data from the API
    try:
        stock_df = yf.download(stock_name, period='4y')
    except:
        exit("Error occured in fetching stock data, please check stop name and try again.")

    monthly_stock_close = stock_df.loc[:,"Close"].resample("M").last().copy()
    monthly_stock_ret = monthly_stock_close.pct_change().dropna()
    monthly_index_close = index_df.loc[:,"Close"].resample("M").last().copy()
    monthly_index_ret = monthly_index_close.pct_change().dropna()

    # turn dataframes into a numpy array to calculate variance and covariance values of index and stock returns
    index = monthly_index_ret.to_numpy()
    stock = monthly_stock_ret.to_numpy()

    # check if size of each array is equal else trim one of them to calculate covariance
    if len(index)<=len(stock):
        min=len(index)
    else:
        min=len(stock)
    var=np.var(index)
    cov=np.cov(stock[:min],index[:min])

    beta = cov/var
    #print(beta)

    return round(beta[0,1],2)

def checkVolatility(raw_beta):
    """
    Checks volatility of the stock based on the beta
    Higher volatility implies higher risk
    Stock recommendations are made based on risk appetite

    Params:
        raw_beta: calculated beta of the stock
    """
    #converting calculated beta of the stock which includes negative values into absolute values for comparison
    beta=abs(raw_beta)

    if (beta>0 and beta<=0.5):
        return("very low")
    elif (beta>0.5 and beta<=1):
        return("low")
    elif (beta>1 and beta<=1.5):
        return("medium")
    elif (beta>1.5 and beta<=2):
        return("high")
    elif beta>2:
        return("very high")
    else:
        pass

    
# ##########TESTING CODE###########################################################
# if __name__ == "__main__":

#     #define the index to compare all stock to (NSE)
#     print("Fetching index data from API, please wait...")

#     try:
#         index_df=yf.download("^NSEI", period ='4y')
#     except:
#         exit("Error occured in fetching index data, please try again.")

#     stock=input("Enter the name of any stock ticker in the Indian NSE : ")
#     stock_name = stock.strip()
#     stock_name = f"{stock_name}.NS" if ".NS" not in stock_name else stock_name

#     beta=calcBeta(stock, index_df)
#     volatility = checkVolatility(beta)
#     print(f"stock has {volatility} volatility")
# ###############END OF TESTING CODE################################################