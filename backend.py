import json
from tkinter import filedialog

# definition of the different archetypes for the gear
archetypes = [
    {
        "name": "DPS",
        "Necklace": ["CriticalHitChancePercent", "CriticalHitDamagePercent", "Attack"],
        "Ring": ["Attack"],
        "Boots": ["Speed", "Attack"],
        "scale": 10,
        "Attack": 3,
        "CriticalHitChancePercent": 2,
        "CriticalHitDamagePercent": 3,
        "Speed": 3
    },
    {
        "name": "Speed",
        "Necklace": ["*"],
        "Ring": ["*"],
        "Boots": ["Speed"],
        "scale": 6,
        "Speed": 3,
    },
    {
        "name": "Eff",
        "Necklace": ["*"],
        "Ring": ["EffectivenessPercent"],
        "Boots": ["Speed"],
        "scale": 6,
        "Speed": 3,
        "EffectivenessPercent": 3
    },
    {
        "name": "Res",
        "Necklace": ["Health", "Defense"],
        "Ring": ["Health", "Defense", "EffectResistancePercent"],
        "Boots": ["Speed", "Health", "Defense"],
        "scale": 10,
        "EffectResistancePercent": 4,
        "Health": 2,
        "Defense": 2,
        "Speed": 2
    },
    {
        "name": "Tank",
        "Necklace": ["Health", "Defense"],
        "Ring": ["Health", "Defense"],
        "Boots": ["Speed", "Health", "Defense"],
        "scale": 8,
        "Health": 3,
        "Defense": 3,
        "Speed": 2
    },
    {
        "name": "Bruiser",
        "Necklace": ["CriticalHitChancePercent", "CriticalHitDamagePercent", "Health", "Defense", "Attack"],
        "Ring": ["Health", "Defense", "Attack"],
        "Boots": ["Speed", "Health", "Defense", "Attack"],
        "scale": 12,
        "Attack": 2,
        "Defense": 2,
        "Health": 3,
        "CriticalHitChancePercent": 3,
        "CriticalHitDamagePercent": 3,
        "Speed": 2
    },
    {
        "name": "Atk DPS",
        "Necklace": ["Attack", "Health", "Defense"],
        "Ring": ["Attack", "Health", "Defense"],
        "Boots": ["Speed", "Attack", "Health", "Defense"],
        "scale": 6,
        "Attack": 3,
        "Speed": 1,
        "Health": 1,
        "Defense": 1,
    },
    {
        "name": "Nuke",
        "Necklace": ["CriticalHitChancePercent", "CriticalHitDamagePercent", "Attack"],
        "Ring": ["Attack"],
        "Boots": ["Attack"],
        "scale": 7,
        "Attack": 3,
        "CriticalHitChancePercent": 2,
        "CriticalHitDamagePercent": 3
    },
]

# path of the gear.txt file
gearpath=filedialog.askopenfilename(title="choose your file")
#gearpath = r"C:\Users\colin\Documents\FribbelsOptimizerSaves\gear.txt"
listOfStats = ["HealthFlat", "DefenseFlat", "AttackFlat", "Speed", "CriticalHitChancePercent",
               "CriticalHitDamagePercent", "EffectivenessPercent", "EffectResistancePercent", "HealthPercent",
               "DefensePercent", "AttackPercent"]


def augmentStats(substats):
    newsubstats = []
    for stat in substats:
        match stat["type"]:
            case "Health":
                stat["value"] += stat["rolls"] * 56
                stat["type"] = "HealthFlat"
            case "Defense":
                stat["value"] += stat["rolls"] * 9
                stat["type"] = "DefenseFlat"
            case "Attack":
                stat["value"] += stat["rolls"] * 11
                stat["type"] = "AttackFlat"
            case "Speed":
                stat["value"] += min(4, (stat["rolls"] - 1) * 1)
            case "CriticalHitDamagePercent":
                stat["value"] += stat["rolls"] * 1
                if stat["rolls"] >= 5:
                    stat["value"] += 2
            case "CriticalHitChancePercent":
                stat["value"] += stat["rolls"] * 1
            case "EffectivenessPercent":
                stat["value"] += (stat["rolls"] - 1) * 1 + 2
            case "EffectResistancePercent":
                stat["value"] += (stat["rolls"] - 1) * 1 + 2
            case "HealthPercent":
                stat["value"] += (stat["rolls"] - 1) * 1 + 2
            case "DefensePercent":
                stat["value"] += (stat["rolls"] - 1) * 1 + 2
            case "AttackPercent":
                stat["value"] += (stat["rolls"] - 1) * 1 + 2

        newsubstats.append(stat)

    return newsubstats


