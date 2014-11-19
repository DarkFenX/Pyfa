# siegeSquadronCommand
#
# Used by:
# Skill: Siege Warfare Specialist
runTime = "early"
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Siege Warfare Specialist"),
                                  "commandBonus", skill.getModifiedItemAttr("squadronCommandBonus") * skill.level)
