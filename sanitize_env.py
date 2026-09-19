#!/usr/bin/env python3
"""
sanitize_env.py — parameterize docker-compose env vars and generate .env.example

Usage:
    python3 sanitize_env.py /path/to/staging-folder

What it does, per docker-compose.yml (or *-compose.yml / *.yaml) it finds:
  1. Backs up the original file once, as <file>.bak (only if a .bak doesn't
     already exist — so re-running never overwrites your original).
  2. Finds environment lines written as:
         KEY: literal_value        (mapping style)
         - KEY=literal_value       (list style)
     and rewrites the value to ${KEY}, in place.
  3. Collects every ${VAR} in the file (the ones it just created, plus any
     that were already there) and writes a .env.example beside the compose
     file: just the variable names, blank values, no real data.
  4. Also pulls in variable NAMES (never values) from any .env file sitting
     in the same folder, in case something is used by the app but isn't
     referenced directly in the compose file.
  5. Prints a report of what it changed, and — separately — a list of things
     it deliberately did NOT touch because auto-fixing them isn't safe:
     hardcoded absolute paths in volumes, and anything password/secret/token
     -shaped that wasn't in a normal KEY: value environment line (e.g.
     embedded in a connection string). Have to manually fix these by hand.

Nothing is deleted. Nothing is uploaded. This only edits files inside the
staging folder that it is pointed at.
"""

import re
import sys
from pathlib import Path

COMPOSE_NAME_RE = re.compile(r'(^|[-_.])compose\.ya?ml$', re.I)

# key: value   (mapping style env entry)
MAP_LINE_RE = re.compile(r'^(?P<indent>\s*)(?P<key>[A-Z][A-Z0-9_]*)\s*:\s*(?P<val>.+?)\s*(?P<comment>#.*)?$')
# - KEY=value  (list style env entry)
LIST_LINE_RE = re.compile(r'^(?P<indent>\s*-\s+)(?P<key>[A-Z][A-Z0-9_]*)=(?P<val>.+?)\s*(?P<comment>#.*)?$')

DOLLAR_VAR_RE = re.compile(r'\$\{([A-Za-z_][A-Za-z0-9_]*)(:-[^}]*)?\}')
SENSITIVE_RE = re.compile(r'PASS|SECRET|TOKEN|KEY|CREDENTIAL|AUTH', re.I)

# things worth flagging for a human, even though we won't auto-fix them
HOST_PATH_RE = re.compile(r'^(?P<indent>\s*-\s+)(?P<path>(~|/)[^:$][^:]*):')
LOOSE_SECRET_RE = re.compile(r'(password|secret|token|api[_-]?key|passphrase)\s*[:=]\s*["\']?[^\s"\'{$][^\s"\']{2,}', re.I)
PEM_RE = re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY')


def find_compose_files(root: Path):
    out = []
    for p in root.rglob('*'):
        if not p.is_file():
            continue
        if '.git' in p.parts or 'node_modules' in p.parts:
            continue
        name = p.name.lower()
        if name in ('docker-compose.yml', 'docker-compose.yaml', 'compose.yml', 'compose.yaml'):
            out.append(p)
        elif COMPOSE_NAME_RE.search(name):
            out.append(p)
    return sorted(out)


