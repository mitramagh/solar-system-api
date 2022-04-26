from flask import Blueprint, jsonify, abort, make_response


class Planet:
    def __init__(self, id, name, description, distance_from_sun):
        self.id = id
        self.name = name
        self.description = description
        self.distance_from_sun = distance_from_sun

planets = [
    Planet(1, "Mercury", "Mercury is the closest planet to the sun and the smallest planet in the solar system", 35.98),
    Planet(2, "Venus", "Venus is the second planet from the sun and is the hottest planet in the solar system", 67.24),
    Planet(3, "Earth", "Earch is our home planet, it is the third planet from the sun", 92.96),
    Planet(4, "Mars", "Mars is the fourth planet from the sun and a cold, desert_like planet", 141.6),
    Planet(5, "Jupiter", "Jupiter is the fifth planet from the sun and the largest planet in the solar system", 483.8),
    Planet(6, "Saturn", "Saturn is the sixth planet from the sun and is famous for its large and distinct ring system", 890.8),
    Planet(7, "Uranus", "Uranus is the seventh planet from the sun and is a bit of an oddball", 1784),
    Planet(8, "Neptune", "Neptune is the eighth planet from the sun and is on average the coldest planet in the solar system", 2793)
]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["GET"])
def get_planest():
    planets_response = []
    for planet in planets:
        planets_response.append({
        "id": planet.id,
        "name": planet.name,
        "description":  planet.description,
        "distance_from_sun" : planet.distance_from_sun 
        })

    return jsonify(planets_response), 200

@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"msg": f"Planet {planet_id} is invalid"}, 400))

    chosen_planet = None
    for planet in planets:
        print(f"{planet_id}", type(planet.id))
        if planet.id == planet_id:
            chosen_planet = planet
            break
    if chosen_planet is None:
        rsp = {"msg": f"Planet {planet_id} is not found"}
        return jsonify(rsp), 404
    rsp = {
        "id": chosen_planet.id,
        "name": chosen_planet.name,
        "description":  chosen_planet.description,
        "distance_from_sun" : chosen_planet.distance_from_sun
    }
    return jsonify(rsp), 200










# def validate_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except:
#         abort(make_response({"message":f"planet {planet_id} invalid"}, 400))
#     for planet in planets:
#         if planet.id == planet_id:
#             return planet
#     abort(make_response({"message":f"planet {planet_id} not found"}, 404))
# @planets_bp.route("/<planet_id>", methods=["GET"])
# def read_one_planet(planet_id):
#     planet = validate_planet(planet_id)
#     return jsonify(planet.to_json(), 200)