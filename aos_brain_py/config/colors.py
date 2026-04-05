# config/colors.py
# Bob Ross-inspired palette for brain visualization

BOB_ROSS_PALETTE = {
    # Core landscape colors
    "phthalo_green": "#123524",      # Deep forest - Visual Cortex
    "prussian_blue": "#0B3D91",      # Deep water - Auditory Cortex  
    "cerulean_blue": "#2A52BE",      # Sky blue - Wernicke's Area
    "yellow_ochre": "#C79B3B",       # Warm earth - Broca's Area
    "burnt_sienna": "#8A3B12",       # Rust/earth - Parietal Cortex
    "alizarin_crimson": "#E32636",   # Deep red - PFC
    "cadmium_red": "#E30022",        # Bright red - Limbic System
    "sap_green": "#507D2A",          # Forest green - Hippocampus
    "midnight_black": "#000000",     # Shadow/deep - Inactive
    "paynes_grey": "#40404F",        # Cool grey - Negative valence
    "cadmium_yellow": "#FFF600",     # Sunshine - Positive valence
    "titanium_white": "#FFFFFF",     # Highlights
}

# Region to color mapping
REGION_COLORS = {
    "visual_cortex": BOB_ROSS_PALETTE["phthalo_green"],
    "auditory_cortex": BOB_ROSS_PALETTE["prussian_blue"],
    "wernicke": BOB_ROSS_PALETTE["cerulean_blue"],
    "broca": BOB_ROSS_PALETTE["yellow_ochre"],
    "parietal": BOB_ROSS_PALETTE["burnt_sienna"],
    "pfc": BOB_ROSS_PALETTE["alizarin_crimson"],
    "limbic": BOB_ROSS_PALETTE["cadmium_red"],
    "hippocampus": BOB_ROSS_PALETTE["sap_green"],
    "basal": BOB_ROSS_PALETTE["burnt_sienna"],
    "cerebellum": BOB_ROSS_PALETTE["prussian_blue"],
    "thalamus": BOB_ROSS_PALETTE["cerulean_blue"],
    "brainstem": BOB_ROSS_PALETTE["paynes_grey"],
    "inactive": BOB_ROSS_PALETTE["midnight_black"],
}

def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple (0-1 range)"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def emotional_tint(valence: float) -> str:
    """
    Get color based on emotional valence (-1.0 to +1.0)
    Negative = cool shadows (Payne's Grey)
    Positive = warm highlights (Cadmium Yellow)
    """
    if valence > 0.3:
        return BOB_ROSS_PALETTE["cadmium_yellow"]
    elif valence < -0.3:
        return BOB_ROSS_PALETTE["paynes_grey"]
    return BOB_ROSS_PALETTE["midnight_black"]
