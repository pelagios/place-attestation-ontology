# A route: the Antonine Itinerary

The Antonine Itinerary is a Roman list of roads, compiled probably in the
third century. Each road, or *iter*, is a line of stations with the distance
from one to the next in Roman miles (*milia passuum*, written *mpm*). This
example takes Iters III and IV, which both run from London into Kent and then
part: Iter III goes on to Dover, Iter IV to Lympne. It shows how
[routes](index.md) are recorded: the route, its members in order, the roads
between them, and the distances.

The text is from G. Parthey and M. Pinder's edition of 1848, page 225, which
also gives the older reference numbers of Wesseling's edition (473.1 to
473.10) that scholars cite. Locations come from
[Pleiades](https://pleiades.stoa.org/).

{download}`Download the example as CSV files <../_generated/downloads/plato-tables-example-antonine.zip>`.
The same data is in the repository as
[PLATO JSON](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-antonine.json),
and part of it, with comments, as
[linked data](https://github.com/pelagios/place-attestation-ontology/blob/main/examples/antonine-routes.ttl).

## What the source says

```text
Item a Londinio ad portum Dubris ..... mpm LXVI sic
Durobrivis ........................... mpm XXVII
Duroverno ............................ mpm XXV
Ad portum Dubris ..................... mpm XIIII

Item a Londinio ad portum Lemanis .... mpm LXVIII sic
Durobrivis ........................... mpm XXVII
Duroverno ............................ mpm XXV
Ad portum Lemanis .................... mpm XVI
```

"From London to the port of Dubris, 66 miles: to Durobrivae 27, to
Durovernum 25, to the port of Dubris 14." The second iter is the same as far
as Canterbury.

## The sources

```{include} ../_generated/examples/antonine/sources.md
```

The Itinerary itself and the edition are two sources: the edition is
`derived_from` the Itinerary, and every row cites the edition, the thing
actually read, with the page and Wesseling line in `locator`. The edition is
out of copyright, so its licence is the Public Domain Mark. Pleiades is a
third source, for the locations.

## The places

```{include} ../_generated/examples/antonine/places.md
```

Three kinds of row share this sheet. The two iters are places in PLATO's
sense, because they are things with a history that other data can point to.
The five stations are places in the everyday sense. The four roads between
stations are *segments*. Each gets a row in the types sheet saying which it
is:

```{include} ../_generated/examples/antonine/types.md
```

The stations have no type here, because the Itinerary does not say what they
are.

## Members, in order

```{include} ../_generated/examples/antonine/relations.md
```

The first fourteen rows put each iter in order. Stations and the roads between
them share one sequence: London 1, the road 2, Rochester 3, the next road 4,
and so on to the port at 7. The two roads to Canterbury appear in both iters,
at the same positions, because both iters run along them; the relations for
each iter cite that iter's own line.

The last rows give each road its ends: `BeginsAt` and `EndsAt`, in the
direction the Itinerary runs. The roads themselves could be travelled either
way; the rows record the Itinerary's direction, and their notes say so.

## Distances

```{include} ../_generated/examples/antonine/properties.md
```

Each road's length is recorded once for each iter that states it, as its own
row with its own locator. Both iters say 27 miles from London to Rochester;
had they disagreed, the two rows would simply disagree, each with its source,
and neither would need correcting. The value is a number, and the unit is
Wikidata's *milia passuum*, so software can convert it; the `notes` keep the
numeral as printed.

Each iter's stated total is recorded too, as the edition prints it. The editors
mark both totals *sic*: the manuscripts differ, and for Iter IV most of them
read LXVI, which is not what its legs add up to. The note records that
disagreement, instead of choosing a reading.

Editions differ too. A transcription of the Itinerary on Wikisource gives the
last leg of Iter IV as XVII, not XVI; cite the edition you read, as this
example does.

## The names and locations

```{include} ../_generated/examples/antonine/names.md
```

The names are the forms the Itinerary writes, in the Latin case its lists use
(*Durobrivis*, "to Durobrivae"), marked `Attested` and explained in the notes.

```{include} ../_generated/examples/antonine/locations.md
```

```{include} ../_generated/examples/antonine/identities.md
```

The coordinates are Pleiades' representative points, sourced to Pleiades, and
each station is matched to its Pleiades record.
