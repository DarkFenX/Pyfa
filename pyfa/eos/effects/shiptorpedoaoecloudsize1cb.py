# shipTorpedoAOECloudSize1CB
#
# Used by:
# Ship: Raven Navy Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battleship").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "aoeCloudSize", ship.getModifiedItemAttr("shipBonusCB") * level)
