# Immich

Self-hosted Google Photos alternative — photo/video backup, ML-based search
and facial recognition, GPU-accelerated.

**What's here:** my `docker-compose.yml`. App images pulled
from [Immich's official releases](https://github.com/immich-app/immich),
pinned by SHA digest rather than a tag.

**Setup decisions:**
- GPU passthrough (`runtime: nvidia`) for the ML container, so face/object
  recognition runs on-device instead of CPU
- Runs on its own bridge network (`immich-isolated-net`), isolated from the
  arr-stack — the media automation containers can't reach the photo library
  or its database, and vice versa
- Images pinned by SHA digest, not `:latest`, so an upstream tag change can't
  silently swap what's running
- `no-new-privileges` on every container

**Why:** Wanted a shared photo backup and search for the household that doesn't hand our libraries to a
third party, and the ML search/face recognition is pretty good once the catalog's built up.