from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location
from . import Items

if TYPE_CHECKING:
    from .World import RabbitAndSteelWorld


class RabbitAndSteelLocation(Location):
    game: str = "Rabbit and Steel"


def create_all_locations(world: RabbitAndSteelWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: RabbitAndSteelWorld) -> None:
    kingdom_outskirts = world.get_region("Kingdom Outskirts")
    kingdom_outskirts.add_locations(kingdom_outskirts_table, RabbitAndSteelLocation)

    crack_in_the_geode = world.get_region("Crack in the Geode")
    crack_in_the_geode.add_locations(crack_in_the_geode_table, RabbitAndSteelLocation)

    # Add the generic locations for the 5 main kingdoms
    for kingdom, locations in kingdom_to_locations.items():
        if kingdom not in world.options.excluded_kingdoms:
            kingdom_region = world.get_region(kingdom)
            kingdom_region.add_locations(locations, RabbitAndSteelLocation)

    pale_keep = world.get_region("The Pale Keep")
    pale_keep.add_locations(pale_keep_table, RabbitAndSteelLocation)

    moonlit_pinnacle = world.get_region("Moonlit Pinnacle")
    moonlit_pinnacle.add_locations(moonlit_pinnacle_table, RabbitAndSteelLocation)

    # Add the class specific locations for all the kingdoms, except for the Moonlit Pinnacle
    if world.options.checks_per_class:
        for class_name in world.options.checks_per_class:
            class_table = class_tables[class_name]

            for kingdom in class_table:
                # Skip Moonlit Pinnacle as there are cases where more or less characters have checks there
                if kingdom == "Moonlit Pinnacle":
                    continue

                if kingdom not in world.options.excluded_kingdoms:
                    class_kingdom = world.get_region(kingdom + " - " + class_name)
                    class_kingdom.add_locations(class_table[kingdom], RabbitAndSteelLocation)

    # Find the classes that will have checks in the Moonlit Pinnacle
    moonlit_classes = []
    if world.options.goal_condition == world.options.goal_condition.option_shira:
        moonlit_classes = Items.class_names
    elif world.options.checks_per_class:
        moonlit_classes = world.options.checks_per_class

    # Add the class locations for the Moonlit Pinnacle
    for class_name in moonlit_classes:
        if class_name in world.options.exclude_class:
            continue
        class_moonlit = world.get_region("Moonlit Pinnacle - " + class_name)
        class_moonlit.add_locations(class_tables[class_name]["Moonlit Pinnacle"], RabbitAndSteelLocation)

    # Add the locations for the checks in a chest
    if world.options.checks_per_item_in_chest:
        kingdom_outskirts.add_locations(kingdom_outskirts_chest_item_table, RabbitAndSteelLocation)
        crack_in_the_geode.add_locations(crack_in_the_geode_chest_item_table, RabbitAndSteelLocation)

        # Add the chests in the remaining kingdoms
        for kingdom_name, chest_table in kingdom_to_chest_locations.items():
            if kingdom_name not in world.options.excluded_kingdoms:
                kingdom_region = world.get_region(kingdom_name)
                kingdom_region.add_locations(chest_table)

    # Add the locations for the checks in a shop
    if world.options.shop_sanity == world.options.shop_sanity.option_global:
        shop_region = world.get_region("Shops")
        shop_region.add_locations(global_shop_table)
    elif world.options.shop_sanity == world.options.shop_sanity.option_regional:
        for kingdom_name, chest_table in kingdom_to_shop_locations.items():
            if kingdom_name not in world.options.excluded_kingdoms:
                kingdom_region = world.get_region(kingdom_name)
                kingdom_region.add_locations(chest_table)


def create_events(world: RabbitAndSteelWorld) -> None:
    moonlit_pinnacle = world.get_region("Moonlit Pinnacle")
    moonlit_pinnacle.add_event("Victory", location_type=RabbitAndSteelLocation, item_type=Items.RabbitAndSteelItem)


location_id = 1

# Locations that should be awarded during the run through Kingdom Outskirts
outskirts_locations = ["Kingdom Outskirts Battle 1", "Kingdom Outskirts Chest 1", "Kingdom Outskirts Battle 2",
                       "Kingdom Outskirts Chest 2", "Kingdom Outskirts Battle 3"]
kingdom_outskirts_table = {}
for location in outskirts_locations:
    kingdom_outskirts_table[location] = location_id
    location_id += 1

# Locations that should be awarded during the run through Crack in the Geode
crack_locations = ["Crack in the Geode Battle 1", "Crack in the Geode Chest 1", "Crack in the Geode Battle 2",
                       "Crack in the Geode Chest 2", "Crack in the Geode Battle 3"]
crack_in_the_geode_table = {}
for location in crack_locations:
    crack_in_the_geode_table[location] = location_id
    location_id += 1

# The 5 main kingdoms have the same structure
# So fill them with the locations that should be awarded during the run through the kingdom
generic_kingdom_locations = ["Battle 1", "Battle 2", "Battle 3", "Chest", "Boss"]
scholars_nest_table = {}
for location in generic_kingdom_locations:
    scholars_nest_table["Scholar's Nest " + location] = location_id
    location_id += 1

kings_arsenal_table = {}
for location in generic_kingdom_locations:
    kings_arsenal_table["King's Arsenal " + location] = location_id
    location_id += 1

red_darkhouse_table = {}
for location in generic_kingdom_locations:
    red_darkhouse_table["Red Darkhouse " + location] = location_id
    location_id += 1

churchmouse_streets_table = {}
for location in generic_kingdom_locations:
    churchmouse_streets_table["Churchmouse Streets " + location] = location_id
    location_id += 1

emerald_lakeside_table = {}
for location in generic_kingdom_locations:
    emerald_lakeside_table["Emerald Lakeside " + location] = location_id
    location_id += 1

darkhouse_depths_table = {}
for location in generic_kingdom_locations:
    darkhouse_depths_table["Darkhouse Depths " + location] = location_id
    location_id += 1

