from __future__ import annotations

from typing import TYPE_CHECKING

from . import Items
from BaseClasses import CollectionState, ItemClassification, LocationProgressType
from worlds.generic.Rules import set_rule, add_item_rule
from .Items import class_names
from .Locations import kingdom_to_locations

if TYPE_CHECKING:
    from .World import RabbitAndSteelWorld

KEEP = "The Pale Keep"
PINNACLE = "Moonlit Pinnacle"
NEST = "Scholar's Nest"
ARSNEAL = "King's Arsenal"
DARKHOUSE = "Red Darkhouse"
STREETS = "Churchmouse Streets"
LAKESIDE = "Emerald Lakeside"
KEEP = "The Pale Keep"
PINNACLE = "Moonlit Pinnacle"

WIZARD = "Wizard"
ASSASSIN = "Assassin"
HEAVYBLADE = "Heavyblade"
DANCER = "Dancer"
DRUID = "Druid"
SPELLSWORD = "Spellsword"
SNIPER = "Sniper"
BRUISER = "Bruiser"
DEFENDER = "Defender"
ANCIENT = "Ancient"


def set_all_rules(world: RabbitAndSteelWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: RabbitAndSteelWorld) -> None:
    kingdom_sanity = world.options.kingdom_sanity
    progressive_regions = world.options.progressive_regions
    excluded_kingdoms = world.options.excluded_kingdoms
    kingdom_sanity_kingdom_order = world.options.kingdom_sanity_kingdom_order
    kingdom_order = world.options.kingdom_order
    max_kingdoms_per_run = world.options.max_kingdoms_per_run
    checks_per_class = world.options.checks_per_class
    class_sanity = world.options.class_sanity

    # Require a class to be unlocked if playing on class sanity
    if class_sanity:
        lobby_to_outskirts = world.get_entrance("Lobby to Kingdom Outskirts")
        set_rule(lobby_to_outskirts, lambda state: state.has_group_unique("Classes", world.player))

    def has_kingdom_sanity_items_to_reach_order(state: CollectionState, our_order: int) -> bool:
        has_prior_kingdom_order = [False for _ in range(our_order - 1)]
        for (kingdom, order) in kingdom_order.items():
            if kingdom in excluded_kingdoms or order == -1:
                continue
            if order >= our_order:
                continue
            if state.has(kingdom, world.player):
                has_prior_kingdom_order[order - 1] = True
        return all(has_prior_kingdom_order)

    def set_kingdoms_connection_rules(state: CollectionState, kingdom: str) -> bool:
        if kingdom_sanity:
            if not state.has(kingdom, world.player):
                return False

            if kingdom_sanity_kingdom_order and not has_kingdom_sanity_items_to_reach_order(state, kingdom_order[kingdom]):
                return False

        if progressive_regions:
            if not kingdom_sanity or kingdom_sanity_kingdom_order:
                return kingdom_order[kingdom] <= state.count("Progressive Region", world.player)
            else:
                return 1 <= state.count("Progressive Region", world.player)

        return True

    if NEST not in excluded_kingdoms:
        outskirts_to_nest = world.get_entrance("Kingdom Outskirts to " + NEST)
        set_rule(outskirts_to_nest, lambda state: set_kingdoms_connection_rules(state, NEST))

    if ARSNEAL not in excluded_kingdoms:
        outskirts_to_king = world.get_entrance("Kingdom Outskirts to " + ARSNEAL)
        set_rule(outskirts_to_king, lambda state: set_kingdoms_connection_rules(state, ARSNEAL))

    if DARKHOUSE not in excluded_kingdoms:
        outskirts_to_red = world.get_entrance("Kingdom Outskirts to " + DARKHOUSE)
        set_rule(outskirts_to_red, lambda state: set_kingdoms_connection_rules(state, DARKHOUSE))

    if STREETS not in excluded_kingdoms:
        outskirts_to_churchmouse = world.get_entrance("Kingdom Outskirts to " + STREETS)
        set_rule(outskirts_to_churchmouse, lambda state: set_kingdoms_connection_rules(state, STREETS))

    if LAKESIDE not in excluded_kingdoms:
        outskirts_to_emerald = world.get_entrance("Kingdom Outskirts to " + LAKESIDE)
        set_rule(outskirts_to_emerald, lambda state: set_kingdoms_connection_rules(state, LAKESIDE))

    # Set the entrance rule for kingdom outskirts to The Pale Keep
    outskirts_to_pale = world.get_entrance("Kingdom Outskirts to " + KEEP)

    def set_pale_keep_rules(state: CollectionState) -> bool:
        if kingdom_sanity:
            if not state.has(KEEP, world.player):
                return False

            if kingdom_sanity_kingdom_order and not has_kingdom_sanity_items_to_reach_order(state, max_kingdoms_per_run + 1):
                return False

            if not kingdom_sanity_kingdom_order and not state.has_group_unique("Kingdoms", world.player, max_kingdoms_per_run + 0):
                return False

        if progressive_regions and max_kingdoms_per_run + 1 > state.count("Progressive Region", world.player):
            return False

        return True

    set_rule(outskirts_to_pale, lambda state: set_pale_keep_rules(state))

    # Set the entrance rule for The Pale Keep to the Moonlit Pinnacle
    pale_to_moonlit = world.get_entrance(KEEP + " to " + PINNACLE)

    def set_moonlit_pinnacle_rules(state: CollectionState) -> bool:
        if kingdom_sanity:
            if not state.has(PINNACLE, world.player):
                return False

        if progressive_regions and max_kingdoms_per_run + 2 > state.count("Progressive Region", world.player):
            return False

        return True

    set_rule(pale_to_moonlit, lambda state: set_moonlit_pinnacle_rules(state))

    # Manually setting class rules, as it doesn't seem to work otherwise
    if class_sanity:
        if WIZARD in checks_per_class:
            outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + WIZARD)
            set_rule(outskirts_to_class, lambda state: state.has(WIZARD, world.player))

            # Set the remaining kingdoms rules
            for kingdom_name in Items.kingdom_names:
                # Skip Moonlit Pinnacle as it has special class rules
                if kingdom_name == PINNACLE:
                    continue

                if kingdom_name not in excluded_kingdoms:
                    kingdom_to_class = world.get_entrance(kingdom_name + " - " + WIZARD)
                    set_rule(kingdom_to_class, lambda state: state.has(WIZARD, world.player))

        if ASSASSIN in checks_per_class:
            outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + ASSASSIN)
            set_rule(outskirts_to_class, lambda state: state.has(ASSASSIN, world.player))

            # Set the remaining kingdoms rules
            for kingdom_name in Items.kingdom_names:
                # Skip Moonlit Pinnacle as it has special class rules
                if kingdom_name == PINNACLE:
                    continue

                if kingdom_name not in excluded_kingdoms:
                    kingdom_to_class = world.get_entrance(kingdom_name + " - " + ASSASSIN)
                    set_rule(kingdom_to_class, lambda state: state.has(ASSASSIN, world.player))

        if HEAVYBLADE in checks_per_class:
            outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + HEAVYBLADE)
            set_rule(outskirts_to_class, lambda state: state.has(HEAVYBLADE, world.player))

            # Set the remaining kingdoms rules
            for kingdom_name in Items.kingdom_names:
                # Skip Moonlit Pinnacle as it has special class rules
                if kingdom_name == PINNACLE:
                    continue

                if kingdom_name not in excluded_kingdoms:
                    kingdom_to_class = world.get_entrance(kingdom_name + " - " + HEAVYBLADE)
                    set_rule(kingdom_to_class, lambda state: state.has(HEAVYBLADE, world.player))

        if DANCER in checks_per_class:
            outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + DANCER)
            set_rule(outskirts_to_class, lambda state: state.has(DANCER, world.player))

            # Set the remaining kingdoms rules
            for kingdom_name in Items.kingdom_names:
                # Skip Moonlit Pinnacle as it has special class rules
                if kingdom_name == PINNACLE:
                    continue

                if kingdom_name not in excluded_kingdoms:
                    kingdom_to_class = world.get_entrance(kingdom_name + " - " + DANCER)
                    set_rule(kingdom_to_class, lambda state: state.has(DANCER, world.player))

        if DRUID in checks_per_class:
            outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + DRUID)
            set_rule(outskirts_to_class, lambda state: state.has(DRUID, world.player))

            # Set the remaining kingdoms rules
            for kingdom_name in Items.kingdom_names:
                # Skip Moonlit Pinnacle as it has special class rules
                if kingdom_name == PINNACLE:
                    continue

                if kingdom_name not in excluded_kingdoms:
                    kingdom_to_class = world.get_entrance(kingdom_name + " - " + DRUID)
                    set_rule(kingdom_to_class, lambda state: state.has(DRUID, world.player))

        if SPELLSWORD in checks_per_class:
            outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + SPELLSWORD)
            set_rule(outskirts_to_class, lambda state: state.has(SPELLSWORD, world.player))

            # Set the remaining kingdoms rules
            for kingdom_name in Items.kingdom_names:
                # Skip Moonlit Pinnacle as it has special class rules
                if kingdom_name == PINNACLE:
                    continue

                if kingdom_name not in excluded_kingdoms:
                    kingdom_to_class = world.get_entrance(kingdom_name + " - " + SPELLSWORD)
                    set_rule(kingdom_to_class, lambda state: state.has(SPELLSWORD, world.player))

        if SNIPER in checks_per_class:
            outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + SNIPER)
            set_rule(outskirts_to_class, lambda state: state.has(SNIPER, world.player))

            # Set the remaining kingdoms rules
            for kingdom_name in Items.kingdom_names:
                # Skip Moonlit Pinnacle as it has special class rules
                if kingdom_name == PINNACLE:
                    continue

                if kingdom_name not in excluded_kingdoms:
                    kingdom_to_class = world.get_entrance(kingdom_name + " - " + SNIPER)
                    set_rule(kingdom_to_class, lambda state: state.has(SNIPER, world.player))

        if BRUISER in checks_per_class:
            outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + BRUISER)
            set_rule(outskirts_to_class, lambda state: state.has(BRUISER, world.player))

            # Set the remaining kingdoms rules
            for kingdom_name in Items.kingdom_names:
                # Skip Moonlit Pinnacle as it has special class rules
                if kingdom_name == PINNACLE:
                    continue

                if kingdom_name not in excluded_kingdoms:
                    kingdom_to_class = world.get_entrance(kingdom_name + " - " + BRUISER)
                    set_rule(kingdom_to_class, lambda state: state.has(BRUISER, world.player))

        if DEFENDER in checks_per_class:
            outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + DEFENDER)
            set_rule(outskirts_to_class, lambda state: state.has(DEFENDER, world.player))

            # Set the remaining kingdoms rules
            for kingdom_name in Items.kingdom_names:
                # Skip Moonlit Pinnacle as it has special class rules
                if kingdom_name == PINNACLE:
                    continue

                if kingdom_name not in excluded_kingdoms:
                    kingdom_to_class = world.get_entrance(kingdom_name + " - " + DEFENDER)
                    set_rule(kingdom_to_class, lambda state: state.has(DEFENDER, world.player))

        if ANCIENT in checks_per_class:
            outskirts_to_class = world.get_entrance("Kingdom Outskirts - " + ANCIENT)
            set_rule(outskirts_to_class, lambda state: state.has(ANCIENT, world.player))

            # Set the remaining kingdoms rules
            for kingdom_name in Items.kingdom_names:
                # Skip Moonlit Pinnacle as it has special class rules
                if kingdom_name == PINNACLE:
                    continue

                if kingdom_name not in excluded_kingdoms:
                    kingdom_to_class = world.get_entrance(kingdom_name + " - " + ANCIENT)
                    set_rule(kingdom_to_class, lambda state: state.has(ANCIENT, world.player))

    # Find the classes that will have checks in the Moonlit Pinnacle
    moonlit_classes = []
    if world.options.goal_condition == world.options.goal_condition.option_shira:
        moonlit_classes = class_names
    elif world.options.checks_per_class:
        moonlit_classes = world.options.checks_per_class

    if class_sanity:
        for moonlit_class in moonlit_classes:
            class_moonlit = world.get_entrance("Moonlit Pinnacle - " + moonlit_class)
            set_rule(class_moonlit, lambda state: state.has(moonlit_class, world.player))

    # Manually add the class rules for Moonlit Pinnacle as passing class_name as state.has() didn't work
    if class_sanity:
        if WIZARD in moonlit_classes:
            class_moonlit = world.get_entrance("Moonlit Pinnacle - " + WIZARD)
            set_rule(class_moonlit, lambda state: state.has(WIZARD, world.player))

        if ASSASSIN in moonlit_classes:
            class_moonlit = world.get_entrance("Moonlit Pinnacle - " + ASSASSIN)
            set_rule(class_moonlit, lambda state: state.has(ASSASSIN, world.player))

        if HEAVYBLADE in moonlit_classes:
            class_moonlit = world.get_entrance("Moonlit Pinnacle - " + HEAVYBLADE)
            set_rule(class_moonlit, lambda state: state.has(HEAVYBLADE, world.player))

        if DANCER in moonlit_classes:
            class_moonlit = world.get_entrance("Moonlit Pinnacle - " + DANCER)
            set_rule(class_moonlit, lambda state: state.has(DANCER, world.player))

        if DRUID in moonlit_classes:
            class_moonlit = world.get_entrance("Moonlit Pinnacle - " + DRUID)
            set_rule(class_moonlit, lambda state: state.has(DRUID, world.player))

        if SPELLSWORD in moonlit_classes:
            class_moonlit = world.get_entrance("Moonlit Pinnacle - " + SPELLSWORD)
            set_rule(class_moonlit, lambda state: state.has(SPELLSWORD, world.player))

        if SNIPER in moonlit_classes:
            class_moonlit = world.get_entrance("Moonlit Pinnacle - " + SNIPER)
            set_rule(class_moonlit, lambda state: state.has(SNIPER, world.player))

        if BRUISER in moonlit_classes:
            class_moonlit = world.get_entrance("Moonlit Pinnacle - " + BRUISER)
            set_rule(class_moonlit, lambda state: state.has(BRUISER, world.player))

        if DEFENDER in moonlit_classes:
            class_moonlit = world.get_entrance("Moonlit Pinnacle - " + DEFENDER)
            set_rule(class_moonlit, lambda state: state.has(DEFENDER, world.player))

        if ANCIENT in moonlit_classes:
            class_moonlit = world.get_entrance("Moonlit Pinnacle - " + ANCIENT)
            set_rule(class_moonlit, lambda state: state.has(ANCIENT, world.player))


def set_all_location_rules(world: RabbitAndSteelWorld) -> None:
    if world.options.class_sanity:
        starting_class = world.get_location("Starting Class")
        starting_class.progress_type = LocationProgressType.PRIORITY

        add_item_rule(
            starting_class,
            lambda item: item.player == world.player and item.is_type("Classes")
        )

    if world.options.goal_condition == world.options.goal_condition.option_shira:
        for class_name in Items.class_names:
            if class_name in world.options.exclude_class:
                continue
            class_victory = world.get_location("Shira - " + class_name)
            class_item = Items.RabbitAndSteelItem("Victory - " + class_name, ItemClassification.progression,
                                                  Items.shira_defeat_items["Victory - " + class_name], world.player)
            class_victory.place_locked_item(class_item)


def set_completion_condition(world: RabbitAndSteelWorld) -> None:
    goal = world.options.goal_condition

    victory = world.get_location("Victory")

    if goal == world.options.goal_condition.option_shira:
        shira_defeats = world.options.shira_defeats.value

        set_rule(victory, lambda state: state.has_group_unique("ShiraVictory", world.player, shira_defeats))

    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
