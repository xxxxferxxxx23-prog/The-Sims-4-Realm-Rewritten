import sims4
from sims.sim_info import SimInfo
from traits.traits import Trait
from traits.trait_type import TraitType
from sims4.tuning.tunable import TunableEnumEntry
from sims4.resources import Types

class MagicalRomanceTraits(TraitType):
    ENCHANTER = TunableEnumEntry(MagicalRomanceTraits, default='enchanter')
    HEARTBOUND = TunableEnumEntry(MagicalRomanceTraits, default='heartbound')
    FICKLE = TunableEnumEntry(MagicalRomanceTraits, default='fickle')

# Romance trait definitions
ENCHANTER_TRAIT = Trait(
    trait_type=MagicalRomanceTraits.ENCHANTER,
    display_name='Enchanter',
    description='This sim excels at charming others with magical allure.',
    buffs=['buff_MagicalEnchanter']
)

HEARTBOUND_TRAIT = Trait(
    trait_type=MagicalRomanceTraits.HEARTBOUND,
    display_name='Heartbound',
    description='This sim forms deep, loyal magical bonds.',
    buffs=['buff_MagicalHeartbound']
)

FICKLE_TRAIT = Trait(
    trait_type=MagicalRomanceTraits.FICKLE,
    display_name='Fickle',
    description='This sim\'s affections change with the magic wind.',
    buffs=['buff_MagicalFickle']
)

# Compatibility matrix based on magical affinity (placeholder for affinity system)
COMPATIBILITY_MAPPING = {
    (MagicalRomanceTraits.ENCHANTER, MagicalRomanceTraits.HEARTBOUND): 0.9,  # High compatibility
    (MagicalRomanceTraits.ENCHANTER, MagicalRomanceTraits.FICKLE): 0.5,
    (MagicalRomanceTraits.HEARTBOUND, MagicalRomanceTraits.FICKLE): 0.3,
}

def calculate_affinity_compatibility(sim_a: SimInfo, sim_b: SimInfo) -> float:
    """Calculate compatibility based on romance traits and magical affinity."""
    trait_a = get_magical_romance_trait(sim_a)
    trait_b = get_magical_romance_trait(sim_b)
    key = (trait_a, trait_b)
    return COMPATIBILITY_MAPPING.get(key, 0.6)  # Default medium compatibility

def get_magical_romance_trait(sim_info: SimInfo):
    for trait in sim_info.trait_tracker:
        if trait.trait_type in [t for t in MagicalRomanceTraits]:
            return trait.trait_type
    return None  # No romance trait
