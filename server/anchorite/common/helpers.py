from anchorite import manager, db
from anchorite.common.models import User, ItemType, UserItem, Action, BrewAction, CollectAction, Recipe, RecipeItem, UnitType, GameState, UserUnit


ITEMS = [
    # icon               name
    ("branch",           "Branch"),
    ("grass",            "Clump of grass"),
    ("frog_leg",         "Frog leg"),
    ("pine_cone",        "Pine cone"),
    ("rumex_alpinus",    "Rumex Alpinus"),
    ("pigweed",          "Pigweed"),
    ("yarrow",           "Yarrow"),
    ("death_cap",        "Deathcap"),
    ("sickener",         "Sickener"),
    ("destroying_angel", "Destroying Angel"),
    ("wild_strawberry",  "Wild Strawberry"),
    ("star",             "Fallen Star"),
]

UNITS = [
    # image            name
    ("brown_monster",  "Brown Monster"),
    ("red_monster",    "Red Monster"),
    ("blue_monster",   "Blue Monster"),
    ("purple_monster", "Purple Monster"),
    ("gold_monster",   "Gold Monster"),
]

RECIPES = [
    # name     outcome              ingreds                                                             duration
    ("brown",  "brown_monster",     ("branch", "sickener", "grass"),                                    30),
    ("red",    "red_monster",       ("branch", "sickener", "grass", "wild_strawberry"),                 50),
    ("blue",   "blue_monster",      ("branch", "sickener", "pigweed", "grass"),                         60),
    ("blue",   "blue_monster",      ("branch", "sickener", "yarrow", "grass"),                          60),
    ("blue",   "blue_monster",      ("branch", "sickener", "rumex_alpinus", "grass"),                   60),
    ("purple", "purple_monster",    ("branch", "death_cap", "pine_cone", "frog_leg"),                   70),
    ("gold",   "gold_monster",      ("branch", "destroying_angel", "star", "death_cap", "pine_cone"),   120),
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
        for icon,name in ITEMS:
            item_type = ItemType()
            item_type.name = name
            item_type.icon = icon
            db.session.add(item_type)
            item_types[icon] = item_type

        user_item_paul = UserItem()
        user_item_paul.user = user
        user_item_paul.item_type = item_types["branch"]
        user_item_paul.count = 10
        db.session.add(user_item_paul)


        unit_types = {}
        for image,name in UNITS:
            unit_type = UnitType()
            unit_type.name = name
            unit_type.image = image
            db.session.add(unit_type)
            unit_types[image] = unit_type


        for name, outcome, items, duration in RECIPES:
            recipe = Recipe()
            recipe.name = name
            recipe.unit_type = unit_types[outcome]
            recipe.duration = duration
            db.session.add(recipe)

            for item in items:
                recipe_item = RecipeItem()
                recipe_item.recipe = recipe
                recipe_item.item_type = item_types[item]
                db.session.add(recipe_item)

    db.session.commit()
