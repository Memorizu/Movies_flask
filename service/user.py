import base64
import hashlib
import hmac

from config import Config
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def create(self, data):
        data['password'] = self.generate_password(data['password'])
        return self.dao.create(data)

    def update(self, data):
        uid = self.dao.get_one(data.get('id'))
        user = self.dao.get_one(uid)
        user.password = data.get('password')
        user.username = data.get('username')
        user.role = data.get('role')
        return self.dao.update(user)

    def update_partial(self, data):
        uid = self.dao.get_one(data.get('id'))
        user = self.dao.get_one(uid)
        if 'username' in data:
            user.username = data.get('username')
        if 'password' in data:
            user.password = data.get('password')
        if 'role' in data:
            user.role = data.get('role')

        return self.dao.update(user)

    def delete(self, uid):
        return self.dao.delete(uid)

    def get_by_name(self, data):
        return self.dao.get_by_name(data)

    def generate_password(self, password):
        hash_password = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            Config.PWD_HASH_SALT,
            Config.PWD_HASH_ITERATIONS
        )

        return base64.b64encode(hash_password)

    def compare_passwords(self, password_hash, password):
        decode_password = base64.b64decode(password_hash)

        hash_password = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            Config.PWD_HASH_SALT,
            Config.PWD_HASH_ITERATIONS
        )

        return hmac.compare_digest(decode_password, hash_password)
