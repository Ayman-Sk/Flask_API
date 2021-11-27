from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from user import User

client = MongoClient("mongodb+srv://ayman:0936309172@chatapp.c6zmq.mongodb.net/ChatDB?retryWrites=true&w=majority",
                     connect=False)

chat_db = client.get_database("ChatDB")
users_collection = chat_db.get_collection("uses")


def add_user(username, password, phone_number, image, is_doctor):
    password_hash = generate_password_hash(password)
    users_collection.insert_one({
        'name': username,
        'password': password_hash,
        '_phone': phone_number,
        'image': image,
        'is_doctor': is_doctor
    })


def get_user(phone_number):
    user_data = users_collection.find_one({'_phone': phone_number})
    return User(user_data['name'], user_data['password'], user_data['_phone'], user_data['image'],
                user_data['is_doctor']) if user_data else None


def is_doctor(phone_number):
    user_data = users_collection.find_one({'_phone': phone_number})
    return True if user_data['is_doctor'] else False


def get_all_doctor():
    doctors = users_collection.find({'is_doctor': True})
    return doctors


# def check_user_by_number(phone_number): user_data = users_collection.find_one({'_phone': phone_number}) return
# User(user_data['_id'], user_data['password'], user_data['_phone'], user_data['image']) if user_data else None


def change_password(phone_number, new_password):
    password_hash = generate_password_hash(new_password)
    filter = {'_phone': phone_number}
    new_value = {"$set": {'password': password_hash}}
    users_collection.update_one(filter, new_value)


def update_user_info(username, phone_number, image):
    filter = {'_phone': phone_number}
    new_value = {"$set": {'name': username, 'image': image}}
    users_collection.update_one(filter, new_value)

# add_user("Ayman", "123456", "+963936309172")
# add_user("Ayham", "654321", "+963956802677")
# add_user("Youssef", "0258", "+963931812177")


# add_user("Youssef_MO", "12345", "+963931812177", "", True)
# add_user("Mohammed", "456", "+963999999999", "", True)