def formatStats(substats):
    newSubstats = {"AttackPercent": 0, "AttackFlat": 0, "Speed": 0, "CriticalHitChancePercent": 0,
                   "CriticalHitDamagePercent": 0, "HealthPercent": 0, "HealthFlat": 0, "DefensePercent": 0,
                   "DefenseFlat": 0, "EffectivenessPercent": 0, "EffectResistancePercent": 0}
    for stat in substats:
        if stat["type"] == "Attack":
            newSubstats["AttackFlat"] += stat["value"]
        elif stat["type"] == "Health":
            newSubstats["HealthFlat"] += stat["value"]
        elif stat["type"] == "Defense":
            newSubstats["DefenseFlat"] += stat["value"]
        else:
            newSubstats[stat["type"]] += stat["value"]
    return newSubstats


def gearScore(augmentedsubstats):
    Score = (augmentedsubstats.get("AttackPercent", 0)
             + augmentedsubstats.get("AttackFlat", 0) * 3.46 / 39
             + augmentedsubstats.get("HealthPercent", 0)
             + augmentedsubstats.get("HealthFlat", 0) * 3.09 / 174
             + augmentedsubstats.get("DefensePercent", 0)
             + augmentedsubstats.get("DefenseFlat", 0) * 4.99 / 31
             + augmentedsubstats.get("Speed", 0) * (8 / 4)
             + augmentedsubstats.get("CriticalHitDamagePercent", 0) * (8 / 7)
             + augmentedsubstats.get("CriticalHitChancePercent", 0) * (8 / 5)
             + augmentedsubstats.get("EffectivenessPercent", 0)
             + augmentedsubstats.get("EffectResistancePercent", 0))
    return round(Score)


def constructItem(filepath):
    itemList=[]
    with open(filepath, "r") as file:
        data = json.load(file)
        items = data['items']
    for item in items:
        currentItem = {"gear": item["gear"],
                       "main": item["main"]["type"],
                       "sub": item["substats"],
                       "set": item["set"],
                       "level": item["level"],
                       "canBeReforged": item["level"] == 85 and not ("Gaveleet's" in item["name"]),
                       "augmentedStats": []}
        if currentItem["canBeReforged"]:
            currentItem["augmentedStats"] = augmentStats(currentItem["sub"])
        else:
            currentItem["augmentedStats"] = currentItem["sub"]

        currentItem["augmentedStats"] = formatStats(currentItem["augmentedStats"])
        currentItem["score"] = gearScore(currentItem["augmentedStats"])
        itemList.append(currentItem)
    return itemList


