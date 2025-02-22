from flask import Blueprint, jsonify, abort, make_response, request
from app.models.planets import Planet
from app import db

# planets = [
#     Planet(1, "Mercury", "Mercury is the closest planet to the sun and the smallest planet in the solar system", 35.98),
#     Planet(2, "Venus", "Venus is the second planet from the sun and is the hottest planet in the solar system", 67.24),
#     Planet(3, "Earth", "Earch is our home planet, it is the third planet from the sun", 92.96),
#     Planet(4, "Mars", "Mars is the fourth planet from the sun and a cold, desert_like planet", 141.6),
#     Planet(5, "Jupiter", "Jupiter is the fifth planet from the sun and the largest planet in the solar system", 483.8),
#     Planet(6, "Saturn", "Saturn is the sixth planet from the sun and is famous for its large and distinct ring system", 890.8),
#     Planet(7, "Uranus", "Uranus is the seventh planet from the sun and is a bit of an oddball", 1784),
#     Planet(8, "Neptune", "Neptune is the eighth planet from the sun and is on average the coldest planet in the solar system", 2793)
# ]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["POST"])
def create_new_planet():
    request_body = request.get_json()
    new_planet = Planet(name=request_body["name"],
                        description=request_body["description"],
                        distance_from_sun=request_body["distance_from_sun"])
    db.session.add(new_planet)
    db.session.commit()

    return {"message": f"Successfully created new planet with id {new_planet.id}"}, 201


@planets_bp.route("", methods=["GET"])
def get_all_planets():
    params = request.args

    if "name" in params:
        planet_name =params["name"]
        planets = Planet.query.filter_by(name=planet_name)
    else:
        planets = Planet.query.all()

    planets_response = []
    for planet in planets:
        planets_response.append({
        "id": planet.id,
        "name": planet.name,
        "description":  planet.description,
        "distance_from_sun" : planet.distance_from_sun 
        })

    return jsonify(planets_response), 200

def get_planet_or_abort(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        rsp = {"message" : f"Invalid id: {planet_id}"}
        abort(make_response(jsonify(rsp), 400))

    chosen_planet = Planet.query.get(planet_id)

    if chosen_planet is None:
        rsp= {"message": f"planet {planet_id} is not found"}
        abort(make_response(jsonify(rsp), 404))
    return chosen_planet

@planets_bp.route('<planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    
    chosen_planet = get_planet_or_abort(planet_id)

    planet_response = {
        "id": chosen_planet.id,
        "name": chosen_planet.name,
        "description":  chosen_planet.description,
        "distance_from_sun" : chosen_planet.distance_from_sun 
        }

    return jsonify(planet_response), 200

@planets_bp.route('/<planet_id>', methods=['PUT'])
def update_planet(planet_id):

    chosen_planet = get_planet_or_abort(planet_id)

    request_body = request.get_json()
    try:
        chosen_planet.name=request_body["name"],
        chosen_planet.description=request_body["description"],
        chosen_planet.distance_from_sun=request_body["distance_from_sun"]

        db.session.commit()

    except KeyError:
        return {"message": "name, description, and distance from sun are required"}, 400    

    return {"message": f"Successfully updated planet with id {chosen_planet.id}"}, 200


@planets_bp.route("/<planet_id>", methods=['DELETE'])
def delete_planet(planet_id):
    
    chosen_planet = get_planet_or_abort(planet_id)

    db.session.delete(chosen_planet)
    db.session.commit()

    return {
        "message": f"planet #{planet_id} successfully deleted"
    }, 200
