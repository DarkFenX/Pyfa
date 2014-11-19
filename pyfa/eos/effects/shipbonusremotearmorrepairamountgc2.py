# shipBonusRemoteArmorRepairAmountGC2
#
# Used by:
# Ship: Exequror
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "armorDamageAmount", ship.getModifiedItemAttr("shipBonusGC2") * level)
