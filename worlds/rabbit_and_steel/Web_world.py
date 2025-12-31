from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .Options import option_groups  # , option_presets


class RabbitAndSteelWeb(WebWorld):
    game = "Rabbit and Steel"

    theme = "grassFlowers"

    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Rabbit and Steel for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Tjwombo"]
    )]

    option_groups = option_groups
    # options_presets = option_presets
