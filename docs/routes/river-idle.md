# A river network: the lower Idle

The River Idle rises in Nottinghamshire and flows north past Retford,
Mattersey and Bawtry to the Trent. Before 1086 its lower course had been
diverted east to reach the Trent through a channel called Bycarr's Dyke, and
Mattersey is recorded as a head of navigation, the farthest point boats
reached, with 1322 as its last date. This
example records the Idle from Mattersey to the Trent as a
[network](index.md) with a direction: the way the water flows.

The river itself comes from REWT, Rivers of England and Wales, Temporally,
which routes the water of England and Wales over the Ordnance Survey's Open
Rivers data. REWT says nothing about the past, so the history comes from two
other datasets: Eljas Oksanen's *Inland Navigation in England and Wales
before 1348* and a table of Acts for river works from 1539 to 1720. All three
are openly licensed.

{download}`Download the example as CSV files <../_generated/downloads/plato-tables-example-river-idle.zip>`.
The same data is in the repository as
[PLATO JSON](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-river-idle.json),
and part of it, with comments, as
[linked data](https://github.com/pelagios/place-attestation-ontology/blob/main/examples/river-idle-network.ttl).

## The sources

```{include} ../_generated/examples/river-idle/sources.md
```

Each is a dataset, cited as one, with its DOI and licence. REWT's citation
carries the Ordnance Survey's attribution, which its licence requires.

## The places

```{include} ../_generated/examples/river-idle/places.md
```

There are four kinds of place here. The Idle itself is the network, and the
Ryton and the Trent are the rivers it meets. The ten reaches are the stretches
of channel between one junction and the next, and the eleven junctions (the
`node-` rows) are where they meet. Mattersey and Bawtry are the towns where
Oksanen places the heads of navigation.

```{include} ../_generated/examples/river-idle/types.md
```

## How the water flows

```{include} ../_generated/examples/river-idle/relations.md
```

Each reach is a `MemberOf` the Idle, numbered downstream, and has two more
rows: `BeginsAt` the junction it leaves and `EndsAt` the junction it reaches.
Those two rows are what give the network its direction; following them from
reach to junction to reach walks down the river.

The last two rows join rivers to rivers: the Ryton `LeadsTo` the Idle, and
the Idle `LeadsTo` the Trent. Rivers are places, so they are joined directly.
Reaches are never joined with `LeadsTo`, which would put a reach between
every pair of places and make every walk across the network take two steps
for one.

The `locator` of each row is REWT's identifier for the reach or junction,
such as `os:link/69644DBA-…`. Those identifiers are kept as locators, not
used as the places' web addresses, because the Ordnance Survey changes them
from one release of its data to the next.

## Lengths and names

```{include} ../_generated/examples/river-idle/properties.md
```

Each reach's length is REWT's, in metres. The last row is different: it
records the Act of Parliament for making the Idle navigable from Retford to
Bawtry, which takes in reaches 1 to 5 of this stretch. The table it comes from
dates it 1720 but cites it as 6 George II, which would be 1732 or 1733; the
row keeps both, as the source gives them, and says so in the note. An Act is
also only evidence that someone *intended* to make a river navigable, not that
they did, and the note says that too.

```{include} ../_generated/examples/river-idle/names.md
```

The Ordnance Survey calls the last two reaches both River Idle and Bycarrs
Dyke. Oksanen's note says the Idle was diverted "through Bycarr's Dyke" before
1086, but it does not say which stretch of today's channel that is. Matching
the old name to the reaches OS calls Bycarrs Dyke is this example's
judgement, so those two rows have a `certainty` of 0.8 and a note explaining
the match.

## The heads of navigation

The types sheet above records Mattersey and Bawtry as heads of navigation, the
farthest points boats reached, as Oksanen gives them: Mattersey last recorded
in 1322, Bawtry after 1348. The `notes` keep Oksanen's own class codes and
references, since this example does not interpret them.

## Locations

```{include} ../_generated/examples/river-idle/locations.md
```

Each reach has its line, as Well-Known Text in the `wkt` column, simplified to
within five metres, and the midpoint of that line as its latitude and
longitude. Each junction has its point. The towns have the points Oksanen
gives.