subterra_sanctum_table = {}
for location in generic_kingdom_locations:
    subterra_sanctum_table["Subterra Sanctum " + location] = location_id
    location_id += 1

atelier_aurum_table = {}
for location in generic_kingdom_locations:
    atelier_aurum_table["Atelier Aurum " + location] = location_id
    location_id += 1

# Helper dictionary to get the locations from the 5 main kingdoms from their name
kingdom_to_locations = {"Scholar's Nest": scholars_nest_table, "King's Arsenal": kings_arsenal_table,
                        "Red Darkhouse": red_darkhouse_table, "Churchmouse Streets": churchmouse_streets_table,
                        "Emerald Lakeside": emerald_lakeside_table, "Darkhouse Depths": darkhouse_depths_table,
                        "Subterra Sanctum": subterra_sanctum_table, "Atelier Aurum": atelier_aurum_table}

# Locations that should be awarded during the run through The Pale Keep
keep_locations = ["The Pale Keep Battle 1", "The Pale Keep Battle 2", "The Pale Keep Battle 3", "The Pale Keep Chest"]
pale_keep_table = {}
for location in keep_locations:
    pale_keep_table[location] = location_id
    location_id += 1

# Locations that should be awarded during the run through the Moonlit Pinnacle
moonlit_pinnacle_table = {
    "Shira": location_id
}
location_id += 1

# Locations that should be awarded for obtaining a specific chest item if chest sanity is on
item_locations = ["Top Left", "Bottom Left", "Middle", "Top Right", "Bottom Right"]

kingdom_outskirts_chest_locations = ["Kingdom Outskirts Chest 1", "Kingdom Outskirts Chest 2"]
kingdom_outskirts_chest_item_table = {}
for chest in kingdom_outskirts_chest_locations:
    for location in item_locations:
        kingdom_outskirts_chest_item_table[chest + " " + location] = location_id
        location_id += 1

crack_in_the_geode_chest_locations = ["Crack in the Geode Chest 1", "Crack in the Geode Chest 2"]
crack_in_the_geode_chest_item_table = {}
for chest in crack_in_the_geode_chest_locations:
    for location in item_locations:
        crack_in_the_geode_chest_item_table[chest + " " + location] = location_id
        location_id += 1

scholars_nest_chest_item_table = {}
for location in item_locations:
    scholars_nest_chest_item_table["Scholar's Nest Chest " + location] = location_id
    location_id += 1

kings_arsenal_chest_item_table = {}
for location in item_locations:
    kings_arsenal_chest_item_table["King's Arsenal Chest " + location] = location_id
    location_id += 1

red_darkhouse_chest_item_table = {}
for location in item_locations:
    red_darkhouse_chest_item_table["Red Darkhouse Chest " + location] = location_id
    location_id += 1

churchmouse_streets_chest_item_table = {}
for location in item_locations:
    churchmouse_streets_chest_item_table["Churchmouse Streets Chest " + location] = location_id
    location_id += 1

emerald_lakeside_chest_item_table = {}
for location in item_locations:
    emerald_lakeside_chest_item_table["Emerald Lakeside Chest " + location] = location_id
    location_id += 1

darkhouse_depths_chest_item_table = {}
for location in item_locations:
    darkhouse_depths_chest_item_table["Darkhouse Depths Chest " + location] = location_id
    location_id += 1

subterra_sanctum_chest_item_table = {}
for location in item_locations:
    subterra_sanctum_chest_item_table["Subterra Sanctum Chest " + location] = location_id
    location_id += 1

atelier_aurum_chest_item_table = {}
for location in item_locations:
    atelier_aurum_chest_item_table["Atelier Aurum Chest " + location] = location_id
    location_id += 1

pale_keep_chest_item_table = {}
for location in item_locations:
    pale_keep_chest_item_table["The Pale Keep Chest " + location] = location_id
    location_id += 1

kingdom_to_chest_locations = {"Scholar's Nest": scholars_nest_chest_item_table,
                              "King's Arsenal": kings_arsenal_chest_item_table,
                              "Red Darkhouse": red_darkhouse_chest_item_table,
                              "Churchmouse Streets": churchmouse_streets_chest_item_table,
                              "Emerald Lakeside": emerald_lakeside_chest_item_table,
                              "Darkhouse Depths": darkhouse_depths_chest_item_table,
                              "Subterra Sanctum": subterra_sanctum_chest_item_table,
                              "Atelier Aurum": atelier_aurum_chest_item_table,
                              "The Pale Keep": pale_keep_chest_item_table}


# Helper function to create the class specific locations for the given kingdom locations
# Excludes chests as those aren't character specific checks ever
def create_class_kingdom_locations(class_location, kingdom_table):
    global location_id

    class_location_table = {}
    for kingdom_location in kingdom_table:
        class_location_table[kingdom_location + " - " + class_location] = location_id
        location_id += 1
    return class_location_table


# Helper dictionary to get the locations for the wizard from the kingdom name
wizard_outskirts_table = create_class_kingdom_locations("Wizard", kingdom_outskirts_table)
wizard_crack_table = create_class_kingdom_locations("Wizard", crack_in_the_geode_table)
wizard_nest_table = create_class_kingdom_locations("Wizard", scholars_nest_table)
wizard_arsenal_table = create_class_kingdom_locations("Wizard", kings_arsenal_table)
wizard_darkhouse_table = create_class_kingdom_locations("Wizard", red_darkhouse_table)
wizard_streets_table = create_class_kingdom_locations("Wizard", churchmouse_streets_table)
wizard_lakeside_table = create_class_kingdom_locations("Wizard", emerald_lakeside_table)
wizard_darkhouse_depths_table = create_class_kingdom_locations("Wizard", darkhouse_depths_table)
wizard_atelier_aurum_table = create_class_kingdom_locations("Wizard", atelier_aurum_table)
wizard_subterra_sanctum_table = create_class_kingdom_locations("Wizard", subterra_sanctum_table)
wizard_keep_table = create_class_kingdom_locations("Wizard", pale_keep_table)
wizard_pinnacle_table = create_class_kingdom_locations("Wizard", moonlit_pinnacle_table)
wizard_tables = {
    "Kingdom Outskirts": wizard_outskirts_table,
    "Crack in the Geode": wizard_crack_table,
    "Scholar's Nest": wizard_nest_table,
    "King's Arsenal": wizard_arsenal_table,
    "Red Darkhouse": wizard_darkhouse_table,
    "Churchmouse Streets": wizard_streets_table,
    "Emerald Lakeside": wizard_lakeside_table,
    "Darkhouse Depths": wizard_darkhouse_depths_table,
    "Atelier Aurum": wizard_atelier_aurum_table,
    "Subterra Sanctum": wizard_subterra_sanctum_table,
    "The Pale Keep": wizard_keep_table,
    "Moonlit Pinnacle": wizard_pinnacle_table
}

