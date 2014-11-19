# shipTrackingLinkRange1Fixed
#
# Used by:
# Ship: Scimitar
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Tracking Computer",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusMC") * level)
