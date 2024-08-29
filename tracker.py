import requests
import sqlite3
import datetime as dt
import bcrypt as bc


# api request to get calories data
api_key =  '4cb53b6c39d39d0b16ea3df4f90c82be'
application_id = '34ac556c'
url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
header = {
    'Content-Type': 'application/json',
    'x-app-id' : application_id,
    'x-app-key' : api_key 
}


# create the databse and cursor
con = sqlite3.connect("database.db")
cursor = con.cursor()



# to put personal info and date info into sql tables
def personal_info(date, username, password):
    name = input("Please enter your name: ")
    while True:
        try:
            # if weight and height are all int, and the gender is either male or female, we want both
            weight = float(input("Please enter your weight in kg: "))
            height = float(input("Please enter your height in cm: "))
            age = int(input("Please enter your age in years: "))
            gender = input("Please Enter your gender(male or female): ")
            if gender.lower() in ('male','female'):
                break
        except ValueError:
            print("Please enter a valid weight")
    if gender.lower() == 'male':
        calories = (9.65 * weight) + (573 * height / 100) - (5.08 * age) + 260
    elif gender.lower() == 'female':
        calories = (7.38 * weight) + (607 * height / 100) - (2.31 * age) + 4
    
     # insert teh new entry into teh sql database
    cursor.execute("INSERT INTO People (name, height, weight, age, calories, username, password) VALUES(?, ?, ?, ?, ?, ?, ?)", (name, height, weight, age, calories, username, password))
    con.commit()
    # to get the last row id of the last insert statement executed--people table
    peopleid = cursor.lastrowid
    cursor.execute("INSERT INTO date (date, calories, people_id) VALUES (?, ?, ?)", (date, calories, peopleid))
    con.commit()
    return peopleid


def Meals(date, id):
    daymeals = ['breakfast', 'lunch', 'dinner', 'snacks']
    # this returns a tuple, need to float the first element only since tuple is like a list
    c = cursor.execute("SELECT calories from People WHERE id = id").fetchone()
    finalc = float(c[0])
    for meal in daymeals:
        while True:
            eat = input(f"What did you eat for {meal} (type end when you listed all): ")
            if eat.lower() == 'end':
                break
            
            data = {
                    'query' : eat.lower()
                    }
            data = requests.post(url, headers = header, json = data)

            # if the request is good
            if data.status_code == 200:


                serving = float(data.json()['foods'][0]['serving_weight_grams'])
                # converting input
                try:
                    # calculate teh calories
                    amount = float(input("How much did you eat (in grams): "))

                    # change calories
                    calories = float((data.json()['foods'][0]['nf_calories']) * (amount / serving))
                    finalc = finalc - calories

                    cursor.execute('INSERT INTO meals (name, date, amount, calories, people_id) VALUES(?, ?, ?, ?, ?)', (eat, date, amount, calories, id))
                    con.commit()
                    
                # shouldn't have any value errors
                except ValueError:
                    print("Not worky")

            # if the request fails, since the api works after testing, it has to be a spelling error 
            else:
                print("Error in retrieving data, please enter again with proper spelling")

    cursor.execute('''
            UPDATE date
            SET calories = ?
            WHERE people_id = ?
''', (finalc, id))

          
def askdecision():
    question = input('''
What do you want to do:
A. Log calories intake      B. Retrieve historical data

''')
    return question

def askaccount():
    answer = input('''
Do you have an account?
Yes                 No 
''')
    return answer


def retrieve(id, date):
    calories = cursor.execute('SELECT calories FROM date WHERE people_id = (?) AND date = (?)', (id, date)).fetchone()
    return calories

def credentials():
    username = input("Username: ").strip()
    password = input("Password: ")
    return username, password
        

def log(id):
    history = input("Please enter a date: ")
                            
    while True:                            
        try:
            result = float(retrieve(id, history)[0])
            break
        except ValueError:
            print("Error retrieving data, please try again")
            continue

                            
    if result >= 0:
        print('You did not meet your calories goal that day')
        
    else:
        print("Congrat! You met the goal that day")
        
def create_account(date):
    username = input("Please enter a username: ")
    password = input("Please enter a password: ")
    byte = password.encode('utf-8')
    
    # encrypt the password for better security
    salt = bc.gensalt()
    hashed = bc.hashpw(byte, salt)
    id = personal_info(date, username, hashed)
    return id
            

def main():
    date = dt.date.today().strftime('%Y-%m-%d')

    while True:
        # ask what user wants to do 
        decision = askaccount()
        if decision.lower() == "yes":

            # provide credentials
            username, password = credentials()

            # take crediential from database
            auth = cursor.execute("SELECT password, id FROM People WHERE username = ?", (username,)).fetchone()
            if auth is not None:
                
                word, id = auth
                # encode the password user has entered
                encode = password.encode('utf-8')

                if bc.checkpw(encode, word):

                    while True:
                        decision = askdecision()
                        if decision == 'A':
                            Meals(date, id)
                            continue

                        elif decision == 'B':
                            log(id)
                            continue
                            

                else:
                    print("Incorrect password")

            else:
                print("Username does not exist")

                    
        elif decision.lower() == "no":
            id = create_account(date)
            
          
main()