# ammoInfluenceRange
#
# Used by:
# Items from category: Charge (559 of 829)
type = "passive"
def handler(fit, module, context):
    module.multiplyItemAttr("maxRange", module.getModifiedChargeAttr("weaponRangeMultiplier"))