# Helper dictionary to get the locations for the assassin from the kingdom name
assassin_outskirts_table = create_class_kingdom_locations("Assassin", kingdom_outskirts_table)
assassin_crack_table = create_class_kingdom_locations("Assassin", crack_in_the_geode_table)
assassin_nest_table = create_class_kingdom_locations("Assassin", scholars_nest_table)
assassin_arsenal_table = create_class_kingdom_locations("Assassin", kings_arsenal_table)
assassin_darkhouse_table = create_class_kingdom_locations("Assassin", red_darkhouse_table)
assassin_streets_table = create_class_kingdom_locations("Assassin", churchmouse_streets_table)
assassin_lakeside_table = create_class_kingdom_locations("Assassin", emerald_lakeside_table)
assassin_darkhouse_depths_table = create_class_kingdom_locations("Assassin", darkhouse_depths_table)
assassin_atelier_aurum_table = create_class_kingdom_locations("Assassin", atelier_aurum_table)
assassin_subterra_sanctum_table = create_class_kingdom_locations("Assassin", subterra_sanctum_table)
assassin_keep_table = create_class_kingdom_locations("Assassin", pale_keep_table)
assassin_pinnacle_table = create_class_kingdom_locations("Assassin", moonlit_pinnacle_table)
assassin_tables = {
    "Kingdom Outskirts": assassin_outskirts_table,
    "Crack in the Geode": assassin_crack_table,
    "Scholar's Nest": assassin_nest_table,
    "King's Arsenal": assassin_arsenal_table,
    "Red Darkhouse": assassin_darkhouse_table,
    "Churchmouse Streets": assassin_streets_table,
    "Emerald Lakeside": assassin_lakeside_table,
    "Darkhouse Depths": assassin_darkhouse_depths_table,
    "Atelier Aurum": assassin_atelier_aurum_table,
    "Subterra Sanctum": assassin_subterra_sanctum_table,
    "The Pale Keep": assassin_keep_table,
    "Moonlit Pinnacle": assassin_pinnacle_table
}

# Helper dictionary to get the locations for the heavyblade from the kingdom name
heavyblade_outskirts_table = create_class_kingdom_locations("Heavyblade", kingdom_outskirts_table)
heavyblade_crack_table = create_class_kingdom_locations("Heavyblade", crack_in_the_geode_table)
heavyblade_nest_table = create_class_kingdom_locations("Heavyblade", scholars_nest_table)
heavyblade_arsenal_table = create_class_kingdom_locations("Heavyblade", kings_arsenal_table)
heavyblade_darkhouse_table = create_class_kingdom_locations("Heavyblade", red_darkhouse_table)
heavyblade_streets_table = create_class_kingdom_locations("Heavyblade", churchmouse_streets_table)
heavyblade_lakeside_table = create_class_kingdom_locations("Heavyblade", emerald_lakeside_table)
heavyblade_darkhouse_depths_table = create_class_kingdom_locations("Heavyblade", darkhouse_depths_table)
heavyblade_atelier_aurum_table = create_class_kingdom_locations("Heavyblade", atelier_aurum_table)
heavyblade_subterra_sanctum_table = create_class_kingdom_locations("Heavyblade", subterra_sanctum_table)
heavyblade_keep_table = create_class_kingdom_locations("Heavyblade", pale_keep_table)
heavyblade_pinnacle_table = create_class_kingdom_locations("Heavyblade", moonlit_pinnacle_table)
heavyblade_tables = {
    "Kingdom Outskirts": heavyblade_outskirts_table,
    "Crack in the Geode": heavyblade_crack_table,
    "Scholar's Nest": heavyblade_nest_table,
    "King's Arsenal": heavyblade_arsenal_table,
    "Red Darkhouse": heavyblade_darkhouse_table,
    "Churchmouse Streets": heavyblade_streets_table,
    "Emerald Lakeside": heavyblade_lakeside_table,
    "Darkhouse Depths": heavyblade_darkhouse_depths_table,
    "Atelier Aurum": heavyblade_atelier_aurum_table,
    "Subterra Sanctum": heavyblade_subterra_sanctum_table,
    "The Pale Keep": heavyblade_keep_table,
    "Moonlit Pinnacle": heavyblade_pinnacle_table
}

