#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import urllib.error
import urllib.request
import re
from dataclasses import dataclass
from urllib.parse import urlparse

PRODUCT = "Signalproof Intelligence Community CLI"
VERSION = "0.3.0"
RELEASE = "V2/RD1"
GENERATION = "Sagittarius Horizon"
DEFAULT_OLLAMA_URL = os.environ.get(
    "SIGNALPROOF_OLLAMA_URL", "http://127.0.0.1:11434"
).rstrip("/")


@dataclass(frozen=True)
class ModelSpec:
    alias: str
    tag: str
    display_name: str
    upstream: str


# Connector declarations only. No model weights are bundled, downloaded or
# installed by this repository or CLI.
SUPPORTED_MODELS = {
    "granite": ModelSpec(
        "granite", "granite4.2:8b", "IBM Granite 4.2 8B", "IBM"
    ),
    "qwen": ModelSpec(
        "qwen", "qwen3.6:latest", "Qwen 3.6", "Qwen / Alibaba"
    ),
    "gemma": ModelSpec(
        "gemma", "gemma4:latest", "Gemma 4", "Google"
    ),
    "ministral": ModelSpec(
        "ministral", "ministral-3:3b", "Ministral 3 3B", "Mistral AI"
    ),
}

MODEL_ORDER = ("granite", "qwen", "gemma", "ministral")


class CommunityError(RuntimeError):
    pass


PUBLIC_WORDMARK = (
    "███████╗ ██╗  ██████╗  ███╗   ██╗  █████╗  ██╗      ██████╗  ██████╗   ██████╗   ██████╗  ███████╗",
    "██╔════╝ ██║ ██╔════╝  ████╗  ██║ ██╔══██╗ ██║      ██╔══██╗ ██╔══██╗ ██╔═══██╗ ██╔═══██╗ ██╔════╝",
    "███████╗ ██║ ██║  ███╗ ██╔██╗ ██║ ███████║ ██║      ██████╔╝ ██████╔╝ ██║   ██║ ██║   ██║ █████╗",
    "╚════██║ ██║ ██║   ██║ ██║╚██╗██║ ██╔══██║ ██║      ██╔═══╝  ██╔══██╗ ██║   ██║ ██║   ██║ ██╔══╝",
    "███████║ ██║ ╚██████╔╝ ██║ ╚████║ ██║  ██║ ███████╗ ██║      ██║  ██║ ╚██████╔╝ ╚██████╔╝ ██║",
    "╚══════╝ ╚═╝  ╚═════╝  ╚═╝  ╚═══╝ ╚═╝  ╚═╝ ╚══════╝ ╚═╝      ╚═╝  ╚═╝  ╚═════╝   ╚═════╝  ╚═╝",
)
PUBLIC_ROW_COLORS = (
    "\x1b[1;38;2;255;228;86m",
    "\x1b[1;38;2;255;222;73m",
    "\x1b[38;2;255;204;41m",
    "\x1b[38;2;255;192;55m",
    "\x1b[38;2;207;136;55m",
    "\x1b[38;2;189;116;44m",
)


def color_enabled(stream=None) -> bool:
    stream = stream if stream is not None else sys.stdout
    return bool(getattr(stream, "isatty", lambda: False)()) and (
        "NO_COLOR" not in os.environ
        and os.environ.get("TERM", "") != "dumb"
    )


ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _visible_len(value: str) -> int:
    return len(ANSI_RE.sub("", value))


def _status_panel(lines: list[str], *, columns: int, ansi: bool) -> str:
    """Site-matched thin gold status frame with title embedded in top border."""
    width = max(64, min(columns, 100))
    inner = width - 2
    title = " SIGNALPROOF COMMUNITY CLI "
    gold = "\x1b[1;38;2;255;215;0m" if ansi else ""
    white = "\x1b[38;2;230;230;230m" if ansi else ""
    reset = "\x1b[0m" if ansi else ""
    trail = max(1, inner - len(title) - 1)
    out = [gold + "┌─" + title + ("─" * max(1, trail - 1)) + "┐" + reset]
    for value in lines:
        raw = ANSI_RE.sub("", value)
        raw = raw[: max(0, inner - 3)]
        padding = " " * max(0, inner - 2 - len(raw))
        body = white + raw + reset if ansi else raw
        out.append(gold + "│" + reset + " " + body + padding + gold + "│" + reset)
    out.append(gold + "└" + ("─" * inner) + "┘" + reset)
    return "\n".join(out)


