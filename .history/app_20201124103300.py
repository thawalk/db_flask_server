import json
from flask import Flask, jsonify, url_for, request, redirect,Response,Request
# from flask_pymongo import PyMongo
import pymongo
from bson.json_util import dumps
import mysql.connector
from werkzeug.serving import run_simple
import os
from dotenv import load_dotenv
import datetime
import time

app = Flask(__name__)

test_collection='test_collection'
# sample='user_collection'
mongo = pymongo.MongoClient('mongodb://54.83.130.150:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
db = pymongo.database.Database(mongo, 'test')
metadata_col = pymongo.collection.Collection(db, 'test_collection')

db = mysql.connector.connect(
    host ='3.84.158.241',
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
@app.route('/search', methods=['GET'])  #TODO: search for book by author or title from mongo 
def search_book():
    data = request.json
    if()
    
    print(data)
    js = json.dumps(data)
    response = Response(js, status=200, mimetype='application/json')
    return response


# @app.route('/review', methods=['POST'])
# def add_review():
#     if not request.json or not request.json['asin'] or type(request.json['asin']) != str or not request.json['overall'] or not request.json['reviewText'] or type(request.json['reviewText']) != str  or not request.json['reviewTime'] or type(request.json['reviewTime']) != str or not request.json['reviewerID'] or type(request.json['reviewerID']) != str  or not request.json['reviewerName'] or type(request.json['reviewerName']) != str  or not request.json['summary'] or type(request.json['summary']) != str  or not request.json['unixReviewTime'] or type(request.json['unixReviewTime']) != int :
#         return 'invalid request msg', 404
#     txt = "INSERT INTO 'kindle_reviews' ('id', 'asin', 'overall', 'reviewText', 'reviewTime', 'reviewerID', 'reviewerName', 'summary', 'unixReviewTime') VALUES (%s)" 
#     values = (None, request.json['asin'], request.json['overall'], request.json['reviewText'], request.json['reviewTime'],  request.json['reviewerID'], request.json['reviewerName'], request.json['summary'], request.json['unixReviewTime'])
#     cur.execute(txt, values)

#     return 'successfully uploaded new review', 200

@app.route('/addBook',methods= ['POST'])
def add_book():
    try:
        data = request.json
        title = data['title']
        asin = data['asin']
        description = data['description']
        price = data['price']
        categories = data['categories']
        message = "Book added successfully"
        metadata_col.insert({"title":title,"asin":asin,"description":description,"price":price,"categories":categories})
        js = json.dumps(message)
        response = Response(js, status=201, mimetype='application/json')
        return response
    except:
        errMsg = "Please include title, asin, description, price and categories."
        js = json.dumps(errMsg)
        response = Response(js, status=400, mimetype='application/json')
        return response

@app.route('/addReview',methods = ['POST']) #TODO: add review INTO sql part
def add_review():
    pass

@app.route('/sortByGenres', methods= ['GET']) #TODO: sort by genres from mongo metadata categories
def sort_by_genres():
    pass



    


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=80)
    app.run(debug=True)