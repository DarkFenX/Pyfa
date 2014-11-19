# eliteBonusInterdictorsMWDSigRadius2
#
# Used by:
# Ships from group: Interdictor (4 of 4)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Interdictors").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                  "signatureRadiusBonus", ship.getModifiedItemAttr("eliteBonusInterdictors2") * level)
