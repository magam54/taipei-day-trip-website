from flask import *
import jwt
import mysql.connector
from mysql.connector import pooling
from connectionPool import mydb
from api_model import getorder,addorder,updateOrder,getCart,checkCart,addCart,updateCart,deleteCart,getUser,statusUser,addUser,loginUser
from api_view import orderView,payView,cartView,userView
import re
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
import random
import requests
import os
from dotenv import load_dotenv

load_dotenv()
partnerID=os.getenv('PartnerID')
APP_KEY=os.getenv('APP_KEY')

api = Blueprint('api',__name__)
CORS(api)
key="myjwtsecret"


@api.errorhandler(500)
def handle_Internal_serverError(event):
    return jsonify (error=True,message="伺服器出錯啦！") , 500

@api.route("/api/key", methods=["POST"])
def getkey():
    return jsonify(partnerID,APP_KEY)


@api.route("/api/order/<ordernumber>", methods=["GET"])
def getorderDetail(ordernumber):
    user = request.cookies.get('token')
    if user is None:
        return jsonify(error=True,message="請登入")
    if user!=None:
        decoded = jwt.decode(user, key, algorithms="HS256")
        email=decoded['email']
        myresult=getorder(ordernumber,email)
        if myresult == "error":
            return jsonify(data="error")
        elif myresult == None:
            return jsonify(data=None)
        else:
            detail_list=orderView(myresult)
            return jsonify(data=detail_list)


@api.route("/api/orders", methods=["POST"])
def sendorder():
    user = request.cookies.get('token')
    if user is None:
        return jsonify(error=True,message="請登入")
    if user!=None:
        decoded = jwt.decode(user, key, algorithms="HS256")
        email=decoded['email']
        # 製作訂單號碼
        number=random.randint(100,999)
        attractionId=request.json['order']['trip']['id']
        usernumber=request.json['contact']['number']
        ordernumber=str(attractionId)+str(usernumber)+str(number)
        # 紀錄訂單資料
        date=request.json['order']['date']
        time=request.json['order']['time']
        cost=request.json['order']['price']
        result=addorder(attractionId,date,time,cost,email,ordernumber,usernumber)
        if result=="ok":
        # 進入付款程序
            payurl='https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
            payheaders={'Content-Type':'application/json','x-api-key':'partner_1ZGwfsVIBrUrUlqPl6D7MNJtlUAiW583BU7XdIH5udIH7kodFBmk0C7r'}
            paybody={
            "prime":request.json['prime'],
            "partner_key":'partner_1ZGwfsVIBrUrUlqPl6D7MNJtlUAiW583BU7XdIH5udIH7kodFBmk0C7r',
            "merchant_id": "magam54_TAISHIN",
            "details":ordernumber,
            "amount":request.json['order']['price'],
            "cardholder": {
            "phone_number":usernumber,
            "name":request.json['contact']['name'],
            "email":request.json['contact']['email']}
            }
            response=requests.post(payurl,json=paybody,headers=payheaders,timeout=90)
            payres=response.json()
            if payres['status'] == 0:
                payresult=updateOrder(ordernumber)
                orderResult=payView(ordernumber)
                return jsonify(data=orderResult)
            else:
                return jsonify(error=True,message="資料有誤，未付款")
        elif result == "error":
            return jsonify(data="error")


# 預定功能
@api.route("/api/booking", methods=["GET"])
def getbooking():
    user = request.cookies.get('token')
    if user is None:
        return jsonify(error=True,message="請登入")
    if user!=None:
        decoded = jwt.decode(user, key, algorithms="HS256")
        email=decoded['email']
        myresult=getCart(email)
        if myresult:
            datalist=cartView(myresult)
            return jsonify (data=datalist)
        else:
            return jsonify(data=None)

@api.route("/api/booking", methods=["POST"])
def newbooking():
    user = request.cookies.get('token')
    if user is None:
        return jsonify(error=True,message="請登入")
    if user!=None:
        decoded = jwt.decode(user, key, algorithms="HS256")
        email=decoded['email']
        attractionId=request.json['attractionId']
        date=request.json['date']
        time=request.json['tourtime']
        price=request.json['price']
        myresult=checkCart(email)
        if not myresult:
            addCart(attractionId,date,time,price,email)
            return jsonify(ok=True)
        else:
            updateCart(attractionId,date,time,price,email)
            return jsonify(ok=True)


@api.route("/api/booking", methods=["DELETE"])
def deletebooking():
    user = request.cookies.get('token')
    if user is None:
        return jsonify(error=True,message="請登入")
    if user!=None:
        decoded = jwt.decode(user, key, algorithms="HS256")
        email=decoded['email']
        deleteCart(email)
        return jsonify(ok=True)


