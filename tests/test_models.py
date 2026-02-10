"""
Unit tests for physics models.
"""

import pytest
import numpy as np
from gammalab import models


def test_get_materials():
    """Test that materials dictionary is accessible."""
    materials = models.get_materials()
    assert isinstance(materials, dict)
    assert 'Pb' in materials
    assert 'H2O' in materials
    assert 'Air' in materials


def test_mu_cm_inv_positive():
    """Test that mu is always positive."""
    for material_key in ['Pb', 'Al', 'H2O', 'Air', 'Tissue']:
        for energy in [0.05, 0.1, 1.0, 5.0, 10.0]:
            mu = models.mu_cm_inv(material_key, energy)
            assert mu > 0, f"mu should be positive for {material_key} at {energy} MeV"


def test_mu_cm_inv_energy_range():
    """Test mu across valid energy range."""
    material_key = 'H2O'
    energies = np.linspace(0.05, 10.0, 20)
    for energy in energies:
        mu = models.mu_cm_inv(material_key, energy)
        assert 1e-6 <= mu <= 100.0, f"mu out of reasonable range at {energy} MeV"


def test_mu_cm_inv_decreases_with_energy():
    """Test that mu generally decreases with increasing energy."""
    material_key = 'Pb'
    mu_low = models.mu_cm_inv(material_key, 0.1)
    mu_high = models.mu_cm_inv(material_key, 10.0)
    assert mu_low > mu_high, "mu should decrease with increasing energy"


def test_mu_cm_inv_invalid_energy():
    """Test that invalid energy raises ValueError."""
    with pytest.raises(ValueError):
        models.mu_cm_inv('H2O', -1.0)
    with pytest.raises(ValueError):
        models.mu_cm_inv('H2O', 0.0)


def test_mu_cm_inv_invalid_material():
    """Test that invalid material raises KeyError."""
    with pytest.raises(KeyError):
        models.mu_cm_inv('InvalidMaterial', 1.0)


def test_transmission_fraction_range():
    """Test that transmission fraction is in (0, 1]."""
    for material_key in ['Pb', 'H2O', 'Air']:
        for energy in [0.1, 1.0, 5.0]:
            for thickness in [0.1, 1.0, 5.0, 10.0]:
                trans = models.transmission_fraction(material_key, energy, thickness)
                assert 0 < trans <= 1, \
                    f"Transmission should be in (0, 1] for {material_key}, E={energy}, x={thickness}"


def test_transmission_decreases_with_thickness():
    """Test that transmission decreases when thickness increases."""
    material_key = 'H2O'
    energy = 1.0
    trans_thin = models.transmission_fraction(material_key, energy, 1.0)
    trans_thick = models.transmission_fraction(material_key, energy, 5.0)
    assert trans_thin > trans_thick, \
        "Transmission should decrease with increasing thickness"


def test_transmission_zero_thickness():
    """Test that zero thickness gives exactly 100% transmission."""
    for material_key in ['Pb', 'H2O', 'Air']:
        trans = models.transmission_fraction(material_key, 1.0, 0.0)
        assert trans == 1.0, f"Zero thickness should give exactly 1.0, got {trans}"


def test_transmission_energy_at_bounds():
    """Test transmission at energy bounds (0.05 and 10.0 MeV)."""
    material_key = 'H2O'
    thickness = 5.0
    
    # Test at minimum energy
    trans_min = models.transmission_fraction(material_key, 0.05, thickness)
    assert 0 < trans_min <= 1, f"Transmission at min energy should be in (0, 1], got {trans_min}"
    
    # Test at maximum energy
    trans_max = models.transmission_fraction(material_key, 10.0, thickness)
    assert 0 < trans_max <= 1, f"Transmission at max energy should be in (0, 1], got {trans_max}"
    
    # At higher energy, transmission should generally be higher (less attenuation)
    assert trans_max > trans_min, "Higher energy should generally give higher transmission"


