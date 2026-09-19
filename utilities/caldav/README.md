# CalDAV (Radicale)

Self-hosted calendar server.

**What's here:** just the `docker-compose.yml` — no configurable env vars,
so no `.env.example`.

**Setup:** wanted to try self-hosting a calendar instead of relying on a
third-party one. Turned out to be pretty painless — running within an hour
or two. Had my local LLM (see `experiments/odysseus/`) generate a custom
`.ics` file from my daily schedule and imported it in, then synced the
calendar to my phone and to Odysseus itself, so I can ask the assistant
about the schedule for the day.

**Why:** wanted my calendar data living on my own hardware instead of
Google's, and it turned out to be one of the easier things in this repo
to stand up.