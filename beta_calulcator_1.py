import yfinance as yf
import pandas as pd
import numpy as np 

#define the index to compare all stock to (NSE)
indexdf=yf.download("^NSEI", period ='4y')

def calc_beta(stockname) :
    stockdf = yf.download(stockname, period='4y')
    #print dataframe
    print(stockdf)
    #turn dataframes into a numpy array to calculate variance and covariance values of index and stock returns
    index = indexdf['Adj Close'].to_numpy()
    stock = stockdf['Adj Close'].to_numpy()

    #check if size of each array is equal else trim one of them to calculate covariance
    if len(index)<=len(stock):
        min=len(index)
    else:
        min=len(stock)

    var=np.var(index)
    cov=np.cov(stock[:min],index[:min])
    beta = cov/var
    print(beta)
    return beta[0,1]

#higher volatility == higher risk -> recommend based on risk appetite
def checkvolatile(beta):
    if beta<1 and beta>0 :
        print(stock," is less volatile")
    if beta>1 :
        print(stock," is very volatile")
    if beta<0 and beta>-1 :
        print(stock," is less volatile")
    if beta<-1 :
        print(stock," is very volatile")

stock=input("Enter the name of any stock ticker in the Indian NSE : ")
beta=calc_beta(stock)
print(beta)
checkvolatile(beta)