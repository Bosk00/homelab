# media-server

Two independently-networked stacks: `arr-stack/` and `immich/`. On the live
server these run from one compose file, split here into separate folders/compose files
since they share no dependencies and are already network-isolated from
each other — arr-stack and Immich can't reach one another's containers or
databases.