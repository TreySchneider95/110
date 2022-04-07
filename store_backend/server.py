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
        if not "name" in coupon or len(coupon['name']) < 5:
            return abort(400, "code is required or not valid")
        if not "discount" in coupon or coupon['discount'] < 5 or coupon['discount'] > 50:
            return abort(400, "discount is required or not valid")
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


@app.route("/api/user", methods = ['post', 'get'])
def save_user():
    if request.method == 'POST':
        user = request.get_json()
        if not "email" in user or len(user['email']) < 1:
            return abort(400, "email is required or not valid")
        if not "username" in user or len(user['username']) < 1:
            return abort(400, "username is required or not valid")
        if not "password" in user or len(user['password']) < 1:
            return abort(400, "password is required or not valid")
        if not "first" in user or len(user['first']) < 1:
            return abort(400, "first name is required or not valid")
        if not "last" in user or len(user['last']) < 1:
            return abort(400, "last name is required or not valid")
        db.users.insert_one(user)
        user["_id"] = str(user["_id"])
        return json.dumps(user)
    elif request.method == 'GET':
        users = list()
        for x in db.users.find({}):
            x["_id"] = str(x["_id"])
            users.append(x)
        return json.dumps(users)

@app.route("/api/user/by_email/<email>", methods = ['get'])
def find_user(email):
    user = db.users.find_one({'email' : email})
    user["_id"] = str(user["_id"])
    return json.dumps(user)


@app.route("/api/user/valid", methods = ['post'])
def validate_user():
    user_attempt = request.get_json()
    if not "username" in user_attempt:
        return abort(400, "user is required")
    if not "password" in user_attempt:
        return abort(400, "password is required")
    user = db.users.find_one({'username' : user_attempt['username'], "password": user_attempt["password"]})
    if not user:
        return  abort(401, "user not found")
    else:
        user["_id"] = str(user["_id"])
        user.pop("password")
        return json.dumps(user)


app.run(debug=True)