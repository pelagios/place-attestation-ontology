# Organising data in spreadsheets

You can put your data into PLATO's shape with an ordinary spreadsheet in
Excel, LibreOffice or Google Sheets, using **temPlato**, PLATO's spreadsheet
template. It has ten sheets, one for
each kind of information, and filling them in is also a way of working out
what your data is: which places it is about, which sources it rests on, and
what each source actually says. Most datasets use only three or four of the
sheets.

## Get temPlato

- {download}`temPlato workbook (.xlsx) <../_generated/downloads/plato-tables-template.xlsx>`:
  the easiest way to start. Hover over any column heading to see what to put
  in it; columns with a fixed list of values offer a drop-down.
- {download}`temPlato as CSV files (.zip) <../_generated/downloads/plato-tables-template.zip>`:
  the same ten sheets as separate CSV files, with the table definitions.

## The ten sheets

| Sheet | One row for each… | Needed? |
|---|---|---|
| [about](reference.md#about) | the dataset as a whole: its title, authors, licence and addresses (one row) | always |
| [places](reference.md#places) | place your data is about | always |
| [sources](reference.md#sources) | source you cite | always |
| [names](reference.md#names) | time a source gives a name for a place | usually |
| [locations](reference.md#locations) | time a source gives a location | if you have coordinates |
| [types](reference.md#types) | time a source says what kind of place it is | if you have types |
| [relations](reference.md#relations) | time a source relates a place to something: a parish in a hundred, a station on a road, a stop on a journey, a person born there | if you have them |
| [connections](reference.md#connections) | figure a source gives about a connection between two places, such as letters sent from one city to another | rarely |
| [properties](reference.md#properties) | other fact a source states, such as a population | rarely |
| [identities](reference.md#identities) | record elsewhere that is the same place as one of yours | if you know them |

The places sheet becomes PLATO's SpatialEntities; each row of names,
locations, types, relations, connections and properties becomes one attestation. The
[ideas in five minutes](../ideas.md) explains what that means.

## Rules that apply everywhere

1. **Keep all ten sheets**, even if you leave some empty apart from their
   headings. Do not rename, reorder or delete columns; leave a cell empty if
   you have nothing to put in it.
2. **Identifiers are yours to choose.** `place_id` and `source_id` can be any
   short text, such as `bristol` or `s12`, as long as each is used only once
   in its sheet. The other sheets use them to refer to a place or a source.
3. **Every row of evidence needs a place, a source and a date.** In names,
   locations, types, relations, connections and properties, fill in `place_id`,
   `source_id` and `date` on every row.
4. **Write the date as your source gives it**, or `undated`. Then, if you can,
   put the earliest and latest years in `from` and `to`, with **at least four
   digits**: `0921`, not `921`. Years BCE take a minus sign, and deep time
   as many digits as it needs (`-12000`). For a single year, put it in both. Leave `to` empty if
   the end is unknown.
5. **Some columns take a fixed word**, such as `Headword` or `ContainedIn`.
   Use it exactly as written, with the same capital letters. The workbook
   offers these as a drop-down; the [vocabularies](../vocabularies.md) page
   lists them all.
6. **One fact per row.** If a source gives two spellings, that is two rows in
   names. If two sources give the same spelling, that is also two rows.
7. **A source that denies something is recorded too.** If a source says a
   place had no market, add a row in types with `market` and `denied` set to
   `yes`. The row is then a denial, so give only the one thing denied. If the
   source only reports something ("it is said"), hedges it, or leaves it
   undecided, set `stance` to `Reported`, `Tentative` or `Doubted`: that is the
   source's stance, not a denial, and not your own certainty.
8. **A relations row names exactly one thing.** Fill in either
   `related_place_id`, for a place in your places sheet, or `related_uri`, for
   something described elsewhere such as a person, with a name for it in
   `related_label`: never both, and never neither. PLATO tools reports a row
   that breaks this rule. [Routes, journeys and networks](../routes/index.md)
   explains the relations for them.

:::{note}
Spreadsheet programs sometimes "correct" what you type: `0921` becomes `921`,
and `1-2` becomes a date. The temPlato workbook formats its columns as text to
prevent this. If you build your own sheets, format the columns as text before
typing, and save CSV files as **CSV UTF-8**.
:::

## What the spreadsheets cannot say

The spreadsheets cover most datasets, but a few things need the
[JSON format](../json.md) instead:

- one piece of evidence that rests on two sources at once, such as the
  place-name surveys' "1252 Cl *et passim* to 1346 Harl";
- one piece of evidence giving several facts together, such as a name and a
  location in a single statement;
- one scholar's comment on another's evidence ("this contradicts that");
- readings that are alternatives to each other, such as a "Neuton" that could
  be either of two Newtons, of which at most one is right;
- a relation type that PLATO does not list, such as your project's own "flows
  into" for a river. In JSON it can say which of PLATO's types it narrows; or
  ask for it to be added to PLATO by
  [opening an issue](https://github.com/pelagios/place-attestation-ontology/issues).

## Checking your tables

The temPlato workbook catches most mistakes as you type. For a full check,
open **[PLATO tools](https://pelagios.org/plato-tools/)**, drop your ten CSV files (or the
workbook, or a zip of the files) onto the page, and press **Check**. It runs
in your browser, so nothing is uploaded, and it lists every problem with its
sheet, row and column, in plain words. It also says what PLATO JSON could
not hold, should you convert the tables later.

If you prefer the command line, or have many sets of tables to check, PLATO
tools runs there too, with the same checks and the same report. You need
[Node.js](https://nodejs.org) 24 or later; then, in a terminal:

```bash
# a folder holding your ten CSV files is one set of tables;
# a zip of them, or the workbook, works the same way
npx github:pelagios/plato-tools check my-tables/
```

Name as many folders or files as you like: each gets its own report, and a
total comes at the end. The [instructions](https://github.com/pelagios/plato-tools#from-the-command-line) list the other options,
including conversion.

The tables are also described in the W3C standard *CSV on the Web* (CSVW), so
any CSVW validator can check them against the
[table definitions](https://w3id.org/plato/schemas/tables/csv-metadata.json).
For example, with Python installed:

```bash
pip install csvw
# put csv-metadata.json in the same folder as your ten CSV files, then:
csvwvalidate csv-metadata.json
```

It reports, with the row and column, any identifier that does not exist, any
missing required value and any value that is not allowed.

## Using your tables

Once your tables are complete and pass the check above, your data is in
PLATO's shape. Any tool that implements PLATO can read it, and any CSVW
processor can turn it into linked data (see [Linked data](../linked-data.md)).
[PLATO tools](https://pelagios.org/plato-tools/) converts the tables to PLATO JSON, RDF or Linked
Places Format in your browser.
You can publish the tables as they are, for example in a repository such as
Zenodo beside a publication, or load them into a platform that works with
PLATO; platforms may prefer either the workbook or the ten CSV files.
