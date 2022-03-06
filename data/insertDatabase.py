import mysql.connector
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()
dbpassword=os.getenv('db_connectpass')

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password=dbpassword,
    database="TaipeiAttractions"
)


with open ("data/taipei-attractions.json") as file:
    data=dict(json.load(file))
    for y in range(len(data["result"]["results"])):
        id=data["result"]["results"][y]["_id"]
        name=data["result"]["results"][y]["stitle"]
        category=data["result"]["results"][y]["CAT2"]
        description=data["result"]["results"][y]["xbody"]
        address=data["result"]["results"][y]["address"]
        transport=data["result"]["results"][y]["info"]
        mrt=data["result"]["results"][y]["MRT"]
        latitude=data["result"]["results"][y]["latitude"]
        longitude=data["result"]["results"][y]["longitude"]
        images=data["result"]["results"][y]["file"]
        image = str(re.findall(r"(?:http\:|https\:)?\/\/.*\.(?:JPG|jpg)",images))
        mycursor=mydb.cursor()
        sql="replace into `attractions` (id, name, category, description, address, transport, mrt, latitude, longitude, image) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val=(id,name,category,description,address,transport,mrt,latitude,longitude,image)
        mycursor.execute(sql,val)
        mydb.commit()
        

