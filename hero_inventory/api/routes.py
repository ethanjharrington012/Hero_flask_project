from flask import Blueprint, request, jsonify
from hero_inventory.helpers import token_required, random_marvel_genorator
from hero_inventory.models import db, hero_schema, heros_schema, Hero  #make sure to know the difference of drone_schema, and drones_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')

def getdata():
    return {'some': 'value'}


@api.route('/heros', methods = ["POST"])
@token_required
def create_hero(our_user):

    name = request.json['name']
    description = request.json['description']
    comic_in = request.json['comic_in']
    super_power = request.json['super_power']
    random_marvel = random_marvel_genorator()
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    hero = Hero(name, description, comic_in, super_power,random_marvel, user_token=user_token)

    db.session.add(hero)
    db.session.commit()

    response = hero_schema.dump(hero)

    return jsonify(response)
    

# retrive(READ) ALL heros
@api.route('/heros', methods = ['GET'])
@token_required
def get_heros(our_user):
    owner = our_user.token
    heros = Hero.query.filter_by(user_token=owner).all()
    response = heros_schema.dump(heros)

    return jsonify(response)

# retirve one drone

@api.route('/heros', methods = ['GET'])
@token_required
def get_hero(our_user, id):
    
    if id:
        hero = Hero.query.get(id)
        response = hero_schema.dump(hero)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Id required'}), 401



@api.route('/heros/<id>', methods = ["PUT"])
@token_required
def update_hero(our_user, id):
    hero.hero = Hero.query.get(id)
    hero.name = request.json['name']
    hero.description = request.json['description']
    hero.comic_in = request.json['comic_in']
    hero.super_power = request.json['super_power']
    hero.random_marvel = random_marvel_genorator()
    hero.user_token = our_user.token

    print(f"User Token: {our_user.token}")

    hero = Hero(name, description, comic_in, super_power, user_token=user_token)

    
    db.session.commit()

    response = hero_schema.dump(hero)

    return jsonify(response)
    
@api.route('/heros/<id>', methods= ['DELETE'])
@token_required
def delete_heros(our_user, id):
    hero = Hero.query.get(id)
    db.session.delete(hero)
    db.session.commit()

    response = hero_schema.dump(hero)
    return jsonify(response)

