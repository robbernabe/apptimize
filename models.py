import datetime
from sqlalchemy import schema
from sqlalchemy import types
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

def now():
    return datetime.datetime.now()

class Networks(Base):
    __tablename__ = 'apptimized_networks'

    id = schema.Column(types.Integer, primary_key=True)
    bssid = schema.Column(types.String)
    ssid = schema.Column(types.String)
    date_added = schema.Column(types.DateTime, default=now)
    enabled = schema.Column(types.Boolean)

class Applications(Base):
    __tablename__ = 'apptimized_applications'

    id = schema.Column(types.Integer, primary_key=True)
    name = schema.Column(types.String)
    ssid = schema.Column(types.String)
    date_added = schema.Column(types.DateTime, default=now)
    enabled = schema.Column(types.Boolean)
