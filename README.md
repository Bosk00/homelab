# Homelab

Self-hosted infrastructure for my household, running on Docker + Docker
Compose on Ubuntu Server — a repurposed laptop acting as a dedicated home
server. Used daily by 4 people for media streaming, photo backup, shared
calendar, ad-blocking DNS, and home automation.

## Structure

homelab/
├── media-server/
│   ├── arr-stack/         # Jellyfin, Sonarr, Radarr, Prowlarr, SABnzbd, Bazarr, Seerr
│   └── immich/            # Photo backup, GPU-accelerated ML search
├── utilities/
│   ├── dashboard/         # Reverse proxy + service dashboard
│   ├── pihole/            # DNS-level ad-blocking
│   ├── homeassistant/     # Automation, sensors, notifications
│   ├── caldav/            # Self-hosted calendar
│   ├── uptime-kuma/       # Tried, replaced by Home Assistant
│   └── reactive-resume/   # Self-hosted resume builder/editor
├── experiments/
│   └── odysseus/          # Self-hosted AI workspace connected to local LLM from Ollama in same docker-compose
├── sanitize_env.py        # Script used to prep this repo (see below)
├── scan_compose.sh        # Script used to prep this repo (see below)
└── README.md


Each folder has its own README with more detail and the reasoning behind
specific setup choices.

## About this repo

Every `docker-compose.yml` here is a copy of what's actually running on my laptop, with
secrets and host-specific paths pulled out into `${VARIABLES}`. Two scripts
in this repo did the heavy lifting:

- **[`sanitize_env.py`](sanitize_env.py)** — scans each compose file,
  rewrites hardcoded values into env-var references, generates a matching
  `.env.example`, and flags anything it can't safely auto-fix (hardcoded
  paths, secrets embedded in connection strings) for a manual pass.
- **[`scan_compose.sh`](scan_compose.sh)** — a read-only sanity check I ran
  alongside it: greps every compose file for anything that still looks like
  a hardcoded path or a literal secret, and counts how many `${VAR}`
  references are already in place.
- **Note on `.env.example`:** the sanitizer generates one for each stack, listing
  every env var the compose file expects with blank values — no real config,
  just names. Decided against including them here — if you're actually trying
  to run one of these, pull the image, read its docs, and set up your own `.env`
  to match the structure in the compose file. The `${VARIABLE}` names in each
  `docker-compose.yml` already tell you what's expected.

Neither is foolproof — both are pattern-based, so anything shaped
unusually (a secret buried in a connection string, a var pulled in via
`env_file` rather than referenced directly) still needed a manual read
of each file. That manual pass is where most of the real fixes came from.

This is meant to show how things are set up, not to be cloned and run —
no real `.env` files are included, and a couple of stacks reference
config/scripts that live outside this repo entirely.

## Recurring decisions across the stacks

- **Network isolation where it matters** — arr-stack and Immich run on
  separate Docker networks and share nothing; media automation can't
  reach the photo library or its database
- **Least-privilege by default** — `no-new-privileges` on every container;
  `cap_drop: ALL` applied where I verified it doesn't break the container
  (see `seerr` in the arr-stack, and `searxng` in odysseus, for examples) —
  most LinuxServer.io images and Immich's containers rely on retained
  capabilities to run as-is via their own PUID/PGID handling, so this
  wasn't applied blanket across the board
- **Pinned images** — SHA digests where possible, dated version tags
  elsewhere, to avoid a silent break or supply-chain surprise from an
  upstream `:latest` tag
- **Things I tried and cut** — LazyLibrarian (arr-stack) and Uptime Kuma
  (utilities) both got removed after testing them against a real use
  case, not left running out of inertia

---

Organized and maintained solo, for actual daily use by my household.