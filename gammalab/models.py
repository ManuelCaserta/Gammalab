"""
Physics and mathematical models for gamma-ray attenuation.

This module intentionally uses simplified educational approximations.
It helps students understand trends, not to compute clinical/engineering values.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
import json
from pathlib import Path
from typing import Any, Callable, Dict

import numpy as np


@dataclass(frozen=True)
class Material:
    """
    Material properties used by simplified attenuation/interaction models.

    Attributes:
        name: Human-readable material name.
        key: Internal material key used in lookups.
        z_eff: Effective atomic number approximation.
        density_g_cm3: Density in g/cm^3.
        mu_coeff: Coefficient used in mu(E) approximation.
        mu_exponent: Exponent used in mu(E) approximation.
        photoelectric_scale: Relative weighting factor for photoelectric heuristic.
        compton_scale: Relative weighting factor for Compton heuristic.
        pair_scale: Relative weighting factor for pair-production heuristic.
    """

    name: str
    key: str
    z_eff: float
    density_g_cm3: float
    mu_coeff: float
    mu_exponent: float
    photoelectric_scale: float = 1.0
    compton_scale: float = 1.0
    pair_scale: float = 1.0


def _default_material_payload() -> Dict[str, Dict[str, float | str]]:
    """Fallback payload used if `materials.json` is not available."""
    return {
        "Pb": {
            "name": "Lead",
            "key": "Pb",
            "z_eff": 82.0,
            "density_g_cm3": 11.35,
            "mu_coeff": 15.0,
            "mu_exponent": 1.3,
            "photoelectric_scale": 1.25,
            "compton_scale": 0.9,
            "pair_scale": 1.35,
        },
        "Al": {
            "name": "Aluminum",
            "key": "Al",
            "z_eff": 13.0,
            "density_g_cm3": 2.7,
            "mu_coeff": 0.8,
            "mu_exponent": 1.2,
            "photoelectric_scale": 0.95,
            "compton_scale": 1.05,
            "pair_scale": 0.9,
        },
        "H2O": {
            "name": "Water",
            "key": "H2O",
            "z_eff": 7.4,
            "density_g_cm3": 1.0,
            "mu_coeff": 0.15,
            "mu_exponent": 1.1,
            "photoelectric_scale": 1.0,
            "compton_scale": 1.1,
            "pair_scale": 0.85,
        },
        "Air": {
            "name": "Air",
            "key": "Air",
            "z_eff": 7.2,
            "density_g_cm3": 0.001225,
            "mu_coeff": 0.0002,
            "mu_exponent": 1.1,
            "photoelectric_scale": 0.8,
            "compton_scale": 1.15,
            "pair_scale": 0.8,
        },
        "Tissue": {
            "name": "Tissue",
            "key": "Tissue",
            "z_eff": 7.4,
            "density_g_cm3": 1.04,
            "mu_coeff": 0.16,
            "mu_exponent": 1.1,
            "photoelectric_scale": 1.0,
            "compton_scale": 1.12,
            "pair_scale": 0.9,
        },
    }


def _load_materials() -> Dict[str, Material]:
    """Load materials from JSON and convert to `Material` objects."""
    path = Path(__file__).with_name("materials.json")
    payload: Dict[str, Dict[str, Any]]
    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
    else:
        payload = _default_material_payload()

    materials: Dict[str, Material] = {}
    for key, item in payload.items():
        materials[key] = Material(
            name=str(item["name"]),
            key=str(item.get("key", key)),
            z_eff=float(item["z_eff"]),
            density_g_cm3=float(item["density_g_cm3"]),
            mu_coeff=float(item["mu_coeff"]),
            mu_exponent=float(item["mu_exponent"]),
            photoelectric_scale=float(item.get("photoelectric_scale", 1.0)),
            compton_scale=float(item.get("compton_scale", 1.0)),
            pair_scale=float(item.get("pair_scale", 1.0)),
        )
    return materials


_MATERIALS: Dict[str, Material] = _load_materials()


def _validate_material_energy(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator: validate `material_key` and `energy_mev` arguments."""

    @wraps(fn)
    def wrapper(material_key: str, energy_mev: float, *args: Any, **kwargs: Any) -> Any:
        if not isinstance(energy_mev, (int, float)) or float(energy_mev) <= 0:
            raise ValueError(f"Energy must be positive, got {energy_mev} MeV")
        if material_key not in _MATERIALS:
            available = ", ".join(sorted(_MATERIALS.keys()))
            raise KeyError(f"Material '{material_key}' not found. Available: {available}")
        return fn(material_key, float(energy_mev), *args, **kwargs)

    return wrapper


