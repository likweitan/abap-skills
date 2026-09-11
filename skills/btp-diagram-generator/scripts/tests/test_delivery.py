from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from btp_builder import BtpDiagram  # noqa: E402


class DeliveryTests(unittest.TestCase):
    def _diagram(self) -> BtpDiagram:
        diagram = BtpDiagram(level="L1", title="Delivery Contract")
        btp = diagram.btp_container()
        diagram.service("hana cloud", in_=btp)
        return diagram

    def test_render_is_deterministic(self) -> None:
        diagram = self._diagram()
        self.assertEqual(diagram.to_xml(), diagram.to_xml())

    def test_failed_atomic_replace_preserves_prior_artifact(self) -> None:
        diagram = self._diagram()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "diagram.drawio"
            output.write_text("trusted prior artifact", encoding="utf-8")

            with patch.object(os, "replace", side_effect=OSError("commit failed")):
                with self.assertRaisesRegex(OSError, "commit failed"):
                    diagram.save(output)

            self.assertEqual(output.read_text(encoding="utf-8"), "trusted prior artifact")
            self.assertEqual(list(output.parent.glob("*.tmp")), [])

    def test_showcase_json_receipt_is_machine_readable(self) -> None:
        diagram = self._diagram()
        with tempfile.TemporaryDirectory() as directory:
            output = diagram.save(Path(directory) / "diagram.drawio")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "validate_diagram.py"),
                    str(output),
                    "--quality",
                    "showcase",
                    "--json",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            receipt = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(receipt["ok"])
            self.assertEqual(receipt["quality"], "showcase")
            self.assertEqual(receipt["validation"]["checksPassed"], 6)
            self.assertEqual(len(receipt["artifact"]["sha256"]), 64)

    def test_quality_profile_promotes_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "off-palette.drawio"
            output.write_text(
                self._diagram().to_xml().replace(
                    "strokeColor=#0070F2", "strokeColor=#123456", 1
                ),
                encoding="utf-8",
            )

            receipts = {}
            for quality in ("standard", "showcase"):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(SCRIPTS / "validate_diagram.py"),
                        str(output),
                        "--quality",
                        quality,
                        "--json",
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                receipts[quality] = (result.returncode, json.loads(result.stdout))

            standard_code, standard = receipts["standard"]
            self.assertEqual(standard_code, 0)
            self.assertTrue(standard["ok"])
            self.assertEqual(standard["diagnostics"][0]["severity"], "warning")
            self.assertEqual(standard["diagnostics"][0]["code"], "style/off-palette")

            showcase_code, showcase = receipts["showcase"]
            self.assertEqual(showcase_code, 1)
            self.assertFalse(showcase["ok"])
            self.assertEqual(showcase["diagnostics"][0]["severity"], "error")


if __name__ == "__main__":
    unittest.main()