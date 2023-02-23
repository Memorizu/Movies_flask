import datetime
import calendar
import hashlib

import jwt
from flask import request, abort

from config import Config
from dao.authentication import AuthDAO
from dao.model.user import User


class AuthService:
    def __init__(self, dao: AuthDAO):
        self.dao = dao

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            Config.PWD_HASH_SALT,
            Config.PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    def auth_required(self, func):
        def wrapper(*args, **kvargs):
            pass

    def create(self, req_json):
        username = req_json.get('username', None)
        password = req_json.get('password', None)
        print(username)
        print(password)
        if None in [username, password]:
            abort(401)

        user = self.dao.session.query(User).filter(User.username == username)
        print(user)
        if user is None:
            abort(401)

        hash_password = self.get_hash(password)
        # print(hash_password)
        if hash_password != user.password:
            abort(401)

        data = {
            "username": user.username,
            "role": user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, Config.SECRET_HERE, algorithm='HS256')
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, Config.SECRET_HERE, algorithm='HS256')
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return self.dao.create(tokens)

    def update(self):
        req_json = request.json
        refresh_token = req_json.get('refresh_token', None)

        if None in refresh_token:
            abort(400)

        try:
            data = jwt.decode(jwt=refresh_token, key=Config.SECRET_HERE, algorithms=Config.ALGO)
        except Exception:
            abort(400)

        username = data.get('username')

        user = self.dao.session.query(User).filter(User.username == username)

        data = {
            "username": user.username,
            "role": user.role
        }
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, Config.SECRET_HERE, algorithm=Config.ALGO)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, Config.SECRET_HERE, algorithm=Config.ALGO)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return self.dao.update(tokens)
