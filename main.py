import database_handler as dbh
import suggestion_system as ss
import simulator as sim
import visualiser as vis
import maskpass as mp
import string
from tabulate import tabulate as tb
from hashlib import sha256


# MENUS
def showLoginMenu():
    print("\n\nAvailable actions: ")
    print("l - Login")
    print("s - Signup")
    print("i - Info")
    print("q - Quit\n")
      

def showLoggedInMenu():
    print("\n\nAvailable actions:")
    print("c - View current portfolio")
    print("u - Update portfolio")
    print("v - Visualise portfolio")
    print("s - Simulate additions/removals")
    print("r - Get recommendation")
    print("p - Update user profile")
    print("l - Logout")
    print("q - Quit\n")


def showVisualiserMenu():
    print("\nAvailable actions: ")
    print("p - Visualise portfolio")
    print("b - Visualise beta")
    print("q - Quit")

def showSimulatorMenu():
    print("\nAvailable actions: ")
    print("a - Simulate addition")
    print("r - Simulate removal")
    print("q - Quit")

def showPortfolioUpdateMenu():
    print("\nAvailable actions: ")
    print("a - Add stock")
    print("d - Remove stocks")
    print("q - Quit")

def showRiskMenu():
    print("\nAvailable actions: ")
    print("vl - Very low")
    print("l - Low")
    print("m - Medium")
    print("h - High")
    print("vh - Very high")

def showProfileUpdateMenu():
    print("\nAvailable actions: ")
    print("p - Update password")
    print("m - Update phone number")
    print("r - Update risk profile")
    print("v - View current profile")
    print("q - Quit")

# VALIDATORS

def validateUname(uname):
    """
    :param uname: entered username to be validated
    :return : 0/1 validation
    """
    allowed = list(string.ascii_letters) + list(string.ascii_letters)  + ["_"]
    if len(uname.split()) > 1:
        return [0, "Spaces not allowed in username"]
    for i in uname:
        if i not in allowed:
            return [0, "Invalid characters used. Allowed characters: alphabets, numbers, underscore"]
    return [1]



def validatePhoneNumber(phone):
    """
    :param phone: phone number to be validated
    :return: 0/1 validation
    """
    if not(phone.isnumeric()):
        return [0, "non numeric characters not allowed in phone number"]
    if len(phone) !=10:
        return [0, "phone number should be of length 10"]
    else:
        return [1]


# HELPERS

def showDocs():
    with open("portfoliobro_docs.txt", "r") as f:
        print(f.read())
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
        return -1

def uSignUp():
    print("\nHello! Let's set up your account.\n")
    legal_name = input("Enter your legal name: ").capitalize()
    uname = input("Enter new username: ")
    validation = validateUname(uname)
    if validation[0] != 1: #validating user names
        print(validation[1])
        print("User creation failed. Please try again.")
        return
    
    while(True):
        passwd = mp.askpass(prompt = "Enter password: ", mask="*")
        passwd_rpt = mp.askpass(prompt = "Re-enter password to confirm: ", mask="*")
        if passwd != passwd_rpt:
            print("Passwords do not match. Please try again.")
        else:
            break
    
    
    phone = input("Enter phone number: ")
    validatePhoneNumber(phone)
    if validatePhoneNumber[0] != 1: #validating phone number
        print(validatePhoneNumber[0])
        print("User creation failed. Please try again.")

    while(True):
        print("\nRisk appetite selection:")
        print("Available options: ")
        showRiskMenu()  
        risk_app_opt = input("Enter your risk appetite: ")
        risk_app = getRisk(risk_app_opt)
        if risk_app != -1:
            dbh.userCreate(uname, legal_name, passwd, phone, risk_app)
            break
        else:
            print("Invalid option. Please try again.")
    return

def showPortfolio(uname):
    portfolio = dbh.getPortfolio(uname)
    headers = ["Symbol", "Shares"]
    print("Your current portfolio: ")
    print(tb(portfolio, headers, tablefmt="grid"))
    return


def updatePortfolio(uname):  
    while True:
        showPortfolioUpdateMenu()
        opt = input("Action>>")
        if opt=='a':
            stock = input("\nEnter listing code: ")
            if dbh.checkIfStockInNifty500(stock)!=0:
                shares = input("Enter number of shares purchased: ")
                dbh.addStock(uname, stock, shares)
            else:
                print("This stock does not exist in the database. Please try again.")
        elif opt=='d':
            stock = input("\nEnter listing code: ")
            shares = int(input("Enter number of shares sold: "))
            avail = dbh.checkStockAvailability(uname, stock)
            if avail == -1:
                print("This stock is not available in your portfolio")
                return
            elif avail < shares:
                print("Insufficient stocks for removal")
            else:
                dbh.removeStock(uname, stock, shares)
        elif opt == 'q':
            return
        else:
            print("\nInvalid option. Please try again.")


