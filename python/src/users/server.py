import uuid
from hashlib import md5
from auth import validate
from auth_svc import access
from flask import Flask, request
from db import mongo

server = Flask(__name__)

@server.route('/signin', methods=['POST'])
def signin():
    '''
    Post request parameters:
        {
            'name': Unique username (str),
            'age': age (int),
            'pw': password (str),
            'cpw': confirm password (str)    
        }
    '''
    msg, err = access.signin(request)
    if not err:
        return msg
    else:
        return err

@server.route('/login', methods=['POST'])
def login():
    '''
    Post request authorization:
    {
        Type: Basic Auth,
        Username: Existing username,
        Password: password,
    }
    '''
    encoded_token, err = access.login(request)
    if not err:
        return encoded_token
    else:
        return err

@server.route('/users', methods=['GET'])
def users():
    '''
    Post request authorization:
    {
        Type: Bearer Token,
        Token: Existing token,
    }
    '''
    decoded_token, err = validate.token(request)
    if not err:
        return decoded_token
    else:
        return err


if __name__=='__main__':
    server.run(host='0.0.0.0', port=5000)


