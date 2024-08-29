import requests
import sqlite3
from io import StringIO
import csv
import json

class person():
    def __initi__(self, name, age, weight, height, gender, calories):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.gender = gender
        self.calories = self.calculate_calories()
    
    def calculate_calories(self):
        if self.gender == 'male':
            calories = (9.65 * self.weight) + (573 * self.height) - (5.08 * self.age) + 260
            return calories
        if self.gender == 'female':
            calories = (7.38 * self.weight) + (607  * self.height) - (2.31  * self.age) + 43
    
api_key =  '4cb53b6c39d39d0b16ea3df4f90c82be'
application_id = '34ac556c'
url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
header = {
    'Content-Type': 'application/json',
    'x-app-id' : application_id,
    'x-app-key' : api_key 
    
}

data = {
    'query' : 'chicken'
}
data = requests.post(url, headers = header, json = data)
nutrition = data.text
file = StringIO(nutrition)
reader = csv.DictReader(file)

key = reader.fieldnames

if data.status_code == 200:
    good = data.json()['foods'][0]['nf_calories']
    print(good)
