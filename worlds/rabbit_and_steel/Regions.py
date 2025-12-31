from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region
from . import Items


if TYPE_CHECKING:
    from .World import RabbitAndSteelWorld


def create_and_connect_regions(world: RabbitAndSteelWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: RabbitAndSteelWorld) -> None:
    lobby = Region("Lobby", world.player, world.multiworld)
    kingdom_outskirts = Region("Kingdom Outskirts", world.player, world.multiworld)

    regions = [lobby, kingdom_outskirts]

    # Creates all remaining base regions: Scholar's Nest - Moonlit Pinnacle
    for kingdom_name in Items.kingdom_names:
        if kingdom_name not in world.options.excluded_kingdoms:
            region = Region(kingdom_name, world.player, world.multiworld)
            regions.append(region)

    # Creates the regions for the class checks for the Kingdom Outskirts,
    # As it is not part of kingdom_names, as we always have access to it
    for class_names in world.options.checks_per_class:
        region = Region("Kingdom Outskirts - " + class_names, world.player, world.multiworld)
        regions.append(region)

    # Creates the regions for the class checks for the regions Scholar's Nest - The Pale Keep
    if world.options.checks_per_class:
        for kingdom_name in Items.kingdom_names:
            if kingdom_name == "Moonlit Pinnacle":
                continue

            if kingdom_name not in world.options.excluded_kingdoms:
                for class_name in world.options.checks_per_class:
                    region = Region(kingdom_name + " - " + class_name, world.player, world.multiworld)
                    regions.append(region)

    # Find the classes that will have checks in the Moonlit Pinnacle
    moonlit_classes = []
    if world.options.goal_condition == world.options.goal_condition.option_shira:
        moonlit_classes = Items.class_names
    elif world.options.checks_per_class:
        moonlit_classes = world.options.checks_per_class

    # Create the regions for those classes
    for class_name in moonlit_classes:
        region = Region("Moonlit Pinnacle - " + class_name, world.player, world.multiworld)
        regions.append(region)

    # Create shop region if all shops share locations
    if world.options.shop_sanity == world.options.shop_sanity.option_global:
        region = Region("Shops", world.player, world.multiworld)
        regions.append(region)

    world.multiworld.regions += regions


def connect_regions(world: RabbitAndSteelWorld) -> None:
    lobby = world.get_region("Lobby")
    kingdom_outskirts = world.get_region("Kingdom Outskirts")
    lobby.connect(kingdom_outskirts, "Lobby to Kingdom Outskirts")

    # Connects the regions Scholar's Nest - The Pale Keep to Kingdom Outskirts
    for kingdom_name in Items.kingdom_names:
        if kingdom_name == "Moonlit Pinnacle":
            continue

        if kingdom_name not in world.options.excluded_kingdoms:
            kingdom_region = world.get_region(kingdom_name)
            kingdom_outskirts.connect(kingdom_region, "Kingdom Outskirts to " + kingdom_name)

    # Connects The Pale Keep to the Moonlit Pinnacle
    pale_keep = world.get_region("The Pale Keep")
    moonlit_pinnacle = world.get_region("Moonlit Pinnacle")
    pale_keep.connect(moonlit_pinnacle, "The Pale Keep to Moonlit Pinnacle")

    # Connects the regions for the class checks for the Kingdom Outskirts to the parent region,
    # As it is not part of kingdom_names, as we always have access to it
    for class_names in world.options.checks_per_class:
        region = world.get_region("Kingdom Outskirts - " + class_names)
        kingdom_outskirts.connect(region, "Kingdom Outskirts - " + class_names)

    # Connects the regions for the class checks for the regions Scholar's Nest - The Pale Keep to their parent region
    if world.options.checks_per_class:
        for kingdom_name in Items.kingdom_names:
            if kingdom_name == "Moonlit Pinnacle":
                continue

            if kingdom_name not in world.options.excluded_kingdoms:
                kingdom_region = world.get_region(kingdom_name)

                for class_name in world.options.checks_per_class:
                    kingdom_class_region = world.get_region(kingdom_name + " - " + class_name)
                    kingdom_region.connect(kingdom_class_region, kingdom_name + " - " + class_name)

    # Find the classes that will have checks in the Moonlit Pinnacle
    moonlit_classes = []
    if world.options.goal_condition == world.options.goal_condition.option_shira:
        moonlit_classes = Items.class_names
    elif world.options.checks_per_class:
        moonlit_classes = world.options.checks_per_class

    # Connect the regions for those classes to the parent region
    for class_name in moonlit_classes:
        moonlit_class_region = world.get_region("Moonlit Pinnacle - " + class_name)
        moonlit_pinnacle.connect(moonlit_class_region, "Moonlit Pinnacle - " + class_name)

    # Connect shop region if all shops share locations
    if world.options.shop_sanity == world.options.shop_sanity.option_global:
        shop_region = world.get_region("Shops")

        for kingdom_name in Items.kingdom_names:
            if kingdom_name == "Moonlit Pinnacle":
                continue

            if kingdom_name not in world.options.excluded_kingdoms:
                kingdom_region = world.get_region(kingdom_name)
                kingdom_region.connect(shop_region, kingdom_name + " to Shop")
