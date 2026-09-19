# Pi-hole

DNS-level ad-blocking and local DNS for the whole household.

**Setup:**
- Web UI on `8053`, not `80` — port 80 is reserved for Nginx Proxy Manager
  on this host
- `FTLCONF_dns_listeningMode=ALL`, required for bridge networking per
  Pi-hole's own docs
- Blocklist also includes smart-plug vendor cloud domains, blocking them
  from phoning home over WAN (see `utilities/homeassistant/` for why —
  DNS-level blocking only, not a real network boundary yet)

**Known limitation:** running in bridge mode means per-device query stats
show Docker's gateway IP instead of each device's real IP — ad-blocking
still works fine, just lose the per-device breakdown in the dashboard.

**Why:** network-wide ad-blocking without installing anything per-device,
plus it's the DNS chokepoint for blocking the smart plugs above.