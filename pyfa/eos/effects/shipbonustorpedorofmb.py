# shipBonusTorpedoROFMB
#
# Used by:
# Ship: Typhoon
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Torpedo",
                                  "speed", ship.getModifiedItemAttr("shipBonusMB") * level)
