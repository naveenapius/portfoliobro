from matplotlib import pyplot as plt


def weightedPortfolioVisualisation(portfolio, uname):
    stocks = []
    shares = []
    for i in portfolio:
        stocks.append(i[0])
        shares.append(i[1])
    plt.pie(shares, labels=stocks)
    plt.title("Portfolio for user {}".format(uname))
    plt.show()