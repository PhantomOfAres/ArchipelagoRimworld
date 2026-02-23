from __future__ import annotations

from dataclasses import dataclass
from typing import Union, Dict, List, TYPE_CHECKING

from Options import Range, DefaultOnToggle, Toggle, OptionCounter, PerGameCommonOptions, \
    Visibility, OptionSet, Choice, OptionGroup

from .Items import class_items, kingdom_items

if TYPE_CHECKING:
    from .World import RabbitAndSteelWorld


class KingdomSanity(DefaultOnToggle):
    """
    Kingdoms must be found before they can be visited
    """
    display_name = "Kingdom Sanity"


class MaxKingdomsPerRun(Range):
    """
    How many kingdoms you visit before heading to the pale keep.
    If progressive regions and/or kingdom sanity is on,
    your run ends in a failure if you are not allowed to visit enough kingdoms.
    """
    display_name = "All Kingdoms"
    range_start = 1
    range_end = 5
    default = 3


class ProgressiveRegions(Toggle):
    """
    Introduces items that increases the amount regions you are currently allowed to visit in a run.
    Includes Pale Keep and Moonlit Pinnacle.
    Outskirts is always accessible.
    """
    display_name = "Progressive Regions"


class ExcludeKingdoms(OptionSet):
    """
    What kingdoms, if any, should not be added to the pool of locations.
    There will always be a generic location that any class can obtain.
    Avaliable Options: [ "Scholar's Nest", "King's Arsenal", "Red Darkhouse", "Churchmouse Streets", "Emerald Lakeside"]
    """
    display_name = "Excluded Kingdoms"
    valid_keys = kingdom_items.keys() - {"The Pale Keep", "Moonlit Pinnacle"}


class UseKingdomOrderWithKingdomSanity(Toggle):
    """
    Introduces another requirement to reaching a kingdom rather than just receiving the item.
    You also need to have at least one kingdom from all the previous orders.
    Kingdom Order is always used if you have Progressive Regions but not Kingdom Sanity,
    so you can't access all kingdoms after receiving one progressive region.
    """
    display_name = "Enforce Kingdom Order With Kingdom Sanity"


class KingdomOrder(OptionCounter):
    """
    Gates visiting a kingdom behind being able to reach the order
    With Progressive Regions, the order directly ties to the number of progressive regions needed
    With Kingdom Sanity, you must be able to visit at least one kingdom in each previous order
    "0" will randomly assign it to an unfilled position if there are no valid positions unfilled,
    it will place it in the last position that doesn't have more than the others.
    Excluded kingdoms are not considered.
    You will be able to choose any kingdom as your first kingdom in a route if logically accessible.
    Throws an error if the number of 'valid' kingdoms is less than 'All Kingdoms'
    """
    display_name = "Kingdom Route Order"
    min = 0
    max = 5
    visibility = Visibility.all
    valid_keys = frozenset([
        "Scholar's Nest",
        "King's Arsenal",
        "Red Darkhouse",
        "Churchmouse Streets",
        "Emerald Lakeside",
        "Darkhouse Depths",
        "Atelier Aurum",
        "Subterra Sanctum"
    ])
    default = {
        "Scholar's Nest": 0,
        "King's Arsenal": 0,
        "Red Darkhouse": 0,
        "Churchmouse Streets": 0,
        "Emerald Lakeside": 0,
        "Darkhouse Depths": 0,
        "Atelier Aurum": 0,
        "Subterra Sanctum": 0
    }


class ClassSanity(Toggle):
    """
    Classes must be found before they can be played
    """
    display_name = "Class Sanity"


class ExcludeClass(OptionSet):
    """
    What class, if any, should not be accounted for in logic.
    Throughout the run you will not be able to play that class at all.
    Avaliable Options:
    ["Wizard", "Assassin", "Heavyblade", "Dancer", "Druid", "Spellsword", "Sniper", "Bruiser", "Defender", "Ancient", "Hammermaid", "Pyromancer", "Grenadier", "Shadow"]
    """
    display_name = "Exclude Class"
    valid_keys = class_items.keys()


class ChecksPerClass(OptionSet):
    """
    What classes should have locations associated with them.
    There will always be a generic location that any class can obtain.
    Available Options:
    ["Wizard", "Assassin", "Heavyblade", "Dancer", "Druid", "Spellsword", "Sniper", "Bruiser", "Defender", "Ancient", "Hammermaid", "Pyromancer", "Grenadier", "Shadow"]
    _ALL can be used to put checks on all classes
    """
    display_name = "Checks Per Class"
    valid_keys = class_items.keys() & {"_ALL"}