def rate(item, archetypes):
    # stats = item.reforgedStats if reforge else item.augmentedStats
    stats = item["augmentedStats"]

    atk_rolls = (stats["AttackPercent"] + (stats["AttackFlat"]) * 3.46 / 39) / 8
    hp_rolls = (stats["HealthPercent"] + (stats["HealthFlat"]) * 3.09 / 174) / 8
    def_rolls = (stats["DefensePercent"] + (stats["DefenseFlat"]) * 4.99 / 31) / 8
    spd_rolls = (stats["Speed"]) / 4
    cr_rolls = (stats["CriticalHitChancePercent"]) / 5
    cd_rolls = (stats["CriticalHitDamagePercent"]) / 7
    eff_rolls = (stats["EffectivenessPercent"]) / 8
    res_rolls = (stats["EffectResistancePercent"]) / 8

    scored_archetypes = []
    for archetype in archetypes:
        scale = archetype["scale"]

        score = (atk_rolls * (archetype.get("Attack") or 0) +
                 hp_rolls * (archetype.get("Health") or 0) +
                 def_rolls * (archetype.get("Defense") or 0) +
                 spd_rolls * (archetype.get("Speed") or 0) +
                 cr_rolls * (archetype.get("CriticalHitChancePercent") or 0) +
                 cd_rolls * (archetype.get("CriticalHitDamagePercent") or 0) +
                 eff_rolls * (archetype.get("EffectivenessPercent") or 0) +
                 res_rolls * (archetype.get("EffectResistancePercent") or 0))

        mains = archetype.get(item["gear"], [])
        match = "*" in mains
        for main in mains:
            if main in item["main"]:
                match = True
                break

        scored_archetypes.append({
            "score": score / scale * (match or (
                    item["gear"] == "Weapon" or item["gear"] == "Helmet" or item["gear"] == "Armor") and 1 or 0.25),
            "name": archetype.get("name")
        })

    # Utiliser cette ligne pour trier scored_archetypes par score
    scored_archetypes.sort(key=lambda x: x["score"], reverse=True)

    return scored_archetypes


def rateAll(itemList, archetypes):
    for item in itemList:
        item["scored_archetypes"] = rate(item, archetypes)
    return itemList

def process_level(itemList):
    count_to_reforge = sum(item["canBeReforged"] for item in itemList)
    count_reforged = sum(item["level"] == 90 for item in itemList)
    count_level_88 = sum(item["level"] == 88 for item in itemList)

    count_gs_gte_70 = sum(item["score"] >= 70 for item in itemList)
    count_gs_gte_75 = sum(item["score"] >= 75 for item in itemList)
    count_gs_gte_80 = sum(item["score"] >= 80 for item in itemList)

    count_gs_gte_70_unreforged = sum(item["score"] >= 70 and item["canBeReforged"] for item in itemList)
    count_gs_gte_75_unreforged = sum(item["score"] >= 75 and item["canBeReforged"] for item in itemList)
    count_gs_gte_80_unreforged = sum(item["score"] >= 80 and item["canBeReforged"] for item in itemList)

    return {
        "number_of_items": len(itemList),
        "level_88": count_level_88,
        "reforged": count_reforged,
        "to_reforge": count_to_reforge,
        "80+gs": count_gs_gte_80,
        "80+gs_inc_unreforged": count_gs_gte_80_unreforged,
        "75+gs": count_gs_gte_75,
        "75+gs_inc_unreforged": count_gs_gte_75_unreforged,
        "70+gs": count_gs_gte_70,
        "70+gs_inc_unreforged": count_gs_gte_70_unreforged
    }

