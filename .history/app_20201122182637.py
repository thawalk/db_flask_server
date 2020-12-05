import json
from flask import Flask, jsonify, url_for, request, redirect,Response,Request
# from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.json_util import dumps
import mysql.connector
from werkzeug.serving import run_simple
import os
from dotenv import load_dotenv
import datetime

app = Flask(__name__)

# mongo_url = os.getenv("mongo_url")
# dbname = os.getenv("database_name")
# mongo_store = MongoClient(mongo_url)
# metadata = mongo_store.dbname.metadata

test_collection='test_collection'
# sample='user_collection'
mongo_url ="54.211.223.244"
dbname ='test'
mongo_store = MongoClient(mongo_url)
metadata = mongo_store.dbname.test_collection
# data = mongo_store.dbname.sample
print("testing metadata find")
print(dumps(list(metadata.find().limit(10))))
print(dumps(list(metadata.find().limit(10))))



db = mysql.connector.connect(
    host ='52.87.158.130',
    user = 'root',
    password = '',
    database = 'reviews'
    )


cur = db.cursor()
# cur.execute("SELECT asin from kindle_reviews group by asin order by avg(overall) desc limit 9 ")
# print(cur.fetchall())
# print("above fetch all")

@app.route('/',methods=["GET"])
def api_root():
    data = {
        'message': 'Welcome to our website. Where reviews are our number one priority'
    }
    js = json.dumps(data)
    response = Response(js, status=200, mimetype='application/json')
    return response

#returns list of categories 
@app.route('/categories', methods = ['GET'])
def get_categories():
    categories = []
    js = json.dumps(data)
    response = Response(js, status=200, mimetype='application/json')
    return response

#Search for book using title, price or asin
@app.route('/search', methods=['GET'])  #lets fix this
def search_book():
    # print("search endpoint")
    data = dumps(metadata.find().limit(20))
    # print(data)
    js = json.dumps("data")
    response = Response(js, status=200, mimetype='application/json')
    return response
    # book = []
    # if title in request.args:
    #     book = metadata.find({'title': title})
    # elif price in request.args:
    #     book = metadata.find({'price':price})
    # elif asin in request.args:
    #     book = metadata.find({'asin':asin})
    # if len(book) > 0:
    #     msg = {'status': 200, 'message': 'book(s) successfully found', 'books': book}
    # else :
    #     msg = {'status': 500, 'message': 'no books found with the following searches'}
    # return jsonify(msg)

@app.route('/review', methods=['POST'])
def add_review():
    if not request.json or not request.json['asin'] or type(request.json['asin']) != str or not request.json['overall'] or not request.json['reviewText'] or type(request.json['reviewText']) != str  or not request.json['reviewTime'] or type(request.json['reviewTime']) != str or not request.json['reviewerID'] or type(request.json['reviewerID']) != str  or not request.json['reviewerName'] or type(request.json['reviewerName']) != str  or not request.json['summary'] or type(request.json['summary']) != str  or not request.json['unixReviewTime'] or type(request.json['unixReviewTime']) != int :
        return 'invalid request msg', 404
    txt = "INSERT INTO 'kindle_reviews' ('id', 'asin', 'overall', 'reviewText', 'reviewTime', 'reviewerID', 'reviewerName', 'summary', 'unixReviewTime') VALUES (%s)" 
    values = (None, request.json['asin'], request.json['overall'], request.json['reviewText'], request.json['reviewTime'],  request.json['reviewerID'], request.json['reviewerName'], request.json['summary'], request.json['unixReviewTime'])
    cur.execute(txt, values)

    return 'successfully uploaded new review', 200


    


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=80)
    app.run(debug=True)