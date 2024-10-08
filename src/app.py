"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.serialize() for user in users]), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error"}), 500
    

@app.route('/characters', methods=['GET'])
def get_characters():
    try:
        characters = Character.query.all()
        return jsonify([character.serialize() for character in characters]), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error"}), 500


@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    try:
        character = Character.query.get(character_id)
        if character is None:
            return jsonify({"msg": "Character not found"}), 404
        return jsonify(character.serialize()), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error"}), 500


@app.route('/planets', methods=['GET'])
def get_planets():
    try:
        planets = Planet.query.all()
        return jsonify([planet.serialize() for planet in planets]), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error"}), 500


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)
        if planet is None:
            return jsonify({"msg": "Planet not found"}), 404
        return jsonify(planet.serialize()), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error"}), 500


@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    try:
        vehicles = Vehicle.query.all()
        return jsonify([vehicle.serialize() for vehicle in vehicles]), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error"}), 500


@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if vehicle is None:
            return jsonify({"msg": "Vehicle not found"}), 404
        return jsonify(vehicle.serialize()), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error"}), 500


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    try:
        user_id = request.json.get('user_id')
        user = User.query.get(user_id)
        planet = Planet.query.get(planet_id)
        
        if user is None or planet is None:
            return jsonify({"msg": "User or Planet not found"}), 404
        
        favorite = Favorite(user_id=user_id, planet_id=planet_id)
        db.session.add(favorite)
        db.session.commit()

        return jsonify(favorite.serialize()), 201
    except Exception as e:
        return jsonify({"msg": "Internal Server Error"}), 500


@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    try:
        user_id = request.json.get('user_id')
        user = User.query.get(user_id)
        character = Character.query.get(character_id)
        
        if user is None or character is None:
            return jsonify({"msg": "User or Character not found"}), 404
        
        favorite = Favorite(user_id=user_id, character_id=character_id)
        db.session.add(favorite)
        db.session.commit()

        return jsonify(favorite.serialize()), 201
    except Exception as e:
        return jsonify({"msg": "Internal Server Error"}), 500


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    try:
        user_id = request.json.get('user_id')
        user = User.query.get(user_id)
        vehicle = Vehicle.query.get(vehicle_id)
        
        if user is None or vehicle is None:
            return jsonify({"msg": "User or Vehicle not found"}), 404
        
        favorite = Favorite(user_id=user_id, vehicle_id=vehicle_id)
        db.session.add(favorite)
        db.session.commit()

        return jsonify(favorite.serialize()), 201
    except Exception as e:
        return jsonify({"msg": "Internal Server Error"}), 500


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    try:
        user_id = request.json.get('user_id')
        favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        
        if favorite is None:
            return jsonify({"msg": "Favorite not found"}), 404
        
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"msg": "Favorite deleted"}), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error"}), 500


@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    try:
        user_id = request.json.get('user_id')
        favorite = Favorite.query.filter_by(user_id=user_id, character_id=character_id).first()
        
        if favorite is None:
            return jsonify({"msg": "Favorite not found"}), 404
        
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"msg": "Favorite deleted"}), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error"}), 500


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
    try:
        user_id = request.json.get('user_id')
        favorite = Favorite.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()
        
        if favorite is None:
            return jsonify({"msg": "Favorite not found"}), 404
        
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"msg": "Favorite deleted"}), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error"}), 500


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"msg": "User not found"}), 404

        favorites = Favorite.query.filter_by(user_id=user_id).all()
        return jsonify([favorite.serialize() for favorite in favorites]), 200
    except Exception as e:
        return jsonify({"msg": "Internal Server Error"}), 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