# Helper dictionary to get the locations for the dancer from the kingdom name
dancer_outskirts_table = create_class_kingdom_locations("Dancer", kingdom_outskirts_table)
dancer_crack_table = create_class_kingdom_locations("Dancer", crack_in_the_geode_table)
dancer_nest_table = create_class_kingdom_locations("Dancer", scholars_nest_table)
dancer_arsenal_table = create_class_kingdom_locations("Dancer", kings_arsenal_table)
dancer_darkhouse_table = create_class_kingdom_locations("Dancer", red_darkhouse_table)
dancer_streets_table = create_class_kingdom_locations("Dancer", churchmouse_streets_table)
dancer_lakeside_table = create_class_kingdom_locations("Dancer", emerald_lakeside_table)
dancer_darkhouse_depths_table = create_class_kingdom_locations("Dancer", darkhouse_depths_table)
dancer_atelier_aurum_table = create_class_kingdom_locations("Dancer", atelier_aurum_table)
dancer_subterra_sanctum_table = create_class_kingdom_locations("Dancer", subterra_sanctum_table)
dancer_keep_table = create_class_kingdom_locations("Dancer", pale_keep_table)
dancer_pinnacle_table = create_class_kingdom_locations("Dancer", moonlit_pinnacle_table)
dancer_tables = {
    "Kingdom Outskirts": dancer_outskirts_table,
    "Crack in the Geode": dancer_crack_table,
    "Scholar's Nest": dancer_nest_table,
    "King's Arsenal": dancer_arsenal_table,
    "Red Darkhouse": dancer_darkhouse_table,
    "Churchmouse Streets": dancer_streets_table,
    "Emerald Lakeside": dancer_lakeside_table,
    "Darkhouse Depths": dancer_darkhouse_depths_table,
    "Atelier Aurum": dancer_atelier_aurum_table,
    "Subterra Sanctum": dancer_subterra_sanctum_table,
    "The Pale Keep": dancer_keep_table,
    "Moonlit Pinnacle": dancer_pinnacle_table
}

# Helper dictionary to get the locations for the druid from the kingdom name
druid_outskirts_table = create_class_kingdom_locations("Druid", kingdom_outskirts_table)
druid_crack_table = create_class_kingdom_locations("Druid", crack_in_the_geode_table)
druid_nest_table = create_class_kingdom_locations("Druid", scholars_nest_table)
druid_arsenal_table = create_class_kingdom_locations("Druid", kings_arsenal_table)
druid_darkhouse_table = create_class_kingdom_locations("Druid", red_darkhouse_table)
druid_streets_table = create_class_kingdom_locations("Druid", churchmouse_streets_table)
druid_lakeside_table = create_class_kingdom_locations("Druid", emerald_lakeside_table)
druid_darkhouse_depths_table = create_class_kingdom_locations("Druid", darkhouse_depths_table)
druid_atelier_aurum_table = create_class_kingdom_locations("Druid", atelier_aurum_table)
druid_subterra_sanctum_table = create_class_kingdom_locations("Druid", subterra_sanctum_table)
druid_keep_table = create_class_kingdom_locations("Druid", pale_keep_table)
druid_pinnacle_table = create_class_kingdom_locations("Druid", moonlit_pinnacle_table)
druid_tables = {
    "Kingdom Outskirts": druid_outskirts_table,
    "Crack in the Geode": druid_crack_table,
    "Scholar's Nest": druid_nest_table,
    "King's Arsenal": druid_arsenal_table,
    "Red Darkhouse": druid_darkhouse_table,
    "Churchmouse Streets": druid_streets_table,
    "Emerald Lakeside": druid_lakeside_table,
    "Darkhouse Depths": druid_darkhouse_depths_table,
    "Atelier Aurum": druid_atelier_aurum_table,
    "Subterra Sanctum": druid_subterra_sanctum_table,
    "The Pale Keep": druid_keep_table,
    "Moonlit Pinnacle": druid_pinnacle_table
}

# Helper dictionary to get the locations for the spellsword from the kingdom name
spellsword_outskirts_table = create_class_kingdom_locations("Spellsword", kingdom_outskirts_table)
spellsword_crack_table = create_class_kingdom_locations("Spellsword", crack_in_the_geode_table)
spellsword_nest_table = create_class_kingdom_locations("Spellsword", scholars_nest_table)
spellsword_arsenal_table = create_class_kingdom_locations("Spellsword", kings_arsenal_table)
spellsword_darkhouse_table = create_class_kingdom_locations("Spellsword", red_darkhouse_table)
spellsword_streets_table = create_class_kingdom_locations("Spellsword", churchmouse_streets_table)
spellsword_lakeside_table = create_class_kingdom_locations("Spellsword", emerald_lakeside_table)
spellsword_darkhouse_depths_table = create_class_kingdom_locations("Spellsword", darkhouse_depths_table)
spellsword_atelier_aurum_table = create_class_kingdom_locations("Spellsword", atelier_aurum_table)
spellsword_subterra_sanctum_table = create_class_kingdom_locations("Spellsword", subterra_sanctum_table)
spellsword_keep_table = create_class_kingdom_locations("Spellsword", pale_keep_table)
spellsword_pinnacle_table = create_class_kingdom_locations("Spellsword", moonlit_pinnacle_table)
spellsword_tables = {
    "Kingdom Outskirts": spellsword_outskirts_table,
    "Crack in the Geode": spellsword_crack_table,
    "Scholar's Nest": spellsword_nest_table,
    "King's Arsenal": spellsword_arsenal_table,
    "Red Darkhouse": spellsword_darkhouse_table,
    "Churchmouse Streets": spellsword_streets_table,
    "Emerald Lakeside": spellsword_lakeside_table,
    "Darkhouse Depths": spellsword_darkhouse_depths_table,
    "Atelier Aurum": spellsword_atelier_aurum_table,
    "Subterra Sanctum": spellsword_subterra_sanctum_table,
    "The Pale Keep": spellsword_keep_table,
    "Moonlit Pinnacle": spellsword_pinnacle_table
}

