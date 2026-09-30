# Your own table of places: CSV and GeoJSON

Many projects keep their places in a table of their own: a spreadsheet saved
as CSV, with a column for the name, one for latitude, one for longitude and
so on, or a GeoJSON file of features exported from a GIS. Such a table is not
yet in PLATO's shape, but most of what it holds has a place there.

[PLATO tools](https://pelagios.org/plato-tools/) reads such a table, works out
which column holds what, lets you correct that, and turns each row into
evidence in PLATO's shape, which you can then check, convert to the
[spreadsheet tables](spreadsheets/index.md) or to Linked Places Format, and
add to.

## What it reads

- **A CSV file** (or a tab-separated file ending `.tsv` or `.tab`) that is not
  one of the sheets of PLATO's own [spreadsheet tables](spreadsheets/index.md).
  Files named after those sheets (`places.csv`, `names.csv` and the rest) are
  read as the tables, as before; a single file of that name whose first column
  is not the sheet's own (a `places.csv` of your own that does not begin with
  `place_id`) is read as a table of places. Several CSV files not named after
  the sheets are not read together: choose one at a time.
- **Plain GeoJSON**: a FeatureCollection, or a single Feature, that is not
  Linked Places Format. Each feature's properties are read as the columns of a
  row, its `id` as one more column, and its geometry is carried if it is well
  formed.

