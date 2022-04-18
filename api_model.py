from flask import *
import jwt
import mysql.connector
from mysql.connector import pooling
from connectionPool import mydb
import re
from werkzeug.exceptions import HTTPException
import random
import requests


# 獲取訂單資料
def getorder(ordernumber,email):
    try:
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        sql=('select `orderId`,`cost`,`time`,`date`,`phone`,`paystatus`,`attractionId`,`order`.`email`,`member`.`name`,`attractions`.`name`,`address`,`image` from `order`,`attractions`,`member` where order.orderId = %s and `order`.`email`=%s and `order`.`attractionId`=`attractions`.`id`')
        values=(ordernumber,email)
        mycursor.execute(sql,values)
        myresult=mycursor.fetchone()
        return myresult
    except:
        return "error"
    finally:
        myconnect.close()

# 加入訂單資料，刪除購物車
def addorder(attractionId,date,time,cost,email,ordernumber,usernumber):
    try:
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        ordersql="insert into `order` (`attractionId`,`date`,`time`,`cost`,`email`,`orderId`,`phone`,`paystatus`) values (%s,%s,%s,%s,%s,%s,%s,%s) "
        ordervalues=(attractionId,date,time,cost,email,ordernumber,usernumber,1)
        mycursor.execute(ordersql,ordervalues)
        cartsql="delete from `cart` where `email`=%s"
        cartvalues=(email,)
        mycursor.execute(cartsql,cartvalues)
        myconnect.commit()
        return "ok"
    except:
        return "error"
    finally:
        myconnect.close()

# 更新訂單付款資料
def updateOrder(ordernumber):
    try:
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        paysql="update `order` set `paystatus`=%s where orderId=%s"
        payvalues=(0,ordernumber)
        mycursor.execute(paysql,payvalues)
        myconnect.commit()
        return "ok"
    except:
        return "error"
    finally:
        myconnect.close()

# 取得預定購物車資料
def getCart(email):
    try:
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        sql="select `attractions`.`id`,`attractions`.`name`,`address`,`image`,`date`,`time`,`cost` from `cart`,`member`,`attractions` where `cart`.`email`=%s and `cart`.`attractionId`=`attractions`.`id`"
        values=(email,)
        mycursor.execute(sql,values)
        myresult=mycursor.fetchone()
        return myresult
    except:
        return "error"
    finally:
        myconnect.close()

# 檢查預定購物車資料
def checkCart(email):
    try:
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        sql="select `cart`.`cartId` from `cart` where email=%s"
        values=(email,)
        mycursor.execute(sql,values)
        myresult=mycursor.fetchall()
        return myresult
    except:
        return "error"
    finally:
        myconnect.close()

# 加入預定購物車資料
def addCart(attractionId,date,time,price,email):
    try:
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        sql="insert into `cart` (`attractionId`,`date`,`time`,`cost`,`email`) values (%s,%s,%s,%s,%s)"
        values=(attractionId,date,time,price,email)
        mycursor.execute(sql,values)
        myconnect.commit()
        return "ok"
    except:
        return "error"
    finally:
        myconnect.close()

# 更新預定購物車資料
def updateCart(attractionId,date,time,price,email):
    try:
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        sql="update `cart` set `attractionId`=%s,`date`=%s,`time`=%s,`cost`=%s,`email`=%s where `email`=%s"
        values=(attractionId,date,time,price,email,email)
        mycursor.execute(sql,values)
        myconnect.commit()
        return "ok"
    except:
        return "error"
    finally:
        myconnect.close()

# 刪除購物車資料
def deleteCart(email):
    try:
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        sql=('delete from `cart` where `email`=%s')
        values=(email,)
        mycursor.execute(sql,values)
        myconnect.commit()
        return "ok"
    except:
        return "error"
    finally:
        myconnect.close()

# 抓取登入資料
def getUser(email):
    try:
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        sql="select `id`,`name`,`email` from `member` where member.email=%s"
        values=(email,)
        mycursor.execute(sql,values)
        myresult=mycursor.fetchone()
        return myresult
    except:
        return "error"
    finally:
        myconnect.close()

# 確認使用者資料
def statusUser(email):
    try:
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        sql=('select email from `member` where member.email=%s')
        values=(email,)
        mycursor.execute(sql,values)
        myresult=mycursor.fetchone()
        return myresult
    except:
        return "error"
    finally:
        myconnect.close()

# 新增使用者資料
def addUser(name,email,password):
    try:
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        sql="insert into `member` (`name`,`email`,`password`) values (%s,%s,%s)"
        values=(name,email,password)
        mycursor.execute(sql,values)
        myconnect.commit()
        return "ok"
    except:
        return "error"
    finally:
        myconnect.close()

# 登入比對使用者資料
def loginUser(email,password):
    try:
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        sql="select `email`,`password` from `member` where member.email=%s and member.password=%s"
        values=(email,password)
        mycursor.execute(sql,values)
        myresult=mycursor.fetchone()
        return myresult
    except:
        return "error"
    finally:
        myconnect.close()