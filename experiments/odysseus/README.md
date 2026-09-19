# Odysseus (experimental)

Testing [Odysseus](https://github.com/pewdiepie-archdaemon/odysseus), a self-hosted
AI workspace, on my homelab laptop.

**What's here:** my `docker-compose.yml`. App source and Dockerfile are
upstream's and aren't reproduced here; `${VAR}`s in the compose file need a
real `.env` that isn't included, since this is meant as a showcase, not a
run-it-yourself setup.

**Setup:**
- Self-hosted Ollama separately, running gpt-oss-20b, and
  connected it to Odysseus as the model backend (I couldn't get the native
  setup working through Cookbook — the model would ignore the GPU and only
  use the CPU. Tried to track it down, ended up on this workaround instead)
- Built and audited a resume-tailoring skill against gpt-oss-20b, running
  several iterations — writing the skill, then checking outputs for
  hallucinations (invented job titles, fabricated details) and tightening the
  prompt/scope each pass until it stopped making things up
- Hardware: RTX 2080 Max-Q (8GB VRAM), i7-9750H, 64GB RAM
- Integrated with my self-hosted CalDAV server (also synced to my phone) and
  Gmail, so I can ask it to check my calendar or draft email replies
- Early-stage — still evaluating performance on this hardware vs. cloud-hosted
  models

**Why:** wanted to see how far a fully local setup could go for everyday task
automation without sending data to a third party.