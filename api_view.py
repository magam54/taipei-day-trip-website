from flask import *
import jwt
import mysql.connector
from mysql.connector import pooling
from connectionPool import mydb
import re
from werkzeug.exceptions import HTTPException
import random
import requests


# 訂單資料呈現處理
def orderView(myresult):
    images=myresult[11]
    #圖片字串處理
    imageString=re.sub(r"[\'\[\]]","",images)
    image=list(filter(None,re.split(r".jpg|.JPG",imageString)))
    attractionlist={
        "id":myresult[6],
        "name":myresult[9],
        "address":myresult[10],
        "image":image[0]+".jpg"
    }
    triplist={
        "attraction":attractionlist,
        "date":myresult[3],
        "time":myresult[2]
    }
    contactlist={
        "name":myresult[8],
        "email":myresult[7],
        "phone":myresult[4]
    }
    orderlist={
        "number":myresult[0],
        "price":myresult[1],
        "trip":triplist,
        "contact":contactlist,
        "status":myresult[5]
    }
    return orderlist

# 付款資料呈現處理
def payView(ordernumber):
    orderResult={}
    orderResult['number']=ordernumber
    paystatus={}
    paystatus['status']=0
    paystatus['msg']="付款成功"
    orderResult['payment']=paystatus
    return orderResult

# 購物車資料呈現處理
def cartView(myresult):
    datalist={}
    attractionlist={}
    attractionlist['id']=myresult[0]
    attractionlist['name']=myresult[1]
    attractionlist['address']=myresult[2]
    images=myresult[3]
    imageString=re.sub(r"[\'\[\]]","",images)
    image=list(filter(None,re.split(r".jpg|.JPG",imageString)))
    attractionlist['image']=image[0]+".jpg"
    datalist['date']=myresult[4]
    datalist['time']=myresult[5]
    datalist['price']=myresult[6]
    datalist['attraction']=attractionlist
    return datalist

# 使用者資料呈現處理
def userView(myresult):
    datalist={}
    id=myresult[0]
    name=myresult[1]
    email=myresult[2]
    datalist['id']=id
    datalist['name']=name
    datalist['email']=email
    return datalist