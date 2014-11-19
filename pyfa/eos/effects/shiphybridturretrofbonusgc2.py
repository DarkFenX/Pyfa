# shipHybridTurretROFBonusGC2
#
# Used by:
# Ship: Exequror Navy Issue
# Ship: Phobos
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "speed", ship.getModifiedItemAttr("shipBonusGC2") * level)
