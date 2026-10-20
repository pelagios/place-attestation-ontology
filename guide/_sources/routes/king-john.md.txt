# A journey: King John in 1215

Medieval kings moved constantly, and the letters they sent out were
witnessed with the place and the day: "Witness ourself between Newbury and
Abingdon, on the 15th of July in the 17th year of our reign". In 1835 T. D. Hardy used those witness clauses, enrolled
on the Chancery rolls, to trace King John from day to day through his whole
reign. This example takes the weeks around the sealing of Magna Carta, from
1 June to 17 July 1215, as Hardy tells them in the remarks that open his
tables (pages 108 to 110). It shows how a [journey](index.md) is recorded:
each stop in order, with the dates the source gives.

{download}`Download the example as CSV files <../_generated/downloads/plato-tables-example-king-john.zip>`.
The same data is in the repository as
[PLATO JSON](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-king-john.json),
and part of it, with comments, as
[linked data](https://github.com/pelagios/place-attestation-ontology/blob/main/examples/king-john-itinerary.ttl).

## What the source says

> Previously to the sealing of Magna Carta, namely, from the 1st to the 3d of
> June 1215, the King was at Windsor, from which place he can be traced, by
> his attestations, to Odiham, and thence to Winchester, where he remained
> until the 8th. From Winchester he went to Merton; he was again at Odiham
> on the 9th, whence he returned to Windsor, and continued there until the
> 15th: on that day he met the barons at Runnemead by appointment, and there
> sealed the great charter of English liberty. The King then returned to
> Windsor, and remained there until the 18th of June, from which time until
> the 23d he was every day both at Windsor and at Runnemead …

The account goes on through Odiham and Winchester to Marlborough, round
Wiltshire and into Dorset, and back by Newbury and Abingdon to Oxford on
17 July. The dates are in the Julian calendar, as the rolls give them.

## The sources

```{include} ../_generated/examples/king-john/sources.md
```

Hardy's book is the source every row cites, with its page. It is
`derived_from` the enrolled letters he read, which are a source of their own,
dated 1215. Wikidata is the source of the locations.

## The journey and its stops

```{include} ../_generated/examples/king-john/places.md
```

```{include} ../_generated/examples/king-john/types.md
```

The journey is a row in the places sheet, typed `itinerary`. Every place the
King stopped at has a row too, once, however often he came back.

```{include} ../_generated/examples/king-john/relations.md
```

Each row makes one stop a member of the journey. Read down the `sequence`
column and the journey unfolds:

- **The date as Hardy writes it** goes in `date`: "until the 8th", "the first
  four days of July", "the following day". The actual days go in `from` and
  `to`. Where Hardy gives no date for a stop he passed through (Odiham on the
  way to Winchester, for instance), `date` says `undated`, and `from` and `to`
  are the dates of the stops either side, which is as close as the source
  allows; the notes say so.
- **Windsor appears four times**, at positions 1, 6, 8 and 9, each with its
  own stay. A place visited twice is two members, not one.
- **Runnymede appears twice.** On 15 June it is stop 7. From the 18th to the
  23rd the King was "every day both at Windsor and at Runnemead", so that row
  has no `sequence`: the source puts neither before the other, and the dates
  say when.
- **Marlborough** gives a length as well as dates: "the first four days of
  July" is `from` 1 July, `to` 4 July, and `duration` `P4D` (four days).
  Where a source gives only a length ("he stayed six weeks"), `duration` can
  stand alone.
- **Oxford**, the last stop, has only a `from`: Hardy gives the day the King
  arrived, not the day he left.
- **Merton** is a member with no location. Hardy does not say which Merton he
  means, so the example does not guess; a stop can be recorded without a
  place on the map.

A platform can work out the journey's overall dates from its stops. It does
not need a row saying "1 June to 17 July" as evidence; the types row gives
that span only because Hardy's pages cover it.

## A stop that did not happen

The last row is a denial. Earlier historians said the King went to the Isle
of Wight straight after Magna Carta; Hardy says "it is unquestionable that
the King did not then visit the Isle of Wight". That is recorded as a member
row with `denied` set to `yes`. It is evidence too: anyone reading the older
histories can see that this claim was examined and rejected, and by whom.
Formats that cannot say "not", such as Linked Places Format, leave a denial
out rather than put the King where the source says he never was.

## Names and locations

```{include} ../_generated/examples/king-john/names.md
```

Where Hardy spells a place differently from today, his spelling is kept as a
name: *Runnemead*, *Corfe-Castle*.

```{include} ../_generated/examples/king-john/locations.md
```

```{include} ../_generated/examples/king-john/identities.md
```

The coordinates are Wikidata's, and each place is matched to its Wikidata
item. Two matches are `closeMatch`: Hardy's "Clarendon" is matched to the
royal palace there, and his "Corfe-Castle" to the castle rather than the
village, and the `basis` column says why.
