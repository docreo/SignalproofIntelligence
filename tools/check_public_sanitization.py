#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()

TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".py",
    ".ps1", ".cmd", ".bat", ".sh", ".js", ".ts", ".tsx", ".jsx",
    ".html", ".css", ".svg", ".xml", ".ini", ".cfg",
}

EXCLUDED_DIRS = {
    ".git", "__pycache__", ".venv", "venv", "node_modules",
}

MODEL_WEIGHT_SUFFIXES = {
    ".gguf", ".safetensors", ".onnx", ".pt", ".pth", ".ckpt",
}

RULES = [
    ("Windows user path", re.compile(r"\b[A-Za-z]:\\Users\\[^\\\s]+", re.IGNORECASE)),
    ("Signalproof workstation path", re.compile(r"\bF:\\(?:SP|Downloads|ai-apps)\\", re.IGNORECASE)),
    ("Unix home path", re.compile(r"(?<![A-Za-z0-9_])/home/[A-Za-z0-9._-]+/")),
    ("private IPv4 10/8", re.compile(r"\b10(?:\.\d{1,3}){3}\b")),
    ("private IPv4 192.168/16", re.compile(r"\b192\.168(?:\.\d{1,3}){2}\b")),
    ("private IPv4 172.16/12", re.compile(r"\b172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2}\b")),
    ("OpenSSH private key", re.compile(r"BEGIN OPENSSH PRIVATE KEY")),
    ("PEM private key", re.compile(r"BEGIN (?:RSA |EC |DSA )?PRIVATE KEY")),
    ("SSH public key material", re.compile(r"\bssh-(?:rsa|ed25519)\s+[A-Za-z0-9+/]{40,}={0,3}")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("OpenAI-style secret", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
]

# Exact private runtime identifiers must not leak into this public repository.
PRIVATE_ROUTE_IDS = (
    "signalproof-granite",
    "local.qwen-home-governed",
    "local.gemma-home-governed",
    "local.ministral-home-governed",
    "local.qwen-governed",
)

# The public Community CLI is connector-only. A real model-pull code path is a
# boundary violation. Documentation may use words such as "download" only to
# state that downloads are forbidden; executable invocation signatures are
# rejected here.
MODEL_PULL_PATTERNS = (
    re.compile(r"\bollama\s+pull\b", re.IGNORECASE),
    re.compile(r"subprocess\.(?:run|call|Popen)\([^\n]*\bpull\b", re.IGNORECASE),
    re.compile(r"os\.system\([^\n]*\b(?:ollama\s+)?pull\b", re.IGNORECASE),
)


def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or path == SELF:
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name not in {"NOTICE", "LICENSE"}:
            continue
        yield path


def main() -> int:
    failures: list[tuple[Path, str, str]] = []

    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in MODEL_WEIGHT_SUFFIXES:
            failures.append((
                path.relative_to(ROOT),
                "model weight artifact forbidden in public connector repository",
                path.name,
            ))
    for path in iter_text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for label, pattern in RULES:
            match = pattern.search(text)
            if match:
                failures.append((path.relative_to(ROOT), label, match.group(0)[:120]))

        lower = text.lower()
        for route_id in PRIVATE_ROUTE_IDS:
            if route_id.lower() in lower:
                failures.append((path.relative_to(ROOT), "private route id", route_id))

        for pattern in MODEL_PULL_PATTERNS:
            match = pattern.search(text)
            if match:
                failures.append((
                    path.relative_to(ROOT),
                    "model download/install execution path",
                    match.group(0)[:120],
                ))

    if failures:
        print("PUBLIC SANITIZATION: FAIL")
        for path, label, sample in failures:
            print(f"- {path}: {label}: {sample!r}")
        return 1

    print("PUBLIC SANITIZATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
