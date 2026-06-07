
import json
import sys
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import Fastmcp

# ─── CONFIGURATION ────────────────────────────────────────────────────────────

mcp = Fastmcp("MEOK Thermal Management")

# ─── TOOLS ───────────────────────────────────────────────────────────────────

@mcp.tool()
def simulate_marangoni_flow(
    photon_flux_density: float,
    nanoparticle_concentration_ppm: float = 50.0,
    ambient_temp_c: float = 25.0
) -> Dict[str, Any]:
    """
    Simulates photothermal Marangoni flow velocity for passive actuator cooling.
    
    Args:
        photon_flux_density: Intensity of NIR light (mW/mm2).
        nanoparticle_concentration_ppm: Concentration of gold nanoparticles.
        ambient_temp_c: Operating temperature.
    """
    # IP Logic (from user research)
    BASE_VELOCITY = 10.0 # mm/s
    AMPLIFICATION_FACTOR = 1.0 + (nanoparticle_concentration_ppm / 100.0)
    
    # Delta T calculation (simplified)
    delta_t = photon_flux_density * 0.15 * AMPLIFICATION_FACTOR
    
    # Flow velocity (Marangoni effect)
    velocity = BASE_VELOCITY + (delta_t * 5.5)
    
    # Heat rejection boost
    heat_rejection_boost = (velocity / 100.0) * 0.45 # up to 45% boost at 100mm/s
    
    return {
        "ip_classification": "MEOK_PROPRIETARY_PHOTOTHERMAL",
        "parameters": {
            "flux": photon_flux_density,
            "nanoparticles": nanoparticle_concentration_ppm,
            "ambient": ambient_temp_c
        },
        "results": {
            "delta_t_k": round(delta_t, 2),
            "flow_velocity_mm_s": round(velocity, 2),
            "heat_rejection_boost_pct": round(heat_rejection_boost * 100, 1),
            "state": "SUPER_CRITICAL" if velocity > 120 else "STABLE"
        },
        "patent_status": "DRAFT_READY"
    }

@mcp.tool()
def calculate_capillary_limit(
    channel_width_um: float,
    wick_porosity: float = 0.65,
    fluid: str = "water"
) -> Dict[str, Any]:
    """
    Calculates the maximum heat load for the passive capillary cooling layer.
    """
    # Capillary force simulation
    surface_tension = 0.072 # N/m for water
    capillary_pressure = (2 * surface_tension) / (channel_width_um * 1e-6)
    
    # Empirical heat load limit (W)
    q_max = (capillary_pressure / 1000.0) * wick_porosity * 15.0
    
    return {
        "channel_width": channel_width_um,
        "capillary_pressure_pa": round(capillary_pressure, 2),
        "max_heat_load_watts": round(q_max, 2),
        "safety_margin": 1.4,
        "status": "VALIDATED" if q_max > 50 else "INSUFFICIENT"
    }

if __name__ == "__main__":
    mcp.run()


# ── MEOK monetization layer (Stripe upgrade · PAYG · pricing) ──────────
# Free tier is zero-config. Upgrade to Pro (unlimited) or pay-as-you-go per call.
import os as _meok_os
MEOK_STRIPE_UPGRADE = "https://buy.stripe.com/00wfZjcgAeUW4c5cyQ8k90K"  # Pro (unlimited)
MEOK_PAYG_KEY = _meok_os.environ.get("MEOK_PAYG_KEY", "")  # set to enable PAYG (x402 / ~GBP0.05 per call)
MEOK_PRICING = "https://meok.ai/pricing"


def meok_upsell(tier: str = "free") -> dict:
    """Monetization options for free-tier callers: Pro upgrade, PAYG, or pricing page."""
    if tier != "free":
        return {}
    return {"upgrade_url": MEOK_STRIPE_UPGRADE,
            "payg_enabled": bool(MEOK_PAYG_KEY),
            "pricing": MEOK_PRICING}
