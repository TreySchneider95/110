from math import prod
from flask import Flask, request, redirect, session, abort
from flask.templating import render_template
import json
# from mock_data import catalog
from config import db
from bson import ObjectId


app = Flask('server')

@app.route("/")
def home():
    return "hello from flask"

@app.route("/me")
def about_me():
    return "Trey Schneider"

@app.route("/api/catalog", methods = ['get'])
def get_catalog():
    products = list()
    for x in db.products.find({}):
        x["_id"] = str(x["_id"])
        products.append(x)
    return json.dumps(products)

@app.route("/api/catalog", methods = ['post'])
def save_catalog():
    product = request.get_json()
    db.products.insert_one(product)
    product["_id"] = str(product["_id"])
    return json.dumps(product)

@app.route("/api/catalog/count", methods = ['get'])
def count_catalog():
    products = list(db.products.find({}))
    return f'{len(products)}'

@app.route("/api/catalog/total", methods = ['get'])
def total_catalog():
    products = list()
    for x in db.products.find({}):
        x["_id"] = str(x["_id"])
        products.append(x)
    return json.dumps(sum([x['price'] for x in products]))

@app.route("/api/catalog/most_expensive", methods = ['get'])
def max_catalog():
    max_num = 0
    products = list()
    for x in db.products.find({}):
        x["_id"] = str(x["_id"])
        products.append(x)
        if x["price"] > max_num:
            max_num = x["price"]
    return json.dumps(max_num)

@app.route("/api/catalog/cheapest", methods = ['get'])
def cheap_catalog():
    prods = list(db.products.find({}))
    min_num = prods[0]['price']
    products = list()
    for x in prods:
        x["_id"] = str(x["_id"])
        products.append(x)
        if x["price"] < min_num:
            min_num = x["price"]
    return json.dumps(min_num)

@app.route("/api/catalog/id/<id>", methods = ['get'])
def get_by_id(id):
    prod = db.products.find_one({'_id' : ObjectId(id)})
    prod["_id"] = str(prod["_id"])
    return json.dumps(prod)

# @app.route("/api/catalog/category", methods = ['get'])
# def get_by_category():
#     products = list()
#     for x in db.products.find({}):
#         x["_id"] = str(x["_id"])
#         products.append(x)
#     results_list = list()
#     for x in products:
#         if x['category'] not in results_list:
#             results_list.append(x['category'])
#     return json.dumps(results_list)

@app.route("/api/catalog/category/<category>", methods = ['get'])
def search_by_category(category):
    prods = list(db.products.find({'category' : category}))
    for x in prods:
        x["_id"] = str(x["_id"])
    return json.dumps(prods)

# @app.route("/sumnumbers", methods = ['get'])
# def sum_numbers():
#     return json.dumps(list(range(1,51)))

allCoupons = []

@app.route("/api/couponCode", methods = ['post', 'get'])
def save_coupon():
    if request.method == 'POST':
        coupon = request.get_json()
        db.coupons.insert_one(coupon)
        coupon["_id"] = str(coupon["_id"])
        return json.dumps(coupon)
    elif request.method == 'GET':
        coupons = list()
        for x in db.coupons.find({}):
            x["_id"] = str(x["_id"])
            coupons.append(x)
        return json.dumps(coupons)


@app.route("/api/couponCode/<code>", methods = ['get'])
def coupon_code(code):
    code = db.coupons.find_one({'code' : code})
    code["_id"] = str(code["_id"])
    return json.dumps(code)


    
app.run(debug=True)