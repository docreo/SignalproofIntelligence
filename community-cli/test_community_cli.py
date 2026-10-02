from __future__ import annotations

import importlib.util
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parent / "signalproof_community.py"
SPEC = importlib.util.spec_from_file_location("signalproof_community", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class CommunityCliTests(unittest.TestCase):
    def test_four_connector_tags_are_exact(self):
        self.assertEqual(
            {k: v.tag for k, v in MODULE.SUPPORTED_MODELS.items()},
            {
                "granite": "granite4.2:8b",
                "qwen": "qwen3.6:latest",
                "gemma": "gemma4:latest",
                "ministral": "ministral-3:3b",
            },
        )
        self.assertEqual(
            MODULE.MODEL_ORDER, ("granite", "qwen", "gemma", "ministral")
        )

    def test_loopback_is_required(self):
        for url in (
            "http://127.0.0.1:11434",
            "http://localhost:11434",
            "http://[::1]:11434",
        ):
            MODULE.require_loopback(url)
        for url in ("https://example.com", "http://example.com:11434"):
            with self.assertRaises(MODULE.CommunityError):
                MODULE.require_loopback(url)

    def test_parser_exposes_all_four_connector_aliases(self):
        parser = MODULE.build_parser()
        for alias in MODULE.MODEL_ORDER:
            args = parser.parse_args(["ask", alias, "hello"])
            self.assertEqual(args.model, alias)
            setup = parser.parse_args(["setup", "--model", alias])
            self.assertEqual(setup.model, alias)

    def test_setup_is_read_only_and_never_downloads(self):
        rows = [
            {
                "alias": alias,
                "display_name": spec.display_name,
                "upstream": spec.upstream,
                "model": spec.tag,
                "installed": False,
                "digest": None,
                "size": None,
                "connection_mode": "LOCAL_OLLAMA_CONNECTOR",
                "governance_mode": "NON_EXECUTING_ADVISORY",
                "direct_model_authority": False,
                "model_install_authority": False,
                "weights_bundled": False,
            }
            for alias, spec in MODULE.SUPPORTED_MODELS.items()
        ]
        out = io.StringIO()
        args = MODULE.build_parser().parse_args(["setup"])
        with patch.object(MODULE, "model_report", return_value=rows), redirect_stdout(out):
            self.assertEqual(args.func(args), 0)
        shown = out.getvalue()
        self.assertIn("read-only", shown.lower())
        self.assertIn("never downloads or bundles model weights", shown)

    def test_status_contract_denies_model_install_authority(self):
        rows = []
        for alias, spec in MODULE.SUPPORTED_MODELS.items():
            rows.append({
                "alias": alias,
                "display_name": spec.display_name,
                "upstream": spec.upstream,
                "model": spec.tag,
                "installed": False,
                "digest": None,
                "size": None,
                "connection_mode": "LOCAL_OLLAMA_CONNECTOR",
                "governance_mode": "NON_EXECUTING_ADVISORY",
                "direct_model_authority": False,
                "model_install_authority": False,
                "weights_bundled": False,
            })
        out = io.StringIO()
        args = MODULE.build_parser().parse_args(["--json", "status"])
        with patch.object(MODULE, "model_report", return_value=rows), redirect_stdout(out):
            self.assertEqual(args.func(args), 0)
        payload = json.loads(out.getvalue())
        self.assertFalse(payload["model_download_authority"])
        self.assertEqual(len(payload["supported_connectors"]), 4)
        self.assertTrue(all(not row["weights_bundled"] for row in payload["supported_connectors"]))

    def test_site_matched_plain_visual(self):
        result = MODULE.render_community_header("granite", columns=120, ansi=False)
        self.assertIn("SIGNALPROOF INTELLIGENCE", result)
        self.assertIn("HUMAN-CONTROLLED AI SYSTEMS", result)
        self.assertIn("SP://COMMUNITY", result)
        self.assertIn("CORE V2/RD1", result)
        self.assertIn("VISUAL V3/RD4", result)
        self.assertIn("┌─ SIGNALPROOF COMMUNITY CLI ", result)
        self.assertIn("└", result)
        self.assertIn("MODEL        IBM Granite 4.2 8B", result)
        self.assertIn("SAGITTARIUS HORIZON", result)
        self.assertIn("COMMUNITY CONNECTORS", result)
        self.assertIn("granite | qwen | gemma | ministral", result)
        self.assertNotIn("\x1b", result)
        self.assertNotIn("SIGNAL KEYS", result)
        self.assertNotIn("signalproof-granite", result)

    def test_color_visual_uses_site_gold_red_green(self):
        result = MODULE.render_community_header("qwen", columns=120, ansi=True)
        self.assertIn("\x1b[", result)
        self.assertIn("SIGNALPROOF INTELLIGENCE", result)
        self.assertIn("YOU", result)
        self.assertIn("[qwen]", result)

    def test_narrow_visual_fails_down_without_private_state(self):
        result = MODULE.render_community_header("gemma", columns=55, ansi=False)
        self.assertIn("SIGNALPROOF", result)
        self.assertIn("Gemma 4", result)
        self.assertNotIn("SIGNAL KEYS", result)

    def test_missing_switch_never_changes_route_or_downloads(self):
        out = io.StringIO()
        args = MODULE.build_parser().parse_args(["chat", "granite"])
        with (
            patch("builtins.input", side_effect=["/model qwen", "/exit"]),
            patch.object(MODULE, "_installed", return_value=False),
            redirect_stdout(out),
        ):
            self.assertEqual(args.func(args), 0)
        shown = out.getvalue()
        self.assertIn("Route unchanged", shown)
        self.assertIn("does not download models", shown)


if __name__ == "__main__":
    unittest.main()