def _validate_thickness(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator: validate third positional argument `thickness_cm`."""

    @wraps(fn)
    def wrapper(material_key: str, energy_mev: float, thickness_cm: float, *args: Any, **kwargs: Any) -> Any:
        if not isinstance(thickness_cm, (int, float)) or float(thickness_cm) < 0:
            raise ValueError(f"Thickness must be non-negative, got {thickness_cm} cm")
        return fn(material_key, energy_mev, float(thickness_cm), *args, **kwargs)

    return wrapper


def get_materials() -> Dict[str, Material]:
    """Return a shallow copy of the material dictionary."""
    return _MATERIALS.copy()


@_validate_material_energy
def mu_cm_inv(material_key: str, energy_mev: float) -> float:
    """
    Compute simplified linear attenuation coefficient in cm^-1.

    Educational approximation:
        mu(E) = a * E^(-b) * f(E)
    where f(E) is a smooth correction to keep behavior realistic at low energies.

    Example:
        >>> mu_cm_inv("H2O", 1.0) > 0
        True
    """
    material = _MATERIALS[material_key]
    mu_base = material.mu_coeff * (energy_mev ** (-material.mu_exponent))
    low_energy_boost = 1.0 + 0.08 * np.exp(-energy_mev / 0.25)
    mu = mu_base * low_energy_boost
    return float(np.clip(mu, 1e-6, 100.0))


@_validate_material_energy
def half_value_layer_cm(material_key: str, energy_mev: float) -> float:
    """
    Compute HVL (Half Value Layer) in cm.

    HVL is the thickness x where transmission equals 0.5:
        HVL = ln(2) / mu
    """
    mu = mu_cm_inv(material_key, energy_mev)
    return float(np.log(2.0) / mu)


@_validate_material_energy
@_validate_thickness
def transmission_fraction(material_key: str, energy_mev: float, thickness_cm: float) -> float:
    """
    Compute transmitted fraction I/I0 with Beer-Lambert law.

    I(x) = I0 * exp(-mu * x)

    Returns:
        A value in (0, 1], exactly 1.0 when thickness is zero.
    """
    if thickness_cm == 0:
        return 1.0

    mu = mu_cm_inv(material_key, energy_mev)
    transmission = float(np.exp(-mu * thickness_cm))
    return float(np.clip(transmission, 1e-10, 1.0))


@_validate_material_energy
def interaction_probabilities(material_key: str, energy_mev: float) -> Dict[str, float]:
    """
    Return normalized heuristic probabilities for interactions.

    Output keys:
    - `photoelectric`
    - `compton`
    - `pair`
    """
    material = _MATERIALS[material_key]
    z_val = material.z_eff
    energy_val = energy_mev

    # Educational heuristics with material-specific scaling.
    weight_photoelectric = (
        material.photoelectric_scale * 2.5 * (z_val ** 3.5) / (energy_val ** 5.0)
    )
    weight_compton = (
        material.compton_scale * 900.0 * energy_val / (0.2 + 0.1 * energy_val ** 0.8)
    )

    pair_threshold_mev = 1.022
    if energy_val > pair_threshold_mev:
        excess_energy = energy_val - pair_threshold_mev
        weight_pair = (
            material.pair_scale * 5.0 * (z_val ** 3.5) * (excess_energy ** 1.8)
        )
    else:
        weight_pair = 0.0

    total_weight = weight_photoelectric + weight_compton + weight_pair
    if total_weight <= 0:
        return {"photoelectric": 1.0 / 3.0, "compton": 1.0 / 3.0, "pair": 1.0 / 3.0}

    probs = {
        "photoelectric": weight_photoelectric / total_weight,
        "compton": weight_compton / total_weight,
        "pair": weight_pair / total_weight,
    }

    for key in probs:
        probs[key] = float(np.clip(probs[key], 0.0, 1.0))

    norm = sum(probs.values())
    if norm > 0:
        for key in probs:
            probs[key] /= norm
    return probs


def calculate_attenuation(energy: float, material: str, thickness: float) -> float:
    """
    Compatibility wrapper around `transmission_fraction`.

    Supports both user-facing names and internal keys.
    """
    material_map = {
        "Water": "H2O",
        "Lead": "Pb",
        "Aluminum": "Al",
        "Tissue": "Tissue",
        "Air": "Air",
    }
    material_key = material if material in _MATERIALS else material_map.get(material, material)
    return transmission_fraction(material_key, energy, thickness)

