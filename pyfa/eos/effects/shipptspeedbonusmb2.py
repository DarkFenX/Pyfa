# shipPTspeedBonusMB2
#
# Used by:
# Ships named like: Maelstrom (3 of 3)
# Ships named like: Tempest Edition (3 of 3)
# Ships named like: Vargur Edition (3 of 3)
# Variations of ship: Tempest (4 of 4)
# Ship: Panther
# Ship: Typhoon Fleet Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                  "speed", ship.getModifiedItemAttr("shipBonusMB2") * level)
