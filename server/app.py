#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize extensions
migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

@app.route('/')
def index():
    return '<h1>Code Challenge</h1>'

# RESTful API for Hero
class HeroesResource(Resource):
    def get(self):
        heroes = Hero.query.all()
        return jsonify([hero.to_dict() for hero in heroes])

    def post(self):
        data = request.get_json()
        new_hero = Hero(
            name=data.get('name'),
            super_name=data.get('super_name')
        )
        db.session.add(new_hero)
        db.session.commit()
        return new_hero.to_dict(), 201

# RESTful API for Hero by ID
class HeroByIdResource(Resource):
    def get(self, id):
        hero = Hero.query.get_or_404(id)
        return hero.to_dict()

    def patch(self, id):
        hero = Hero.query.get_or_404(id)
        data = request.get_json()
        if 'name' in data:
            hero.name = data['name']
        if 'super_name' in data:
            hero.super_name = data['super_name']
        db.session.commit()
        return hero.to_dict()

    def delete(self, id):
        hero = Hero.query.get_or_404(id)
        db.session.delete(hero)
        db.session.commit()
        return {}, 204

# RESTful API for Power
class PowersResource(Resource):
    def get(self):
        powers = Power.query.all()
        return jsonify([power.to_dict() for power in powers])

    def post(self):
        data = request.get_json()
        new_power = Power(
            name=data.get('name'),
            description=data.get('description')
        )
        db.session.add(new_power)
        db.session.commit()
        return new_power.to_dict(), 201

# RESTful API for HeroPower
class HeroPowersResource(Resource):
    def get(self):
        hero_powers = HeroPower.query.all()
        return jsonify([hero_power.to_dict() for hero_power in hero_powers])

    def post(self):
        data = request.get_json()
        new_hero_power = HeroPower(
            hero_id=data.get('hero_id'),
            power_id=data.get('power_id'),
            strength=data.get('strength')
        )
        db.session.add(new_hero_power)
        db.session.commit()
        return new_hero_power.to_dict(), 201

# Add the resources to the API
api.add_resource(HeroesResource, '/heroes')
api.add_resource(HeroByIdResource, '/heroes/<int:id>')
api.add_resource(PowersResource, '/powers')
api.add_resource(HeroPowersResource, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
