import json
import pymongo
from flask import Flask, jsonify, url_for, request, redirect,Response,Request
import pymongo
from bson.json_util import dumps
import mysql.connector
from werkzeug.serving import run_simple
import os
from dotenv import load_dotenv
import datetime
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

test_collection='test_collection'
mongo = pymongo.MongoClient('mongodb://54.83.130.150:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
metadata_db = pymongo.database.Database(mongo, 'test')
metadata_col = pymongo.collection.Collection(metadata_db, 'test_collection')
userlogging_db = pymongo.database.Database(mongo,'user_analytics')
userlogging_col = pymongo.collection.Collection(userlogging_db,'logging')

metadata_db = mysql.connector.connect(
    host ='3.84.158.241',
    user = 'root',
    password = '',
    database = 'reviews',
    )

cur = metadata_db.cursor()

def user_logging(userid,timestamp,req,res):
    return userlogging_col.insert({"id":userid,"timestamp":timestamp,"request":req,"response":res})



@app.route('/',methods=["GET"])
def api_root():
    data = {
        'message': 'Welcome to our website. Where reviews are our number one priority'
    }
    js = json.dumps(data)
    response = Response(js, status=200, mimetype='application/json')
    user_logging(123,datetime.datetime.now().isoformat(),"GET",200)
    return response

@app.route('/categories', methods = ['GET']) #TODO: #returns list of categories 
def get_categories():
    categories = []
    js = json.dumps(data)
    response = Response(js, status=200, mimetype='application/json')
    user_logging(123,datetime.datetime.now().isoformat(),"GET",200)
    return response

@app.route('/search', methods=['GET'])  #now it only searches for TITLE. the mongo metadata does not have author
def search_book():
    try:
        title = request.args.get("title")
        result = metadata_col.find({"title":title})
        print(result)
        result_array = dumps(list(result))
        print(result_array)
        js = json.dumps(result_array)
        response = Response(result_array, status=200, mimetype='application/json')
        user_logging(123,datetime.datetime.now().isoformat(),"GET",200)
        return response
    except:
        errMsg = "Please include title."
        js = json.dumps(errMsg)
        user_logging(123,datetime.datetime.now().isoformat(),"GET",400)
        response = Response(js, status=400, mimetype='application/json')
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
    # if not request.json or not request.json['asin'] or type(request.json['asin']) != str or not request.json['overall'] or not request.json['reviewText'] or type(request.json['reviewText']) != str  or not request.json['reviewTime'] or type(request.json['reviewTime']) != str or not request.json['reviewerID'] or type(request.json['reviewerID']) != str  or not request.json['reviewerName'] or type(request.json['reviewerName']) != str  or not request.json['summary'] or type(request.json['summary']) != str  or not request.json['unixReviewTime'] or type(request.json['unixReviewTime']) != int :
    #     return 'invalid request msg', 404
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
        user_logging(123,datetime.datetime.now().isoformat(),"POST",201)
        return response
    except:
        errMsg = "Please include title, asin, description, price and categories."
        js = json.dumps(errMsg)
        response = Response(js, status=400, mimetype='application/json')
        user_logging(123,datetime.datetime.now().isoformat(),"POST",400)
        return response

@app.route('/addReview',methods = ['POST']) #TODO: add review INTO sql part
def add_review():
    try:
        data = request.json
        asin = data["asin"]
        helpful = [0,0]
        overall = data["overall"]
        reviewText = data["reviewText"]
        reviewTime = data["reviewTime"]
        reviewerID = data["reviewerID"]
        reviewerName = data["reviewerName"]
        summary = data["summary"]
        unixReviewTime = int(time.time())
        mySQL_insert_query = f"""INSERT INTO reviews.kindle_reviews (asin, helpful, overall, reviewText, reviewTime, reviewerID, reviewerName, summary, unixReviewTime)
VALUES ("{asin}","{helpful}",{overall},"{reviewText}","{reviewTime}","{reviewerID}","{reviewerName}","{summary}","{unixReviewTime}");"""    
        cur.execute(mySQL_insert_query)
        metadata_db.commit()
        message = "Successfully uploaded review"
        js = json.dumps(message)
        response = Response(js, status=201, mimetype='application/json')
        user_logging(123,datetime.datetime.now().isoformat(),"POST",201)
        return response
    except:
        errMsg = "An error occurred. Please check if you have all fields."
        js = json.dumps(errMsg)
        response = Response(js, status=400, mimetype='application/json')
        user_logging(123,datetime.datetime.now().isoformat(),"POST",400)
        return response

@app.route('/sortByGenres', methods= ['GET']) #TODO: sort by genres from mongo metadata categories
def sort_by_genres():
    pass

@app.route('/sortByRating' , methods = ['GET'])
def sort_by_ratings():   #sort by increasing ratings,  decreasing rating
    try:
        rating_preference = request.args.get("rating_preference")
        if(rating_preference == 'increasing'): #means rating 1 will come out first
            mySQL_sort_query = """SELECT * FROM reviews.kindle_reviews ORDER BY overall ASC LIMIT 10;"""
        else: #means rating 5 will come out first
            mySQL_sort_query = """SELECT * FROM reviews.kindle_reviews ORDER BY overall DESC LIMIT 10;"""
        cur.execute(mySQL_sort_query)
        result_set = cur.fetchall()
        r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in result_set]
        js = json.dumps(r)
        response = Response(js, status=200, mimetype='application/json')
        user_logging(123,datetime.datetime.now().isoformat(),"GET",200)
        return response
        
    except:
        errMsg = "An error occurred. Please check if you have all fields."
        js = json.dumps(errMsg)
        response = Response(js, status=400, mimetype='application/json')
        user_logging(123,datetime.datetime.now().isoformat(),"GET",400)
        return response



if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=80)   #remember to change this part
    app.run(debug=True)
