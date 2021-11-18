-- Sirius faction standing script
require "factions.standing.lib.base"

_fcap_kill     = 10 -- Kill cap
_fdelta_distress = {-0.5, 0} -- Maximum change constraints
_fdelta_kill     = {-5, 1} -- Maximum change constraints
_fcap_misn     = 30 -- Starting mission cap, gets overwritten
_fcap_misn_var = "_fcap_sirius"
_fthis         = faction.get("Sirius")