# Helper dictionary to get the locations for the sniper from the kingdom name
sniper_outskirts_table = create_class_kingdom_locations("Sniper", kingdom_outskirts_table)
sniper_crack_table = create_class_kingdom_locations("Sniper", crack_in_the_geode_table)
sniper_nest_table = create_class_kingdom_locations("Sniper", scholars_nest_table)
sniper_arsenal_table = create_class_kingdom_locations("Sniper", kings_arsenal_table)
sniper_darkhouse_table = create_class_kingdom_locations("Sniper", red_darkhouse_table)
sniper_streets_table = create_class_kingdom_locations("Sniper", churchmouse_streets_table)
sniper_lakeside_table = create_class_kingdom_locations("Sniper", emerald_lakeside_table)
sniper_darkhouse_depths_table = create_class_kingdom_locations("Sniper", darkhouse_depths_table)
sniper_atelier_aurum_table = create_class_kingdom_locations("Sniper", atelier_aurum_table)
sniper_subterra_sanctum_table = create_class_kingdom_locations("Sniper", subterra_sanctum_table)
sniper_keep_table = create_class_kingdom_locations("Sniper", pale_keep_table)
sniper_pinnacle_table = create_class_kingdom_locations("Sniper", moonlit_pinnacle_table)
sniper_tables = {
    "Kingdom Outskirts": sniper_outskirts_table,
    "Crack in the Geode": sniper_crack_table,
    "Scholar's Nest": sniper_nest_table,
    "King's Arsenal": sniper_arsenal_table,
    "Red Darkhouse": sniper_darkhouse_table,
    "Churchmouse Streets": sniper_streets_table,
    "Emerald Lakeside": sniper_lakeside_table,
    "Darkhouse Depths": sniper_darkhouse_depths_table,
    "Atelier Aurum": sniper_atelier_aurum_table,
    "Subterra Sanctum": sniper_subterra_sanctum_table,
    "The Pale Keep": sniper_keep_table,
    "Moonlit Pinnacle": sniper_pinnacle_table
}

# Helper dictionary to get the locations for the bruiser from the kingdom name
bruiser_outskirts_table = create_class_kingdom_locations("Bruiser", kingdom_outskirts_table)
bruiser_crack_table = create_class_kingdom_locations("Bruiser", crack_in_the_geode_table)
bruiser_nest_table = create_class_kingdom_locations("Bruiser", scholars_nest_table)
bruiser_arsenal_table = create_class_kingdom_locations("Bruiser", kings_arsenal_table)
bruiser_darkhouse_table = create_class_kingdom_locations("Bruiser", red_darkhouse_table)
bruiser_streets_table = create_class_kingdom_locations("Bruiser", churchmouse_streets_table)
bruiser_lakeside_table = create_class_kingdom_locations("Bruiser", emerald_lakeside_table)
bruiser_darkhouse_depths_table = create_class_kingdom_locations("Bruiser", darkhouse_depths_table)
bruiser_atelier_aurum_table = create_class_kingdom_locations("Bruiser", atelier_aurum_table)
bruiser_subterra_sanctum_table = create_class_kingdom_locations("Bruiser", subterra_sanctum_table)
bruiser_keep_table = create_class_kingdom_locations("Bruiser", pale_keep_table)
bruiser_pinnacle_table = create_class_kingdom_locations("Bruiser", moonlit_pinnacle_table)
bruiser_tables = {
    "Kingdom Outskirts": bruiser_outskirts_table,
    "Crack in the Geode": bruiser_crack_table,
    "Scholar's Nest": bruiser_nest_table,
    "King's Arsenal": bruiser_arsenal_table,
    "Red Darkhouse": bruiser_darkhouse_table,
    "Churchmouse Streets": bruiser_streets_table,
    "Emerald Lakeside": bruiser_lakeside_table,
    "Darkhouse Depths": bruiser_darkhouse_depths_table,
    "Atelier Aurum": bruiser_atelier_aurum_table,
    "Subterra Sanctum": bruiser_subterra_sanctum_table,
    "The Pale Keep": bruiser_keep_table,
    "Moonlit Pinnacle": bruiser_pinnacle_table
}

# Helper dictionary to get the locations for the defender from the kingdom name
defender_outskirts_table = create_class_kingdom_locations("Defender", kingdom_outskirts_table)
defender_crack_table = create_class_kingdom_locations("Defender", crack_in_the_geode_table)
defender_nest_table = create_class_kingdom_locations("Defender", scholars_nest_table)
defender_arsenal_table = create_class_kingdom_locations("Defender", kings_arsenal_table)
defender_darkhouse_table = create_class_kingdom_locations("Defender", red_darkhouse_table)
defender_streets_table = create_class_kingdom_locations("Defender", churchmouse_streets_table)
defender_lakeside_table = create_class_kingdom_locations("Defender", emerald_lakeside_table)
defender_darkhouse_depths_table = create_class_kingdom_locations("Defender", darkhouse_depths_table)
defender_atelier_aurum_table = create_class_kingdom_locations("Defender", atelier_aurum_table)
defender_subterra_sanctum_table = create_class_kingdom_locations("Defender", subterra_sanctum_table)
defender_keep_table = create_class_kingdom_locations("Defender", pale_keep_table)
defender_pinnacle_table = create_class_kingdom_locations("Defender", moonlit_pinnacle_table)
defender_tables = {
    "Kingdom Outskirts": defender_outskirts_table,
    "Crack in the Geode": defender_crack_table,
    "Scholar's Nest": defender_nest_table,
    "King's Arsenal": defender_arsenal_table,
    "Red Darkhouse": defender_darkhouse_table,
    "Churchmouse Streets": defender_streets_table,
    "Emerald Lakeside": defender_lakeside_table,
    "Darkhouse Depths": defender_darkhouse_depths_table,
    "Atelier Aurum": defender_atelier_aurum_table,
    "Subterra Sanctum": defender_subterra_sanctum_table,
    "The Pale Keep": defender_keep_table,
    "Moonlit Pinnacle": defender_pinnacle_table
}

