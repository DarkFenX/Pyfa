# eliteBonusHeavyInterdictorsHybridOptimal1
#
# Used by:
# Ship: Phobos
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Heavy Interdiction Cruisers").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors1") * level)
