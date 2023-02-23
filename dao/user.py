from dao.model.user import User
from implemented import auth_service

class UserDAO:

    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(User).all()

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def create(self, data):
        new_user = User(**data)
        new_user['password'] = auth_service.get_hash(new_user['password'])
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def update(self, user):
        self.session.add(user)
        self.session.commit()

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

