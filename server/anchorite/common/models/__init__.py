from anchorite import db
from flask.ext.login import UserMixin
from flask.ext.scrypt import generate_random_salt, generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    salt = db.Column(db.String(100))
    password_hash= db.Column(db.String(100))
    actions = db.relationship("Action", backref="user", lazy="dynamic")
    items = db.relationship("UserItem", backref="user", lazy="dynamic")
    units = db.relationship("UserUnit", backref="user", lazy="dynamic")

    def __init__(self, username, password):
        self.name = username
        self.salt = generate_random_salt()
        self.password_hash = generate_password_hash(password, self.salt)

    def check_password(self, password):
        return check_password_hash(password, self.password_hash, self.salt)

class ItemType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    icon = db.Column(db.String(80))
    user_items = db.relationship("UserItem", backref="item_type", lazy="dynamic")
    recipe_items = db.relationship("RecipeItem", backref="item_type", lazy="dynamic")

    def to_json(self):
        return dict(id=self.id, name=self.name, icon=self.icon)


class UserItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_type_id = db.Column(db.Integer, db.ForeignKey('item_type.id'))
    count = db.Column(db.Integer, default=1)
    def to_json(self):
        return dict(id=self.id,
            user_id=self.user_id,
            item_type_id=self.item_type_id,
            count =self.count)


class Action(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     type = db.Column(db.String(80))
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
     tick = db.Column(db.Integer, default=0)

     __mapper_args__ = {
        "polymorphic_identity": "action",
        "polymorphic_on": type
     }

     def execute(self):
         pass

class BrewAction(Action):
    __mapper_args__ = {
       "polymorphic_identity": "brew_action"
    }

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def execute(self):
        pass

    def __repr__(self):
        return "[Action] Brew: {}".format(repr(self.recipe))
class CollectAction(Action):
    __mapper_args__ = {
       "polymorphic_identity": "collect_action"
    }

    def execute(self):
        pass

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_type.id'))
    brew_actions = db.relationship("BrewAction", backref="recipe", lazy="dynamic")
    recipe_items = db.relationship("RecipeItem", backref="recipe", lazy="dynamic")

    def __repr__(self):
        first = True
        out = "[Recipe] "
        for item in self.recipe_items:
            if first:
               first = False
               out += "{}x {}".format(item.count, item.item_type.name)
            else:
                out += "+ {}x {}".format(item.count, item.item_type.name)

        out += " = {}".format(self.output.name)
        return out

    def to_json(self):
        return dict(id=self.id,
            unit_type_id=self.unit_type_id,
            recipe_items=list(map(RecipeItem.to_json, self.recipe_items)))


class RecipeItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    item_type_id = db.Column(db.Integer, db.ForeignKey('item_type.id'))
    count = db.Column(db.Integer, default=1)

    def to_json(self):
        return dict(recipe_id=self.recipe_id,
            count=self.count,
            item_type_id=self.item_type_id)

class UnitType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipes = db.relationship("Recipe", backref="output", lazy="dynamic")
    name = db.Column(db.String(80))

    def to_json(self):
        return dict(id=self.id, name=self.name)

class GameState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tick = db.Column(db.Integer)

class UserUnit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_type.id'))
    count = db.Column(db.Integer, default=1)
    def to_json(self):
        return dict(id=self.id,
            user_id=self.user_id,
            unit_type_id=self.unit_type_id,
            count =self.count)
