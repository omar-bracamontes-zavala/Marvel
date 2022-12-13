import uuid
from db import mongo
from hashlib import md5
from auth import generate

def signin(request):
    name = request.args.get('name', None)
    age = request.args.get('age', None)
    password = request.args.get('pw', None)
    confirmation_password = request.args.get('cpw', None)

    if not name or not age or not password or not confirmation_password:
        return None, ('Missing data', 400)

    if not password==confirmation_password:
        return None, ('Invalid data', 400)

    mongo.Users.insert_one({'id':str(uuid.uuid4()), 'name':name, 'age':age, 'password': md5(password.encode()).hexdigest()})

    return 'User successfully created! Log In', None

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("Missing credentials", 401)

    # check db for user and password
    user = mongo.Users.find_one({'name':auth.username})
    if user:
        name = user['name']
        password = user['password']

        if auth.username!=name or md5(auth.password.encode()).hexdigest()!=password:
            return None, ('Invalid credentials', 401)
        else:
            id = user['id']
            age = user['age']
            return generate.token(user['id'],auth.username,age = user['age']), None
    else:
        return None, ('Invalid credentials', 401)