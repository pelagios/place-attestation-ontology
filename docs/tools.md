# Checking, converting and comparing

[PLATO tools](https://pelagios.org/plato-tools/) works on data in PLATO's
shape. It checks a file for mistakes, converts it to another format, and shows
whether a new version of a published dataset has kept what the earlier one
said. It runs in your browser: your files are never uploaded, and it works for
datasets of any size your disk can hold. It also runs
[from the command line](https://github.com/pelagios/plato-tools#from-the-command-line),
for many files at a time, with the same checks and the same reports.

To use it, open the page and drop a file on it (or choose one), then press
**Check**, choose a format and press **Convert**, or press **Compare with the
earlier version**.

## What it reads and writes

| Format | Read | Write |
|---|---|---|
| The [spreadsheet tables](spreadsheets/index.md): the ten CSV files, a zip of them, or the temPlato workbook | yes | yes, as a zip of the ten CSV files |
| [PLATO JSON](json.md), place-centric or attestation-centric, and JSON Lines | yes | yes (place-centric) |
| [Linked data](linked-data.md): N-Triples, N-Quads or Turtle | yes | N-Triples |
| Linked Places Format, version 1 | yes | yes |
| [Annotations from Recogito](annotations.md) | yes | no |

A gzipped file (ending `.gz`) is read as it is.

## Checking

**Check** holds a file to PLATO's own definitions. A JSON document is checked
against PLATO's JSON Schemas; spreadsheet tables against their table
definitions, and against the rules those definitions cannot state, such as
that a relation names a place or something else, one or the other; linked
data against the terms the ontology defines. It also finds two mistakes no
schema can: a route or network that, through its members, is a member of
itself; and an identity match written under one place that names another place
as its subject.

The report comes in three parts:

- **Problems** must be put right before the data is valid PLATO. Each is
  named in plain words, with where it is: the sheet, row and column, or the
  place and the key.
- **Warnings** are worth a look, but the data can still be used.
- **Would not be carried over** lists what PLATO JSON has no place for, should
  you convert the file.

A file that stops part-way, or is damaged, is reported as a problem in the
file, with what could be read before it.

## Converting

PLATO JSON and linked data hold everything PLATO can say, and converting
between them loses nothing. The spreadsheet tables and Linked Places Format
hold less, by design: see [what the spreadsheets cannot say](spreadsheets/index.md#what-the-spreadsheets-cannot-say).
Two rules govern what PLATO tools does about that.

**Nothing is left out without saying so.** The report names everything the
target format has no place for, in words ("The pronunciation of a name…:
Linked Places Format has no place for this, so it is left out").

**Nothing is written that would mislead.** Where leaving a detail out would
change what a statement says, the whole statement is left out, and the report
says so:

| | PLATO JSON, linked data | Spreadsheet tables | Linked Places Format |
|---|---|---|---|
| A [denial](glossary.md): the source says something was *not* so | kept | kept, one thing denied per row | left out |
| A statement that a later one withdraws or replaces | kept, with what withdraws it | left out | left out |
| A [computed value](glossary.md), worked out by software | kept, marked as computed | left out | left out |
| A figure from a [statistical table](statistics.md) | kept | left out | left out |
| Identity matches made together, in one statement | kept | left out | left out |
| How firmly the source says it ([stance](glossary.md)) | kept | kept | the statement is kept; its stance is reported as left out |

So a file in the tables or in Linked Places Format shows the dataset as it
stands now. It never shows a withdrawn statement as current, a denied market
as a market, or one figure from a table as a fact about the whole place.

**Web addresses for your identifiers.** Converting spreadsheet tables, PLATO
tools turns each place's and source's identifier (such as `bristol`) into a web
address, under the base you give on the page ("Web address for your
identifiers"). Without one, it uses the `base_uri` of the
[about sheet](spreadsheets/first-dataset.md#7-say-what-the-dataset-is), which
is where it belongs; without that, a stand-in, `https://example.org/my-dataset/`,
which is not a permanent address. Converting *to* the tables, an address is
kept only if reading the tables back would give the same one; otherwise the
report says it is lost.

## Comparing two versions

Once a dataset says it is published, its attestations are only ever added
to: none is deleted or changed, and a correction is a new attestation that
withdraws or replaces the old one, which stays. Why, and what that makes
possible, is explained under
[citing a place in a gazetteer that changes](linked-data.md#citing-a-place-in-a-gazetteer-that-changes).

**Compare with the earlier version** shows that a new version has kept to
this. Choose the new version first, then press the button and choose the
earlier one. The two may be in different formats: what is compared is what
each attestation says, not how the file writes it.

**Problems** are what breaks the rule:

- an attestation of the earlier version that is missing from the later one;
- an attestation that says something different in the later one;
- a name, location, date, type, property or citation, with a web address of
  its own, that attestations point to, and that the later version describes
  differently, or no longer describes at all though attestations still point to
  it. It is part of what those attestations say, so changing it changes them.

For the first few of each, the report shows what changed: what one version
says and the other does not. Each problem says how to put it right.

**Warnings** do not break the rule:

- a place or a source described differently, since those may be corrected;
- an identity match removed or changed;
- an attestation added without the date it was made (`created`), without
  which the dataset's state at an earlier moment cannot be worked out;
- a later version that is not marked published, gives the same version as
  the earlier one, or names another as the version before it.

Before the earlier version is published the rule does not yet apply, so
everything is listed as a warning, and the report says why.

**Give your attestations web addresses.** An attestation without an address
of its own (in JSON, an `@id`) can only be found by what it says. If one goes
missing, the check cannot tell whether it was deleted or changed, and no later
attestation can withdraw or replace it, since there is nothing to point to.
The report counts such attestations. PLATO recommends that every attestation in
a published dataset has a permanent address. The spreadsheet tables have no
column for one, so this applies to data published as JSON or linked data.

A comparison that could not read the whole of either version does not pass,
and nor does one whose earlier version holds no attestations: in both cases
nothing, or not everything, was compared.
