import jwt, datetime

def token(id, username, age):
    return jwt.encode(
        payload={'id':id, 'username':username, 'age':age, 'exp':datetime.datetime.now(tz=datetime.timezone.utc)+datetime.timedelta(days=1), 'iat':datetime.datetime.utcnow()},
        key='secret_api_key',
        algorithm='HS256'
    )