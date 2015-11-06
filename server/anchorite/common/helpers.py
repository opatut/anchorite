from anchorite import manager, db
from anchorite.common.models import User, ItemType, UserItem, Action, BrewAction, CollectAction, Recipe, RecipeItem, UnitType

@manager.command
def init(seed=False):
    db.drop_all()
    db.create_all()

    if seed:
        user = User()
        user.name = "paul"
        user.password = "hunter2"
        db.session.add(user)

        item_type_pebble = ItemType()
        item_type_pebble.name = "Pebble"
        item_type_pebble.icon = "pebble"
        db.session.add(item_type_pebble)

        user_item_paul = UserItem()
        user_item_paul.user = user
        user_item_paul.item_type = item_type_pebble
        user_item_paul.count = 10 
        db.session.add(user_item_paul)

        unit_type = UnitType()
        unit_type.name = "forestmonster"
        db.session.add(unit_type)

        recipe = Recipe()
        recipe.unit_type = unit_type
        db.session.add(recipe)

        recipe_item = RecipeItem()
        recipe_item.recipe = recipe
        recipe_item.item_type = item_type_pebble
        recipe_item.count = 1
        db.session.add(recipe_item)

        action = BrewAction()
        action.recipe = recipe
        action.user = user
        action.tick = 0
        db.session.add(action)

    db.session.commit()
