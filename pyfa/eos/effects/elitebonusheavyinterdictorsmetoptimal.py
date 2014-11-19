# eliteBonusHeavyInterdictorsMETOptimal
#
# Used by:
# Ship: Devoter
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Heavy Interdiction Cruisers").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusHeavyInterdictors1") * level)
