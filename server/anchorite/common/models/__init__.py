from anchorite import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    actions = db.relationship("Action", backref="user", lazy="dynamic")
    inventory = db.relationship("InventoryEntry", backref="user", lazy="dynamic")

class ItemType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    icon = db.Column(db.Text)

class InventoryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)

# class Action(db.Model):
#     id =
#     name =
#     user_id =
