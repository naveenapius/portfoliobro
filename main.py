import database_handler as dbh
LOGIN_STATUS = 0

def uLogin(uname, passwd):
    uname = input("Enter username: ")
    passwd = input("Enter password: ")


def uSignUp():
    print("Hello! Let's set up your account.")
    legal_name = input("Enter your legal name: ")
    uname = input("Enter new username: ")
    passwd = input("Enter password: ")
    phone = input("Enter phone number: ")
    dbh.userCreate(uname, legal_name, passwd, phone)
    return




#main
print("Welcome to portfoliobro!")
while LOGIN_STATUS==0:
    user_action = int(input("Choose action: Login(1) or Signup(2)\n>>>"))
    if user_action == 1:
        uLogin()
    elif user_action == 2:
        uSignUp()
    else:
        print("Sorry, that's an invalid choice. Please try again.")