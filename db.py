from flask import Flask
from flask_pymongo import pymongo
from app import app

CONNECTION_STRING = 'mongodb+srv://mongoadmin:j0yc329@cluster0.8yefw.gcp.mongodb.net/healthy_ship?retryWrites=true&w=majority'

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('healthy_ship')
vehicle_collection = pymongo.collection.Collection(db, 'vehicles')