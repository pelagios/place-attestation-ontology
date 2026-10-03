# Your own table of places: CSV, GeoJSON or a workbook

Many projects keep their places in a table of their own: a spreadsheet, as an
Excel or OpenDocument workbook or saved as CSV, with a column for the name, one
for latitude, one for longitude and so on, or a GeoJSON file of features
exported from a GIS. Such a table is not yet in PLATO's shape, but most of
what it holds has a place there.

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
- **A workbook** (`.xlsx` or `.ods`) that is not PLATO's own spreadsheet
  tables, one sheet at a time: see [A workbook of your own](#a-workbook-of-your-own).
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

### A workbook of your own

A workbook is read as PLATO's [spreadsheet tables](spreadsheets/index.md), as
before, when its sheets are named after the tables' sheets: two or more of
them, or a single one that begins as that sheet does (a `places` sheet whose
first column is `place_id`). Any other `.xlsx` or `.ods` workbook is a table of
places, and its columns are matched as a CSV file's are.

**One sheet is read.** It is the first sheet that is not hidden, unless you
choose another. **On the page**, choose it in *Sheet to read*, above the table
of columns: its columns are then read and guessed afresh. **On the command
line**, give `--sheet NAME` to `check`, `convert` or `preview`; a name the
workbook does not have is refused, and the message names the sheets it has.
The report names the sheets not read. To read several, read each in turn, or
put their rows on one sheet.

**The report also names**

- a **hidden sheet**, whether or not it is the one read. Only an Excel
  workbook's hidden sheets are known: an OpenDocument (`.ods`) workbook's are
  not marked as hidden when it is read, so a hidden first sheet is the one
  read. Check the report's *read "…"* line;
- a **formula saved without its value**, as a program that does not calculate
  may save it. The cell is read as empty. Open the workbook in a spreadsheet
  program, let it calculate, and save it again;
- a **cell holding an error**, such as `#DIV/0!`, `#N/A` or `#REF!`. It carries
  nothing: it is read as empty, never as the error's text;
- an **empty sheet**, which is an error: choose the sheet that holds the table.

**Each cell is read as it is stored, not as the workbook shows it**, exactly
as the spreadsheet tables reader reads a workbook:

| In the workbook | Read as |
|---|---|
| A coordinate formatted to show `51.38` | every digit it has: `51.381088` |
| A very small or very large number | written out in full, never with an exponent: `0.0000001`, not `1e-7` |
| A percentage shown as `95%` | the number, `0.95` |
| A date | an ISO date, `1990-05-06` |
| A date with a time of day | `1991-07-02T10:30:00`, with no time zone, as the workbook gives none |
| A time of day alone | `12:00:00` |
| Text, such as `007` | the text as it is: `007` |

A workbook is read whole into memory, and one over 50 MB is warned of: save a
very large sheet as CSV (UTF-8), which is read a row at a time.

For example, a workbook `sites.xlsx` made for this guide has three sheets: a
hidden one, *Old list*; *Sites*; and *Notes*. *Sites* is

| id | name | latitude | longitude | surveyed | finds |
|---|---|---|---|---|---|
| bath | Aquae Sulis | 51.38 | -2.36 | 1990-05-06 | 120 |
| york | Eboracum | 53.96 | -1.08 | 1991-07-02 10:30 | `=F2*2`, saved without its value |
| wroxeter | Viroconium | 52.6744 | `#N/A` | 1992-04-01 | `#DIV/0!` |

with the coordinates of the first two rows formatted to show two decimal
places. Checked with the base `https://example.org/survey/`, *Sites* is read,
as the first sheet not hidden, and gives three places. Aquae Sulis has its
point at every digit stored, `51.381088, -2.359019`, and the notes "surveyed:
1990-05-06" and "finds: 120"; Eboracum's note is "surveyed:
1991-07-02T10:30:00". The report says:

```text
sites.xlsx: read "Sites"; not read "Old list", "Notes"
"Old list" in sites.xlsx, not read
row 4, column "longitude", cell D4: #N/A
row 4, column "finds", cell F4: #DIV/0!
cell F3 of "Sites", column "finds": =F2*2
row 4: latitude 52.6744 with no longitude
```

Saved as `sites.ods`, the same workbook reads *Old list* first, as its hidden
flag is not known, and `--sheet Sites` reads *Sites*.

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
`note` and `skip`. A column of a gazetteer's ids, made into web addresses
with a pattern, is written
`{"field": "address", "pattern": "https://pleiades.stoa.org/places/{id}"}` in
place of the field's name (see [A column of gazetteer ids](#a-column-of-gazetteer-ids)).
A column the file names that the table does not have, or a column the file
leaves out, is reported, and a column left out is kept as a note.

## Previewing the first records

Before you check or convert a whole file, you can see what its first records
become. **On the page**, choose **Preview the first 10 records**, once the
columns are matched (for a TEI edition, once the file is chosen). **On the
command line**, give

```text
plato-tools preview --limit 3 my-places.csv
```

with `--limit N` for how many records (10 if you leave it out), and the same
`--columns`, `--sheet`, `--base` and reading options a conversion would take.
The records are shown in PLATO JSON, as a conversion reads them, with what was
lost from them so far, grouped as the report groups it. On the command line,
the records go to the standard output, one a line, and the rest to the
standard error; `--json` prints it all as one JSON object.

A preview is made of a table of places (a CSV file, plain GeoJSON or a sheet of
a workbook), a [TEI edition](tei.md), or [annotations from
Recogito](annotations.md). Any other format is refused, since the first part of
a set of spreadsheet tables or of a PLATO JSON file could be taken for the
whole.

- **It writes nothing**, and checks nothing as a whole: a problem further on,
  such as an id used again after the records shown, is not found. If the file
  cannot be read past a problem among the first records, the preview stops
  there, and says why.
- **It stops early.** Reading stops at the first record past the limit, so a
  preview of a large file is quick.
- **It says how many records there are only when it has read them all.** The
  line above the records says *first 3 of 3 records* only when the whole file
  was read; otherwise *the first 3 records read; the rest not read*, as a file
  is never read to its end to count it.

It also says why the records shown may not be all there are, or not in the
order a conversion writes them: the rest of the file was not read; a
conversion gathers attestations by the place each is about once the whole
file is read; places made from rows that share an id are made only at the end
(so none is shown); and in a TEI edition, a place name that points to a
`<place>` later in the file, or that may be in the editors' words, waits, and
is not shown.

For example, `plato-tools preview --limit 2 --base https://example.org/survey/ sites.xlsx`,
with the workbook [above](#a-workbook-of-your-own), prints Aquae Sulis and
Eboracum as two places, and says

```text
sites.xlsx: a table of places (the sheet “Sites” of a workbook), its columns matched to PLATO (place-centric): the first 2 records read; the rest not read; nothing checked or written
  Reading stopped after the first 2 records: the rest of the file was not read, so nothing after them, and no problem in it, is shown.
```

with, as losses so far, the sheets not read, the hidden sheet and the formula
saved without its value, but not the error cells of row 4, which was not
read. Without `--limit`, it reads all three rows, and the line says *first 3 of
3 records*.

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
- **Two rows with the same id**: refused, unless you choose to read them as
  one place (see [Rows that share an id](#rows-that-share-an-id)). Each id
  becomes a place's address, so reading stops at the second row, the report
  names the id and both rows, and you correct the duplicate, match another
  column as the id, or choose that reading option.

A column headed as an id that holds web addresses, such as Pleiades
addresses, is guessed to be the places' web addresses instead.

### Rows that share an id

Some tables have a row for each piece of evidence, not for each place: three
rows from three sources, all with the id of one place. Read as they stand,
the repeated id is refused, as above. If every row with the same id really is
evidence about the same place, choose the **reading option** *Rows with the
same id are one place* (on the page, under **Reading options**, below the
table of columns), or give `--same-id` on the command line. Then:

- each id is one place, with its address made from the id under the base
  address, as before;
- each row is one attestation about that place, with its own names, location,
  dates and notes, citing its row;
- the place's label is the name its rows agree on. Where their names differ,
  none is picked: the label is the id, every name stays in its own row's
  attestation, and the report lists the names, so that you can check the rows
  are one place;
- a row with no id names no place, so it is reported and left out.

The option needs a column read as the place id; without one it is refused,
on the page and on the command line, with the reason. It is for tables of
places only: `--same-id` with no CSV or GeoJSON among the inputs is refused.

For example, PLATO tools' test file `duplicate-ids.csv` is

```text
id,name,lat,lon
a,Alpha,50.1,-1.1
b,Beta,50.2,-1.2
a,Alpha again,50.3,-1.3
```

Read as it stands, it is refused at row 4: "The id "a" is used by more than
one row (row 2 and row 4)…", ending with the advice to read rows with the same
id as one place (Reading options, or `--same-id`). With `--same-id` and the
base `https://example.org/demo/`, it gives two places.
`https://example.org/demo/place/a` has two attestations, *Alpha* (row 2) and
*Alpha again* (row 4), each with its own point; as the names differ, its label
is `a`, and the report warns: `"a": Alpha / Alpha again`.
`https://example.org/demo/place/b`, *Beta*, has one.

### A column of gazetteer ids

A table may hold a gazetteer's ids, not its web addresses: a column
`pleiades_id` of numbers such as `579885`. An id is not an address, and the
same number can mean different places in different gazetteers, so such a
column is kept as a note until you say which gazetteer it is. PLATO tools
**suggests** a pattern when the column's heading names Pleiades, GeoNames or
Wikidata and at least half its values have the shape of that gazetteer's ids:

| Gazetteer | Its ids | The pattern suggested |
|---|---|---|
| Pleiades | digits | `https://pleiades.stoa.org/places/{id}` |
| GeoNames | digits | `https://sws.geonames.org/{id}/` |
| Wikidata | `Q` and digits | `http://www.wikidata.org/entity/{id}` |

A suggestion is never used until you **confirm** it. On the page, tick *Make
web addresses* in the column's row of the table of columns. On the command
line, the guess and a note print the pattern; give it back in the file for
`--columns`, as
`"pleiades_id": {"field": "address", "pattern": "https://pleiades.stoa.org/places/{id}"}`.
Once confirmed, the column is read as the places' web addresses: each id
replaces `{id}`, each row becomes an attestation about the place at that
address, and its notes say how the address was made.

You may also write a pattern of your own for another gazetteer. It must hold
`{id}` once, after the address's host, and make a web address (`http` or
`https`); its ids may hold only letters, digits and `. _ ~ -`. A pattern for
the World Historical Gazetteer is refused, as WHG's short codes do not name
one record, and `whg:` followed by a number is never made into an address.

A value of the wrong shape (not digits, for Pleiades) makes no address, and is
reported; the row is then read without it, so with an id it becomes a place of
its own, keeping the value in its notes. A value that is already a full web
address is read as one.

For example, PLATO tools' test file
[`gazetteer-ids.csv`](https://github.com/pelagios/plato-tools/blob/main/test/fixtures/generic/gazetteer-ids.csv)
is

```text
id,name,pleiades_id
1,Athenae,579885
2,Roma,423025
3,Ostia,422995
4,Somewhere,whg:12345
5,Bad id,57-9885
6,No address,
```

Checked as it is, the column `pleiades_id` is kept as a note, with the
suggestion: "3 of its 5 sampled values have the form of Pleiades ids, so it
can be read as the place's web address, made with the pattern
https://pleiades.stoa.org/places/{id}, once you confirm that pattern". With
the pattern confirmed, Athenae is an attestation about
`https://pleiades.stoa.org/places/579885`, with the note "Place address made
from the value 579885 in the column "pleiades_id" with the pattern
https://pleiades.stoa.org/places/{id}", and so are Roma and Ostia. `whg:12345`
and `57-9885` are reported as not the shape of a Pleiades id, and rows 4, 5
and 6, which have ids of their own, become places of their own under the base
address.

### World Historical Gazetteer addresses

Addresses of the [World Historical Gazetteer](https://whgazetteer.org) are
treated as in a [TEI edition](tei.md#world-historical-gazetteer-addresses): a
reconciliation id (`place:gn:2988507`) or an entity page is written as
`https://w3id.org/whg/id/place:…`, with a note giving what the table said,
and a `/places/<number>/portal/` address holding a database record, or an
address on WHG's staging copy, is refused and reported.

### Pleiades, GeoNames and Wikidata addresses

So that one place does not become two addresses, an address of Pleiades,
GeoNames or Wikidata is written in the one form that gazetteer gives it, as
in a [TEI edition](tei.md#gazetteer-addresses-in-one-form):
`http://pleiades.stoa.org/places/579885` becomes
`https://pleiades.stoa.org/places/579885`, a Wikidata page
`https://www.wikidata.org/wiki/Q90` becomes
`http://www.wikidata.org/entity/Q90`, and so on. The attestation's notes give
what the table said, the rule, and the version of the rules, such as "Place
address given as https://www.wikidata.org/wiki/Q90 (rule wikidata-page,
hermes-addresses 1)". An address made from an id through a pattern follows
the same rules. A Pleiades address that names part of a place's record, or
ends `#this`, is carried as written and reported.

## What each column becomes

| Matched as | In PLATO |
|---|---|
| Name | The place's label, and a **name** of the attestation |
| Alternative names | Further **names** of the attestation |
| Latitude and longitude | A **location**, made exactly as the locations sheet makes one |
| WKT, GeoJSON geometry, or a GeoJSON feature's own geometry | A **location** with that shape |
| Place id | The place's **address**, under the base address, and its own identifier |
| Place's web address | What the attestation is **about**, in its gazetteer's one form |
| A gazetteer's ids, with a pattern you confirmed | What the attestation is **about**, made from the id |
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
- **A workbook's error cells, and formulas saved without their values**,
  which are read as empty: see [A workbook of your own](#a-workbook-of-your-own).
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
row is an attestation about the place at its address, written in Wikidata's
own form, `http://www.wikidata.org/entity/Q220`. Roma's attestation has the
names *Roma*, *Rome* and *Urbs*, a point, the type "city", the
*Itinerarium Antonini* as its source, and the notes "Remarks: the capital"
and "Place address given as https://www.wikidata.org/wiki/Q220 (rule
wikidata-page, hermes-addresses 1)". The two Lutetia rows are two attestations
about one place, `http://www.wikidata.org/entity/Q90`. Because the rows give
names but not labels for Wikidata's places, the report warns that each place's
address is used as its label.
