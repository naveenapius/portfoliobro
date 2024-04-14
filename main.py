import database_handler as dbh
from matplotlib import pyplot as plt
import suggestion_system as ss
import simulator as sim
LOGIN_STATUS = 0 # latch for login management


def simulatorHelper(uname):
    portfolio = dbh.getPortfolio(uname)
    print("\nAvailable actions: ")
    print("a - Simulate addition")
    print("r - Simulate removal")

    o = input("Action>> ")
    flag = 0 if o=='a' else '1'
    stock = input("Enter stock to simulate: ")
    vol = int(input("Enter volume: "))

    print("New portfolio beta: ",sim.simulate(portfolio, stock, vol, flag))
    return




def getVisualisation(portfolio, uname):
    stocks = []
    shares = []
    for i in portfolio:
        stocks.append(i[0])
        shares.append(i[1])
    plt.pie(shares, labels=stocks)
    plt.title("Portfolio for user {}".format(uname))
    plt.show()


def uLogin():
    global user_name
    user_name = input("\nEnter username: ")
    passwd = input("Enter password: ")
    status = dbh.userLogin(user_name, passwd)
    if status == 1:
        print(("User {} logged in successfully!\n").format(user_name))
        return 1
    else:
        print(status)
        return 0


def uSignUp():
    print("\nHello! Let's set up your account.\n")
    legal_name = input("Enter your legal name: ")
    uname = input("Enter new username: ")
    passwd = input("Enter password: ")
    phone = input("Enter phone number: ")
    risk_app = input("Enter your risk appetite: ")
    dbh.userCreate(uname, legal_name, passwd, phone, risk_app)
    return

def showPortfolio(uname):
    portfolio = dbh.getPortfolio(uname)
    for i in portfolio:
        print("{} : {}")

def updatePortfolio(uname):
    print("\n Available actions: ")
    print("a - Add stock")
    print("d - Remove stocks")
    opt = input("Action>>")
    if opt=='a':
        stock = input("\nEnter listing code: ")
        shares = input("Enter number of shares purchased: ")
        dbh.addStock(uname, stock, shares)
    elif opt=='d':
        stock = input("\nEnter listing code: ")
        shares = input("Enter number of shares sold: ")
        dbh.removeStock(uname, stock, shares)
    else:
        print("\nInvalid option. Please try again.")
    return


def showLoginMenu():
    print("\n\nAvailable actions: ")
    print("l - Login")
    print("s - Signup")
    print("q - Quit\n")
    
    

def showLoggedInMenu():
    print("\n\nAvailable actions:")
    print("u - Update portfolio")
    print("v - Visualise portfolio")
    print("s - Simulate additions/removals")
    print("r - Get recommendation")
    print("l - Logout")
    print("q - Quit\n")



#main
while True:
    if LOGIN_STATUS==0:
        showLoginMenu()
        opt = input("Action>> ")
        if opt=='l':
            r = uLogin()
            LOGIN_STATUS = 1 if r==1 else 0
        elif opt=='s':
            uSignUp()
        elif opt=='q':
            print("Bye!")
            exit()
        else:
            print("Invalid option. Please try again.")
    elif LOGIN_STATUS==1:
        showLoggedInMenu()
        opt = input("Action>> ")
        if opt=='u':
            updatePortfolio(user_name)
        elif opt=='v':
            portfolio = dbh.getPortfolio(user_name)
            getVisualisation(portfolio, user_name)
        elif opt=='s':
            simulatorHelper(user_name)
        elif opt=='l':
            LOGIN_STATUS = 0
            print("User logged out successfully!")
        elif opt=='r':
            risk_app = dbh.getRiskAppetite(user_name)
            portfolio = dbh.getPortfolio(user_name)
            suggested = (ss.suggestions(portfolio, risk_app))
            print("Suggestions")
            for i, stocks in suggested.items():
                print("---------------------------")
                print(i)
                print("---------------------------")
                for j in stocks:
                    for k in j:
                        print(k[0])

        elif opt=='q':
            print("Automatic user logout")
            print("Bye!")
            exit()
        else:
            print("Invalid option. Please try again.")