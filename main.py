import database_handler as dbh
import suggestion_system as ss
import simulator as sim
import maskpass as mp
import visualiser as vis
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







def uLogin():
    global user_name
    user_name = input("\nEnter username: ")
    passwd = mp.askpass(prompt = "Enter password: ", mask="*")
    status = dbh.userLogin(user_name, passwd)
    if status == 1:
        print(("User {} logged in successfully!\n").format(user_name))
        return 1
    else:
        print(status)
        return 0


def getRisk(opt):
    if opt == 'vl':
        return "very low"
    elif opt == 'l':
        return "low"
    elif opt == "m":
        return "medium"
    elif opt == "h":
        return "high"
    elif opt == "vh":
        return "very high"
    else:
        return 0

def uSignUp():
    print("\nHello! Let's set up your account.\n")
    legal_name = input("Enter your legal name: ")
    uname = input("Enter new username: ")
    while(True):
        passwd = mp.askpass(prompt = "Enter password: ", mask="*")
        passwd_rpt = mp.askpass(prompt = "Re-enter password to confirm: ", mask="*")
        if passwd != passwd_rpt:
            print("Passwords do not match. Please try again.")
        else:
            break
    
    
    phone = input("Enter phone number: ")
    while(True):
        print("\nRisk appetite selection:")
        print("Available options: ")
        print("vl - Very low\nl - Low\nm - Medium\nh - High\nvh - Very high")
        risk_app_opt = input("Enter your risk appetite: ")
        risk_app = getRisk(risk_app_opt)
        if risk_app != 0:
            dbh.userCreate(uname, legal_name, passwd, phone, risk_app)
            break
        else:
            print("Invalid option. Please try again.")
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


def showVisualiserMenu():
    print("\nAvailable actions: ")
    print("p - Visualise portfolio contents")
    print("b - Visualise beta of portfolio")
    print("r - Visualise risk/return of portfolio\n")

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
            showVisualiserMenu()
            opt = input("Action>> ")
            if opt=='p':
                vis.weightedPortfolioVisualisation(portfolio, user_name)
            elif opt=='b':
                vis.betaVisualisation(portfolio, user_name)
            elif opt=='r':
                vis.riskReturnVisualisation(portfolio,user_name)
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