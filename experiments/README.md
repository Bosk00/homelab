# Experiments

Stacks in here are testing/eval-stage, not day-to-day infrastructure like
the rest of the homelab — things I'm actively trying out, benchmarking, or
still deciding whether to keep running long-term.

## odysseus/

See [`odysseus/README.md`](odysseus/) for details.

One setup note: I considered giving Ollama its own separate compose file,
but running it as its own service inside the same `docker-compose.yml` as
Odysseus works fine, so I kept it to one file instead of managing two.