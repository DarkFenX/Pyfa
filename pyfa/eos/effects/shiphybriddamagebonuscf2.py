# shipHybridDamageBonusCF2
#
# Used by:
# Ships named like: Merlin (3 of 3)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusCF2") * level)
