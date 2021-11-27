from werkzeug.security import check_password_hash
import json


class User:
    def __init__(self, username, password, phone_number, image, is_doctor):
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.image = image
        self.is_doctor = is_doctor

    @staticmethod
    def is_authenticated(self):
        return True

    @staticmethod
    def is_active(self):
        return True

    @staticmethod
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
