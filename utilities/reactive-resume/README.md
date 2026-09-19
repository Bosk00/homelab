# Reactive Resume

Self-hosted resume builder — build, format, and export resumes without a
third-party account.

**What's here:** my `docker-compose.yml`. App image from
[Reactive Resume's official releases](https://github.com/reactive-resume/reactive-resume),
pinned at v5.3.0.

**Note:** the app also reads secrets directly from a `.env` file (`env_file`)
that never appears in the compose YAML itself — `DATABASE_URL`,
`ACCESS_TOKEN_SECRET`, `REFRESH_TOKEN_SECRET` — worth knowing if you're
setting this up yourself, since the sanitizer script can't catch these on
its own.

**Setup:** found this online, saw it was self-hostable, and figured I'd try
it out. Pretty cool once it's actually up and running, which wasn't hard to do.

**Why:** wanted my resume data sitting on my own Postgres instance instead
of a hosted builder's database, and it's genuinely a solid tool once it's
set up.