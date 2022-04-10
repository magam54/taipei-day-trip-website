from flask import *
import jwt
import mysql.connector
from mysql.connector import pooling
from connectionPool import mydb
import re
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
import random
import requests

api = Blueprint('api',__name__)
CORS(api)
key="myjwtsecret"


@api.errorhandler(500)
def handle_Internal_serverError(event):
    return jsonify (error=True,message="伺服器出錯啦！") , 500

@api.route("/api/order/<ordernumber>", methods=["GET"])
def getorder(ordernumber):
    user = request.cookies.get('token')
    if user is None:
        return jsonify(error=True,message="請登入")
    if user!=None:
        decoded = jwt.decode(user, key, algorithms="HS256")
        email=decoded['email']
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        sql=('select `orderId`,`cost`,`time`,`date`,`phone`,`paystatus`,`attractionId`,`order`.`email`,`member`.`name`,`attractions`.`name`,`address`,`image` from `order`,`attractions`,`member` where order.orderId = %s and `order`.`email`=%s')
        values=(ordernumber,email)
        mycursor.execute(sql,values)
        myresult=mycursor.fetchone()
        myconnect.close()
        if myresult == None:
            return jsonify(data=None)
        else:
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
            return jsonify(data=orderlist)

@api.route("/api/orders", methods=["POST"])
def sendorder():
    user = request.cookies.get('token')
    if user is None:
        return jsonify(error=True,message="請登入")
    if user!=None:
        decoded = jwt.decode(user, key, algorithms="HS256")
        email=decoded['email']
        # 製作訂單號碼
        orderResult={}
        number=random.randint(100,999)
        attractionId=request.json['order']['trip']['id']
        usernumber=request.json['contact']['number']
        ordernumber=str(attractionId)+str(usernumber)+str(number)
        orderResult['number']=ordernumber
        # 記錄訂單狀態
        date=request.json['order']['date']
        time=request.json['order']['time']
        cost=request.json['order']['price']
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        ordersql="insert into `order` (`attractionId`,`date`,`time`,`cost`,`email`,`orderId`,`phone`,`paystatus`) values (%s,%s,%s,%s,%s,%s,%s,%s) "
        ordervalues=(attractionId,date,time,cost,email,ordernumber,usernumber,1)
        mycursor.execute(ordersql,ordervalues)
        cartsql="delete from `cart` where `email`=%s"
        cartvalues=(email,)
        mycursor.execute(cartsql,cartvalues)
        myconnect.commit()
        myconnect.close()
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
            myconnect=mydb.get_connection()
            mycursor=myconnect.cursor()
            paysql="update `order` set `paystatus`=%s where orderId=%s"
            payvalues=(0,ordernumber)
            mycursor.execute(paysql,payvalues)
            myconnect.commit()
            myconnect.close()
            paystatus={}
            paystatus['status']=0
            paystatus['msg']="付款成功"
            orderResult['payment']=paystatus
            return jsonify(data=orderResult)
        else:
            return jsonify(error=True,message="資料有誤，未付款")


# 預定功能
@api.route("/api/booking", methods=["GET"])
def getbooking():
    user = request.cookies.get('token')
    if user is None:
        return jsonify(error=True,message="請登入")
    if user!=None:
        decoded = jwt.decode(user, key, algorithms="HS256")
        email=decoded['email']
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        sql="select `attractions`.`id`,`attractions`.`name`,`address`,`image`,`date`,`time`,`cost` from `cart`,`member`,`attractions` where `cart`.`email`=%s and `cart`.`attractionId`=`attractions`.`id`"
        values=(email,)
        mycursor.execute(sql,values)
        myresult=mycursor.fetchone()
        myconnect.close()
        if myresult:
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
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        sql="select `cart`.`cartId` from `cart` where email=%s"
        values=(email,)
        mycursor.execute(sql,values)
        myresult=mycursor.fetchall()
        myconnect.close()
        if not myresult:
            myconnect=mydb.get_connection()
            mycursor=myconnect.cursor()
            sql="insert into `cart` (`attractionId`,`date`,`time`,`cost`,`email`) values (%s,%s,%s,%s,%s)"
            values=(attractionId,date,time,price,email)
            mycursor.execute(sql,values)
            myconnect.commit()
            myconnect.close()
            return jsonify(ok=True)
        else:
            myconnect=mydb.get_connection()
            mycursor=myconnect.cursor()
            sql="update `cart` set `attractionId`=%s,`date`=%s,`time`=%s,`cost`=%s,`email`=%s where `email`=%s"
            values=(attractionId,date,time,price,email,email)
            mycursor.execute(sql,values)
            myconnect.commit()
            myconnect.close()
            return jsonify(ok=True)


@api.route("/api/booking", methods=["DELETE"])
def deletebooking():
    user = request.cookies.get('token')
    if user is None:
        return jsonify(error=True,message="請登入")
    if user!=None:
        decoded = jwt.decode(user, key, algorithms="HS256")
        email=decoded['email']
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        sql=('delete from `cart` where `email`=%s')
        values=(email,)
        mycursor.execute(sql,values)
        myconnect.commit()
        myconnect.close()
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
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        sql="select `id`,`name`,`email` from `member` where member.email=%s"
        values=(email,)
        mycursor.execute(sql,values)
        myresult=mycursor.fetchone()
        myconnect.close()
        datalist={}
        id=myresult[0]
        name=myresult[1]
        email=myresult[2]
        datalist['id']=id
        datalist['name']=name
        datalist['email']=email
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
        myconnect=mydb.get_connection()
        mycursor=myconnect.cursor()
        sql=('select email from `member` where member.email=%s')
        values=(email,)
        mycursor.execute(sql,values)
        myresult=mycursor.fetchone()
        myconnect.close()
        if not myresult:
            myconnect=mydb.get_connection()
            mycursor=myconnect.cursor()
            sql="insert into `member` (`name`,`email`,`password`) values (%s,%s,%s)"
            values=(name,email,password)
            mycursor.execute(sql,values)
            myconnect.commit()
            myconnect.close()
            return jsonify(ok=True)
        else:
            return jsonify(error=True,message="電子郵件重複")
# 直接insert不用select? mysql設定unique 有error 加 rollback


# 登入使用者帳戶
@api.route("/api/user", methods=["PATCH"])
def login():
    email=request.json['email']
    password=request.json['password']
    myconnect=mydb.get_connection()
    mycursor=myconnect.cursor()
    sql="select `email`,`password` from `member` where member.email=%s and member.password=%s"
    values=(email,password)
    mycursor.execute(sql,values)
    myresult=mycursor.fetchone()
    myconnect.close()
    if myresult:
        encoded = jwt.encode({"email": email}, key, algorithm="HS256")
        res = make_response(jsonify(ok=True))
        res.set_cookie(key='token',value=encoded)
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

