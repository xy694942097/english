"""Resolve historical document paths used by generators after the UI/filesystem migration."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPING = json.loads((ROOT / 'engineering/design/document-paths-2026-10-11.json').read_text())


def document_path(old_path):
    return ROOT / MAPPING.get(str(old_path), str(old_path))


def write_document(path, text, *args, **kwargs):
    """Generators can still compose relative links using their old output base."""
    import os
    import re
    from urllib.parse import unquote
    path = Path(path)
    relative = str(path.relative_to(ROOT))
    old = next((old for old, new in MAPPING.items() if new == relative), None)
    if old:
        def rewrite(match):
            raw = match.group(1).strip()
            target = raw.strip('<>')
            link, sep, fragment = target.partition('#')
            if not link or re.match(r'^[a-z]+:|^//', link, re.I):
                return match.group(0)
            original = os.path.normpath(str(Path(old).parent / unquote(link)))
            destination = ROOT / MAPPING.get(original, original)
            rel = os.path.relpath(destination, path.parent) + (sep + fragment if sep else '')
            return '](' + ('<' + rel + '>' if raw.startswith('<') else rel) + ')'
        text = re.sub(r'\]\(([^)\n]+)\)', rewrite, text)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path.write_text(text, *args, **kwargs)