# Helper dictionary to get the locations for the ancient from the kingdom name
ancient_outskirts_table = create_class_kingdom_locations("Ancient", kingdom_outskirts_table)
ancient_crack_table = create_class_kingdom_locations("Ancient", crack_in_the_geode_table)
ancient_nest_table = create_class_kingdom_locations("Ancient", scholars_nest_table)
ancient_arsenal_table = create_class_kingdom_locations("Ancient", kings_arsenal_table)
ancient_darkhouse_table = create_class_kingdom_locations("Ancient", red_darkhouse_table)
ancient_streets_table = create_class_kingdom_locations("Ancient", churchmouse_streets_table)
ancient_lakeside_table = create_class_kingdom_locations("Ancient", emerald_lakeside_table)
ancient_darkhouse_depths_table = create_class_kingdom_locations("Ancient", darkhouse_depths_table)
ancient_atelier_aurum_table = create_class_kingdom_locations("Ancient", atelier_aurum_table)
ancient_subterra_sanctum_table = create_class_kingdom_locations("Ancient", subterra_sanctum_table)
ancient_keep_table = create_class_kingdom_locations("Ancient", pale_keep_table)
ancient_pinnacle_table = create_class_kingdom_locations("Ancient", moonlit_pinnacle_table)
ancient_tables = {
    "Kingdom Outskirts": ancient_outskirts_table,
    "Crack in the Geode": ancient_crack_table,
    "Scholar's Nest": ancient_nest_table,
    "King's Arsenal": ancient_arsenal_table,
    "Red Darkhouse": ancient_darkhouse_table,
    "Churchmouse Streets": ancient_streets_table,
    "Emerald Lakeside": ancient_lakeside_table,
    "Darkhouse Depths": ancient_darkhouse_depths_table,
    "Atelier Aurum": ancient_atelier_aurum_table,
    "Subterra Sanctum": ancient_subterra_sanctum_table,
    "The Pale Keep": ancient_keep_table,
    "Moonlit Pinnacle": ancient_pinnacle_table
}

# Helper dictionary to get the locations for the hammermaid from the kingdom name
hammermaid_outskirts_table = create_class_kingdom_locations("Hammermaid", kingdom_outskirts_table)
hammermaid_crack_table = create_class_kingdom_locations("Hammermaid", crack_in_the_geode_table)
hammermaid_nest_table = create_class_kingdom_locations("Hammermaid", scholars_nest_table)
hammermaid_arsenal_table = create_class_kingdom_locations("Hammermaid", kings_arsenal_table)
hammermaid_darkhouse_table = create_class_kingdom_locations("Hammermaid", red_darkhouse_table)
hammermaid_streets_table = create_class_kingdom_locations("Hammermaid", churchmouse_streets_table)
hammermaid_lakeside_table = create_class_kingdom_locations("Hammermaid", emerald_lakeside_table)
hammermaid_darkhouse_depths_table = create_class_kingdom_locations("Hammermaid", darkhouse_depths_table)
hammermaid_atelier_aurum_table = create_class_kingdom_locations("Hammermaid", atelier_aurum_table)
hammermaid_subterra_sanctum_table = create_class_kingdom_locations("Hammermaid", subterra_sanctum_table)
hammermaid_keep_table = create_class_kingdom_locations("Hammermaid", pale_keep_table)
hammermaid_pinnacle_table = create_class_kingdom_locations("Hammermaid", moonlit_pinnacle_table)
hammermaid_tables = {
    "Kingdom Outskirts": hammermaid_outskirts_table,
    "Crack in the Geode": hammermaid_crack_table,
    "Scholar's Nest": hammermaid_nest_table,
    "King's Arsenal": hammermaid_arsenal_table,
    "Red Darkhouse": hammermaid_darkhouse_table,
    "Churchmouse Streets": hammermaid_streets_table,
    "Emerald Lakeside": hammermaid_lakeside_table,
    "Darkhouse Depths": hammermaid_darkhouse_depths_table,
    "Atelier Aurum": hammermaid_atelier_aurum_table,
    "Subterra Sanctum": hammermaid_subterra_sanctum_table,
    "The Pale Keep": hammermaid_keep_table,
    "Moonlit Pinnacle": hammermaid_pinnacle_table
}

# Helper dictionary to get the locations for the pyromancer from the kingdom name
pyromancer_outskirts_table = create_class_kingdom_locations("Pyromancer", kingdom_outskirts_table)
pyromancer_crack_table = create_class_kingdom_locations("Pyromancer", crack_in_the_geode_table)
pyromancer_nest_table = create_class_kingdom_locations("Pyromancer", scholars_nest_table)
pyromancer_arsenal_table = create_class_kingdom_locations("Pyromancer", kings_arsenal_table)
pyromancer_darkhouse_table = create_class_kingdom_locations("Pyromancer", red_darkhouse_table)
pyromancer_streets_table = create_class_kingdom_locations("Pyromancer", churchmouse_streets_table)
pyromancer_lakeside_table = create_class_kingdom_locations("Pyromancer", emerald_lakeside_table)
pyromancer_darkhouse_depths_table = create_class_kingdom_locations("Pyromancer", darkhouse_depths_table)
pyromancer_atelier_aurum_table = create_class_kingdom_locations("Pyromancer", atelier_aurum_table)
pyromancer_subterra_sanctum_table = create_class_kingdom_locations("Pyromancer", subterra_sanctum_table)
pyromancer_keep_table = create_class_kingdom_locations("Pyromancer", pale_keep_table)
pyromancer_pinnacle_table = create_class_kingdom_locations("Pyromancer", moonlit_pinnacle_table)
pyromancer_tables = {
    "Kingdom Outskirts": pyromancer_outskirts_table,
    "Crack in the Geode": pyromancer_crack_table,
    "Scholar's Nest": pyromancer_nest_table,
    "King's Arsenal": pyromancer_arsenal_table,
    "Red Darkhouse": pyromancer_darkhouse_table,
    "Churchmouse Streets": pyromancer_streets_table,
    "Emerald Lakeside": pyromancer_lakeside_table,
    "Darkhouse Depths": pyromancer_darkhouse_depths_table,
    "Atelier Aurum": pyromancer_atelier_aurum_table,
    "Subterra Sanctum": pyromancer_subterra_sanctum_table,
    "The Pale Keep": pyromancer_keep_table,
    "Moonlit Pinnacle": pyromancer_pinnacle_table
}

