import json

x = {'username': 'Ayman Mtn', 'room': '+963936309172', 'message': '{"sender":{"id":0,"name":"Ayman Mtn",'
                                                                  '"phoneNumber":"+963968148943","imageUrl":""},'
                                                                  '"time":"03:11 AM","text":"هاي","isRead":true,'
                                                                  '"isLiked":false,"isImage":false}'}
y = {1: {'name': 'John', 'age': '27', 'sex': 'Male'},
     2: {'name': 'Marie', 'age': '22', 'sex': 'Female'}}

z=json.loads(x['message'])
print(z['text'])
print('أيمن')
