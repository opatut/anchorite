from anchorite import manager, db
from anchorite.common.models import User, ItemType, UserItem, Action, BrewAction, CollectAction, Recipe, RecipeItem, UnitType, GameState, UserUnit


items = [
    # icon       name
    ("branch", "branch"),
    ("bunch_of_gras", "gras"),
    ("frog_leg", "frog leg"),
    ("pine_cone", "pine cone"),
    ("rumex_alpinus", "rumex_alpinus"),
    ("pigweed", "pigweed"),
    ("yarrow", "yarrow"),
    ("death_cap", "death_cap"),
    ("sickener", "sickener"),
    ("destroying_angel", "destroying_angel"),
    ("wild_strawberry", "wild_strawberry"),
    ("star", "star"),
]

units = [
    # image       name
    ("forestmonster", "Forest Monster"),
    ("pib", "Pib"),
]

recipes = [
    #rec.name      rec.outcome    rec.ingreds  rec.duration

    ("brown", "forestmonster", ("branch", "sickener", "gras", 30),
    ("red", "red_monster", ("branch", "sickener", "gras", "wild_strawberry"), 50)
    ("blue", "blue_monster", ("branch", "sickener", "pigweed", "gras"), 60)
    ("blue", "blue_monster", ("branch", "sickener", "yarrow", "gras"), 60)
    ("blue", "blue_monster", ("branch", "sickener", "rumex_alpinus", "gras"), 60)
    ("purple", "purple_monster", ("branch", "death_cap", "pine_cone", "frog_leg"), 70)
    ("gold", "gold_monster", ("branch", "destroying_angel", "star", "death_cap", "pine_cone"),120h)
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


        for name, outcome, items, duration in recipes:
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