def render_community_header(
    alias: str,
    *,
    columns: int | None = None,
    ansi: bool | None = None,
    installed: bool | None = None,
) -> str:
    """Match the site's approved CLI structure using public-only facts."""
    if alias not in SUPPORTED_MODELS:
        raise ValueError("unsupported public model alias")
    if columns is None:
        columns = shutil.get_terminal_size(fallback=(120, 30)).columns
    columns = max(1, int(columns))
    if ansi is None:
        ansi = color_enabled()

    reset = "\x1b[0m" if ansi else ""
    red = "\x1b[38;2;227;24;53m" if ansi else ""
    gold = "\x1b[1;38;2;255;211;49m" if ansi else ""
    green = "\x1b[38;2;67;207;117m" if ansi else ""
    gray = "\x1b[38;2;157;157;157m" if ansi else ""
    rows: list[str] = []

    if columns >= max(map(len, PUBLIC_WORDMARK)):
        rows.extend(
            (PUBLIC_ROW_COLORS[i] + line + reset) if ansi else line
            for i, line in enumerate(PUBLIC_WORDMARK)
        )
    else:
        rows.append(gold + "SIGNALPROOF" + reset)

    bar = red + ("═" * min(columns, 100)) + reset
    rows.extend((
        bar,
        gold + "SIGNALPROOF INTELLIGENCE" + reset
        + "  " + red + "//" + reset
        + "  " + gold + "HUMAN-CONTROLLED AI SYSTEMS" + reset,
        red + "SP://COMMUNITY" + reset + "  //  "
        + gold + "CORE " + RELEASE + reset + "  //  "
        + gold + "VISUAL V3/RD4" + reset,
        bar,
        "",
    ))

    state = (
        "READY"
        if installed is True
        else "NOT INSTALLED LOCALLY"
        if installed is False
        else "UNVERIFIED (CHECKED ON FIRST PROMPT)"
    )
    spec = SUPPORTED_MODELS[alias]
    panel = [
        "OPERATOR     LOCAL USER",
        "TRANSPORT    LOOPBACK ONLY",
        f"ROUTE        {alias}",
        f"MODEL        {spec.display_name}",
        f"TAG          {spec.tag}",
        f"STATE        {state}",
    ]
    if columns >= 64:
        rows.append(_status_panel(panel, columns=columns, ansi=ansi))
    else:
        rows.append(gold + "SIGNALPROOF COMMUNITY CLI" + reset)
        rows.extend(panel)

    rows.extend((
        "",
        "Commands: /help  /status  /routes  /model granite  /model qwen  /model gemma  /model ministral  /exit",
        "No silent model failover. Model changes require an explicit /model command.",
        "",
        green + "YOU" + reset + "  " + gray + f"[{alias}]" + reset + "  " + green + ">" + reset,
        "",
        gold + "SAGITTARIUS HORIZON  //  GENERATION V1  //  COMMUNITY CONNECTORS" + reset,
    ))
    return "\n".join(rows)


def require_loopback(url: str) -> None:
    parsed = urlparse(url)
    if (
        parsed.scheme != "http"
        or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}
    ):
        raise CommunityError(
            "community local-model transport must remain HTTP loopback-only"
        )


def request_json(
    base_url: str,
    path: str,
    *,
    method: str = "GET",
    payload: dict | None = None,
    timeout: int = 300,
) -> dict:
    require_loopback(base_url)
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        base_url.rstrip("/") + path,
        data=data,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            value = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read(2048).decode("utf-8", errors="replace")
        raise CommunityError(f"Ollama HTTP {exc.code}: {detail}") from exc
    except (
        urllib.error.URLError,
        TimeoutError,
        OSError,
        json.JSONDecodeError,
    ) as exc:
        raise CommunityError(f"local Ollama unavailable: {exc}") from exc
    if not isinstance(value, dict):
        raise CommunityError("Ollama returned a non-object response")
    return value


