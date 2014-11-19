# eliteBonusCommandShipsHeavyMissileExplosionVelocityCS2
#
# Used by:
# Ship: Claymore
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Command Ships").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "aoeVelocity", ship.getModifiedItemAttr("eliteBonusCommandShips2") * level)
