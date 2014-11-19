# shipBonusHTFalloffGB2
#
# Used by:
# Ships named like: Kronos (4 of 4)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                  "falloff", ship.getModifiedItemAttr("shipBonusGB2") * level)
