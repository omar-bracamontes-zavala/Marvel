from flask import Flask, request
import jwt

server = Flask(__name__)

@server.route('/validate', methods=['POST'])
def validate():
    encoded_token = request.headers['Authorization']
    
    if not encoded_token:
        return 'Missing credentails', 401
    
    encoded_token = encoded_token.split(' ')[1]
    try:
        decoded_token = jwt.decode(
            encoded_token, 'secret_api_key', algorithms=['HS256']
        )
    except:
        return 'Not authorized', 403
    return decoded_token, 200