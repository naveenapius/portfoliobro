import mysql.connector
from hashlib import sha1

#initialising connection

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="portfoliobro_test",
    port="3307",
    buffered=True
    )
cur = conn.cursor()


def generateUID(name, phone):
    '''
    params:
        null
    returns:
        15digit user id string
    '''
    seed = (name +str(phone)).encode()#converts name into a base 26 integer and adds phone number to generate seed value
    return sha1(seed).hexdigest()[-15:] #last 15 characters of hash 


def initUser(name, phone=0000, email=''):
    uid = generateUID(name, phone)
    # try:
    insert_user = 'INSERT INTO users values("{}", "{}", "{}", "{}")'.format(uid, name, phone, email)
    cur.execute(insert_user)
    print("User added to database.")
    # return 0
    # except:
    #     print("Unable initialise user. Check database")
    #     return 1


# print(generateUID('damian', 8129482072))

initUser('naveena', 8129482072, 'piusnaveena@gmail.com')