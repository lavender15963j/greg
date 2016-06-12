import os

from flask import (Flask, render_template, url_for, Markup, request, redirect,
                   make_response)
                   
from AccountHander import AccountHander
from Handler import Handler
                   
app = Flask(__name__)

active = Markup("class='active'")
dbUrl = "store.db3"
accountHandler = AccountHander(dbUrl)
handler = Handler(dbUrl)

#-----------------------------------HomePage-----------------------------------
@app.route('/')
def homePage():
    data = {"title": "Home",
            "Home": active,
            }
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if account:
        data["userName"] = "Hello " + account.userName
        data["hasLogIn"] = True
    return render_template("Index.html", **data)
    
#------------------------------------Log In Out--------------------------------
@app.route('/LogIn', methods=["GET", "POST"])
def logIn():
    if request.method == "GET":
        data = {"title": "LogIn",
                "LogIn": active,
                }
        return render_template("LogIn.html", **data)
    elif request.method == "POST":
        accountName = request.form["account"]
        password = request.form["password"]
        sessionId = request.form["account"]
        account = accountHandler.hasTheAccount(accountName, password)
        if account:
            sessionId = accountHandler.insertSession(account)
            resp = make_response(redirect(url_for('homePage')))
            resp.set_cookie('sessionId', sessionId)
            return resp
        else:
            data = {"title": "LogIn",
                    "LogIn": active,
                    "wrong": "Account or Password are wrong !!",
                    }
            return render_template("LogIn.html", **data)
            
@app.route('/LogOut')
def logOut():
    accountHandler.deleteSession(request.cookies.get('sessionId'))
    return redirect(url_for('homePage'))
    
#---------------------------------Register--------------------------------------
@app.route('/Register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        data = {"title": "Register",
                "Register": active,
                }
        return render_template("Register.html", **data)
    elif request.method == "POST":
        accountName = request.form["accountName"]
        password = request.form["password"]
        userName = request.form["userName"]
        phone = "%s" % request.form["phone"]
        address = request.form["address"]
        e_mail = request.form["e_mail"]
        account = accountHandler.insertAccount(accountName, 
                                               password, userName, 
                                               phone, address, e_mail)
        sessionId = accountHandler.insertSession(account)
        resp = make_response(redirect(url_for('homePage')))
        resp.set_cookie('sessionId', sessionId)
        return resp
        
#----------------------------------Order---------------------------------------
@app.route('/Order')
def order():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    orderList = handler.selectAllOrder()
    print orderList
    data = {"title": "Order",
            "Order": active,
            "hasLogIn": True,
            "userName": "Hello " + account.userName,
            "orderList": orderList,
             }
    return render_template("Order.html", **data)
    
#####---------------------------------add--------------------------------------
@app.route('/Order/AddOrder', methods=["GET", "POST"])
def addOrder():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    memberList = handler.selectAllMember()
    productList = handler.selectAllProduct()
    if request.method == "GET":
        data = {"title": "AddOrder",
                "Order": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "memberList": memberList,
                "productList": productList,
                }
        return render_template("AddOrder.html", **data)
    elif request.method == "POST":
        M_ID = int(request.form['M_ID'])
        P_ID = int(request.form['P_ID'])
        R_Date = request.form['R_Date']
        D_Date = request.form['D_Date']
        total = int(request.form['total'])
        I_No = request.form['I_No']
        handler.insertOrder(M_ID, P_ID, R_Date, D_Date, total, I_No)
        return redirect(url_for('order'))
        
#----------------------------------Member---------------------------------------
@app.route('/Member')
def member():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    memberList = handler.selectAllMember()
    
    data = {"title": "Member",
            "Member": active,
            "hasLogIn": True,
            "userName": "Hello " + account.userName,
            "memberList": memberList,
             }
    return render_template("Member.html", **data)
#####---------------------------------add--------------------------------------
@app.route('/Member/AddMember', methods=["GET", "POST"])
def addMember():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if request.method == "GET":
        data = {"title": "AddMember",
                "Order": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                }
        return render_template("AddMember.html", **data)
    elif request.method == "POST":
        name = request.form['name']
        country = request.form['country']
        city = request.form['city']
        zip_code = request.form['zip_code']
        road = request.form['road']
        phone = request.form['phone']
        e_mail = request.form['e_mail']
        handler.insertMember(name, country, city, zip_code, road, phone, e_mail)
        return redirect(url_for('member'))
    
#----------------------------------Product---------------------------------------
@app.route('/Product')
def product():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    productList = handler.selectAllProduct()
    
    data = {"title": "Product",
            "Product": active,
            "hasLogIn": True,
            "userName": "Hello " + account.userName,
            "productList": productList,
             }
    return render_template("Product.html", **data)
    
#####---------------------------------add--------------------------------------
@app.route('/Product/AddProduct', methods=["GET", "POST"])
def addProduct():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    supplierList = handler.selectAllSupplier()
    if request.method == "GET":
        data = {"title": "AddProduct",
                "Order": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                "supplierList": supplierList,
                }
        return render_template("AddProduct.html", **data)
    elif request.method == "POST":
        S_ID = int(request.form['S_ID'])
        name = request.form['name']
        type = request.form['type']
        cost = int(request.form['cost'])
        price = int(request.form['price'])
        handler.insertProduct(S_ID, name, type, cost, price)
        return redirect(url_for('product'))
    
#----------------------------------Supplier---------------------------------------
@app.route('/Supplier')
def supplier():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    supplierList = handler.selectAllSupplier()
    
    data = {"title": "Supplier",
            "Supplier": active,
            "hasLogIn": True,
            "userName": "Hello " + account.userName,
            "supplierList":  supplierList,
             }
    return render_template("Supplier.html", **data)
#####---------------------------------add--------------------------------------
@app.route('/Supplier/AddSupplier', methods=["GET", "POST"])
def addSupplier():
    account = accountHandler.getAccountDataBySessionId(
                request.cookies.get('sessionId'))
    if request.method == "GET":
        data = {"title": "AddSupplier",
                "Order": active,
                "hasLogIn": True,
                "userName": "Hello " + account.userName,
                }
        return render_template("AddSupplier.html", **data)
    elif request.method == "POST":
        name = request.form['name']
        country = request.form['country']
        city = request.form['city']
        zip_code = request.form['zip_code']
        road = request.form['road']
        phone = request.form['phone']
        handler.insertSupplier(name, country, city, zip_code, road, phone)
        return redirect(url_for('supplier'))

    
#-------------------------------------MAIN-------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
