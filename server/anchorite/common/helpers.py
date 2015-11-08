from anchorite import manager, db
from anchorite.common.models import User, ItemType, UserItem, Action, BrewAction, CollectAction, Recipe, RecipeItem, UnitType, GameState, UserUnit

USERS = [
    ("paul",  "hunter2", ("caro", "mel", "lasse")),
    ("caro",  "hunter2", ("paul", "mel", "lasse")),
    ("mel",   "hunter2", ("paul", "caro")),
    ("lasse", "hunter2", ("paul", "caro")),
]

ITEMS = [
    # icon               name               rarity
    ("branch",           "Branch",          70),
    ("grass",            "Clump of grass",  50),
    ("frog_leg",         "Frog leg",        20),
    ("pine_cone",        "Pine cone",       40),
    ("rumex_alpinus",    "Rumex Alpinus",   25),
    ("pigweed",          "Pigweed",         25),
    ("yarrow",           "Yarrow",          25),
    ("death_cap",        "Deathcap",        30),
    ("sickener",         "Sickener",        50),
    ("destroying_angel", "Destroying Angel",15),
    ("wild_strawberry",  "Wild Strawberry", 20),
    ("star",             "Fallen Star",     2),
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

    item_types = {}
    for icon,name,rarity in ITEMS:
        item_type = ItemType()
        item_type.name = name
        item_type.icon = icon
        item_type.rarity = rarity
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

    if seed:
        users = {}
        for name, password, _ in USERS:
            user = User(name, password)
            users[name] = user
            db.session.add(user)

        for name, _, friends in USERS:
            for friend in friends:
                users[name].friends.append(users[friend])


    db.session.commit()
