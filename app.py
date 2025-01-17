from flask import *
from api_controller import api
import mysql.connector
from mysql.connector import pooling
import jwt
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
import requests

app=Flask(__name__, static_folder='static')
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False
app.register_blueprint(api)
CORS(app)

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.run(host="0.0.0.0",port=3000,debug=True)