# Helper dictionary to get the locations for the grenadier from the kingdom name
grenadier_outskirts_table = create_class_kingdom_locations("Grenadier", kingdom_outskirts_table)
grenadier_crack_table = create_class_kingdom_locations("Grenadier", crack_in_the_geode_table)
grenadier_nest_table = create_class_kingdom_locations("Grenadier", scholars_nest_table)
grenadier_arsenal_table = create_class_kingdom_locations("Grenadier", kings_arsenal_table)
grenadier_darkhouse_table = create_class_kingdom_locations("Grenadier", red_darkhouse_table)
grenadier_streets_table = create_class_kingdom_locations("Grenadier", churchmouse_streets_table)
grenadier_lakeside_table = create_class_kingdom_locations("Grenadier", emerald_lakeside_table)
grenadier_darkhouse_depths_table = create_class_kingdom_locations("Grenadier", darkhouse_depths_table)
grenadier_atelier_aurum_table = create_class_kingdom_locations("Grenadier", atelier_aurum_table)
grenadier_subterra_sanctum_table = create_class_kingdom_locations("Grenadier", subterra_sanctum_table)
grenadier_keep_table = create_class_kingdom_locations("Grenadier", pale_keep_table)
grenadier_pinnacle_table = create_class_kingdom_locations("Grenadier", moonlit_pinnacle_table)
grenadier_tables = {
    "Kingdom Outskirts": grenadier_outskirts_table,
    "Crack in the Geode": grenadier_crack_table,
    "Scholar's Nest": grenadier_nest_table,
    "King's Arsenal": grenadier_arsenal_table,
    "Red Darkhouse": grenadier_darkhouse_table,
    "Churchmouse Streets": grenadier_streets_table,
    "Emerald Lakeside": grenadier_lakeside_table,
    "Darkhouse Depths": grenadier_darkhouse_depths_table,
    "Atelier Aurum": grenadier_atelier_aurum_table,
    "Subterra Sanctum": grenadier_subterra_sanctum_table,
    "The Pale Keep": grenadier_keep_table,
    "Moonlit Pinnacle": grenadier_pinnacle_table
}

# Helper dictionary to get the locations for the shadow from the kingdom name
shadow_outskirts_table = create_class_kingdom_locations("Shadow", kingdom_outskirts_table)
shadow_crack_table = create_class_kingdom_locations("Shadow", crack_in_the_geode_table)
shadow_nest_table = create_class_kingdom_locations("Shadow", scholars_nest_table)
shadow_arsenal_table = create_class_kingdom_locations("Shadow", kings_arsenal_table)
shadow_darkhouse_table = create_class_kingdom_locations("Shadow", red_darkhouse_table)
shadow_streets_table = create_class_kingdom_locations("Shadow", churchmouse_streets_table)
shadow_lakeside_table = create_class_kingdom_locations("Shadow", emerald_lakeside_table)
shadow_darkhouse_depths_table = create_class_kingdom_locations("Shadow", darkhouse_depths_table)
shadow_atelier_aurum_table = create_class_kingdom_locations("Shadow", atelier_aurum_table)
shadow_subterra_sanctum_table = create_class_kingdom_locations("Shadow", subterra_sanctum_table)
shadow_keep_table = create_class_kingdom_locations("Shadow", pale_keep_table)
shadow_pinnacle_table = create_class_kingdom_locations("Shadow", moonlit_pinnacle_table)
shadow_tables = {
    "Kingdom Outskirts": shadow_outskirts_table,
    "Crack in the Geode": shadow_crack_table,
    "Scholar's Nest": shadow_nest_table,
    "King's Arsenal": shadow_arsenal_table,
    "Red Darkhouse": shadow_darkhouse_table,
    "Churchmouse Streets": shadow_streets_table,
    "Emerald Lakeside": shadow_lakeside_table,
    "Darkhouse Depths": shadow_darkhouse_depths_table,
    "Atelier Aurum": shadow_atelier_aurum_table,
    "Subterra Sanctum": shadow_subterra_sanctum_table,
    "The Pale Keep": shadow_keep_table,
    "Moonlit Pinnacle": shadow_pinnacle_table
}

# Helper dictionary to get the locations for a class from their class name
class_tables = {
    "Wizard": wizard_tables,
    "Assassin": assassin_tables,
    "Heavyblade": heavyblade_tables,
    "Dancer": dancer_tables,
    "Druid": druid_tables,
    "Spellsword": spellsword_tables,
    "Sniper": sniper_tables,
    "Bruiser": bruiser_tables,
    "Defender": defender_tables,
    "Ancient": ancient_tables,
    "Hammermaid": hammermaid_tables,
    "Pyromancer": pyromancer_tables,
    "Grenadier": grenadier_tables,
    "Shadow": shadow_tables
}

shop_locations = ["Full Heal Potion Slot", "Level Up Slot", "Potion 1 Slot", "Potion 2 Slot", "Potion 3 Slot",
                  "Primary Upgrade Slot", "Secondary Upgrade Slot", "Special Upgrade Slot", "Defensive Upgrade Slot"]
global_shop_table = {}
for location in shop_locations:
    global_shop_table[location] = location_id
    location_id += 1
scholars_nest_shop_table = {}
for location in shop_locations:
    scholars_nest_shop_table["Scholar's Nest Shop " + location] = location_id
    location_id += 1
kings_arsenal_shop_table = {}
for location in shop_locations:
    kings_arsenal_shop_table["King's Arsenal Shop " + location] = location_id
    location_id += 1
red_darkhouse_shop_table = {}
for location in shop_locations:
    red_darkhouse_shop_table["Red Darkhouse Shop " + location] = location_id
    location_id += 1
churchmouse_streets_shop_table = {}
for location in shop_locations:
    churchmouse_streets_shop_table["Churchmouse Streets Shop " + location] = location_id
    location_id += 1
emerald_lakeside_shop_table = {}
for location in shop_locations:
    emerald_lakeside_shop_table["Emerald Lakeside Shop " + location] = location_id
    location_id += 1
