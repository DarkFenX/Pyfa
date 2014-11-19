# subsystemBonusAmarrDefensive2RemoteArmorRepairAmount
#
# Used by:
# Subsystem: Legion Defensive - Adaptive Augmenter
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Amarr Defensive Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "armorDamageAmount", module.getModifiedItemAttr("subsystemBonusAmarrDefensive2") * level)
