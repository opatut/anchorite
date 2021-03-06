from anchorite import db
from datetime import datetime
from flask.ext.login import UserMixin, current_user
from flask.ext.scrypt import generate_random_salt, generate_password_hash, check_password_hash
import math
from random import shuffle, random, randint, choice

friends = db.Table('friends', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'))
)

class AttackChance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_a_id = db.Column(db.Integer, db.ForeignKey('unit_type.id'))
    type_b_id = db.Column(db.Integer, db.ForeignKey('unit_type.id'))
    a_chance = db.Column(db.Integer)
    b_chance = db.Column(db.Integer)

    @classmethod
    def find(cls, type_a, type_b):
        return cls.query.filter_by(type_a_id=type_a.id, type_b_id=type_b.id).first()


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    start = db.Column(db.Float, default=0)
    end = db.Column(db.Float, default=0)

    __mapper_args__ = {
        "polymorphic_identity": "action",
        "polymorphic_on": type
    }

    def execute(self):
        pass

    def to_json(self):
        return dict(id=self.id,
            type=self.type,
            user_id=self.user_id,
            start=self.start,
            end=self.end,
            )

class BrewAction(Action):
    id = db.Column(db.Integer, db.ForeignKey('action.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    __mapper_args__ = {
       "polymorphic_identity": "brew_action"
    }

    def to_json(self):
        d = Action.to_json(self)
        d["recipe_id"] = self.recipe_id
        return d

    def execute(self):
        unit_type = self.recipe.unit_type
        unit = UserUnit(unit_type=unit_type)
        self.user.write_message('You brew a {}'.format(unit_type.name))
        self.user.units.append(unit)

    def __repr__(self):
        return "[Action] Brew: {}".format(repr(self.recipe))

class CollectAction(Action):
    id = db.Column(db.Integer, db.ForeignKey('action.id'), primary_key=True)

    __mapper_args__ = {
       "polymorphic_identity": "collect_action"
    }

    def execute(self):
        items = ItemType.query.all()
        chance_sum = sum([ item.rarity for item in items ])

        n = random() * chance_sum
        for item in items:
            if item.rarity > n:
                self.user.add_item(item.id)
                self.user.write_message('You found a {}'.format(item.name))
                break
            else:
                n -= item.rarity

class AttackAction(Action):
    id = db.Column(db.Integer, db.ForeignKey('action.id'), primary_key=True)
    target_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    units = db.relationship("UserUnit", backref="attack_action", lazy="dynamic")

    __mapper_args__ = {
       "polymorphic_identity": "attack_action"
    }

    def execute(self):
        attacker = self.user
        defender = self.target_user

        e_losses = 0
        u_losses = 0

        def win():
            items_stolen = {}

            # steal stuff, for every unit alive
            for unit in units:
                items = defender.items.all()
                if items:
                    item = choice(items)
                    items_stolen[item.item_type.name] = items_stolen.get(item.item_type.name, 0) + 1
                    attacker.add_item(item.item_type_id)
                    defender.remove_item(item.item_type_id)

            print(items_stolen)
            loot = ', '.join(['{} {}'.format(count, name) for name, count in items_stolen.items()]) or 'nothing'
            attacker.write_message('VICTORY! You win against {}. Your units bring back loot: {}.'.format(defender.name, loot))
            defender.write_message('THIEFS! You were raided by {}. They took from you: {}.'.format(attacker.name, loot))

        def lose():
            attacker.write_message('DEFEAT! You lost all {} units in your attack against {}.'.format(u_losses, defender.name))
            defender.write_message('DEFENSE! You defended against {} units from {}, losing {} units on your own.'.format(u_losses, attacker.name, e_losses))

        # get units
        enemies = defender.units.filter_by(attack_action=None).all()
        units = self.units.all()
        shuffle(enemies)
        shuffle(units)

        # roll for luck
        luck = random()

        if not enemies:
            win()
        else:
            # take only half of the enemy units, but at least one
            enemies = enemies[:max(1, math.ceil(len(enemies) / 2.0))]

            while units and enemies:
                i1 = randint(0, len(units) - 1)
                i2 = randint(0, len(enemies) - 1)
                u = units[i1]
                e = enemies[i2]

                chance1 = AttackChance.find(u.unit_type, e.unit_type)
                chance2 = AttackChance.find(e.unit_type, u.unit_type)

                u_strength = 1
                e_strength = 1.4

                if chance1:
                    u_strength *= chance1.a_chance
                    e_strength *= chance1.b_chance
                elif chance2:
                    e_strength *= chance2.a_chance
                    u_strength *= chance2.b_chance

                ratio = u_strength / (e_strength + u_strength)

                print('Fight', u.unit_type.name, e.unit_type.name, u_strength, e_strength, ratio)

                if random() < ratio:
                    # unit wins
                    db.session.delete(e)
                    e_losses += 1
                    del enemies[i2]
                else:
                    db.session.delete(u)
                    u_losses += 1
                    del units[i1]

            if units: win()
            if enemies: lose()

        # "return" units home
        self.units = []

    def to_json(self):
        d = Action.to_json(self)
        d["target_user_id"] = self.target_user_id
        d["units"] = [unit.to_json() for unit in self.units]
        return d

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_type.id'))
    brew_actions = db.relationship("BrewAction", backref="recipe", lazy="dynamic")
    recipe_items = db.relationship("RecipeItem", backref="recipe", lazy="dynamic")
    duration = db.Column(db.Integer, default=0)

    def __repr__(self):
        first = True
        out = "[Recipe] "
        for item in self.recipe_items:
            if first:
               first = False
               out += "{}x {}".format(item.count, item.item_type.name)
            else:
                out += "+ {}x {}".format(item.count, item.item_type.name)

        out += " = {}".format(self.unit_type.name)
        return out

    def to_json(self):
        return dict(id=self.id,
            unit_type_id=self.unit_type_id,
            recipe_items=list(map(RecipeItem.to_json, self.recipe_items)),
            duration=self.duration)


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
    recipes = db.relationship("Recipe", backref="unit_type", lazy="dynamic")
    user_units = db.relationship("UserUnit", backref="unit_type", lazy="dynamic")
    name = db.Column(db.String(80))
    image = db.Column(db.String(80))
    attack = db.Column(db.Integer)
    defence = db.Column(db.Integer)

    def to_json(self):
        return dict(id=self.id, name=self.name, image=self.image)

class GameState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tick = db.Column(db.Float)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    salt = db.Column(db.String(100))
    password_hash= db.Column(db.String(100))

    actions = db.relationship("Action", backref="user", lazy="dynamic", foreign_keys=[Action.user_id])
    items = db.relationship("UserItem", backref="user", lazy="dynamic")
    units = db.relationship("UserUnit", backref="user", lazy="dynamic")
    incoming_attacks = db.relationship("AttackAction", backref="target_user", lazy="dynamic", foreign_keys=[AttackAction.target_user_id])
    messages = db.relationship("Message", backref="user", lazy="dynamic")

    friends = db.relationship("User",
        backref="friended",
        lazy="dynamic",
        secondary="friends",
        primaryjoin=(id == friends.c.user_id),
        secondaryjoin=(id == friends.c.friend_id))

    def __init__(self, username, password):
        self.name = username
        self.salt = generate_random_salt()
        self.password_hash = generate_password_hash(password, self.salt)

    def add_item(self, item_type_id, count=1):
        item = self.items.filter(UserItem.item_type_id == item_type_id).first()
        if item:
            item.count += count
        else:
            self.items.append(UserItem(item_type_id=item_type_id, count=count))

    def remove_item(self, item_type_id, count=1):
        item_remove = self.items.filter(UserItem.item_type_id == item_type_id).first()
        item_remove.count -= 1
        if item_remove.count <= 0:
            db.session.delete(item_remove)

    def queue_action(self, action, duration):
        current_tick = GameState.query.get(0).tick
        action.start = current_tick

        # find last action
        if action.type in ('brew_action', 'collect_action'):
            active_actions = self.actions.order_by(db.desc(Action.end)).all()

            if active_actions:
                action.start = active_actions[0].end
        # else start right away
        action.end = action.start + duration

        self.actions.append(action)

    def check_password(self, password):
        return check_password_hash(password, self.password_hash, self.salt)

    def write_message(self, text):
        message = Message(text=text, user_id=self.id, date=datetime.utcnow())
        db.session.add(message)
        return message

    def to_json(self):
        return dict(id=self.id, name=self.name)


class ItemType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    icon = db.Column(db.String(80))
    rarity = db.Column(db.Integer)
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


class UserUnit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_type.id'))
    attack_action_id = db.Column(db.Integer, db.ForeignKey('attack_action.id'))
    happyness = db.Column(db.Integer)
    health = db.Column(db.Integer)

    def kill(self):
        db.session.delete(self)

    def apply_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def to_json(self):
        return dict(id=self.id,
            user_id=self.user_id,
            unit_type_id=self.unit_type_id,
            attack_action_id=self.attack_action_id,
            happyness=self.happyness,
            health=self.health)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.Text)

    def to_json(self):
        return dict(id=self.id, date=str(self.date), text=self.text)
