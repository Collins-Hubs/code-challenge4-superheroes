from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, CheckConstraint
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # Relationship: Hero can have multiple powers through HeroPower
    powers = relationship('HeroPower', back_populates='hero')
    power_list = association_proxy('powers', 'power')  # Proxy to get powers directly

    # Serialization rules: include `name`, `super_name` and proxy `power_list`
    serialize_only = ('id', 'name', 'super_name', 'power_list')

    def __repr__(self):
        return f'<Hero {self.id}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # Relationship: Power can be linked to multiple heroes through HeroPower
    heroes = relationship('HeroPower', back_populates='power')

    # Serialization rules: include `name`, `description`, and proxy `heroes`
    serialize_only = ('id', 'name', 'description', 'heroes')

    # Add validation for name and description
    @validates('name', 'description')
    def validate_not_empty(self, key, value):
        if not value:
            raise ValueError(f'{key.capitalize()} cannot be empty')
        return value

    def __repr__(self):
        return f'<Power {self.id}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    strength = db.Column(db.String, nullable=False)

    # Relationship: linking heroes and powers
    hero = relationship('Hero', back_populates='powers')
    power = relationship('Power', back_populates='heroes')

    # Add validation for strength
    @validates('strength')
    def validate_strength(self, key, value):
        allowed_strengths = ['low', 'medium', 'high']
        if value not in allowed_strengths:
            raise ValueError("Strength must be one of 'low', 'medium', or 'high'")
        return value

    # Serialization rules: include `strength`, `hero`, and `power`
    serialize_only = ('id', 'strength', 'hero', 'power')

    def __repr__(self):
        return f'<HeroPower {self.id} with strength {self.strength}>'
