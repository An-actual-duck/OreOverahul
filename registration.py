from siege import game

from core.tuning import Tuning
from core.tuning.item import ItemTuning
from core.template.item import RemnaTier, RemnaType
from core.monster.boss import handleBossDefeat

def worldLoadEvent(world):
    if world.remnaLevel == 3:
        world.remnaLevel = 4

# Called when the mod is loaded
def register():
    # Loading data
    # Overriding tuning info
    # registering events

    game.events['world_load'].listen(worldLoadEvent)

    my_ore_tuning = {
        "cobalt": 70,
        "tin_ore": 1,
        "draconium": 95,
        "lead_ore": 17,
        "malachite": 31,
        "mithril": 51,
        "orichalcum": 85,
        "platinum": 43,
        "titanium": 60,
        "uranium": 52
    }
    Tuning.ORE_LEVEL.update(my_ore_tuning)

    new_remna_drops = {
        4: {
            RemnaType.Fire: "remna_of_hephaestus",
            RemnaType.Water: "remna_of_poseidon",
            RemnaType.Wind: "remna_of_zephyrus",
            RemnaType.Earth: "remna_of_atlas",
            RemnaType.Light: "remna_of_apollo"
        }

    }
    Tuning.REMNA_TYPES.update(new_remna_drops)

    RemnaTier.add("Four")

    Tuning.REMNA_LOOT_LEVELS.append((4, 70))

    new_shop_prices = {
        "draconium_ingot": (3000, 30),
        "orichalcum_ingot": (1010, 11),
        "cobalt_ingot": (790, 9),
        "titanium_ingot": (680, 8),
        "mithril_ingot": (570, 7),
        "uranium_ingot": (570, 7),
        "platinum_ingot": (500, 7),
        "malachite_omgpt": (360, 5),
        "lead_ingot": (220, 3),
        "tin_ingot": (60, 0),
        "quick_silver_ingot": (230, 2),
        "steel_ingot": (330, 5),
        "hardened_gold_ingot": (420, 6),
        "hardened_adamantite_ingot": (450, 7),
        "hardened_corium_ingot": (520, 8),
        "radiant_osmium_ingot": (800, 10),
        "radiant_mithril_ingot": (900, 11),
        "radiant_titanium_ingot": (1000, 12),
        "radiant_cobalt_ingot": (1100, 13),
        "radiant_orichalcum_ingot": (1200, 14),
        "reinforced_osmium_ingot": (900, 12),
        "reinforced_mithril_ingot": (1000, 13),
        "reinforced_titanium_ingot": (1100, 14),
        "reinforced_cobalt_ingot": (1200, 15),
        "reinforced_orichalcum_ingot": (1300, 16),
        "atomic_osmium_ingot": (1000, 13),
        "atomic_mithril_ingot": (1100, 14),
        "atomic_titanium_ingot": (1200, 15),
        "atomic_cobalt_ingot": (1300, 16),
        "atomic_orichalcum_ingot": (1400, 17)

    }
    ItemTuning.PRICES.update(new_shop_prices)


# Called when the mod is unloaded / client is closed
def unregister():
    # Save data
    # unregister events
    game.events['world_load'].remove(worldLoadEvent)
