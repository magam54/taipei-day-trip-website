import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()
dbpassword=os.getenv('db_connectpass')

mydb = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,
    pool_reset_session=True,
    host="127.0.0.1",
    user="root",
    password=dbpassword,
    database="TaipeiAttractions"
)