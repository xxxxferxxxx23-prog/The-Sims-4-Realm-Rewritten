import sims4
from sims.sim_info import SimInfo
from sims.household import Household
from traits.traits import Trait
from sims4.tuning.tunable import TunableReference, TunableEnumEntry
from sims4.resources import Types

# Enum for Bloodline Strength
class BloodlineStrength:
    WEAK = 0
    STRONG = 1
    ANCIENT = 2

# Tunable references for bloodline traits
BLOODLINE_TRAITS = {
    BloodlineStrength.WEAK: TunableReference(manager=sims4.resources.get_resource_manager(Types.TRAIT)),
    BloodlineStrength.STRONG: TunableReference(manager=sims4.resources.get_resource_manager(Types.TRAIT)),
    BloodlineStrength.ANCIENT: TunableReference(manager=sims4.resources.get_resource_manager(Types.TRAIT)),
}

# Tunable for magical affinity traits (assuming we have them)
MAGIC_AFFINITY_TRAITS = [
    TunableReference(manager=sims4.resources.get_resource_manager(Types.TRAIT)),  # e.g., Elemental, Shadow, Spirit, Alchemy
]

def get_bloodline_strength(sim_info: SimInfo) -> int:
    """Determine the bloodline strength of a sim based on lineage."""
    # Check if sim has ancient trait from founders
    if any(isinstance(trait, BLOODLINE_TRAITS[BloodlineStrength.ANCIENT].return_type) for trait in sim_info.trait_tracker):
        return BloodlineStrength.ANCIENT
    
    # Count magical traits
    magic_count = sum(1 for trait in sim_info.trait_tracker if trait in MAGIC_AFFINITY_TRAITS)
    
    if magic_count >= 2:
        return BloodlineStrength.STRONG
    else:
        return BloodlineStrength.WEAK

def assign_inherited_traits(child: SimInfo, mother: SimInfo, father: SimInfo):
    """Assign traits to a newborn based on parents' magical affinities."""
    # Get parents' magical traits
    mother_magics = [trait for trait in mother.trait_tracker if trait in MAGIC_AFFINITY_TRAITS]
    father_magics = [trait for trait in father.trait_tracker if trait in MAGIC_AFFINITY_TRAITS]
    
    # Inherited magic: random selection or combination
    possible_magics = list(set(mother_magics + father_magics))
    if possible_magics:
        # Simple: inherit one random magic trait
        inherited_trait = sims4.random.choice(possible_magics)
        child.add_trait(inherited_trait)
    
    # Assign bloodline strength
    mother_strength = get_bloodline_strength(mother)
    father_strength = get_bloodline_strength(father)
    
    # Child gets the higher strength
    child_strength = max(mother_strength, father_strength)
    if child_strength in BLOODLINE_TRAITS:
        child.add_trait(BLOODLINE_TRAITS[child_strength])

# Hook into sim creation (on sim birth)
@sims4.callback_priority(sims4.Priority.LOW)
def on_sim_birth(child: SimInfo, mother: SimInfo, father: SimInfo):
    assign_inherited_traits(child, mother, father)
