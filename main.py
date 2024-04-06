import database_handler as dbh
LOGIN_STATUS = 0


def uLogin():
    uname = input("Enter username: ")
    passwd = input("Enter password: ")
    status = dbh.userLogin(uname, passwd)
    if status == 1:
        print(("User {} logged in successfully!").format(uname))
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
    dbh.userCreate(uname, legal_name, passwd, phone)
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
            pass
        elif opt=='v':
            pass
        elif opt=='s':
            pass
        elif opt=='l':
            LOGIN_STATUS = 0
            print("User logged out successfully!")
        elif opt=='q':
            print("Automatic user logout")
            print("Bye!")
            exit()
        else:
            print("Invalid option. Please try again.")