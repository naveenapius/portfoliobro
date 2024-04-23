from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import matplotlib
from mpl_toolkits.axisartist.parasite_axes import SubplotHost

import yfinance as yf
import json
import portfolio_beta_calculator as pbc

def weightedPortfolioVisualisation(portfolio, uname):
    priced_portfolio=pbc.getStockPrices(portfolio)
    stocks = []
    shares = []
    weights = []
    for entry in priced_portfolio:
        stocks.append(entry[0])
        shares.append(entry[1])
        weights.append(entry[1]*entry[2])
    plt.pie(weights, labels=stocks)
    plt.title("Portfolio for user {}".format(uname))
    plt.show()

def betaVisualisation(portfolio,uname) :
    portfolio_beta = pbc.calcPortfolioBeta(portfolio)
    stocks = []
    beta = []
    for entry in portfolio:
        stocks.append(entry[0])
    f = open('database.json')
    Listing = json.load(f)
    for stock in stocks :
        for Company in Listing :
            if Company["Symbol"] == stock :
                beta.append(Company["Beta"])
    fig1=plt.figure()

    ax1= SubplotHost(fig1,111)
    fig1.add_subplot(ax1)

    #defining colour scale for risk factor
    ax1.add_patch(matplotlib.patches.Rectangle((-1,0), 5, 0.5, color="#B3D4B4"))
    ax1.add_patch(matplotlib.patches.Rectangle((-1,0.5), 5, 0.5, color="#E5EC9E"))
    ax1.add_patch(matplotlib.patches.Rectangle((-1,1), 5, 0.5, color="#FEF5AB"))
    ax1.add_patch(matplotlib.patches.Rectangle((-1,1.5), 5, 0.5, color="#FCCF8F"))
    ax1.add_patch(matplotlib.patches.Rectangle((-1,2), 5, 0.5, color="#F5BCAA"))

    #plotting beta values on graph
    ax1.bar (stocks,beta)
    ax1.bar ("Aggregate Value", portfolio_beta)
    ax1.xaxis.set_label_text('Stocks in Portfolio')
    ax1.set_ylim([0, 2.5])

    #setting second y-axis to show volatility classes
    ax2= ax1.twinx()
    offset = -25,0 
    new_axisline1 = ax2.get_grid_helper().new_fixed_axis
    ax2.axis["left"] = new_axisline1(loc="left",axes=ax2, offset=offset)
    ax2.axis["right"].set_visible(False)
    ax2.set_yticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5])
    ax2.yaxis.set_major_formatter(ticker.NullFormatter())
    ax2.yaxis.set_minor_locator(ticker.FixedLocator([0.25,0.75,1.25,1.75,2.25]))
    ax2.yaxis.set_minor_formatter(ticker.FixedFormatter(['very low','low','medium','high','very high']))

    #Final Annotations
    ax2.yaxis.set_label_text("Risk Factor")
    ax2.yaxis.set_label_position('left') 
    plt.title("Beta Values for all Stocks in Portfolio for User {}".format(uname))
    plt.xlabel("Stocks in Portfolio")
    i=0
    for x in beta :
        plt.annotate (x,xy=(i-0.1,beta[i]+0.02),size=10)
        i+=1
    plt.annotate (portfolio_beta,xy=(i-0.1,float(portfolio_beta)+0.02),size=10)
    plt.show()

def riskReturnVisualisation(portfolio,uname) :
    f = open('database.json')
    Listing = json.load(f)
    stocks = []
    mean_ret = []
    beta = []
    for entry in portfolio:
        stocks.append(entry[0])
    
    for stock in stocks :
        stock_name= f"{stock}.NS" if ".NS" not in stock else stock
        try:
            stock_df = yf.download(stock_name, period='4y')
        except:
            exit("Error occured in fetching stock data, please check stop name and try again.")

        daily_close = stock_df.loc[:,"Close"].copy()
        daily_ret = daily_close.pct_change().dropna()
        mean_ret.append(daily_ret.mean()*252)
    
    for stock in stocks :
        for Company in Listing :
            if Company["Symbol"] == stock :
                beta.append(Company["Beta"])
    ulim=max(mean_ret)
    llim=min(mean_ret)
    
    fig1=plt.figure(figsize=(8,8))
    ax=SubplotHost(fig1,111)
    fig1.add_subplot(ax)

    ax.scatter(mean_ret,beta)
    ax.set_ylim([0,2.5])

    ax.set_xticks([0.0, ulim+0.1])
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(['Low','High']))
    ax.set_yticks([0.0,0.5,1.0,1.5,2.0,2.5])
    ax.yaxis.set_major_formatter(ticker.FixedFormatter(['','','','','','High']))


    plt.title("Risk/Return of Portfolio for User {}".format(uname))
    plt.xlabel("Return -->")
    plt.ylabel("Risk -->")
    i=0
    for stock in stocks :
        plt.annotate (stock,xy=(mean_ret[i]+0.005,beta[i]),size=10)
        i+=1
    plt.show()