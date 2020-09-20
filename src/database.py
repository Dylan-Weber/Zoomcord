from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/user_data.db"
db = SQLAlchemy(app)


class PairData(db.Model):
    pair_id = db.Column(db.String, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, unique=False)


class UserData(db.Model):
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    user_name = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    last_guild_id = db.Column(db.String, unique=False, nullable=False)
    last_channel_id = db.Column(db.Integer, unique=False, nullable=False)
    min_speed = db.Column(db.Float, unique=False, nullable=True)
    punishments = db.Column(db.String, unique=False, nullable=True)
    last_punishment = db.Column(db.TIMESTAMP, unique=False, nullable=True)
    last_update = db.Column(db.TIMESTAMP, unique=False, nullable=False)


def store_pair_data(pair_id, user_id):
    timestamp = datetime.datetime.now()
    db.session.merge(PairData(pair_id=pair_id, user_id=user_id, timestamp=timestamp))
    db.session.commit()


DEFAULT_MIN_SPEED = 0
DEFAULT_PUNISHMENTS = ""


def store_discord_data(user_id, user_name, guild_id, channel_id):
    timestamp = datetime.datetime.now()
    db.session.merge(UserData(user_id=user_id, user_name=user_name,
                              last_guild_id=guild_id, last_channel_id=channel_id,
                              last_update=timestamp))
    db.session.commit()


def store_settings_data(user_id, min_speed, punishments):
    timestamp = datetime.datetime.now()
    db.session.merge(UserData(user_id=user_id, min_speed=min_speed,
                              punishments=punishments, last_update=timestamp))
    db.session.commit()


MAXIMUM_PAIR_ID_AGE_IN_SECONDS = 5*60


def is_too_old(timestamp):
    now = datetime.datetime.now()
    maximum_age = datetime.timedelta(seconds=MAXIMUM_PAIR_ID_AGE_IN_SECONDS)
    return timestamp < now - maximum_age


def get_user_id_from_pair_id(pair_id):
    data = PairData.query.filter_by(pair_id=pair_id).first()
    if data is not None:
        if is_too_old(data.timestamp):
            delete_pair_data(data)
        else:
            return data.user_id
    return None


def get_pair_id_from_user_id(user_id):
    data = PairData.query.filter_by(user_id=user_id).first()
    if data is not None:
        if is_too_old(data.timestamp):
            delete_pair_data(data)
        else:
            return data.pair_id
    return None


def get_user_data(user_id):
    data = UserData.query.filter_by(user_id=user_id).first()
    if data is not None:
        return (data.user_id, data.user_name, data.last_guild_id,
                data.last_channel_id, data.min_speed, data.punishments, data.timestamp)
    else:
        return None


def delete_pair_data(pair_data):
    db.session.delete(pair_data)
    db.session.commit()
