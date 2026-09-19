# Arr Stack

Media automation: request → find → download → organize → serve, hands-off.

  **What's here:** my `docker-compose.yml`. Images from
[LinuxServer.io](https://www.linuxserver.io/) and each project's own
GitHub, pinned by SHA digest.

**Stack:**
- **Jellyfin** — media server, GPU-accelerated transcoding, sized for a few
  concurrent streams across the household
- **Prowlarr** — indexer management, feeds Sonarr/Radarr
- **Sonarr** / **Radarr** — TV/movie automation
- **SABnzbd** — download client
- **Bazarr** — subtitles
- **Seerr** — request UI, so I don't have to touch the other six directly

**Setup decisions:**
- Runs on its own network (`media-automation-net`), isolated from Immich —
  media automation never touches the photo library or its database
- GPU passthrough on Jellyfin only, for hardware transcoding
- Per-service resource limits, sized to what each container actually needs
- Images pinned by SHA digest, not `:latest`
- Paths and PUID/PGID/TZ pulled into `${VARS}` — see `.env.example`

**Tried and removed:** added LazyLibrarian for ebook automation, but my
family couldn't find the books they wanted through it, so it came out of
the stack.

**Why:** wanted to see how hard it was to set up a self-hosted media-server
(not that hard), also replaced a manual "download, rename, move file" habit
with something that does it consistently and lets me request from my phone.