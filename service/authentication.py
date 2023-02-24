import datetime
import calendar
import jwt
from flask import  abort
from config import Config

from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):

        user = self.user_service.get_by_name(username)

        if user is None:
            raise abort(404)

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                abort(400)

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

        return tokens

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=Config.SECRET_HERE, algorithms=Config.ALGO)
        username = data.get('username')

        return self.generate_tokens(username, None, is_refresh=True)