def process_stats(itemList):
    #count the number of item with more than a number of speed and if they are speed set
    count_25_speed = sum(1 for item in itemList if item["augmentedStats"]["Speed"]>=25)
    count_25_speed_set_speed = sum(1 for item in itemList if item["augmentedStats"]["Speed"]>=25 and item["set"]=="SpeedSet")
    count_22_speed = sum(1 for item in itemList if item["augmentedStats"]["Speed"]>=22)
    count_22_speed_set_speed = sum(1 for item in itemList if item["augmentedStats"]["Speed"]>=22 and item["set"]=="SpeedSet")
    count_20_speed = sum(1 for item in itemList if item["augmentedStats"]["Speed"]>=20)
    count_20_speed_set_speed = sum(1 for item in itemList if item["augmentedStats"]["Speed"]>=20 and item["set"]=="SpeedSet")
    count_18_speed = sum(1 for item in itemList if item["augmentedStats"]["Speed"]>=18)
    count_18_speed_set_speed = sum(1 for item in itemList if item["augmentedStats"]["Speed"]>=18 and item["set"]=="SpeedSet")
    count_15_speed = sum(1 for item in itemList if item["augmentedStats"]["Speed"]>=15)
    count_15_speed_set_speed = sum(1 for item in itemList if item["augmentedStats"]["Speed"]>=15 and item["set"]=="SpeedSet")
    #count the number of item with more than a number of hp/def/atk/eff/res/crit dmg/crit chance
    count_30_hp = sum(1 for item in itemList if item["augmentedStats"]["HealthPercent"]>=30)
    count_40_hp = sum(1 for item in itemList if item["augmentedStats"]["HealthPercent"]>=40)

    count_30_def = sum(1 for item in itemList if item["augmentedStats"]["DefensePercent"]>=30)
    count_40_def = sum(1 for item in itemList if item["augmentedStats"]["DefensePercent"]>=40)

    count_30_atk = sum(1 for item in itemList if item["augmentedStats"]["AttackPercent"]>=30)
    count_40_atk = sum(1 for item in itemList if item["augmentedStats"]["AttackPercent"]>=40)

    count_30_eff = sum(1 for item in itemList if item["augmentedStats"]["EffectivenessPercent"]>=30)
    count_40_eff = sum(1 for item in itemList if item["augmentedStats"]["EffectivenessPercent"]>=40)

    count_30_res = sum(1 for item in itemList if item["augmentedStats"]["EffectResistancePercent"]>=30)
    count_40_res = sum(1 for item in itemList if item["augmentedStats"]["EffectResistancePercent"]>=40)

    count_27_crit_dmg = sum(1 for item in itemList if item["augmentedStats"]["CriticalHitDamagePercent"]>=27)
    count_35_crit_dmg = sum(1 for item in itemList if item["augmentedStats"]["CriticalHitDamagePercent"]>=35)

    count_20_crit_chance = sum(1 for item in itemList if item["augmentedStats"]["CriticalHitChancePercent"]>=20)
    count_25_crit_chance = sum(1 for item in itemList if item["augmentedStats"]["CriticalHitChancePercent"]>=25)

    return {
        "25+Speed": count_25_speed,
        "25+Speed - Speed Set": count_25_speed_set_speed,
        "22+Speed": count_22_speed,
        "22+Speed - Speed Set": count_22_speed_set_speed,
        "20+Speed": count_20_speed,
        "20+Speed - Speed Set": count_20_speed_set_speed,
        "18+Speed": count_18_speed,
        "18+Speed - Speed Set": count_18_speed_set_speed,
        "15+Speed": count_15_speed,
        "15+Speed - Speed Set": count_15_speed_set_speed,
        "30% HP": count_30_hp,
        "40% HP": count_40_hp,
        "30% Def": count_30_def,
        "40% Def": count_40_def,
        "30% Attack": count_30_atk,
        "40% Attack": count_40_atk,
        "30% Eff": count_30_eff,
        "40% Eff": count_40_eff,
        "30% Res": count_30_res,
        "40% Res": count_40_res,
        "27% Crit Dmg": count_27_crit_dmg,
        "35% Crit Dmg": count_35_crit_dmg,
        "20% Crit Chance": count_20_crit_chance,
        "25% Crit Chance": count_25_crit_chance
    }

def process_graph(itemList):
    archetypes_stats = {}
    set_stats = {}
    archetype_set_stats = {}

    for item in itemList:
        archetype_name = item["scored_archetypes"][0]["name"]
        set_name = item["set"]

        # Archetypes stats
        archetypes_stats[archetype_name] = archetypes_stats.get(archetype_name, 0) + 1

        # Set stats
        set_stats[set_name] = set_stats.get(set_name, 0) + 1

        # Archetype and Set stats
        if set_name not in archetype_set_stats:
            archetype_set_stats[set_name] = {}

        archetype_set_stats[set_name][archetype_name] = \
            archetype_set_stats[set_name].get(archetype_name, 0) + 1

    return {
        "number_of_item_per_archetypes": archetypes_stats,
        "number_of_item_per_set": set_stats,
        "number_of_item_per_archetypes_per_set": archetype_set_stats
    }

def analyse(itemList):
    itemList=rateAll(itemList, archetypes)
    resultsLevel = process_level(itemList)
    resultsStats = process_stats(itemList)
    resultsGraph = process_graph(itemList)
    return resultsLevel, resultsStats, resultsGraph
itemList = constructItem(gearpath)
analyse(itemList)
