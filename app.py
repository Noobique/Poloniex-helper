from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql, time, json


app = Flask(__name__)
app.config.from_object('config')
app.config['SERVER_NAME'] = 'example.com'

db = SQLAlchemy(app)

from models import Ticker, RawData
