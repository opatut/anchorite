from anchorite import manager, db
from anchorite.common.models import User, ItemType, UserItem, Action, BrewAction, CollectAction, Recipe, RecipeItem, UnitType, GameState, UserUnit


items = [
    # icon       name
    ("pebble", "Pebble"),
    ("branch", "Branch"),
    ("bunch_of_gras", "Bunch of gras"),
    ("frog_leg", "frog leg"),
    ("green_muscus", "green muscus"),
    ("pine_cone", "pine cone"),
    ("rumex_alpinus", "Rumex Alpinus"),
    ("pigweed", "Pigweed"),
    ("fly_agaric", "Fly agaric"),
    ("yallow", "Yallow"),
    ("death_cap", "Death cap"),
    ("sickener", "Sickener"),
    ("destroying_angel", "Destroying angel"),
]

units = [
    # image       name
    ("forestmonster", "Forest Monster"),
    ("blubb", "Blubb"),
    ("pib", "Pib"),
]


@manager.command
def init(seed=False):
    db.drop_all()
    db.create_all()

    db.session.add(GameState(id=0, tick=0))

    if seed:
        user = User("paul", "hunter2")
        db.session.add(user)

        item_types = {}
        for icon,name in items:
            item_type = ItemType()
            item_type.name = name
            item_type.icon = icon
            db.session.add(item_type)
            item_types[icon] = item_type

        user_item_paul = UserItem()
        user_item_paul.user = user
        user_item_paul.item_type = item_types["pebble"]
        user_item_paul.count = 10
        db.session.add(user_item_paul)


        unit_types = {}
        for image,name in units:
            unit_type = UnitType()
            unit_type.name = name
            unit_type.image = image
            db.session.add(unit_type)
            unit_types[image] = unit_type

        recipe = Recipe()
        recipe.output = unit_types["forestmonster"]
        recipe.duration = 15
        db.session.add(recipe)

        recipe_item = RecipeItem()
        recipe_item.recipe = recipe
        recipe_item.item_type = item_types["pebble"]
        recipe_item.count = 1
        db.session.add(recipe_item)

        action = BrewAction()
        action.recipe = recipe
        action.user = user
        action.tick = 0
        db.session.add(action)

    db.session.commit()
