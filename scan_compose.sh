#!/bin/bash
# save as scan_compose.sh, run from inside homelab-repo-staging/

echo "=== Scanning all docker-compose.yml files ==="
echo

find . -name "docker-compose.yml" -o -name "*-compose.yml" | while read -r file; do
  echo "----------------------------------------"
  echo "FILE: $file"
  echo "----------------------------------------"

  echo "-- Hardcoded absolute/home paths (need \${VAR} treatment):"
  grep -n "~/\|/home/\|/mnt/storage" "$file" | grep -v '\${' || echo "  (none found)"

  echo
  echo "-- Possible secrets (password/token/key/secret literal values):"
  grep -ni "password\s*:\|secret\s*:\|token\s*:\|api_key\s*:\|-----BEGIN" "$file" | grep -v '\${' || echo "  (none found)"

  echo
  echo "-- Already using env vars (good, no action needed):"
  grep -n '\${' "$file" | wc -l | xargs echo "  count:"

  echo
done