def strip_quotes(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
        return v[1:-1]
    return v


def process_file(path: Path):
    text = path.read_text()
    lines = text.splitlines(keepends=False)
    new_lines = []
    fixed = []  # (line_no, key)
    skipped_already_param = 0

    for i, line in enumerate(lines, 1):
        replaced = False
        for rx, fmt in ((MAP_LINE_RE, "map"), (LIST_LINE_RE, "list")):
            m = rx.match(line)
            if not m:
                continue
            key = m.group('key')
            val = strip_quotes(m.group('val'))
            comment = m.group('comment') or ''
            if not val or val.startswith('${'):
                if val.startswith('${'):
                    skipped_already_param += 1
                continue
            if val.lower() in ('true', 'false'):
                continue
            indent = m.group('indent')
            if fmt == "map":
                new_line = f"{indent}{key}: ${{{key}}}"
            else:
                new_line = f"{indent}{key}=${{{key}}}"
            if comment:
                new_line += f"  {comment}"
            new_lines.append(new_line)
            fixed.append((i, key))
            replaced = True
            break
        if not replaced:
            new_lines.append(line)

    new_text = "\n".join(new_lines) + ("\n" if text.endswith("\n") else "")

    if fixed:
        backup = path.with_suffix(path.suffix + '.bak')
        if not backup.exists():
            backup.write_text(text)
        path.write_text(new_text)

    return new_text, fixed, skipped_already_param


def collect_vars(text: str):
    return sorted(set(m.group(1) for m in DOLLAR_VAR_RE.finditer(text)))


def collect_env_file_keys(env_path: Path):
    keys = []
    if not env_path.exists():
        return keys
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k = line.split('=', 1)[0].strip()
        if re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', k):
            keys.append(k)
    return keys


def write_env_example(compose_path: Path, var_names, local_env_only_keys):
    out_path = compose_path.parent / '.env.example'
    all_names = sorted(set(var_names) | set(local_env_only_keys))
    if not all_names:
        return None
    lines = [f"# Generated from {compose_path.name} — fill in real values in a local .env, never commit .env"]
    for name in all_names:
        tag = "" if name in var_names else "  # used by the app, not referenced directly in compose"
        lines.append(f"{name}={tag}")
    out_path.write_text("\n".join(lines) + "\n")
    return out_path


def scan_leftover_risks(text: str, path: Path):
    findings = []
    for i, line in enumerate(text.splitlines(), 1):
        if HOST_PATH_RE.match(line):
            findings.append((i, "hardcoded host path", line.strip()))
        if PEM_RE.search(line):
            findings.append((i, "embedded private key block", line.strip()[:60] + "..."))
        elif LOOSE_SECRET_RE.search(line) and '${' not in line:
            findings.append((i, "secret-shaped value not in a plain env line", line.strip()))
    return findings


def main():
    if len(sys.argv) != 2:
        print("usage: python3 sanitize_env.py /path/to/staging-folder")
        sys.exit(1)

    root = Path(sys.argv[1]).expanduser().resolve()
    if not root.is_dir():
        print(f"not a directory: {root}")
        sys.exit(1)

    compose_files = find_compose_files(root)
    if not compose_files:
        print(f"no compose files found under {root}")
        sys.exit(0)

    print(f"found {len(compose_files)} compose file(s) under {root}\n")

    all_leftovers = []

    for cf in compose_files:
        rel = cf.relative_to(root)
        new_text, fixed, already = process_file(cf)
        var_names = collect_vars(new_text)
        local_env_keys = collect_env_file_keys(cf.parent / '.env')
        env_example = write_env_example(cf, var_names, local_env_keys)
        leftovers = scan_leftover_risks(new_text, cf)

        print(f"── {rel} ──")
        if fixed:
            for line_no, key in fixed:
                print(f"   fixed  line {line_no}: {key} → ${{{key}}}  (backup saved as {cf.name}.bak)")
        else:
            print("   nothing to auto-fix")
        if already:
            print(f"   ({already} value(s) already used ${{...}}, left alone)")
        if env_example:
            print(f"   wrote  {env_example.relative_to(root)}  ({len(var_names) + len(local_env_keys)} var(s))")
        if leftovers:
            print("   needs a human look:")
            for line_no, kind, snippet in leftovers:
                print(f"     line {line_no} — {kind}: {snippet}")
                all_leftovers.append((rel, line_no, kind, snippet))
        print()

    print("=" * 60)
    if all_leftovers:
        print(f"{len(all_leftovers)} item(s) across all files need a manual look — see 'needs a human look' lines above.")
        print("These are usually: a hardcoded /home or /mnt path in a volume mount,")
        print("or a secret embedded inside a URL/connection string rather than a plain KEY: value line.")
    else:
        print("Nothing flagged for manual review. Still worth reading each .env.example once before committing.")
    print()
    print("Next: open a couple of the changed compose files and the .env.example files to sanity check,")
    print("then delete the .bak files once you're happy:")
    print(f"    find {root} -name '*.bak' -delete")


if __name__ == '__main__':
    main()