darkhouse_depths_shop_table = {}
for location in shop_locations:
    darkhouse_depths_shop_table["Darkhouse Depths Shop " + location] = location_id
    location_id += 1
atelier_aurum_shop_table = {}
for location in shop_locations:
    atelier_aurum_shop_table["Atelier Aurum Shop " + location] = location_id
    location_id += 1
subterra_sanctum_shop_table = {}
for location in shop_locations:
    subterra_sanctum_shop_table["Subterra Sanctum Shop " + location] = location_id
    location_id += 1
pale_keep_shop_table = {}
for location in shop_locations:
    pale_keep_shop_table["The Pale Keep Shop " + location] = location_id
    location_id += 1

kingdom_to_shop_locations = {"Scholar's Nest": scholars_nest_shop_table,
                             "King's Arsenal": kings_arsenal_shop_table,
                             "Red Darkhouse": red_darkhouse_shop_table,
                             "Churchmouse Streets": churchmouse_streets_shop_table,
                             "Emerald Lakeside": emerald_lakeside_shop_table,
                             "Darkhouse Depths": darkhouse_depths_shop_table,
                             "Atelier Aurum": atelier_aurum_shop_table,
                             "Subterra Sanctum": subterra_sanctum_shop_table,
                             "The Pale Keep": pale_keep_shop_table}

# Dictionary that contains all the locations
location_table = kingdom_outskirts_table | scholars_nest_table | kings_arsenal_table | red_darkhouse_table | \
                 churchmouse_streets_table | emerald_lakeside_table | pale_keep_table | moonlit_pinnacle_table | \
                 crack_in_the_geode_table | darkhouse_depths_table | subterra_sanctum_shop_table | atelier_aurum_table | \
                 kingdom_outskirts_chest_item_table | crack_in_the_geode_chest_item_table | scholars_nest_chest_item_table | kings_arsenal_chest_item_table | \
                 red_darkhouse_chest_item_table | churchmouse_streets_chest_item_table | emerald_lakeside_chest_item_table | pale_keep_chest_item_table | \
                 darkhouse_depths_chest_item_table | atelier_aurum_chest_item_table | subterra_sanctum_chest_item_table | \
                 wizard_outskirts_table | wizard_nest_table | wizard_arsenal_table | \
                 wizard_darkhouse_table | wizard_streets_table | wizard_lakeside_table | wizard_keep_table | \
                 wizard_pinnacle_table | assassin_outskirts_table | assassin_nest_table | assassin_arsenal_table | \
                 assassin_darkhouse_table | assassin_streets_table | assassin_lakeside_table | assassin_keep_table | \
                 assassin_pinnacle_table | heavyblade_outskirts_table | heavyblade_nest_table | heavyblade_arsenal_table | \
                 heavyblade_darkhouse_table | heavyblade_streets_table | heavyblade_lakeside_table | heavyblade_keep_table | \
                 heavyblade_pinnacle_table | dancer_outskirts_table | dancer_nest_table | dancer_arsenal_table | \
                 dancer_darkhouse_table | dancer_streets_table | dancer_lakeside_table | dancer_keep_table | \
                 dancer_pinnacle_table | druid_outskirts_table | druid_nest_table | druid_arsenal_table | \
                 druid_darkhouse_table | druid_streets_table | druid_lakeside_table | druid_keep_table | druid_pinnacle_table | \
                 spellsword_outskirts_table | spellsword_nest_table | spellsword_arsenal_table | spellsword_darkhouse_table | \
                 spellsword_streets_table | spellsword_lakeside_table | spellsword_keep_table | spellsword_pinnacle_table | \
                 sniper_outskirts_table | sniper_nest_table | sniper_arsenal_table | sniper_darkhouse_table | \
                 sniper_streets_table | sniper_lakeside_table | sniper_keep_table | sniper_pinnacle_table | \
                 bruiser_outskirts_table | bruiser_nest_table | bruiser_arsenal_table | bruiser_darkhouse_table | \
                 bruiser_streets_table | bruiser_lakeside_table | bruiser_keep_table | bruiser_pinnacle_table | \
                 defender_outskirts_table | defender_nest_table | defender_arsenal_table | defender_darkhouse_table | \
                 defender_streets_table | defender_lakeside_table | defender_keep_table | defender_pinnacle_table | \
                 ancient_outskirts_table | ancient_nest_table | ancient_arsenal_table | ancient_darkhouse_table | \
                 ancient_streets_table | ancient_lakeside_table | ancient_keep_table | ancient_pinnacle_table | \
                 hammermaid_outskirts_table | hammermaid_nest_table | hammermaid_arsenal_table | hammermaid_darkhouse_table | \
                 hammermaid_streets_table | hammermaid_lakeside_table | hammermaid_keep_table | hammermaid_pinnacle_table | \
                 pyromancer_outskirts_table | pyromancer_nest_table | pyromancer_arsenal_table | pyromancer_darkhouse_table | \
                 pyromancer_streets_table | pyromancer_lakeside_table | pyromancer_keep_table | pyromancer_pinnacle_table | \
                 grenadier_outskirts_table | grenadier_nest_table | grenadier_arsenal_table | grenadier_darkhouse_table | \
                 grenadier_streets_table | grenadier_lakeside_table | grenadier_keep_table | grenadier_pinnacle_table | \
                 shadow_outskirts_table | shadow_nest_table | shadow_arsenal_table | shadow_darkhouse_table | \
                 shadow_streets_table | shadow_lakeside_table | shadow_keep_table | shadow_pinnacle_table | \
                 global_shop_table | scholars_nest_shop_table | kings_arsenal_shop_table | red_darkhouse_shop_table | \
                 churchmouse_streets_shop_table | emerald_lakeside_shop_table | pale_keep_shop_table | \
                 darkhouse_depths_shop_table | atelier_aurum_shop_table | subterra_sanctum_shop_table
