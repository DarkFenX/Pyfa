# shipCruiseMissileVelocityBonusCB3
#
# Used by:
# Ships named like: Raven (6 of 6)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battleship").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Cruise Missiles"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusCB3") * level)
