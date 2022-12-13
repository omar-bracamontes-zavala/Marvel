import jwt

def token(request):
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return None, ("Missing credentials", 401)

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, 'secret_api_key', algorithms=["HS256"]
        )
    except:
        return None, ("Not authorized", 403)

    return decoded, None