def test_transmission_very_large_thickness():
    """Test transmission with very large thickness values."""
    material_key = 'Pb'
    energy = 0.1  # Low energy for strong attenuation
    large_thickness = 1000.0  # Very large thickness
    
    trans = models.transmission_fraction(material_key, energy, large_thickness)
    assert 0 <= trans < 0.01, f"Very large thickness should give near-zero transmission, got {trans}"


def test_mu_cm_inv_energy_bounds():
    """Test mu calculation at energy bounds."""
    material_key = 'H2O'
    
    # Test at minimum energy
    mu_min = models.mu_cm_inv(material_key, 0.05)
    assert mu_min > 0, f"mu at min energy should be positive, got {mu_min}"
    
    # Test at maximum energy
    mu_max = models.mu_cm_inv(material_key, 10.0)
    assert mu_max > 0, f"mu at max energy should be positive, got {mu_max}"
    
    # mu should decrease with increasing energy
    assert mu_min > mu_max, "mu should decrease with increasing energy"


def test_half_value_layer_energy_bounds():
    """Test HVL calculation at energy bounds."""
    material_key = 'H2O'
    
    # Test at minimum energy
    hvl_min = models.half_value_layer_cm(material_key, 0.05)
    assert hvl_min > 0, f"HVL at min energy should be positive, got {hvl_min}"
    
    # Test at maximum energy
    hvl_max = models.half_value_layer_cm(material_key, 10.0)
    assert hvl_max > 0, f"HVL at max energy should be positive, got {hvl_max}"
    
    # HVL should increase with energy (less attenuation at higher energy)
    assert hvl_max > hvl_min, "HVL should increase with increasing energy"


def test_pb_attenuates_more_than_air():
    """Test that Pb attenuates more than Air at same energy and thickness."""
    energy = 0.1  # Low energy where difference is most pronounced
    thickness = 5.0
    
    trans_pb = models.transmission_fraction('Pb', energy, thickness)
    trans_air = models.transmission_fraction('Air', energy, thickness)
    
    assert trans_pb < trans_air, \
        f"Pb should attenuate more than Air (Pb trans={trans_pb:.4f}, Air trans={trans_air:.4f})"


def test_pb_attenuates_more_than_water():
    """Test that Pb attenuates more than Water at same energy and thickness."""
    energy = 0.1
    thickness = 5.0
    
    trans_pb = models.transmission_fraction('Pb', energy, thickness)
    trans_water = models.transmission_fraction('H2O', energy, thickness)
    
    assert trans_pb < trans_water, \
        f"Pb should attenuate more than Water (Pb trans={trans_pb:.4f}, H2O trans={trans_water:.4f})"


def test_transmission_fraction_invalid_inputs():
    """Test that invalid inputs raise appropriate errors."""
    with pytest.raises(ValueError):
        models.transmission_fraction('H2O', -1.0, 1.0)
    with pytest.raises(ValueError):
        models.transmission_fraction('H2O', 1.0, -1.0)
    with pytest.raises(KeyError):
        models.transmission_fraction('InvalidMaterial', 1.0, 1.0)


def test_calculate_attenuation_backward_compatibility():
    """Test backward compatibility of calculate_attenuation function."""
    # Test with material name
    result1 = models.calculate_attenuation(1.0, "Water", 5.0)
    assert 0 < result1 <= 1
    
    # Test with material key
    result2 = models.calculate_attenuation(1.0, "H2O", 5.0)
    assert abs(result1 - result2) < 1e-6, "Water and H2O should give same result"


def test_interaction_probabilities_sum_to_one():
    """Test that interaction probabilities sum to 1.0."""
    for material_key in ['Pb', 'Al', 'H2O', 'Air', 'Tissue']:
        for energy in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
            probs = models.interaction_probabilities(material_key, energy)
            total = probs['photoelectric'] + probs['compton'] + probs['pair']
            assert abs(total - 1.0) < 1e-6, \
                f"Probabilities should sum to 1.0, got {total} for {material_key} at {energy} MeV"


