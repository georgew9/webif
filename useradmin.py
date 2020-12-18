from flask_login import LoginManager,UserMixin

from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash

import json

USERS = [
    {
        "id": 1,
        "name": 'admin',
        "password": generate_password_hash('123456')
    },
    {
        "id": 2,
        "name": 'george',
        "password": generate_password_hash('gra320')
    }
]


class Loginm():

	#login_manager = None


	def create_user(user_name, password):
	    """创建一个用户"""
	    user = {
	        "name": user_name,
	        "password": generate_password_hash(password),
	        "id": uuid.uuid4()
	    }
	    USERS.append(user)

	def get_user(user_name):
	    """根据用户名获得用户记录"""
	    global USERS

	    for user in USERS:
	        if user.get("name") == user_name:
	            return user
	    return None

	def load_user():

		global USERS

		fu = open("/home/pi/ai/webif/users", "r")
		USERS=json.loads(fu.read())
		fu.close()


	def save_user():

		global USERS

		fu = open("/home/pi/ai/webif/users", "w")
		fu.write(json.dumps(USERS))
		fu.close()

	def chpass_user(user_name,password):
	    """根据用户名获得用户记录"""
	    global USERS

	    for user in USERS:
	        if user.get("name") == user_name:
	        	user['password']= generate_password_hash(password)
	        	print (password,user['password'])
	        	#self.save_user()
	        	return True
	    return False


class User(UserMixin):
    """用户类"""
    def __init__(self, user):
        self.username = user.get("name")
        self.password_hash = user.get("password")
        self.id = user.get("id")

    def verify_password(self, password):
        """密码验证"""
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """获取用户ID"""
        return self.id

    @staticmethod
    def get(user_id):
        """根据用户ID获取用户实体，为 login_user 方法提供支持"""
        global USERS
        if not user_id:
            return None
        for user in USERS:
            if user.get('id') == user_id:
                return User(user)
        return None