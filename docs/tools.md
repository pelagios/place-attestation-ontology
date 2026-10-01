# Checking, converting and comparing

[PLATO tools](https://pelagios.org/plato-tools/) works on data in PLATO's
shape. It checks a file for mistakes, converts it to another format, and shows
whether a new version of a published dataset has kept what the earlier one
said, and it prepares a dataset for [publishing](#publishing-your-dataset).
It runs in your browser: your files are never uploaded. A dataset of a million
places has been checked and converted there, within the storage the browser
allows the page (see [large datasets](#large-datasets)). It also runs
[from the command line](https://github.com/pelagios/plato-tools#from-the-command-line),
for many files at a time, with the same checks and the same reports.

To use it, open the page and drop a file on it (or choose one), then press
**Check**, choose a format and press **Convert**, press **Compare with the
earlier version**, or choose what to prepare for publishing and press
**Prepare**. A page of its own, Chora, shows a dataset's places on a map
and adds the locations you draw there: see [placing on the map](#chora).

## What it reads and writes

| Format | Read | Write |
|---|---|---|
| The [spreadsheet tables](spreadsheets/index.md): the ten CSV files, a zip of them, or the temPlato workbook | yes | yes, as a zip of the ten CSV files |
| [PLATO JSON](json.md), place-centric or attestation-centric, and JSON Lines | yes | yes (place-centric) |
| [Linked data](linked-data.md): N-Triples, N-Quads or Turtle | yes | N-Triples |
| Linked Places Format, version 1 | yes | yes |
| [Annotations from Recogito](annotations.md) | yes | no |
| [Place names in a TEI edition](tei.md) | yes | no |
| [Your own table of places](tables-of-places.md): any CSV, or GeoJSON | yes, with the columns matched to PLATO's fields | no |

A gzipped file (ending `.gz`) is read as it is.

(large-datasets)=
## Large datasets

These figures come from PLATO tools' own test runs. In the browser
(Chromium), a million places in the spreadsheet tables, a CSV of 296 MB, were
checked, converted and saved in about 17½ minutes, using about 1.3 GB of
memory and, at the peak, 3.6 GB of the browser's storage. All of DEEP, 24.8
million triples in 2.6 GB, was read in about 10 minutes, with 756 MB of memory
and 5.2 GB of storage.

In the browser, the limit is the storage the browser allows the site. Before
it starts, the page estimates what a file will need and warns if that looks
like too much: roughly four times the file for most formats, forty times a
gzipped file, and twelve times the text of spreadsheet tables. Private windows
allow very little, so use an ordinary window. How much other browsers, such as
Safari, allow has not been measured.

If the page warns, use the
[command line](https://github.com/pelagios/plato-tools#from-the-command-line).
It has no storage allowance and is not held to a browser tab's memory: the same million
places converted in 6 minutes 38 seconds with 367 MB of memory. It still needs
disk, about one and a half to two times the uncompressed input, so give
`--work-dir` a folder on a disk with room if the temporary folder is small. It
needs memory wherever the whole of something must be held: a workbook (`.xlsx`
or `.ods`) is read whole, so save very large tables as CSV files instead; the
Data Cube check holds the whole graph; and a match review holds the places of
both datasets. Gzipping a file makes it smaller to keep and send, but not
smaller to work on. The command line also takes many files at once.

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

**Web addresses for your identifiers.** PLATO fixes how the spreadsheet
tables' identifiers become web addresses, so that every tool gives the same
ones. The base is the one given for the conversion, if any (on the page,
"Web address for your identifiers"), and otherwise the `base_uri` of the
[about sheet](spreadsheets/first-dataset.md#7-say-what-the-dataset-is), which
is where it belongs; a `/` is added to it unless it already ends in `/` or
`#`. A place's address is the base, then `place/`, then its `place_id`
(`https://w3id.org/my-project/place/bristol`), and a source's is the base,
then `source/`, then its `source_id`. In both, every character other than a
letter, a digit or one of `- . _ ~` is percent-encoded (written as a code such
as `%20`), so keep identifiers to those characters. The dataset's own address
is the about sheet's `dataset_uri`, or the base (with its `/`) if that is
empty. Without any base, PLATO tools uses a stand-in,
`https://example.org/my-dataset/`, which is not a permanent address. Converting *to* the tables, an address is
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
- an attestation that says the same but has lost its web address, or has
  been given another: later statements point to it by that address;
- a name, location, date, type, property or citation, with a web address of
  its own, that attestations point to, and that the later version describes
  differently, or no longer describes at all though attestations still point to
  it. It is part of what those attestations say, so changing it changes them.

For the first few attestations, names and other facets that changed, the
report shows what changed: what one version says and the other does not.
Each problem says how to put it right.

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

(match-review)=
## Reviewing matches

A match review asks, place by place: is this Newton that Newton? Choose your
dataset, press **Match with another dataset…**, and choose the other one, in
any format PLATO tools reads. Places whose names are alike, and that are near
each other, are suggested as possible matches; you accept or reject each, and
your decisions are written as [attestations](glossary.md), like any other.
Matching two files on your computer sends nothing anywhere.

A suggestion is a claim by no one until a person decides (see
[candidate sets](json.md#candidate-sets)), so none goes into your dataset:
only your decisions do. For each suggestion, choose one of:

- **Same place**: the suggestion is your place. The matches you accept for
  one place are written together as one attestation, so they stand or fall
  together.
- **Not this one**: the suggestion is wrong, and there is no more to say.
  Nothing is written.
- **Different places**: you can say why the two are *not* the same place.
  Your reason is written with a [denial](glossary.md): an attestation that
  the two are not the same place.

**Save the review** keeps the suggestions and your decisions so far in a
file of their own, the work file. To carry on, choose the same dataset,
press **Resume a review…** and choose the work file. It is yours: a working
file of PLATO tools, not PLATO data, and it is not published.

When you have done, press **Finish**. By default you get your dataset with
the new attestations added, as a PLATO JSON document, offered to save only
once the [version check](#comparing-two-versions) has found nothing of the
original deleted or changed. Or you can choose a PLATO file of only the new
attestations, each naming its place by its web address.

**Still to come: looking places up in the World Historical Gazetteer.** A
later version will also look your places up in the
[World Historical Gazetteer](https://whgazetteer.org/) (WHG), online and only
if you choose, for the same review. You will use a WHG token of your own,
and allow the lookup in the **Permissions** panel of PLATO tools, which
also says where the token is kept. Only the names
shown in the preview are sent, with their coordinates if you choose, and
nothing else of your dataset. WHG's scores rank the answers to one search
only, not how likely a match is, so the decision is still yours.

(chora)=
## Placing on the map

**Chora**, a page of its own in PLATO tools (**Open Chora** on the main
page, or [straight to it](https://pelagios.org/plato-tools/chora.html)),
shows a dataset's places on a map, with everything their attestations say of
each one over time, and lets you add a location you have worked out
yourself: a point, a line or an area, drawn on the map, or traced from a
historical map laid over it. It runs in your
browser like the rest of PLATO tools, and reads the formats in
[the table above](#what-it-reads-and-writes). A table of places of your own
is read with its columns matched as PLATO tools guesses them; to correct the
matching, convert the table to PLATO JSON on the main page and open that.
Files already chosen on the main page are offered when you open Chora.

Drop a file on the page, or choose one. The map shows every place with a
location, grouped where they crowd together (it shows the first 50,000; find
others by name). Find a place by any part of a name, or click it on the
map. The search looks in the name each place is listed under and in every
name its attestations give it, as written and in Latin letters (`toponym`
and `romanized`), except names denied or in a statement withdrawn or
replaced. A place found by another name is listed with it: *Byzantium — also
Constantinople*. Capitals and accents make no difference, and letters such
as œ, æ, þ, ð and ß, and ligatures such as ﬁ, match as they are spelt out
(*Brabœuf* finds *braboeuf*). The list shows fifty places at a time, with
**Previous** and **Next**, and marks a place with *no location* recorded. A IIIF Georeference Annotation, which places a map
rather than describing places, is not a dataset, and Chora says so: to lay
the map over the basemap, paste it under **Historical maps** (see
[tracing from a historical map](#tracing-from-a-historical-map)).

Chora works in one tab at a time: a second Chora tab says that it is open
in another. The main page and Chora can be open together.

**A place's card** lists what its attestations say: its names, types,
locations, related places (click one the dataset has to go to it) and sources. *Over time*
draws each dated statement as a bar from its start to its end, by year, and
lists those dated only in words. A statement the source makes less than
firmly is labelled: *denied* (the source says it was not so), *doubted*,
*reported* (as said by others) or *tentative*. On the map, a place's
locations are drawn in the same colours: a firm one solid, the others dashed
(a point, hollow), and a denied one, where the place is said *not* to be,
faint. A statement that a later one withdraws or replaces is left out, as
PLATO requires of any view of the dataset as it stands; the card says how
many were left out.

**A place with no location** is shown by what the dataset says about it
instead: the places it is related to, if they have locations, or else the
outline of its country, from its country codes (`ccodes`). The card says
which. Where there is neither, it says there is nothing to place it by.

### Drawing a location

Choose a place, then draw with the tools on the map: **Point**; **Line**,
clicking each point and the last one again to finish; or **Area**, clicking
each corner and the first one again to finish. **Edit** moves or reshapes a
drawing, and **Stop** ends drawing. Point at a tool, or reach it with the
keyboard, and it says what it does. Each drawing appears under *Your
drawings* in the place's card, where you can say what it marks (the whole
place, a feature of it, or a point standing for it) and how well the
location is known (exact, approximate, uncertain, historical approximate),
or remove it. A drawing that crosses the 180° meridian, in the Pacific,
cannot be recorded as it is drawn, so it is not kept, and the card says why.

Drawings are kept in this browser until you save, even if you close the
page: open the same file again, unchanged, and they come back, with their
places. To keep nothing between visits, turn off **Keep my working data
between visits** in the **Permissions** panel: drawings not yet saved are
then cleared the next time you open Chora, so save them before you leave.

### Tracing from a historical map

Under **Historical maps**, paste a georeference (a IIIF Georeference
Annotation, such as one made in [Allmaps](https://allmaps.org)), or the
address of one, of a IIIF manifest or of a IIIF image, and press **Add the
map**. The map is laid over the basemap, placed on the earth by its
georeference. Where it holds several georeferences of one image, made
separately, Chora lists them, each with the date it was last changed and its
number of control points, and you choose one (the most recently changed is
chosen to begin with). A map that comes with no georeference can be looked
for in Allmaps with **Look for a georeference**; or you can georeference it
in the Allmaps Editor, from the link that says it sends the map's address,
and paste here the georeference it makes.

Each map shown names the site its image comes from, with its credit and
licence, and has **Opacity**, **Show**, **Fit** and **Remove**. A map whose
licence allows only non-commercial use has one line more, saying that this
may bear on how what you trace from it can be reused. The maps you add are
kept between visits, as drawings are, unless **Keep my working data between
visits** is off.

No map's site is asked until you allow it in the **Permissions** panel, as
for a basemap: its image server, which sees which map you view and which
parts of it, and Allmaps, which learns which map a georeference was looked
for. Each has its own *Needs permission* line under the paste box, and one
reload brings them all. An address that forwards to another site, as some
archives' addresses do, is not followed: Chora offers it as a link to open in
a new tab, so that you can paste the address it ends at. If your browser
does not show that it enforces the page's protection, no map is shown.

To trace, choose a place and draw over the map by hand, with the same tools.
A drawing on a map is traced from it (from the topmost, where maps overlap),
and *Traced from* in the place's card lets you choose another map it lies
on, or the basemap. A traced point is, until you change it, *a point
standing for it*, of approximate precision, since a map's symbol stands for
a place rather than drawing it: choose *a feature of it* where the map draws
the feature itself, such as a church drawn as such. A traced drawing can also
mark *where the map writes its name*. A drawing moved or reshaped is traced
again; if it no longer lies on the map, it no longer cites it, and the card
says so.

### What a drawing records

Each drawing becomes a **new attestation** of its place, holding one
location. An attestation already in the dataset is never changed, since a
correction is a new attestation, not an edit (see
[comparing two versions](#comparing-two-versions)). With the location, the
new attestation records:

- **who drew it** (`contributor`): your name, and your ORCID iD if you give
  one. Chora asks before your first save, keeps the answer in this browser
  (see [who sees what](#which-map-and-who-sees-what)), and shows it as *Saving as* your name, with *change* and *forget me*.
  It is never taken from the dataset, since the person drawing is not
  necessarily the person who made it. A mistyped ORCID iD is caught, by its
  last digit, before anything is saved;
- **when it was drawn** (`created`);
- **how it was drawn**, in its `notes`, since PLATO has no term for this,
  such as "Drawn by hand on the Natural Earth basemap at zoom 9 in PLATO
  tools (Chora)". A basemap you pasted in yourself is not named there, only
  called "a basemap pasted by the contributor", since its address may be a
  private one and the notes are published with the dataset.

A drawing traced from a historical map records where it came from as PLATO
sets out for a geometry traced from a map (`plato:Geometry`, in the
[ontology reference](https://pelagios.org/place-attestation-ontology/)). It
cites the map as its evidence (`cito:citesAsEvidence`), with the canvas and
the area traced as the locator, and the map's licence where it is known; and
it cites the georeference as the method used (`cito:usesMethodIn`), as a
source of its own derived from the map. Its notes begin with the
georeference's address, its transformation and number of control points, and
when it was retrieved, and the canvas and manifest, since a georeference can
be changed after you trace from it; then comes "Traced by hand from a
georeferenced historical map at zoom 9 in PLATO tools (Chora)."

It has no web address of its own yet: **Mint** gives it one when you
[publish the dataset](#the-four-parts-in-order).

### Saving

**Save as PLATO JSON** writes the whole dataset, not the drawings alone, as
one PLATO JSON document (place-centric): every place and attestation as it
was read, with the drawings added after each place's own attestations. A
dataset in another format is converted, and the page lists anything the
conversion reported. The file is named after yours, ending `.chora.json`.

In the same run, the version check
([comparing two versions](#comparing-two-versions)) compares it with the
file you opened, and must find every attestation there exactly as it was,
every place described as it was, and exactly as many new attestations as you
drew, whether or not the dataset is published. A dataset with no attestations
yet, such as a list of places still to be located, can be saved too: the
check then finds only your drawings, as it must. Only when the check passes
is the file offered to save; otherwise the page says what went wrong, and
not to use it. Problems the dataset already had are listed even when the
check passes, since the saved file has them too.

Nothing is saved if a drawing is for a place whose attestations are not
written as a list, as PLATO requires: the drawing could only replace them.
The page names the place, to be corrected in the dataset first.

Where your browser asks where to save a file, the drawings are no longer
kept in the browser once it is saved. Where it simply downloads the file,
the page cannot tell when the download is complete, so the drawings are
kept, and the file still offered, until you press **The download is
complete: let these drawings go**. Either way, to add more, open the saved
file. If you change the drawings before saving the file, it is no longer
offered: save again.

### Which map, and who sees what

The map you see first, from [Natural Earth](https://www.naturalearthdata.com/),
comes from this site, so opening Chora sends nothing anywhere else. Its
borders are Natural Earth's borders as they are in practice, not a statement
on any dispute.

Under **Basemap** you can choose another, fetched from its provider:
OpenFreeMap (Liberty, Bright or Positron), OpenStreetMap, CARTO (Positron,
Voyager or Dark Matter), or a style address or tile address of your own,
pasted in, including one with a key. No other site is asked until you allow
it in the **Permissions** panel, from the button at the top of the page, the
same panel as on the main page. A basemap not yet allowed is not used: one
line, *Needs permission*, opens the panel at it. The panel names every site
the basemap will ask, since one provider may serve it from several, and says
what they will see: the part of the world you are looking at, and your
address on the internet, as any website does; never your files, which stay
on your computer. There you can allow it, or allow it for this tab only, or
choose *Never*, and it is no longer offered. A basemap allowed is used once
the page is reloaded: the panel offers the reload, keeping the dataset, the
place and the view, and asks first if something would be lost, such as a
line half drawn. One withdrawn gives way to Natural Earth at once. A style
you paste in is read from its own site once you allow that; if it names
further sites, each needs your permission too before the map uses them. The
page refuses any request to a site other than this one and those you have
allowed, and says how many it refused. If your browser does not show that it
enforces this protection, no other site is asked, and the page says so. A
basemap that cannot be loaded gives way to Natural Earth, and the page says
why.

Your permissions, your choice of basemap, any address you paste (with any
key in it), your name as the one drawing, the historical maps you add, and
your working data are kept in
this browser. PLATO tools is on pelagios.org, which other Pelagios sites
share, so, as the panel says, any Pelagios site can read them, on this
computer only.

### Still to come

- **Assisted tracing**: help in following what a historical map draws,
  rather than tracing it wholly by hand.
- **Adopting a location from a match**: taking a location from a matching
  record in another gazetteer, such as the World Historical Gazetteer. That
  records two claims, kept apart as PLATO keeps them: that this place is
  that record, and, as a new attestation citing the gazetteer, where it is.

## Publishing your dataset

Publishing a dataset means giving it addresses that will still work in
twenty years, a website where people and software can find each place, and a
record in a repository that gives it a DOI. PLATO tools prepares all of that
from the dataset itself, in four parts. On the page, choose the part under
*to publish it* and press **Prepare**; the release's name, the previous
release, the GitHub repository and the rest are under *Options*. From the
command line, each part is `publish` followed by its name.

Nothing leaves your computer. Neither the page nor the command line sends
anything anywhere: they write files, and uploading them, depositing them or
opening a pull request is for you to do. The page gives each result as a file
(a folder comes as a zip); the command line writes folders.

Every part checks the dataset first, and writes nothing to publish from a
dataset that has problems. It needs to know the dataset's base address:
`base_uri` in the [about sheet](spreadsheets/first-dataset.md#7-say-what-the-dataset-is),
or `uriSpace` in PLATO JSON. Record it there rather than giving it for each
run (on the page, "Web address for your identifiers"; on the command line,
`--base`), so that every part, and every later release, uses the same one.

### The four parts, in order

1. **Report** says what the dataset's description still lacks to be
   [FAIR](index.md#plato-and-fair-data): a title, a description long enough
   for search engines, authors with ORCIDs (whose check digits are tested),
   a licence given as its web address, a version, what the dataset covers,
   and a base address that will last. It counts the checks passed, and
   writes the deposit files (below). Put right what it lists, in the about
   sheet or the `gazetteer` header, and run it again.
2. **Mint** writes a copy of the dataset in which every attestation has a
   permanent address of its own, as PLATO JSON Lines (its name ends
   `-with-ids.jsonl`). This copy is what you publish, and what the other
   parts read.
3. **Site** makes a website for GitHub Pages from that copy, with the
   workflow that publishes it.
4. **w3id** writes the redirect rules that send your w3id.org addresses to
   the site. Only for a published dataset whose base is a w3id.org address.

```bash
npx github:pelagios/plato-tools publish report my-tables/
npx github:pelagios/plato-tools publish mint my-tables/ --previous my-gazetteer-1.0.jsonl
npx github:pelagios/plato-tools publish site my-tables-with-ids.jsonl --repo my-project/my-gazetteer
npx github:pelagios/plato-tools publish w3id my-tables-with-ids.jsonl --repo my-project/my-gazetteer --maintainer my-github-name
```

A part that finds problems says so and ends with exit status 1, like
**Check**.

### Addresses

Every address is made from the base, which always ends in `/`:

| What | Address |
|---|---|
| The dataset, and its home page | `<base>` |
| A place | `<base>place/<id>` |
| A source | `<base>source/<id>` |
| An attestation | `<base>place/<id>#a-<hash>` |
| A frozen release | `<base>release/<name>` |
| The latest dataset, to download | `<base>download/<file>` |

The addresses of places and sources are PLATO's own rule, set out under
[spreadsheets to RDF](linked-data.md#spreadsheets-to-rdf) and in
[step 7 of a first dataset](spreadsheets/first-dataset.md#7-say-what-the-dataset-is);
the rest are how PLATO tools lays out what it publishes. A release is named
with `--release` (on the page, "Release name"); its dataset's own address
(`@id`) should then be the release's, with `isVersionOf` the base, and the
report says what to set.

An attestation's address is part of its place's: `#a-` and the first eight
digits of a hash of what the attestation says. So minting the same data again
gives the same addresses, even from spreadsheet tables, which have no column
for them. An address an attestation already has is never changed. Give the
previous release with `--previous` (on the page, "Previous release"), and
every attestation it published keeps the address it had there.

Keep the identifiers of places and sources to letters, digits and
`- . _ ~`, in one part (no `/`), not starting with `.`, not ending in
`.jsonld`, `.ttl` or `.html` (w3id reads those endings as a request for that
format), and never two that differ only in capital letters: a website cannot
serve any other as a file. While the dataset is a
draft the report counts any other as a problem; once it is published its
addresses are frozen, and the site lists such places as held only in the
downloads.

### What "published" commits you to

A dataset is published when its `status` is `published`. From then on:

- its attestations are only ever added to (see
  [comparing two versions](#comparing-two-versions));
- the addresses of its places, sources and attestations are frozen;
- minting with `--previous` checks the new version against the previous
  release, as **Compare with the earlier version** does, and writes nothing
  if anything published was deleted or changed. Against a previous release
  that was still a draft, it writes the copy and warns you what would be
  refused once that release is published.

Until then, the site says on every page that the dataset is a draft and not
to be cited, and asks search engines to leave it out.

### The deposit files

**Report** writes a folder (its name ends `-deposit`) of files made from the
dataset's description, for a repository that gives it a DOI. Its
`README.txt` says what to check and fill in before you deposit.

| File | What it is for | Where it goes |
|---|---|---|
| `.zenodo.json` | Zenodo's description of the deposit | At the top of the GitHub repository the dataset is released from, where Zenodo reads it with each release |
| `CITATION.cff` | How to cite the dataset | At the top of the same repository, where GitHub shows *Cite this repository* from it |
| `datacite.json` | DataCite's description, for a repository that registers DOIs itself | Sent to that repository, with the DOI added |

Once Zenodo has given the dataset a DOI for all its versions (the concept
DOI), run the report again with it (`--concept-doi`, or "Concept DOI" on the
page) to put it in `CITATION.cff` and `datacite.json`, and give it to
**site** too, which shows it on the home page.

### The site

**Site** makes a website with a page and a JSON-LD document (`.jsonld`) for
every place and source, at the paths the addresses above lead to, and
optionally Turtle as well (`--turtle`). Each attestation with an address is
marked on its place's page, so its address opens the page at it. The home
page describes the dataset in the form search engines such as Google Dataset
Search read, and offers the whole dataset to download as PLATO JSON Lines,
N-Triples and spreadsheet tables.

Beside the site, a second folder (its name ends `-repo`) holds what goes into
your GitHub repository: a GitHub Actions workflow,
`.github/workflows/pages.yml`, and a `README-agora.md` saying how to set it
up. Once the workflow is committed and the repository's Pages settings have
Source set to *GitHub Actions*, every push that changes the dataset rebuilds
the site and publishes it. The workflow runs the same version of PLATO tools
that made it, so the site is made the same way every time, and publishes
nothing if the dataset has problems. The site itself is never committed.

So what you commit is the copy that **mint** wrote, with its attestation
addresses. The workflow never makes addresses: made there, they would be
made again on every run, and an address that changes is no address at all.
For a published dataset, the workflow stops if any attestation has no
address. Before you push, look at the site on your own computer: the
command line writes it to a folder (its name ends `-site`), which you can
open through a local web server, such as `npx serve my-tables-with-ids-site`.

If the dataset is not at the top of your repository, say where it is with
`--dataset-path`. The page cannot tell which folder spreadsheet tables were
chosen from, so for tables it guesses, and says so: correct the path in the
workflow, or make the site from the command line.

**Size.** GitHub Pages serves at most 1 GB for a site, and gives up on a
deployment that takes more than ten minutes. PLATO tools estimates the site's
size before it writes anything. Past the limit the page stops and says what
to do; the command line writes the site anyway, with a warning, for hosting
elsewhere. To stay within it, leave out Turtle, or publish a subset of the
places with `--only`, a file listing their identifiers, one to a line:

```bash
npx github:pelagios/plato-tools publish site my-tables-with-ids.jsonl --repo my-project/my-gazetteer --only places-to-show.txt
```

The addresses of the places left out lead to the site's "not found" page,
which points to the downloads, where every place is.

### How long your addresses last

That depends on the base, and the report grades it:

- **A w3id.org address** (`https://w3id.org/my-gazetteer/`) passes. It is a
  permanent redirect: if the site ever moves, the rules are changed and every
  address still works.
- **A domain of your own** (`https://gazetteer.example.ac.uk/`) is a warning:
  the addresses last as long as you keep the domain and its site. When the
  base is at the root of the domain, the site carries the `CNAME` file GitHub
  Pages needs; set the same domain in the repository's Pages settings and
  point the domain at GitHub as GitHub's documentation says. GitHub Pages
  serves a custom domain only from the root of a site, so a base further down
  the domain gets no `CNAME`, and the report says why.
- **A GitHub Pages address** (`https://my-project.github.io/my-gazetteer/`),
  a local one or a stand-in such as `example.org` is a warning while the
  dataset is a draft and a problem once it is published. A github.io address
  changes if the repository is renamed or moves to another owner, and every
  citation of it breaks. Use it to try things out; publish under a w3id.org
  address instead, with the site still on github.io behind it.

### Registering a w3id.org address

[w3id.org](https://w3id.org) gives permanent addresses by redirecting them,
under rules kept in a public GitHub repository, `perma-id/w3id.org`. A new
name is added by a pull request there. **w3id** writes everything that pull
request needs, into a folder whose name starts `w3id-`, and only for a
dataset that is published and whose base is a w3id.org address. It needs the
GitHub names of the people who will look after the name (`--maintainer`,
once each; "w3id maintainers" on the page), and where the site is: the
repository (`--repo`), or the site's address if it is somewhere else
(`--site-url`).

The folder holds the rules and a README for w3id.org, the pull request's
title and text (`PULL_REQUEST.md`), a list of real addresses of the dataset
with what each should answer, and a script, `test-w3id.sh`, that asks for
each. `STEPS.md` goes through it in order:

1. Test the rules on your own computer before anything else, in a local
   copy of the web server w3id.org runs (with Docker), with
   `sh test-w3id.sh http://localhost:8080`. Every line should say PASS.
2. Open the pull request yourself, from your own GitHub account, with the
   test results pasted into its text. PLATO tools never opens it: once it is
   merged, the addresses are public and meant to be cited for good.
3. Once it is merged, test the live addresses: `sh test-w3id.sh`.

The rules send a browser to a place's page and any other client to its
JSON-LD, and a request for `.jsonld`, `.ttl` or `.html` to that file. The
site must be live before the rules are merged, since they only send people
there.
