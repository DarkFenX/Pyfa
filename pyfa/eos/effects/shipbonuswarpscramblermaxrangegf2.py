# shipBonusWarpScramblerMaxRangeGF2
#
# Used by:
# Ship: Garmur
# Ship: Utu
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Warp Scrambler",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusGF2") * level)
