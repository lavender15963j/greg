import sqlite3

from Order import Order
from Member import Member
from Product import Product
from Supplier import Supplier

class Handler(object):
    def __init__(self, dataUrl):
        self.dbName = dataUrl
        
    def selectAllOrder(self):
        conn = sqlite3.connect(self.dbName)
        orderCursor = conn.cursor()
        
        orderData = orderCursor.execute(
            "select * from 'order' t1, 'member' t2, 'product' t3, 'supplier' t4 where t1.'Member ID' = t2.ID "
            "and t1.'Product ID' = t3.ID and t3.'Supplier ID' = t4.ID order by t1.'Request Date' DESC"
        ).fetchall()
        
        print orderData
        
        orderList = []
        for od in orderData:
            member = Member(od[7], od[8], od[9], od[10], od[11], od[12], od[13], od[14])
            supplier = Supplier(od[21], od[22], od[23], od[24],od[25],od[26],od[27])
            product = Product(od[15], od[16], od[17], od[18], od[19], supplier)
            order = Order(od[0], member, product, od[3], od[4], od[5], od[6])
            orderList.append(order)
        
        orderCursor.close()
        conn.close()
        return orderList
        
    def selectAllMember(self):
        conn = sqlite3.connect(self.dbName)
        memberCursor = conn.cursor()
        
        memberData = memberCursor.execute(
            "select * from 'member'"
        ).fetchall()
        
        print memberData
        
        memberList = []
        for m in memberData:
            member =Member(m[0], m[1], m[2], m[3], m[4], m[5], m[6],m[7])
            memberList.append(member)
        
        memberCursor.close()
        conn.close()
        return memberList
        
    def selectAllProduct(self):
        conn = sqlite3.connect(self.dbName)
        productCursor = conn.cursor()
        
        productData = productCursor.execute(
            "select * from 'product' t1, 'supplier' t2 where t1.'Supplier ID' = t2.ID"
        ).fetchall()
        
        print productData
        
        productList = []
        for p in productData:
            supplier = Supplier(p[6], p[7], p[8], p[9], p[10], p[11], p[12])
            product = Product(p[0], p[1], p[2], p[3], p[4], supplier)
            productList.append(product)
        
        productCursor.close()
        conn.close()
        return productList
        
    def selectAllSupplier(self):
        conn = sqlite3.connect(self.dbName)
        supplierCursor = conn.cursor()
        
        supplierData = supplierCursor.execute(
            "select * from 'member'"
        ).fetchall()
        
        print supplierData
        
        supplierList = []
        for s in supplierData:
            supplier = Supplier(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
            supplierList.append(supplier)
        
        supplierCursor.close()
        conn.close()
        return supplierList
        
    def insertOrder(self, M_ID, P_ID, R_Date, D_Date, total, I_No):
        conn = sqlite3.connect(self.dbName)
        orderCursor = conn.cursor()
        
        orderCursor.execute(
            "insert into 'order' values(Null, %d, %d, '%s', '%s', %d, '%s')" % (M_ID, P_ID, R_Date, D_Date, total, I_No)
        )
        
        conn.commit()
        orderCursor.close()
        conn.close()