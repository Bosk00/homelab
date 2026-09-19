# Home Assistant

Home automation — lights, notifications, sensor monitoring, and a couple of
physical automations around the server itself.

**Setup:**
- CPU usage/temp sensors integrated into the HA UI, tracking the laptop
  acting as the server
- Replaced Uptime Kuma for that same monitoring (see
  `utilities/uptime-kuma/`) — comparing the CPU usage CSV before/after
  running Uptime Kuma showed a clear bump while it was active, so I cut it
- Custom webhook notifications straight to my phone
- Smart light switches integrated into HA, with time-based automations
  (on/off on a schedule)
- Integrated my existing smart plugs into HA, then blocked them from
  phoning home to their manufacturer's cloud (see below)
- Smart plug wired to a laptop cooling pad for the server laptop: temp above 55°C
  for 30 seconds turns the fan on automatically; back under 40°C for 2
  minutes turns it off

**Smart plug cloud blocking:** the plugs are cloud-dependent by default, so
I added their vendor's cloud domains to Pi-hole's blocklist (see
`utilities/pihole/`) to stop them reaching out over WAN — automation runs
entirely local through HA either way, so there's no functional loss.
DNS-level blocking isn't a real boundary though: the plugs can still resolve
the domain if they ever hardcode an IP or use DoH, and my current router 
can't do WAN-block/LAN-allow at the firewall level. A custom router/firewall 
to actually segment this properly is next on the list.

**Why:** wanted to self-host as many IoT devices as possible. The webhooks to my
phone for anything that needs attention, and the automations (lights,
fan control) mean I'm not manually babysitting either.

*Automation logic (lighting schedules, routines, etc.) lives in HA's own
config and isn't included here — this repo only covers the container
setup.*