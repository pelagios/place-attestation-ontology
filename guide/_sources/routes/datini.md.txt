# A network of correspondence: the Datini letters

Francesco di Marco Datini, a merchant of Prato who died in 1410, ran a firm
with offices across the western Mediterranean, and kept its letters. The
*Datini Correspondence Metadata* describes 145,417 of them, one record each:
which city a letter was sent from and to, the day it was sent and the day it
arrived. Counted city by city, they make a [network](index.md): places joined
by the post that ran between them.

Unlike the River Idle, where a reach of river is a thing in the landscape,
the connection between Florence and Barcelona is a relationship, not a road.
There is nothing between the two cities to record as a place of its own, so
the connection is recorded directly, and what the source says about it goes
with it.

{download}`Download the example as CSV files <../_generated/downloads/plato-tables-example-datini.zip>`.
The same data is in the repository as
[PLATO JSON](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-datini.json),
and part of it, with comments, as
[linked data](https://github.com/pelagios/place-attestation-ontology/blob/main/examples/datini-network.ttl).

## The sources

```{include} ../_generated/examples/datini/sources.md
```

The dataset is the first source. The second is this example's own work: the
counts of letters and the delivery times, worked out from the dataset's
records on a stated day. It is a source of its own, `derived_from` the
dataset, because the figures are findings someone made from the records, not
statements the records make. Anyone who wants to check them can see what they
came from and how.

## The network and its cities

```{include} ../_generated/examples/datini/places.md
```

```{include} ../_generated/examples/datini/types.md
```

```{include} ../_generated/examples/datini/relations.md
```

Each city is a `MemberOf` the network, with no `sequence`: nothing in the
letters puts the cities in an order.

## The connections

```{include} ../_generated/examples/datini/connections.md
```

This is the **connections** sheet. Each row joins two cities with `LeadsTo`,
from the city in `place_id` to the one in `related_place_id`, and gives one
figure about that connection: the number of letters, or the median number of
days they took to arrive. Two figures about one connection are two rows.

Letters went both ways between Florence and Pisa, but not equally: 16,261
from Florence to Pisa, 6,414 back. Each direction is its own connection, with
its own figures, which is why these rows use `LeadsTo` twice and not
`ConnectedTo` once.

The delivery time is a median: half the letters took less time, half more.
The records contain impossible delays, letters apparently received before
they were sent or years later, which probably come from how their dates
were written. They move an average a long way but a median hardly at all. So the median is
given, over the letters with both dates and a delay of up to a year, and the
note on each row says exactly which letters that is. `date`, `from` and `to`
give the years of sending that the figures cover, as the dataset dates them.

## Names, locations and identities

```{include} ../_generated/examples/datini/names.md
```

The archive files each city under an Italian name, in capitals (*FIRENZE*,
*BARCELLONA*); these are recorded as the dataset's headwords.

```{include} ../_generated/examples/datini/locations.md
```

```{include} ../_generated/examples/datini/identities.md
```

The coordinates are the dataset's own, and each city is matched to its
Wikidata item.
