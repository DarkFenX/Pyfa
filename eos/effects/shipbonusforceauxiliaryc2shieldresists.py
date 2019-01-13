# shipBonusForceAuxiliaryC2ShieldResists
#
# Used by:
# Variations of ship: Minokawa (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("shieldEmDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryC2"),
                           skill="Caldari Carrier")
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryC2"),
                           skill="Caldari Carrier")
    fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryC2"),
                           skill="Caldari Carrier")
    fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("shipBonusForceAuxiliaryC2"),
                           skill="Caldari Carrier")