def inventory(base_url: str) -> dict[str, dict]:
    payload = request_json(base_url, "/api/tags", timeout=10)
    rows = payload.get("models")
    if not isinstance(rows, list):
        raise CommunityError("Ollama model inventory returned an invalid shape")
    result: dict[str, dict] = {}
    for row in rows:
        if isinstance(row, dict):
            name = str(row.get("name") or row.get("model") or "").strip()
            if name:
                result[name] = row
    return result


def model_report(base_url: str) -> list[dict]:
    available = inventory(base_url)
    report = []
    for alias in MODEL_ORDER:
        spec = SUPPORTED_MODELS[alias]
        row = available.get(spec.tag, {})
        report.append({
            "alias": spec.alias,
            "display_name": spec.display_name,
            "upstream": spec.upstream,
            "model": spec.tag,
            "installed": spec.tag in available,
            "digest": str(row.get("digest") or "") or None,
            "size": row.get("size"),
            "connection_mode": "LOCAL_OLLAMA_CONNECTOR",
            "governance_mode": "NON_EXECUTING_ADVISORY",
            "direct_model_authority": False,
            "model_install_authority": False,
            "weights_bundled": False,
        })
    return report


def governed_advisory(
    base_url: str,
    alias: str,
    prompt: str,
    *,
    timeout: int = 900,
) -> dict:
    if alias not in SUPPORTED_MODELS:
        raise CommunityError(
            "unsupported model alias; choose granite, qwen, gemma, or ministral"
        )
    if not isinstance(prompt, str) or not prompt.strip():
        raise CommunityError("prompt must be non-empty")

    spec = SUPPORTED_MODELS[alias]
    available = inventory(base_url)
    if spec.tag not in available:
        raise CommunityError(
            f"connector target is not installed in local Ollama: {spec.tag}. "
            "Install/obtain the model independently under its upstream terms, "
            "then retry."
        )
    digest = str(available[spec.tag].get("digest") or "").strip()
    if not digest:
        raise CommunityError(f"local model digest is unavailable for {spec.tag}")

    system = (
        "You are connected through Signalproof Intelligence Community advisory "
        "mode. You may explain, analyze, draft, summarize, or recommend. "
        "You have no tool, file, browser, credential, model-install, or remote "
        "server authority and must not claim an external action was executed."
    )
    body = {
        "model": spec.tag,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt.strip()},
        ],
        "stream": False,
    }
    if alias == "qwen":
        body["think"] = False

    result = request_json(
        base_url, "/api/chat", method="POST", payload=body, timeout=timeout
    )
    message = result.get("message")
    if not isinstance(message, dict):
        raise CommunityError("model response did not contain a message object")
    answer = str(message.get("content") or "").strip()
    if not answer:
        raise CommunityError("model returned an empty final response")

    return {
        "product": PRODUCT,
        "version": VERSION,
        "release": RELEASE,
        "generation": GENERATION,
        "route": alias,
        "model": spec.tag,
        "model_digest": digest,
        "connection_mode": "LOCAL_OLLAMA_CONNECTOR",
        "governance_mode": "NON_EXECUTING_ADVISORY",
        "direct_model_authority": False,
        "model_install_authority": False,
        "browser_authority": False,
        "response": answer,
    }


def render_models(rows: list[dict]) -> None:
    print("Signalproof Intelligence Community CLI - local model connectors")
    print()
    for row in rows:
        marker = "READY" if row["installed"] else "NOT INSTALLED LOCALLY"
        print(f"{row['alias']:<10} {row['model']:<22} {marker}")
    print()
    print(
        "Connector definitions only. This CLI never downloads or bundles model weights."
    )
    print("No silent model substitution; exact listed tags are used.")


def cmd_setup(args) -> int:
    # Backward-compatible Public1 command. It is now strictly read-only.
    rows = model_report(args.ollama_url)
    if args.model:
        rows = [row for row in rows if row["alias"] == args.model]
    if args.json:
        print(json.dumps({
            "status": "READ_ONLY_CONNECTOR_CHECK",
            "downloads_performed": False,
            "models": rows,
        }, indent=2, sort_keys=True))
    else:
        render_models(rows)
        print()
        print(
            "Setup is read-only in this release. Install models independently "
            "from their upstream distribution/runtime if you choose to use them."
        )
    return 0


