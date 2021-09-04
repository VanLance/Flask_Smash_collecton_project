import re
from flask import Blueprint, json, request, jsonify
from werkzeug.wrappers import Response
from smash_inventory.helpers import token_required
from smash_inventory.models import db, User, Character, character_schema, characters_schema

api = Blueprint('api', __name__, url_prefix= '/api')

@api.route('/getdata')
@token_required
def get_data(current_user_token):
    return { 'some' : 'value' }

# Create character Endpoint
@api.route('/characters', methods = ['Post'])
@token_required
def create_character(current_user_token):
    name=request.json['name']
    description = request.json['description']
    games_appeared_in = request.json['games_appeared_in']
    abilities = request.json['abilities']
    weight = request.json['weight']
    # date_created = request.json['date_created']
    jumps = request.json['jumps']
    user_token = current_user_token.token

    character = Character(name,description,games_appeared_in,abilities, weight, jumps, user_token)
    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)

#Retrieve ALL Characters Endpoint
@api.route('/characters',methods = ['GET'])
@token_required
def get_characters(current_user_token):
    owner = current_user_token.token
    characters = Character.query.filter_by(user_token = owner).all()
    response = characters_schema.dump(characters)
    return jsonify(response)

# RETRIEVE ONE character ENDPOINT
@api.route('/characters/<id>', methods = ['GET'])
@token_required
def get_character(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        character = Character.query.get(id)
        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({'message' : 'Valid Token Required'}),401

#UPDATE character ENDPOINT
@api.route('/characters/<id>', methods = ['Post', 'PUT'])
@token_required
def update_character(current_user_token, id):
    character = Character.query.get(id) # Get character Instance

    character.name = request.json['name']
    character.description = request.json['description']
    character.price = request.json['price']
    character.games_appeared_in = request.json['games_appeared_in']
    character.abilities = request.json['abilities']
    character.weight = request.json['weight']
    character.jumps = request.json['date_created']
    character.user_token = current_user_token.token
    
    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)

    # DELETE character ENDPOINT
@api.route('/characters/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user_token, id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)