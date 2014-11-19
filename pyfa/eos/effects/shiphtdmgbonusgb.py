# shipHTDmgBonusGB
#
# Used by:
# Ships named like: Hyperion (3 of 3)
# Ships named like: Kronos (4 of 4)
# Ship: Dominix Navy Issue
# Ship: Megathron Federate Issue
# Ship: Sin
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusGB") * level)