def updateUserProfile(uname):
    while True:
        showProfileUpdateMenu()
        opt = input("Action>> ")
        if opt == "p":
            # update password
            current_password = mp.askpass(prompt = "Enter current password: ", mask="*")
            current_password_hashed = sha256(current_password.encode()).hexdigest()
            old_password = dbh.getPassword(uname)
            if current_password_hashed != old_password:
                print("Incorrect password entered. Please try again.")
            else:
                new_pass = mp.askpass(prompt = "Enter new password: ", mask="*")
                new_pass_repeat = mp.askpass(prompt = "Repeat new password: ", mask="*")
                if new_pass != new_pass_repeat:
                    print("Passwords do not match. Please try again.")
                else:
                    dbh.updatePassword(uname, sha256(new_pass.encode()).hexdigest())
                    print("Password updated successfully.")
        elif opt == "m":
            newphone = input("Enter new phone number: ")
            f = validatePhoneNumber(newphone)[0]
            if f==0:
                print("Invalid phone number entered. Please try again.")
            else:
                dbh.updatePhoneNumber(uname, newphone)
                print("Phone number updated successfully.")
        elif opt == "r":
            showRiskMenu()
            newrisk = input("Enter new risk: ")
            if getRisk(newrisk) == -1:
                print("Invalid option entered. Please try again.")
            else:
                dbh.updateRisk(uname, getRisk(newrisk))
                print("Risk appetite successfully updated.")
        elif opt == "v":
            print("\nCurrent profile: ")
            print("Legal Name: ", dbh.getLegalName(uname))
            print("Phone Number: ", dbh.getPhoneNumber(uname))
            print("Risk Appetite: ", dbh.getRiskAppetite(uname))
        elif opt == "q":
            return
        else:
            print("Invalid option. Please try again.")
            

def simulatorHelper(uname): 
    portfolio = dbh.getPortfolio(uname)
    while(True):
        showSimulatorMenu()
        o = input("Action>> ")
        if o=='a':
            flag = 0
            stock = input("Enter stock to simulate: ")
            check  = dbh.checkIfStockInNifty500(stock)
            if check != 0:
                vol = int(input("Enter volume: "))
                return sim.simulate(portfolio, stock, vol, flag)
            else:
                print("Stock not available in database. Please try again.")
        elif o=='r':
            flag = 1
            stock = input("Enter stock to simulate: ")
            check  = dbh.checkIfStockInNifty500(stock)
            if check != 0:
                vol = int(input("Enter volume: "))
                return sim.simulate(portfolio, stock, vol, flag)
            else:
                print("Stock not available in database. Please try again.")
        elif o=='q':
            return
        else:
            print("Invalid option. Please try again.")

def visualiserHelper(user_name):
    portfolio = dbh.getPortfolio(user_name)
    while True:
        showVisualiserMenu()
        opt = input("Action>> ")
        if opt=='p':
            vis.weightedPortfolioVisualisation(portfolio, user_name)
            return
        elif opt=='b':
            vis.betaVisualisation(portfolio, user_name)
            return
        elif opt=='q':
            return
        else:
            print("Invalid option. Please try again.")



if __name__ == '__main__':
    LOGIN_STATUS = 0 # latch for login management
    while True:
        if LOGIN_STATUS==0:
            showLoginMenu()
            opt = input("Action>> ")
            if opt=='l':
                r = uLogin()
                LOGIN_STATUS = 1 if r==1 else 0
            elif opt=='s':
                uSignUp()
            elif opt=='i':
                showDocs()
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
            elif opt == 'c':
                showPortfolio(user_name)
            elif opt=='v':
                visualiserHelper(user_name)
            elif opt=='s':
                beta = simulatorHelper(user_name)
                try: 
                    print("Old portfolio beta: ", beta[0])
                    print("New portfolio beta: ", beta[1])
                except TypeError:
                    pass
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
            elif opt == 'p':
                updateUserProfile(user_name)
            elif opt=='q':
                print("Automatic user logout") 
                print("Bye!")
                exit()
            else:
                print("Invalid option. Please try again.")