# shipBonusTitanC2ROFBonus
#
# Used by:
# Variations of ship: Leviathan (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher XL Cruise", "speed",
                                  src.getModifiedItemAttr("shipBonusTitanC2"), skill="Caldari Titan")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rapid Torpedo", "speed",
                                  src.getModifiedItemAttr("shipBonusTitanC2"), skill="Caldari Titan")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher XL Torpedo", "speed",
                                  src.getModifiedItemAttr("shipBonusTitanC2"), skill="Caldari Titan")
