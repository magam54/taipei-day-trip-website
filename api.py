from flask import *
import jwt
import mysql.connector
import mysql.connector.pooling
from connectionPool import mydb
import re
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

api = Blueprint('api',__name__)
CORS(api)
key="myjwtsecret"


@api.errorhandler(500)
def handle_Internal_serverError(event):
    return jsonify (error=True,message="伺服器出錯啦！") , 500

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
        # myconnect.close()
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
        if not myresult:
            myconnect.close()
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
        if not myresult:
            mycursor=myconnect.cursor()
            sql="insert into `cart` (`attractionId`,`date`,`time`,`cost`,`email`) values (%s,%s,%s,%s,%s)"
            values=(attractionId,date,time,price,email)
            mycursor.execute(sql,values)
            myconnect.commit()
            myconnect.close()
            return jsonify(ok=True)
        if myresult:
            mycursor=myconnect.cursor()
            sql="update `cart` set `attractionId`=%s,`date`=%s,`time`=%s,`cost`=%s,`email`=%s where `email`=%s"
            values=(attractionId,date,time,price,email,email)
            mycursor.execute(sql,values)
            myconnect.commit()
            myconnect.close()
            return jsonify(ok=True)
        else:
            return jsonify(error=True,message="輸入錯誤")

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
        # print("第二個",myconnect)
        mycursor=myconnect.cursor()
        sql="select `id`,`name`,`email` from `member` where member.email=%s"
        values=(email,)
        mycursor.execute(sql,values)
        myresult=mycursor.fetchone()
        myconnect.close()
        # print("第二個",myconnect)
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
    name=request.json['name']
    email=request.json['email']
    password=request.json['password']
    myconnect=mydb.get_connection()
    mycursor=myconnect.cursor()
    sql=('select email from `member` where member.email=%s')
    values=(email,)
    mycursor.execute(sql,values)
    myresult=mycursor.fetchall()
    if not myresult:
        mycursor=myconnect.cursor()
        sql="insert into `member` (`name`,`email`,`password`) values (%s,%s,%s)"
        values=(name,email,password)
        mycursor.execute(sql,values)
        myconnect.commit()
        myconnect.close()
        return jsonify(ok=True)
    if myresult:
        return jsonify(error=True,message="電子郵件重複")
    if request.json==None:
        return jsonify(error=True,message="註冊失敗")

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
    if myresult==None:
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