def cmd_models(args) -> int:
    rows = model_report(args.ollama_url)
    if args.json:
        print(json.dumps(rows, indent=2, sort_keys=True))
    else:
        render_models(rows)
    return 0


def cmd_status(args) -> int:
    rows = model_report(args.ollama_url)
    payload = {
        "product": PRODUCT,
        "version": VERSION,
        "release": RELEASE,
        "generation": GENERATION,
        "ollama_url": args.ollama_url,
        "transport": "LOOPBACK_ONLY",
        "model_download_authority": False,
        "supported_connectors": rows,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        render_models(rows)
    return 0


def cmd_ask(args) -> int:
    result = governed_advisory(
        args.ollama_url, args.model, args.prompt, timeout=args.timeout
    )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["response"])
    return 0


def _installed(base_url: str, alias: str) -> bool:
    try:
        return SUPPORTED_MODELS[alias].tag in inventory(base_url)
    except CommunityError:
        return False


def cmd_chat(args) -> int:
    alias = args.model
    print(render_community_header(alias, installed=None))
    while True:
        try:
            prompt = input(f"YOU [{alias}] > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if prompt.lower() in {"/exit", "/quit", "exit", "quit"}:
            break
        if not prompt:
            continue
        lower = prompt.lower()
        if lower == "/help":
            print(
                "/status | /routes | /model granite | /model qwen | "
                "/model gemma | /model ministral | /exit"
            )
            continue
        if lower == "/status":
            rows = model_report(args.ollama_url)
            current = next(row for row in rows if row["alias"] == alias)
            print(json.dumps(current, indent=2, sort_keys=True))
            continue
        if lower == "/routes":
            render_models(model_report(args.ollama_url))
            continue
        if lower == "/model":
            print(f"Current: {alias} -> {SUPPORTED_MODELS[alias].tag}")
            print("Available: granite, qwen, gemma, ministral")
            continue
        if lower.startswith("/model "):
            requested = lower.split(None, 1)[1].strip()
            if requested not in SUPPORTED_MODELS:
                print("ERROR: choose granite, qwen, gemma, or ministral")
                continue
            if not _installed(args.ollama_url, requested):
                print(
                    "ERROR: connector target is not installed locally: "
                    + SUPPORTED_MODELS[requested].tag
                )
                print("Route unchanged. This CLI does not download models.")
                continue
            print(f"Signalproof community route changed: {alias} -> {requested}")
            alias = requested
            continue
        try:
            result = governed_advisory(
                args.ollama_url, alias, prompt, timeout=args.timeout
            )
            print(f"Signalproof [{alias.upper()}] > {result['response']}")
        except CommunityError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
    print("Signalproof Intelligence Community session closed.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=PRODUCT)
    parser.add_argument("--ollama-url", default=DEFAULT_OLLAMA_URL)
    parser.add_argument("--json", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser(
        "setup",
        help="read-only compatibility command: check exact connector targets",
    )
    p.add_argument(
        "--model",
        choices=MODEL_ORDER,
        help="limit readiness check to one connector",
    )
    p.set_defaults(func=cmd_setup)

    p = sub.add_parser(
        "models", help="list exact supported local model connectors"
    )
    p.set_defaults(func=cmd_models)

    p = sub.add_parser(
        "status", help="show local connector readiness without downloading models"
    )
    p.set_defaults(func=cmd_status)

    p = sub.add_parser(
        "ask", help="send one advisory prompt through an exact local connector"
    )
    p.add_argument("model", choices=MODEL_ORDER)
    p.add_argument("prompt")
    p.add_argument("--timeout", type=int, default=900)
    p.set_defaults(func=cmd_ask)

    p = sub.add_parser("chat", help="open a local advisory connector session")
    p.add_argument("model", choices=MODEL_ORDER)
    p.add_argument("--timeout", type=int, default=900)
    p.set_defaults(func=cmd_chat)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        require_loopback(args.ollama_url)
        return args.func(args)
    except CommunityError as exc:
        if getattr(args, "json", False):
            print(json.dumps({"status": "error", "error": str(exc)}))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
