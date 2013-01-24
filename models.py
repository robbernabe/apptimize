import datetime
from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship
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
    application = relationship('Applications')

    def __init__(self, bssid, ssid, date_added, enabled):
        self.bssid = bssid
        self.ssid = ssid
        self.date_added = date_added
        self.enabled = enabled


class Applications(Base):
    __tablename__ = 'apptimized_applications'

    id = schema.Column(types.Integer, primary_key=True)
    name = schema.Column(types.String)
    path = schema.Column(types.String)
    date_added = schema.Column(types.DateTime, default=now)
    enabled = schema.Column(types.Boolean)
    network_id = schema.Column(types.Integer, ForeignKey('apptimized_networks.id'))

    def __init__(self, name, path, date_added, enabled):
        self.name = name
        self.path = path
        self.date_added = date_added
        self.enabled = enabled
