from anchorite import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    actions = db.relationship("Action", backref="user", lazy="dynamic")
    items = db.relationship("UserItem", backref="user", lazy="dynamic")

class ItemType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    icon = db.Column(db.String(80))
    user_items = db.relationship("UserItem", backref="item_type", lazy="dynamic")
    # ...

class UserItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_type_id = db.Column(db.Integer, db.ForeignKey('item_type.id'))
    count = db.Column(db.Integer)

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

    def execute(self):
        pass

class CollectAction(Action):
    __mapper_args__ = {
       "polymorphic_identity": "collect_action"
    }

    def execute(self):
        pass

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brew_actions = db.relationship("BrewAction", backref="recipe", lazy="dynamic")
    items = db.relationship("RecipeItem", backref="recipe", lazy="dynamic")

class RecipeItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    item_type_id = db.Column(db.Integer, db.ForeignKey('item_type.id'))
    count = db.Column(db.Integer)

class UnitType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe = db.relationship("Recipe", backref="output", lazy="dynamic")
    name = db.Column(db.String(80))
