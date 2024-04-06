import database_handler as dbh
LOGIN_STATUS = 0
UNAME = ""


def uLogin():
    global user_name
    user_name = input("Enter username: ")
    passwd = input("Enter password: ")
    status = dbh.userLogin(user_name, passwd)
    if status == 1:
        print(("User {} logged in successfully!").format(user_name))
        return 1
    else:
        print(status)
        return 0


def uSignUp():
    print("Hello! Let's set up your account.")
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
    print("Current user: {}".format(uname))
    print("Available actions: ")
    print("Add stock (a)")
    print("Remove stock (d)")
    opt = input("Action>>")
    if opt=='a':
        stock = input("Enter listing code: ")
        shares = input("Enter number of shares purchased: ")
        dbh.addStock(uname, stock, shares)
    elif opt=='d':
        stock = input("Enter listing code: ")
        shares = input("Enter number of shares sold: ")
        dbh.removeStock(uname, stock, shares)
    else:
        print("Invalid option. Please try again.")
    return


def showLoginMenu():
    print("\n\nAvailable actions: ")
    print("Login (l)")
    print("Signup (su)")
    print("Quit (q)\n")
    
    

def showLoggedInMenu():
    print("\n\nAvailable actions:")
    print("Update portfolio (u)")
    print("Visualise portfolio (v)")
    print("Simulate additions/removals (s)")
    print("Get recommendation (r)")
    print("Logout (l)")
    print("Quit (q)\n")



#main
while True:
    if LOGIN_STATUS==0:
        showLoginMenu()
        opt = input("Action>> ")
        if opt=='l':
            r = uLogin()
            LOGIN_STATUS = 1 if r==1 else 0
        elif opt=='su':
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
            pass
        elif opt=='s':
            pass
        elif opt=='l':
            LOGIN_STATUS = 0
            print("User logged out successfully!")
        elif opt=='r':
            pass
        elif opt=='q':
            print("Automatic user logout")
            print("Bye!")
            exit()
        else:
            print("Invalid option. Please try again.")