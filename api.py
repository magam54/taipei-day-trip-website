from flask import *
import mysql.connector
import mysql.connector.pooling
from connectionPool import mydb
import re
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

api = Blueprint('api',__name__)
CORS(api)

@api.errorhandler(500)
def handle_Internal_serverError(event):
    return jsonify (error=True,message="出錯啦！") , 500

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