class ShuffleItemSets(Toggle):
    """
    Item sets must be found before they can appear in treasure spheres
    """
    display_name = "Shuffle Item Sets"


# TODO add option for modded items


class ChecksPerItemInChest(Toggle):
    """
    Each item in a chest is an archipelago item.
    Shuffles treasure spheres into the item pool.
    Does not add one per class if 'Checks Per Class' is on
    """
    display_name = "Checks Per Item In Chest"


class UpgradeSanity(Choice):
    """
    What is required to have an upgrade appear in a shop, will randomly be chosen between available options still
    None: Any upgrade is always available
    Simple: Just need to get 'Ruby' item to unlock all the Ruby upgrades
    Full: Need to get 'Ruby Primary' item to unlock the ruby upgrade for the primary
    """
    display_name = "Upgrade Sanity"
    option_none = 0
    option_simple = 1
    option_full = 2
    default = 0


class PotionSanity(Choice):
    """
    How the top shelf of the shop appears
    None: Default behavior
    Locked: Hp and level will be in their position when their item is found, and potions are added to the pool as they are found
    Roulette: Randomly fills the slots with unlocked 'potions', meaning hp and level are not guaranteed
    """
    display_name = "Potion Sanity"
    option_none = 0
    option_locked = 1
    option_roulette = 2
    default = 0


class GoalCondition(Choice):
    """
    Set your Goal Condition.
    Shira: Defeat Shira x number of times, which is configured below
    """
    display_name = "Goal Condition"
    option_shira = 1
    default = 1


class ShiraDefeats(Range):
    """
    If goal is set to Shira, how many unique classes must defeat Shira to goal
    """
    display_name = "Required Shira Kills"
    range_start = 1
    range_end = 10
    default = 1


class ShopSanity(Choice):
    """
    Shops contain ap items to purchase, ap item is required to purchase before you can purchase the normal shop item in that slot
    None: Shops do not carry ap items
    Global: Shops carry the same ap items, and only need to be purchased once to unblock that slot
    Regional: Each kingdom contains their own ap items that need to be purchased
    """
    display_name = "Shop Sanity"
    option_none = 0
    option_global = 1
    option_regional = 2
    default = 0


@dataclass
class RabbitAndSteelOptions(PerGameCommonOptions):
    kingdom_sanity: KingdomSanity
    max_kingdoms_per_run: MaxKingdomsPerRun
    progressive_regions: ProgressiveRegions
    excluded_kingdoms: ExcludeKingdoms
    kingdom_sanity_kingdom_order: UseKingdomOrderWithKingdomSanity
    kingdom_order: KingdomOrder
    class_sanity: ClassSanity
    exclude_class: ExcludeClass
    checks_per_class: ChecksPerClass
    shuffle_item_sets: ShuffleItemSets
    checks_per_item_in_chest: ChecksPerItemInChest
    upgrade_sanity: UpgradeSanity
    potion_sanity: PotionSanity
    goal_condition: GoalCondition
    shira_defeats: ShiraDefeats
    shop_sanity: ShopSanity


def get_option_value(world: RabbitAndSteelWorld, player: int, name: str) -> Union[int, Dict, List]:
    option = getattr(world, name, None)
    if option is None:
        return 0

    return option[player].value


# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup(
        "Kingdom Options",
        [KingdomSanity, MaxKingdomsPerRun, ProgressiveRegions, ExcludeKingdoms, UseKingdomOrderWithKingdomSanity,
         KingdomOrder]
    ),
    OptionGroup(
        "Gameplay Options",
        [ClassSanity, ExcludeClass, ChecksPerClass, ShuffleItemSets, ChecksPerItemInChest, UpgradeSanity, PotionSanity,
         ShopSanity],
    ),
    OptionGroup(
        "Goal Options",
        [GoalCondition, ShiraDefeats],
    ),
]

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
# option_presets = {
#     "boring": {
#         "hard_mode": False,
#         "hammer": False,
#         "extra_starting_chest": False,
#         "start_with_one_confetti_cannon": False,
#         "trap_chance": 0,
#         "confetti_explosiveness": ConfettiExplosiveness.range_start,
#         "player_sprite": PlayerSprite.option_human,
#     },
#     "the true way to play": {
#         "hard_mode": True,
#         "hammer": True,
#         "extra_starting_chest": True,
#         "start_with_one_confetti_cannon": True,
#         "trap_chance": 50,
#         "confetti_explosiveness": ConfettiExplosiveness.range_end,
#         "player_sprite": PlayerSprite.option_duck,
#     },
# }
