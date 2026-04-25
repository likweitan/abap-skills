"""SAP Fiori Horizon palette constants for BTP solution diagrams."""
from __future__ import annotations

# Primary
BTP_BORDER       = "#0070F2"
BTP_FILL         = "#EBF8FF"
NON_SAP_BORDER   = "#475E75"
NON_SAP_FILL     = "#F5F6F7"
TEXT_TITLE       = "#1D2D3E"
TEXT_SECONDARY   = "#556B82"

# Semantic
POS_BORDER       = "#188918"
POS_FILL         = "#F5FAE5"
POS_TEXT         = "#266F3A"
CRIT_BORDER      = "#C35500"
CRIT_FILL        = "#FFF8D6"
NEG_BORDER       = "#D20A0A"
NEG_FILL         = "#FFEAF4"

# Accent
TEAL_BORDER      = "#07838F"
TEAL_FILL        = "#DAFDF5"
INDIGO_BORDER    = "#5D36FF"
INDIGO_FILL      = "#F1ECFF"
PINK_BORDER      = "#CC00DC"
PINK_FILL        = "#FFF0FA"

# Chrome
WHITE            = "#FFFFFF"
LEGEND_STROKE    = "#EAECEE"
BROWN            = "#793802"

# Set used by the validator
PALETTE: frozenset[str] = frozenset({
    BTP_BORDER, BTP_FILL, NON_SAP_BORDER, NON_SAP_FILL,
    TEXT_TITLE, TEXT_SECONDARY,
    POS_BORDER, POS_FILL, POS_TEXT,
    CRIT_BORDER, CRIT_FILL,
    NEG_BORDER, NEG_FILL,
    TEAL_BORDER, TEAL_FILL,
    INDIGO_BORDER, INDIGO_FILL,
    PINK_BORDER, PINK_FILL,
    WHITE, LEGEND_STROKE, BROWN,
})

PALETTE_LC: frozenset[str] = frozenset(c.lower() for c in PALETTE)
