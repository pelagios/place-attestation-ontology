# Your first contribution

This walkthrough builds a small contribution from one source: a London customs
account of 1480 to 1485 that mentions Bristol and Deptford Strand. It uses
five of the eight sheets. The finished tables are the *customs* example,
which you can {download}`download as CSV files <../_generated/downloads/plato-tables-example-customs.zip>`
and open beside this page.

Start from the {download}`template workbook <../_generated/downloads/plato-tables-template.xlsx>`.
Only the columns you fill in are shown below; leave the others empty.

## 1. List your places

One row per place, with an identifier you make up and a label to list it
under. The label is only for display: the names the place has in your sources
go in the names sheet.

```{include} ../_generated/examples/customs/places.md
```

## 2. List your sources

One row per source. The `date` is when the source itself was made, as the
catalogue gives it; `from` and `to` are the years it spans.

```{include} ../_generated/examples/customs/sources.md
```

The second source, GeoNames, is there because the coordinates in step 4 come
from it, not from the customs account. Every row says which source it comes
from, so a location taken from a modern database is never mistaken for one
found in a fifteenth-century document.

## 3. Record the names

One row for each name a source gives, spelt exactly as the source spells it.
`place_id` and `source_id` point at the rows you made in steps 1 and 2.

```{include} ../_generated/examples/customs/names.md
```

The first row says: *the customs account, for 1480 to 1485, calls Bristol
"Bristowe"*. The second says how sure the contributor is of a damaged reading
(`certainty` 0.7) and why (`notes`). *Deptford Strand* names both a place and
a street, hence two name types.

## 4. Record locations

Latitude and longitude in decimal degrees, as most web maps give them. The
`geometry_role` says what the point marks: here a point standing in for the
whole town, rather than its outline or one particular building.

```{include} ../_generated/examples/customs/locations.md
```

GeoNames does not date its coordinates, so the date is `undated`.

## 5. Record what kind of place it is

The account treats Bristol as a port. The type can be written in your own
words, with the matching concept from a published vocabulary (here the Getty
Art & Architecture Thesaurus) if you know it.

```{include} ../_generated/examples/customs/types.md
```

## 6. Say which records elsewhere are the same place

If you know that one of your places is already in GeoNames, Wikidata or the
World Historical Gazetteer, say so in identities. This is what lets your
evidence join everyone else's.

```{include} ../_generated/examples/customs/identities.md
```

## What happens to your rows

Each row of names, locations and types becomes one **attestation**: a
statement that this source, for this date, gives this name, location or type
for this place. Your four evidence rows become four attestations about two
places, each keeping its source, its date and your certainty. Nothing you
entered is merged or overwritten, and a user of the combined data can always
see who said what, and when.

For a richer example, with manuscripts copied later, "ibid." references and
editorial headwords, see the [place-name survey example](survey-example.md).
Every column is described in the [sheet reference](reference.md).
