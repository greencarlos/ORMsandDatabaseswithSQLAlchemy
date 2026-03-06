import jose
from jose import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
import os

SECRET_KEY = os.environ.get('SECRET_KEY') or "hello world"

def encode_token(user_id):
    payload = {
            'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),
            'iat': datetime.now(timezone.utc),
            'sub': str(user_id)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

            if not token:
                return jsonify({'message': 'missing token'})

            try:
                data = jwt.decode(token)
                print(data)
                member_id = data['sub']
            except jwt.ExpriedSignatureError as e:
                return jsonify({'message': 'token expired'}), 400
            except jst.InvalidTokenError:
                return jsonify({'message': 'invalid token'}), 400

            return f(member_id, *args, **kwargs)

        else:
            return jsonify({'message': 'You must be logged in to access this.'}), 400


    return decorated
