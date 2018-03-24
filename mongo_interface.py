#mongo_interface.py
#creates mongo connection

from pymongo import MongoClient

#mongo stuff setup
client = MongoClient("localhost", 27017)
db = client["wimp"]