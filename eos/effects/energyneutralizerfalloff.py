# energyNeutralizerFalloff
#
# Used by:
# Modules from group: Energy Neutralizer (54 of 54)
from eos.const import FittingModuleState
from eos.modifiedAttributeDict import ModifiedAttributeDict

type = "active", "projected"


def handler(fit, src, context, **kwargs):
    if "projected" in context and ((hasattr(src, "state") and src.state >= FittingModuleState.ACTIVE) or
                                   hasattr(src, "amountActive")):
        amount = src.getModifiedItemAttr("energyNeutralizerAmount")

        if 'effect' in kwargs:
            amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

        time = src.getModifiedItemAttr("duration")

        fit.addDrain(src, time, amount, 0)
