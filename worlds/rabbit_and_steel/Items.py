from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .World import RabbitAndSteelWorld


class RabbitAndSteelItem(Item):
    game: str = "Rabbit and Steel"
    item_type: str = ""

    def set_type(self, type_name: str):
        self.item_type = type_name

    def is_type(self, type_name: str):
        return self.item_type == type_name


def get_random_filler_item_name(world: RabbitAndSteelWorld) -> str:
    if world.random.randint(0, 99) < -1:
        return "future trap"

    # TODO: split between all filler items
    return "Gold"


def create_item_with_classification(world: RabbitAndSteelWorld, name: str) -> RabbitAndSteelItem:
    classification = get_classification(name)

    # TODO update classification that change with options

    return RabbitAndSteelItem(name, classification, item_table[name], world.player)


def get_classification(name: str) -> ItemClassification:
    if name in kingdom_items.keys():
        return ItemClassification.progression
    elif name in class_items.keys():
        return ItemClassification.progression
    elif name in other_progression_items.keys():
        return ItemClassification.progression_skip_balancing
    elif name in useful_items.keys():
        return ItemClassification.useful
    elif name in itemset_items.keys():
        return ItemClassification.useful
    elif name in upgrade_items.keys():
        return ItemClassification.useful
    elif name in specific_upgrade_items.keys():
        return ItemClassification.useful
    elif name in potion_items.keys():
        return ItemClassification.useful
    return ItemClassification.filler


def create_all_items(world: RabbitAndSteelWorld) -> None:
    kingdom_sanity = world.options.kingdom_sanity.value
    excluded_kingdoms = world.options.excluded_kingdoms.value
    exclude_class = world.options.exclude_class.value

    itempool: list[RabbitAndSteelItem] = []

    if kingdom_sanity:
        for kingdom in kingdom_items:
            if kingdom in excluded_kingdoms:
                continue
            itempool += [world.create_item_with_type(kingdom, "Kingdoms")]

    progressive_regions = world.options.progressive_regions.value
    max_kingdoms_per_run = world.options.max_kingdoms_per_run.value

    if progressive_regions:
        for i in range(max_kingdoms_per_run + 2):
            itempool += [world.create_item("Progressive Region")]

    class_sanity = world.options.class_sanity.value

    if class_sanity:
        for class_item in class_items:
            if class_item in exclude_class:
                continue
            if class_item == world.starting_class_name:
                continue
            itempool += [world.create_item_with_type(class_item, "Classes")]

    shuffle_itemsets = world.options.shuffle_item_sets.value
    if shuffle_itemsets:
        for itemset_item in itemset_items:
            itempool += [world.create_item(itemset_item)]

    create_real_item_chests = world.options.checks_per_item_in_chest.value  # logical or shuffle individual items (might not actually want that)

    num_real_chests = 6
    if create_real_item_chests:
        for i in range(num_real_chests):
            itempool += [world.create_item("Treasuresphere")]

    upgrade_sanity = world.options.upgrade_sanity
    if upgrade_sanity == "simple":
        for upgrade_item in upgrade_items:
            itempool += [world.create_item(upgrade_item)]
    elif upgrade_sanity == "full":
        for upgrade_item in specific_upgrade_items:
            itempool += [world.create_item(upgrade_item)]

    potion_sanity = world.options.potion_sanity
    if potion_sanity != "none":
        for potion_item in potion_items:
            itempool += [world.create_item(potion_item)]

    number_of_items = len(itempool)

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    if world.options.goal_condition == world.options.goal_condition.option_shira:
        number_of_unfilled_locations -= (len(class_items) - len(exclude_class))

    itempool += [world.create_filler() for _ in range(number_of_unfilled_locations - number_of_items)]

    world.multiworld.itempool += itempool


item_id = 1

kingdom_names = [
    "Scholar's Nest", "King's Arsenal", "Red Darkhouse", "Churchmouse Streets", "Emerald Lakeside", "The Pale Keep",
    "Moonlit Pinnacle"]
kingdom_items = {}
for item in kingdom_names:
    kingdom_items[item] = item_id
    item_id += 1

class_names = ["Wizard", "Assassin", "Heavyblade", "Dancer", "Druid", "Spellsword", "Sniper", "Bruiser", "Defender",
               "Ancient"]
class_items = {}
for item in class_names:
    class_items[item] = item_id
    item_id += 1

itemset_names = [
    "Arcane Set", "Night Set", "Timespace Set", "Wind Set", "Bloodwolf Set", "Assassin Set", "Rockdragon Set",
    "Flame Set", "Gem Set", "Lightning Set", "Shrine Set", "Lucky Set", "Life Set", "Poison Set", "Depth Set",
    "Darkbite Set", "Timegem Set", "Youkai Set", "Haunted Set", "Gladiator Set", "Sparkblade Set", "Swiftflight Set",
    "Sacredflame Set", "Ruins Set", "Lakeshrine Set"]
itemset_items = {}
for item in itemset_names:
    itemset_items[item] = item_id
    item_id += 1

upgrade_names = ["Emerald Gem", "Garnet Gem", "Ruby Gem", "Sapphire Gem", "Opal Gem"]
upgrade_items = {}
for item in upgrade_names:
    upgrade_items[item] = item_id
    item_id += 1

specific_upgrade_names = [
    "Primary Emerald Gem", "Primary Garnet Gem", "Primary Ruby Gem", "Primary Sapphire Gem", "Primary Opal Gem",
    "Secondary Emerald Gem", "Secondary Garnet Gem", "Secondary Ruby Gem", "Secondary Sapphire Gem", "Secondary Opal Gem",
    "Special Emerald Gem", "Special Garnet Gem", "Special Ruby Gem", "Special Sapphire Gem", "Special Opal Gem",
    "Defensive Emerald Gem", "Defensive Garnet Gem", "Defensive Ruby Gem", "Defensive Sapphire Gem",
    "Defensive Opal Gem"]
specific_upgrade_items = {}
for item in specific_upgrade_names:
    specific_upgrade_items[item] = item_id
    item_id += 1

potion_names = [
    "Full Heal Potion", "Level Up Potion", "Regen Potion", "Essence of Spell", "Darkness Potion", "Quickening Potion",
    "Winged Potion", "Essence of Wit", "Swifthand Potion", "Fire Potion", "Strength Potion", "Gold Potion",
    "Luck Potion", "Essence of Steel", "Evasion Potion", "Longarm Potion", "Vitality Potion"]
potion_items = {}
for item in potion_names:
    potion_items[item] = item_id
    item_id += 1

shira_defeat_names = [
    "Victory - Wizard", "Victory - Assassin", "Victory - Heavyblade", "Victory - Dancer", "Victory - Druid",
    "Victory - Spellsword",
    "Victory - Sniper", "Victory - Bruiser", "Victory - Defender", "Victory - Ancient"]
shira_defeat_items = {}
for item in shira_defeat_names:
    shira_defeat_items[item] = item_id
    item_id += 1

other_progression_items = {
    "Progressive Region": item_id,
}
item_id += 1

useful_items = {
    "XP": item_id,
    "Treasuresphere": item_id + 1,
}
item_id += 2

filler_item = {
    "Gold": item_id,
}
item_id += 1

item_table = kingdom_items | class_items | itemset_items | other_progression_items | useful_items | filler_item | \
    upgrade_items | specific_upgrade_items | potion_items | shira_defeat_items

