import mysql.connector
import mysql.connector.pooling
import os
from dotenv import load_dotenv

load_dotenv()
dbpassword=os.getenv('db_connectpass')

mydb = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,
    host="127.0.0.1",
    user="root",
    password=dbpassword,
    database="TaipeiAttractions"
)