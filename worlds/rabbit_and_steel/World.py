from typing import Dict, Any

from Options import OptionError
from worlds.AutoWorld import World

from . import Items, Locations, Options, Regions, Rules, Web_world
from .Items import class_names

client_version = 1


class RabbitAndSteelWorld(World):
    """
     Rabbit and Steel game description.
    """

    game = "Rabbit and Steel"

    topology_present = True

    web = Web_world.RabbitAndSteelWeb()

    options_dataclass = Options.RabbitAndSteelOptions
    options: Options.RabbitAndSteelOptions

    item_name_to_id = Items.item_table
    location_name_to_id = Locations.location_table

    origin_region_name = "Lobby"

    item_name_groups = {
        "Kingdoms": Items.kingdom_names,
        "Classes": Items.class_names,
        "Itemsets": Items.itemset_names,
        "Upgrades": Items.upgrade_names,
        "Potions": Items.potion_names,
        "ShiraVictory": Items.shira_defeat_names,
    }

    starting_class_name = ""

    def create_regions(self) -> None:
        Regions.create_and_connect_regions(self)
        Locations.create_all_locations(self)

    def set_rules(self) -> None:
        Rules.set_all_rules(self)

    def create_item(self, name: str) -> Items.RabbitAndSteelItem:
        return Items.create_item_with_classification(self, name)

    def create_item_with_type(self, name: str, type_name: str) -> Items.RabbitAndSteelItem:
        item = Items.create_item_with_classification(self, name)
        item.set_type(type_name)
        return item

    def create_items(self) -> None:
        Items.create_all_items(self)

    def get_filler_item_name(self) -> str:
        return Items.get_random_filler_item_name(self)

    def assign_kingdom_order(self) -> None:
        max_kingdoms_per_run = self.options.max_kingdoms_per_run.value
        kingdom_order = self.options.kingdom_order.value
        excluded_kingdoms = self.options.excluded_kingdoms.value

        unset_kingdoms = [kingdom for (kingdom, order) in kingdom_order.items() if
                          order == 0 and kingdom not in excluded_kingdoms]
        order_amounts = dict.fromkeys([order for order in range(1, max_kingdoms_per_run + 1)], 0)

        # Ensure we have enough valid kingdoms and assign the kingdoms that have a specific value
        valid_placements = 0
        for (kingdom, value) in kingdom_order.items():
            if kingdom in excluded_kingdoms:
                continue
            if value <= 0:
                if value == 0:
                    valid_placements += 1
                continue
            if value > max_kingdoms_per_run:
                raise OptionError(f"Player {self.player_name} has an order value above the number of visitable "
                                  f"kingdoms in a run:\n"
                                  f"{kingdom} has value {value} and needs to be at most {max_kingdoms_per_run}")
            order_amounts[value] = order_amounts.get(value, 0) + 1
            valid_placements += 1

        if valid_placements < max_kingdoms_per_run:
            raise OptionError(f"Player {self.player_name} has too many inaccessible kingdoms: "
                              f"\n{kingdom_order}\nhas {valid_placements} and needs at least {max_kingdoms_per_run}")

        # Place the regions with order 0
        while len(unset_kingdoms) > 0:
            kingdom_to_set = self.random.choice(unset_kingdoms)
            unset_kingdoms.remove(kingdom_to_set)

            smallest_order_len = 1
            smallest_occurrence = 10
            for (order, amount) in reversed(order_amounts.items()):
                if amount < smallest_occurrence:
                    smallest_order_len = order
                    smallest_occurrence = amount

            kingdom_order[kingdom_to_set] = smallest_order_len
            order_amounts[smallest_order_len] += 1

        # Ensure there are at least one kingdom per accessible order
        buffer = 0
        for i in range(1, max_kingdoms_per_run + 1):
            buffer += order_amounts[i]
            buffer -= 1
            if buffer < 0:
                raise OptionError(f"Player {self.player_name} can not reach all valid kingdoms: \n{kingdom_order}")

    def generate_early(self) -> None:
        shared_classes = list(set(self.options.checks_per_class) & set(self.options.exclude_class))
        if len(shared_classes) != 0:
            raise OptionError(f"Player {self.player_name} is excluding classes, but expects to get checks with the "
                              f"class: {shared_classes}")

        if len(self.options.exclude_class.value) == len(class_names):
            raise OptionError(f"Player {self.player_name} is excluding all classes, but at least one is needed to play")

        if self.options.goal_condition == self.options.goal_condition.option_shira and \
                self.options.shira_defeats.value > len(class_names) - len(self.options.exclude_class.value):
            raise OptionError(f"Player {self.player_name} needs to kill Shira more times than available classes")

        if ((self.options.progressive_regions and not self.options.kingdom_sanity) or
                (self.options.kingdom_sanity and self.options.kingdom_sanity_kingdom_order)):
            self.assign_kingdom_order()

        if self.options.class_sanity:
            self.starting_class_name = self.random.choice(tuple(class_names - set(self.options.exclude_class)))
            self.multiworld.push_precollected(self.create_item_with_type(self.starting_class_name, "Classes"))

        kingdom_order = self.options.kingdom_order.value
        excluded_kingdoms = self.options.excluded_kingdoms.value
        for kingdom in kingdom_order.keys():
            if kingdom in excluded_kingdoms:
                kingdom_order[kingdom] = -1

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.options.as_dict(
            "kingdom_sanity", "max_kingdoms_per_run", "progressive_regions", "excluded_kingdoms",
            "kingdom_sanity_kingdom_order", "kingdom_order", "class_sanity", "checks_per_class", "shuffle_item_sets",
            "checks_per_item_in_chest", "upgrade_sanity", "potion_sanity", "goal_condition", "shira_defeats",
            "shop_sanity")
