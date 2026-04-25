"""SAP BTP Solution Diagram builder package.

Quick-start:

    from btp_builder import BtpDiagram
    d = BtpDiagram(level="L1", title="My Scenario")
    btp = d.btp_container()
    sub = d.subaccount(parent=btp, label="Subaccount")
    wz  = d.service("work zone",  in_=sub)
    tc  = d.service("task center", in_=sub, right_of=wz)
    ci  = d.service("cloud identity", in_=btp, below=tc)
    eu  = d.user("End User", left_of=btp)
    ac  = d.app_client("Application Clients\\n(Mobile or Desktop)", below=eu)
    s4  = d.external("SAP S/4HANA On-Premise Solutions", right_of=btp, kind="sap")
    d.connect(eu, ac); d.connect(ac, wz)
    d.connect(wz, tc); d.connect(tc, ci, kind="dblhd")
    d.connect(tc, s4)
    d.save("btp.drawio")        # validates first; raises on errors
"""
from .builder import BtpDiagram, NodeRef
from .icons import lookup_icon, list_icons, list_aliases
from .palette import PALETTE
from .styles import STYLES, port_pins
from .svg import upscale_svg_b64, patch_style_size

__all__ = [
    "BtpDiagram",
    "NodeRef",
    "lookup_icon",
    "list_icons",
    "list_aliases",
    "PALETTE",
    "STYLES",
    "port_pins",
    "upscale_svg_b64",
    "patch_style_size",
]
