from math import *

from flask import  (
    Flask,
    render_template,
    request,
    g,
    session,
    redirect,
    url_for
)
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify
import pymongo 
from pymongo import MongoClient 



### Tạo APP
app = Flask(__name__)
#, static_url_path='', static_folder='/static'
app.secret_key = "adtekdev"

### LIÊN KẾT TỚI DB MONGO
MONGO_URI = 'mongodb+srv://cuteo1232:Hainam08@cluster0-iuz4b.mongodb.net/test?retryWrites=true&w=majority'
cluster = MongoClient(MONGO_URI)

db =  cluster.ATN  # cluster["ATN"]


### CODE Flask - Python Web

@app.route('/')
def  index():
    return render_template("index.html")


@app.route('/home')
def  home():
    return render_template("home.html", username=session['username'], fullname=session['fullname'])

@app.route('/login', methods=['GET', 'POST'])
def  login():

    if session.get('logged_in_flag'):
        if session['logged_in_flag']:
            return redirect(url_for('home'))

    query_parameters = request.args
    vusername = query_parameters.get("username")
    vpassword = query_parameters.get("password")

    collection = db.account
    ### ch-eck Account / Tài khoản USER
    results = collection.find({"username":vusername, "password": vpassword}) 


    if  results.count() == 1:
        session['logged_in_flag'] = True
        session['username'] = results[0]["username"]
        session['fullname'] = results[0]["fullname"]
        return render_template("home.html", username=results[0]["username"], fullname=results[0]["fullname"])
    else:
        session['logged_in_flag'] = False
        return render_template("login.html", mesg = "")

@app.route('/logout', methods=['GET', 'POST'])
def  logout():
    #if session.get('logged_in_flag'):
    if 'logged_in_flag' in session:
        session['logged_in_flag'] = False
    return ""


@app.route('/profile')
def  profile():
    return render_template("profile.html")

@app.route('/products', methods=['GET', 'POST'])
def products():
    collection = db.product 
    lpro = collection.find()
    return render_template("product-listA1.html", productList = lpro)

@app.route('/addProduct', methods=['GET', 'POST'])
def addProduct():
    if ("productName" in request.args  and "productPrice" in request.args):
        pName = request.args.get("productName")
        pPrice = request.args.get("productPrice")
        newProduct = {"name" : pName, "price" : pPrice}
        collection = db.product 
        collection.insert_one(newProduct)
    return render_template("addProduct.html")
    
@app.route('/addOrder', methods=['GET', 'POST'])
def addOrder():
    global total
    total = 0
    collection = db.product
    lpro =  collection.find()
    product= collection.find()
    if ("username" in request.args  and "orderid" in request.args and "productName" in request.args):
        oID = request.args.get("orderid")
        uName = request.args.get("username")
        pPrice = request.args.get("productName")
        oDate =  request.args.get("date")
        for Products in  product:
            total = total + int(Products["price"])*int(pPrice)
        newOrder = {"orderid" : oID, "username": uName, "date" : oDate, "total" : total}
        collection = db.OrderList
        collection.insert_one(newOrder)
    return render_template("addorder.html", productList = lpro)

@app.route('/report', methods=['GET', 'POST'])
def report():
    global vtotal
    vtotal = 0
    collection = db.OrderList
    lpro = collection.find()
    for x in collection.find():
        vtotal = vtotal + int(x["total"])
    newReport = {"total" : vtotal}
    db.report.insert_one(newReport)
    return render_template("report.html", orderList = lpro, total = newReport)
    

