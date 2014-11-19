# shipBonusAfterburnerSpeedFactor2CB
#
# Used by:
# Ship: Nightmare
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Caldari Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Afterburner"),
                                  "speedFactor", module.getModifiedItemAttr("shipBonus2CB") * level)
