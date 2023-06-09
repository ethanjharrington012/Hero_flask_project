from flask import request, jsonify, json
from functools import wraps
import secrets
import decimal
import requests

from hero_inventory.models import User

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split()[1]
            print(token)

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            our_user = User.query.filter_by(token=token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is invalid'})
        except:
            our_user = User.query.filter_by(token=token).first()
            if token != our_user.token and secrets.compare_digest(token, our_user.token):
                return jsonify({'message': 'Token is invalid'})
        return our_flask_function(our_user, *args, **kwargs)
    return decorated

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)

# API
def random_marvel_genorator():
    url = "https://marvel-quote-api.p.rapidapi.com/"

    headers = {
        "content-type": "application/octet-stream",
        "X-RapidAPI-Key": "74ebc0e9dcmsh71dea7912518c41p16e12ejsn683db21b9e6a",
        "X-RapidAPI-Host": "marvel-quote-api.p.rapidapi.com"
    }

    response = requests.request("GET",url, headers=headers)

    data = response.json()
    return data


