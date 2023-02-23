import hashlib
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




