from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import matplotlib
from mpl_toolkits.axisartist.parasite_axes import SubplotHost

import yfinance as yf
import json
import portfolio_beta_calculator as pbc
import database_handler as dbh

def weightedPortfolioVisualisation(portfolio, uname):
    priced_portfolio=pbc.getStockPrices(portfolio)
    weights = []
    labels = []
    for entry in priced_portfolio:
        labels.append("{} ({}) ".format(entry[0],entry[1]))
        weights.append(entry[1]*entry[2])
    colors=['#FFADAD','#E4F1EE','#D9EDF8','#DEDAF4','#A8D1D1','#FFCBCB','#FDFFB6','#FFD6A5','#FFADAD','#E4F1EE','#D9EDF8','#DEDAF4','#A8D1D1','#FFCBCB','#FDFFB6']
    plt.pie(weights, labels=labels, textprops=dict(weight='bold'), colors=colors)
    plt.title("Portfolio for {}".format(dbh.getLegalName(uname)),weight='bold')
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
    fig1=plt.figure(figsize=(12,6))

    ax1= SubplotHost(fig1,111)
    fig1.add_subplot(ax1)

    #defining colour scale for risk factor
    ax1.add_patch(matplotlib.patches.Rectangle((-1,0), 5, 0.5, color="#B3D4B4"))
    ax1.add_patch(matplotlib.patches.Rectangle((-1,0.5), 5, 0.5, color="#E5EC9E"))
    ax1.add_patch(matplotlib.patches.Rectangle((-1,1), 5, 0.5, color="#FEF5AB"))
    ax1.add_patch(matplotlib.patches.Rectangle((-1,1.5), 5, 0.5, color="#FCCF8F"))
    ax1.add_patch(matplotlib.patches.Rectangle((-1,2), 5, 0.5, color="#F5BCAA"))

    #plotting beta values on graph
    ax1.bar (stocks,beta,color='#4c4d52')
    ax1.bar ("Portfolio", portfolio_beta,color='#6277ad')
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
    plt.title("Beta Values for all Stocks in Portfolio for {}".format(dbh.getLegalName(uname)),weight='bold')
    plt.xlabel("Stocks in Portfolio")
    i=0
    for x in beta :
        plt.annotate (x,xy=(i-0.1,beta[i]+0.02),size=10)
        i+=1
    plt.annotate (portfolio_beta,xy=(i-0.1,float(portfolio_beta)+0.02),size=10)
    plt.show()