A IIIF Georeference Annotation, as [Allmaps](https://allmaps.org) makes them,
is refused if it is dropped on its own, and the message says why: it places a
map image on the earth, and is a map's georeference, not a dataset of places.

**A CSV file must be well formed.** A quotation mark that opens a cell and is
never closed, or a stray one inside a quoted cell (one there is written twice,
`""`), stops the file, naming the line: after it, where rows begin and end
cannot be told. Two columns with the same heading are each known by the
heading and their place, such as `name (column 3)`, in the matching and in
the notes, and the report warns you once. Give each column a heading of its
own to be sure which is which.

Coordinates must be decimal degrees of longitude and latitude (WGS 84), as
GeoJSON requires. A GeoJSON file that names another coordinate reference
system is refused, rather than read as degrees it is not.

### Plain GeoJSON or Linked Places Format?

[Linked Places Format](https://github.com/LinkedPasts/linked-places-format)
(LPF) is itself GeoJSON, with members of its own for names, dates and
identifiers. PLATO tools reads a file as LPF, with LPF's own reader, only when
it shows LPF's structure near its start: it names LPF's `@context`, or a
feature has a `names` list whose items have a `toponym`, a `when` with
`timespans`, or an `@id` of its own, beside its `type` and `geometry`.
Anything else is plain GeoJSON, read as a table of places as this page
describes. A property that is merely called `toponym`, `timespans` or `@id`,
inside a feature's `properties`, does not make a file LPF.

## Matching the columns

PLATO tools guesses which column holds what from the column headings (case,
accents, spaces and punctuation do not count, so `Place Name`, `place_name`
and `PLACENAME` are the same) and from the values in the first 50 rows. A
column headed `lat` counts as latitude only if it holds numbers; a column
headed `wikidata` counts as the place's web address only if it holds web
addresses. Every column is matched to exactly one of these:

| Choice | What it means |
|---|---|
| Name | The place's name: its label, and a name the table attests |
| Alternative names | Other names; several in one cell separated by `;` or `\|`, or a list in GeoJSON |
| Latitude, Longitude | A point, in decimal degrees |
| Point or shape, as WKT text | A geometry in Well-Known Text |
| Point or shape, as GeoJSON | A GeoJSON geometry written out in the cell |
| Place id | The place's own identifier in the table, from which its web address is made |
| Place's web address | The place's address in a gazetteer (Wikidata, Pleiades, GeoNames, WHG…) |
| Kind of place | A type; several in one cell separated by `;` or `\|` |
| Language of the name | A language code, such as `en`, `la` or `grc` |
| Source | The source the row comes from: a title, or a web address |
| Date, as the source writes it | The date in the source's own words |
| Earliest date, Latest date | A year (such as `-0500` or `1066`) or an ISO date |
| Keep as a note | Carried in the attestation's notes, as "column: value" |
| Don't carry over | Left out, and named in the report |

A column the tools do not recognise is kept as a note. It is never turned
into one of PLATO's properties: all that is known of it is its heading, and a
property would claim the source said something PLATO defines.

**On the page**, before anything is checked or converted, PLATO tools shows a
table, *Which column holds what*: each column, three examples from the file,
what it will be read as, and why. Change any choice that is wrong. Warnings
follow your choices: for instance, that the places will have no web addresses,
or that there is a latitude column with no longitude. **Save this matching**
keeps your choices as a small JSON file, and **Use a saved matching…** applies
it again, to this file or another like it.

**On the [command line](https://github.com/pelagios/plato-tools#from-the-command-line)**,
the guess is printed with each table, one line for each column with its
reason, and then as JSON:

```text
{"id":"id","name":"name","latitude":"latitude","longitude":"longitude", …, "description":"note"}
```

Save that line to a file, correct it, and give it back with
`--columns FILE`. It is the same JSON the page saves. The fields are named in
it as `name`, `alternativeNames`, `latitude`, `longitude`, `wkt`, `geometry`,
`id`, `address`, `type`, `language`, `source`, `date`, `start` and `end`, or
`note` and `skip`. A column the file names that the table does not have, or a
column the file leaves out, is reported, and a column left out is kept as a
note.

## Places, or evidence about places

What each row becomes depends on whether a column holds places' web
addresses.

**With a column of web addresses** (matched as *Place's web address*), each
row is evidence about the place at that address: an attestation about it,
with the row's names, location, type and dates. Two rows with the same
address are two attestations about one place. A row whose address cannot be
used becomes a new place of its own if it has an id and a name, and is
otherwise reported and left out.

**Without one**, each row is a place of your own, with one attestation
holding what the row says of it.

### Place ids and the base address

A place of your own needs a permanent web address, and PLATO tools makes it
exactly as the spreadsheet tables do from `place_id`: the **base address**,
then `place/`, then the id. With the base `https://example.org/roman-britain/`,
the place with id `bath` is `https://example.org/roman-britain/place/bath`.
The id itself is kept too, as the place's own identifier. Choose a base you
control and will keep, and give it with `--base` on the command line, or in
Options on the page; without one, a stand-in base is used and the report warns
that the addresses are not permanent. See
[Say what the dataset is](spreadsheets/first-dataset.md#7-say-what-the-dataset-is)
for how to choose a base.

- **No id column**: the places have no web addresses at all, and the report
  says so once. They can be checked and converted, but not published or
  linked to until they have ids. No address is ever made from a row's number
  or its name, since it would change whenever the table did. Add a column of
  ids that will not change, or match an existing column as the id.
- **A row with no id** in the id column: that place has no web address, with
  a warning.
- **Two rows with the same id**: refused. Each id becomes a place's address,
  so reading stops at the second row, the report names the id and both rows,
  and you correct the duplicate or match another column as the id.

A column headed as an id that holds web addresses, such as Pleiades
addresses, is guessed to be the places' web addresses instead.

### World Historical Gazetteer addresses

Addresses of the [World Historical Gazetteer](https://whgazetteer.org) are
treated as in a [TEI edition](tei.md#world-historical-gazetteer-addresses): a
reconciliation id (`place:gn:2988507`) or an entity page is written as
`https://w3id.org/whg/id/place:…`, with a note giving what the table said,
and a `/places/<number>/portal/` address holding a database record, or an
address on WHG's staging copy, is refused and reported.

## What each column becomes

| Matched as | In PLATO |
|---|---|
| Name | The place's label, and a **name** of the attestation |
| Alternative names | Further **names** of the attestation |
| Latitude and longitude | A **location**, made exactly as the locations sheet makes one |
| WKT, GeoJSON geometry, or a GeoJSON feature's own geometry | A **location** with that shape |
| Place id | The place's **address**, under the base address, and its own identifier |
| Place's web address | What the attestation is **about** |
| Kind of place | A **type** (with its address, when the value is a web address) |
| Language of the name | The name's **language** |
| Source | The citation's **source**; with no source, the file is cited, with the row ("row 2", "feature 3") as the locator |
| Date; earliest and latest dates | The **timespan**: the date in the source's words, the earliest start, the latest end |
| Anything else | The attestation's **notes** |

The full mapping, for developers, is beside PLATO tools'
[CSV and GeoJSON test files](https://github.com/pelagios/plato-tools/blob/main/test/fixtures/generic/README.md#the-mapping).

## What is left out, and why

Each of these is named in the report, with the row or feature where it
happened.

- **A column you chose not to carry over**, once, by name.
- **A location that cannot be read**: a latitude with no longitude (or the
  reverse), a coordinate that is not a number in decimal degrees (degrees,
  minutes and seconds must be converted first), or one off the earth's range,
  often a sign that the two are the wrong way round. The rest of the row is
  carried.
- **A geometry that is not well formed**, in a GeoJSON feature or written out
  in a cell: a position that is not two or three numbers, or is off the
  earth's range; a line of fewer than two positions; a ring of a polygon of
  fewer than four, or one that does not end where it begins; or anything that
  is not a GeoJSON Point, LineString, Polygon or one of their Multi forms. The
  report says what is wrong, that geometry is left out, and the rest of the
  row is carried.
- **A GeometryCollection**, which PLATO does not accept. Give each of its
  geometries as a feature of its own.
- **An earliest or latest date that is not a year or an ISO date**, such as
  "c. 75". Match the column as *Date, as the source writes it* instead to keep
  it in the source's words. A year of fewer than four digits is padded, so
  `71` becomes `0071`.
- **A language that is not a language code**, such as "Latin (classical)":
  the name is carried without a language.
- **A row with no name (and no alternative name) and no web address**, which
  has nothing to be a place or to be about. With a column of web addresses, a row with a name but no
  usable address, and no id, is left out too.
- **Cells beyond the last column** of a CSV row, and members of a GeoJSON
  feature besides its `type`, `id`, `geometry` and `properties`, such as a
  `bbox`.

## Two examples

These are small files made up for PLATO tools' tests.

**A table of places with ids.** This CSV file has an id column and no web
addresses:

```text
id,name,latitude,longitude,type,start,end,language,description
bath,Aquae Sulis,51.3811,-2.3590,spa,0060,0410,la,Roman baths
york,Eboracum,53.9590,-1.0815,fortress,71,,la,
```

Every heading is recognised except `description`, which is kept as a note.
With the base address `https://example.org/roman-britain/`, the first row
becomes the place `https://example.org/roman-britain/place/bath`, labelled
"Aquae Sulis", with one attestation: the name *Aquae Sulis* in Latin, a point
at 51.3811, -2.3590, the type "spa", a timespan from 0060 to 0410, the file
cited with "row 2" as the locator, and the note "description: Roman baths".
York's start, `71`, is written `0071`.

**Rows about gazetteer places.** This CSV file has odd headings and a column of
Wikidata addresses:

```text
Place Name,LAT,Long,wikidata,Feature Type,Alt. names,Source,Remarks
Roma,41.8933,12.4829,https://www.wikidata.org/wiki/Q220,city,Rome; Urbs,Itinerarium Antonini,the capital
Lutetia,48.8566,2.3522,https://www.wikidata.org/wiki/Q90,settlement,Paris,,
Lutetia Parisiorum,48.85,2.35,https://www.wikidata.org/wiki/Q90,,,,a second row about the same place
```

`Place Name`, `LAT`, `Long`, `Feature Type` and `Alt. names` are recognised
despite their case and punctuation; `wikidata` holds web addresses, so each
row is an attestation about the place at its address. Roma's attestation has
the names *Roma*, *Rome* and *Urbs*, a point, the type "city", the
*Itinerarium Antonini* as its source, and the note "Remarks: the capital". The
two Lutetia rows are two attestations about one place, Q90. Because the rows
give names but not labels for Wikidata's places, the report warns that each
place's address is used as its label.
