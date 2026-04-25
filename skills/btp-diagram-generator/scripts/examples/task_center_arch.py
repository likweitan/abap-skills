"""Regenerate the BTP Task Center architecture using the new btp_builder API.

This is the canonical "Quick Path" example referenced in SKILL.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from btp_builder import BtpDiagram


def main() -> Path:
    d = BtpDiagram(level="L1", title="Task Center Reference Architecture")

    # Layout: BTP container in centre, users on left, externals on right.
    btp = d.btp_container(x=260, y=80, w=560, h=440, sub_label="Subaccount", env_label="Multi-Cloud")
    sub = d.subaccount(parent=btp, label="Subaccount", x=btp.x + 24, y=btp.y + 110, w=520, h=170)

    # Inside the Subaccount card: Work Zone → Task Center
    wz = d.service("work zone", in_=sub, x=sub.x + 60, y=sub.y + 60)
    tc = d.service("task center", right_of=wz)

    # Cloud Identity sits inside BTP container, below Task Center
    ci = d.service("cloud identity", below=tc)

    # Users on the left
    eu = d.user("End User", x=60, y=btp.y + 100)
    ac = d.app_client("Application Clients\n(Mobile or Desktop)", below=eu)

    # External systems on the right
    s4 = d.external("SAP S/4HANA\nOn-Premise Solutions",
                    x=btp.right_edge() + 40, y=btp.y + 70, kind="sap")
    third = d.external("3rd Party\nApplications",
                       below=s4, kind="non-sap")
    cloud = d.external("SAP Cloud\nApplications",
                       below=third, kind="sap")

    # 3rd-party IdP at the bottom, dashed up to Cloud Identity
    idp = d.idp("3rd-party Identity Provider",
                x=ci.center_x() - 140, y=btp.bottom_edge() + 60)

    # Wire it up
    d.connect(eu, ac, direction="down")
    d.connect(ac, wz, direction="right")
    d.connect(wz, tc, kind="dblhd")
    d.connect(tc, ci, kind="dblhd", direction="down")
    d.connect(tc, s4, direction="right")
    d.connect(tc, third, direction="right")
    d.connect(tc, cloud, direction="right")
    d.connect(idp, ci, kind="dashed", direction="up")

    # examples/ → scripts/ → btp-diagram-generator/ → skills/ → .github/ → repo root
    out = Path(__file__).resolve().parents[5] / "btp-task-center-architecture.drawio"
    d.save(out)
    print(f"wrote {out}")
    return out


if __name__ == "__main__":
    main()
