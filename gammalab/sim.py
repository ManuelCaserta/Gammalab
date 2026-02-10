"""
Monte Carlo simulation for gamma-ray interactions (educational).

This implementation is intentionally simplified and is NOT suitable for
medical/engineering safety calculations.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import numpy as np

from gammalab.models import interaction_probabilities, mu_cm_inv


def run_monte_carlo(
    material_key: str,
    energy_mev: float,
    thickness_cm: float,
    n_photons: int,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Simulate N photons crossing a slab of thickness x.

    Simplified model:
    1) Interact within x with probability p = 1 - exp(-mu*x)
    2) If interaction occurs, assign mechanism using heuristic probabilities

    Args:
        material_key: Material key (e.g. "Pb", "H2O", "Air").
        energy_mev: Photon energy in MeV (> 0).
        thickness_cm: Slab thickness in cm (>= 0).
        n_photons: Number of photons (> 0).
        seed: Optional random seed for reproducibility.

    Returns:
        Dictionary with counts and fractions for transmission/interactions.
    """
    if n_photons <= 0:
        raise ValueError(f"n_photons must be positive, got {n_photons}")
    if thickness_cm < 0:
        raise ValueError(f"thickness_cm must be non-negative, got {thickness_cm}")

    rng = np.random.default_rng(seed)
    mu = mu_cm_inv(material_key, energy_mev)
    analytical_transmission = float(np.exp(-mu * thickness_cm))

    interaction_prob = 1.0 - analytical_transmission
    interaction_prob = float(np.clip(interaction_prob, 0.0, 1.0))

    interact_rand = rng.random(n_photons)
    interacts = interact_rand < interaction_prob
    n_interactions = int(np.sum(interacts))
    n_transmitted = int(n_photons - n_interactions)

    interaction_types = np.array([], dtype=np.int8)
    if n_interactions > 0:
        probs = interaction_probabilities(material_key, energy_mev)
        cumulative = np.array(
            [
                probs["photoelectric"],
                probs["photoelectric"] + probs["compton"],
                1.0,
            ],
            dtype=float,
        )
        type_rand = rng.random(n_interactions)
        # side='left': index i where cumulative[i] >= r → 0 se r < cum[0], 1 se cum[0]<=r<cum[1], 2 se r>=cum[1]
        interaction_types = np.searchsorted(cumulative, type_rand, side="left")
        # clamp to 0,1,2 (searchsorted can return 3 if r>=1.0 per float rounding)
        interaction_types = np.clip(interaction_types, 0, 2)

    photoelectric_count = int(np.sum(interaction_types == 0))
    compton_count = int(np.sum(interaction_types == 1))
    pair_count = int(np.sum(interaction_types == 2))

    transmitted_fraction = n_transmitted / n_photons
    interaction_fraction = n_interactions / n_photons

    if n_interactions > 0:
        photoelectric_fraction = photoelectric_count / n_interactions
        compton_fraction = compton_count / n_interactions
        pair_fraction = pair_count / n_interactions
    else:
        photoelectric_fraction = 0.0
        compton_fraction = 0.0
        pair_fraction = 0.0

    return {
        "n_photons": int(n_photons),
        "transmitted": n_transmitted,
        "interactions": n_interactions,
        "photoelectric_count": photoelectric_count,
        "compton_count": compton_count,
        "pair_count": pair_count,
        "transmitted_fraction": float(transmitted_fraction),
        "interaction_fraction": float(interaction_fraction),
        "photoelectric_fraction": float(photoelectric_fraction),
        "compton_fraction": float(compton_fraction),
        "pair_fraction": float(pair_fraction),
        "analytical_transmission": analytical_transmission,
    }