# 取得當前使用者登入資訊
@api.route("/api/user", methods=["GET"])
def getuser():
    user = request.cookies.get('token')
    if user is None:
        return jsonify(data=None)
    if user!=None:
        decoded = jwt.decode(user, key, algorithms="HS256")
        email=decoded['email']
        myresult=getUser(email)
        datalist=userView(myresult)
        return jsonify(data=datalist)

# 註冊新使用者
@api.route("/api/user", methods=["POST"])
def register():
    if request.json==None:
        return jsonify(error=True,message="註冊失敗")
    else:
        name=request.json['name']
        email=request.json['email']
        password=request.json['password']
        myresult=statusUser(email)
        if not myresult:
            addUser(name,email,password)
            return jsonify(ok=True)
        else:
            return jsonify(error=True,message="電子郵件重複")

# 直接insert不用select? mysql設定unique 有error 加 rollback


# 登入使用者帳戶
@api.route("/api/user", methods=["PATCH"])
def login():
    email=request.json['email']
    password=request.json['password']
    myresult=loginUser(email,password)
    if myresult:
        encoded = jwt.encode({"email": email}, key, algorithm="HS256")
        res = make_response(jsonify(ok=True))
        res.set_cookie(key='token',value=encoded,samesite='None',secure=True)
        return res
    else:
        return jsonify(error=True,message="帳號或密碼錯誤")
        
# 登出
@api.route("/api/user", methods=["DELETE"])
def logout():
    res=make_response(jsonify(ok=True))
    res.delete_cookie('token')
    return res


@api.route("/api/attractions", methods=["GET"])
def getAttractions():
    page=request.args.get("page",type=int,default=0)
    keyword=request.args.get("keyword",default="")
    myconnect=mydb.get_connection()
    mycursor=myconnect.cursor()
    sql=("select `id`,`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`image` from `attractions` where attractions.name like %s order by `id` ASC limit %s,%s")
    values=(("%"+keyword+"%"),12*page,13)
    mycursor.execute(sql,values)
    myresult=mycursor.fetchall()
    myconnect.close()
    #資料庫資料處理
    if len(myresult) == 13 :
        nextPage=page+1
    else:
        nextPage=None
    n=0
    mylist=[]
    while n < len(myresult) and n < 12 : 
        mydict={}
        mydict["id"]=myresult[n][0]
        mydict["name"]=myresult[n][1]
        mydict["category"]=myresult[n][2]
        mydict["description"]=myresult[n][3]
        mydict["address"]=myresult[n][4]
        mydict["transport"]=myresult[n][5]
        mydict["mrt"]=myresult[n][6]
        mydict["latitude"]=myresult[n][7]
        mydict["longitude"]=myresult[n][8]
        images=myresult[n][9]
        imageString=re.sub(r"[\'\[\]]","",images)
        image=list(filter(None,re.split(r".jpg|.JPG",imageString)))
        imagelist=[]
        for i in image:
            i += ".jpg"
            imagelist.append(i)
        mydict["images"]=imagelist
        mylist.append(mydict)
        n = n+1
    headlist={}
    headlist["nextPage"]=nextPage
    headlist["data"]=mylist
    return jsonify (headlist)

@api.route("/api/attractions/<attractionId>", methods=["GET"])
def getAttractionsID(attractionId):
    myconnect=mydb.get_connection()
    mycursor=myconnect.cursor()
    sql=('select `id`,`name`,`category`,`description`,`address`,`transport`,`mrt`,`latitude`,`longitude`,`image` from `attractions` where attractions.id = %s')
    values=(attractionId,)
    mycursor.execute(sql,values)
    myresult=mycursor.fetchone()
    myconnect.close()
    #圖片字串處理
    if myresult == None:
        return jsonify(error=True,message="沒有這個景點唷")
    else:
        images=myresult[9]
        imageString=re.sub(r"[\'\[\]]","",images)
        image=list(filter(None,re.split(r".jpg|.JPG",imageString)))
        imagelist=[]
        for i in image:
            i += ".jpg"
            imagelist.append(i)
        mydict={
            "id":myresult[0],
            "name":myresult[1],
            "category":myresult[2],
            "description":myresult[3],
            "address":myresult[4],
            "transport":myresult[5],
            "mrt":myresult[6],
            "latitude":myresult[7],
            "longitude":myresult[8],
            "image":imagelist}
        headlist={}
        headlist["data"]=mydict
        return jsonify(headlist)

