"""Insightify backend package.

Importing this package configures stdout/stderr for UTF-8 so Unicode
log characters (✓, ✗, emojis) never crash on Windows consoles that
default to cp1252/legacy encodings.
"""
import sys

for _stream in (sys.stdout, sys.stderr):
    try:
        if _stream is not None and hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        # Non-fatal: fall back to whatever encoding is available
        pass
