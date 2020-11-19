import json
from flask import Flask, jsonify, url_for, request, redirect,Response,Request
# from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.json_util import dumps
import mysql.connector
from werkzeug.serving import run_simple
import os
from dotenv import load_dotenv

app = Flask(__name__)

# mongo_url = os.getenv("mongo_url")
# dbname = os.getenv("database_name")
# mongo_store = MongoClient(mongo_url)
# metadata = mongo_store.dbname.metadata

bruh='test_collection'
# sample='user_collection'
mongo_url ="52.207.207.58"
dbname ='test'
mongo_store = MongoClient(mongo_url)
metadata = mongo_store.dbname.bruh
# data = mongo_store.dbname.sample
print(metadata.find({'price': '19.99'}))

db = mysql.connector.connect(
    host ='18.234.193.20',
    user = 'root',
    password = '',
    database = 'reviews'
    )


cur = db.cursor()
cur.execute("SELECT asin from kindle_reviews group by asin order by avg(overall) desc limit 9 ")
print(cur.fetchall())

@app.route('/',methods=["GET"])
def api_root():
    data = {
        'message': 'Welcome to SUTD room service. /rooms to see more info'
    }
    js = json.dumps(data)
    response = Response(js, status=200, mimetype='application/json')
    return response

if __name__ == '__main__':
    app.run(port=5000, debug=True)