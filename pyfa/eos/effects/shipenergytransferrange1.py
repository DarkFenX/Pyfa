# shipEnergyTransferRange1
#
# Used by:
# Ship: Guardian
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Capacitor Transmitter",
                                  "powerTransferRange", ship.getModifiedItemAttr("shipBonusAC") * level)