def test_interaction_probabilities_range():
    """Test that all probabilities are in [0, 1]."""
    for material_key in ['Pb', 'H2O', 'Air']:
        for energy in [0.1, 1.0, 5.0]:
            probs = models.interaction_probabilities(material_key, energy)
            for key, value in probs.items():
                assert 0 <= value <= 1, \
                    f"Probability {key} should be in [0, 1], got {value} for {material_key} at {energy} MeV"


def test_pair_production_threshold():
    """Test that pair production is 0 below 1.022 MeV and >0 above threshold."""
    # Below threshold
    probs_below = models.interaction_probabilities('Pb', 1.0)
    assert probs_below['pair'] == 0.0, \
        f"Pair production should be 0 below 1.022 MeV, got {probs_below['pair']}"
    
    # Above threshold
    probs_above = models.interaction_probabilities('Pb', 2.0)
    assert probs_above['pair'] > 0.0, \
        f"Pair production should be >0 above 1.022 MeV, got {probs_above['pair']}"


def test_photoelectric_dominates_low_energy_high_z():
    """Test that photoelectric > compton at low energy (0.1 MeV) in Pb."""
    probs = models.interaction_probabilities('Pb', 0.1)
    assert probs['photoelectric'] > probs['compton'], \
        f"At 0.1 MeV in Pb, photoelectric ({probs['photoelectric']:.4f}) should be > compton ({probs['compton']:.4f})"


def test_compton_dominates_mid_energy_water():
    """Test that compton is largest at 1.0 MeV in water/tissue."""
    probs_water = models.interaction_probabilities('H2O', 1.0)
    assert probs_water['compton'] > probs_water['photoelectric'], \
        f"At 1.0 MeV in H2O, compton ({probs_water['compton']:.4f}) should be > photoelectric ({probs_water['photoelectric']:.4f})"
    assert probs_water['compton'] > probs_water['pair'], \
        f"At 1.0 MeV in H2O, compton ({probs_water['compton']:.4f}) should be > pair ({probs_water['pair']:.4f})"
    
    probs_tissue = models.interaction_probabilities('Tissue', 1.0)
    assert probs_tissue['compton'] > probs_tissue['photoelectric'], \
        f"At 1.0 MeV in Tissue, compton should be > photoelectric"


def test_pair_production_increases_with_energy():
    """Test that pair production increases with energy above threshold."""
    probs_low = models.interaction_probabilities('Pb', 2.0)
    probs_high = models.interaction_probabilities('Pb', 10.0)
    assert probs_high['pair'] > probs_low['pair'], \
        f"Pair production should increase with energy (2 MeV: {probs_low['pair']:.4f}, 10 MeV: {probs_high['pair']:.4f})"


def test_pair_production_increases_with_z():
    """Test that pair production increases with Z at same energy."""
    energy = 5.0
    probs_water = models.interaction_probabilities('H2O', energy)
    probs_pb = models.interaction_probabilities('Pb', energy)
    assert probs_pb['pair'] > probs_water['pair'], \
        f"Pair production should be higher for Pb than H2O at {energy} MeV"


def test_interaction_probabilities_invalid_inputs():
    """Test that invalid inputs raise appropriate errors."""
    with pytest.raises(ValueError):
        models.interaction_probabilities('H2O', -1.0)
    with pytest.raises(ValueError):
        models.interaction_probabilities('H2O', 0.0)
    with pytest.raises(KeyError):
        models.interaction_probabilities('InvalidMaterial', 1.0)

def test_hvl_validation_invalid_material():
    """HVL should fail for unknown material."""
    with pytest.raises(KeyError):
        models.half_value_layer_cm("Unknown", 1.0)


def test_calculate_attenuation_invalid_material():
    """Backward-compatibility wrapper should still validate material."""
    with pytest.raises(KeyError):
        models.calculate_attenuation(1.0, "Unknown", 1.0)

