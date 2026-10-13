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
**Prepare**. **Show on the map** opens Chora, which shows a dataset's places
on a map and adds the locations you draw there: see
[placing on the map](#chora).
Not sure where to start? [Methodos](#methodos) leads you through a whole
workflow, step by step, from three questions.

## What it reads and writes

| Format | Read | Write |
|---|---|---|
| The [spreadsheet tables](spreadsheets/index.md): the ten CSV files, a zip of them, or the temPlato workbook | yes | yes, as a zip of the ten CSV files |
| [PLATO JSON](json.md), place-centric or attestation-centric, and JSON Lines | yes | yes (place-centric) |
| [Linked data](linked-data.md): N-Triples, N-Quads or Turtle | yes | N-Triples |
| Linked Places Format, version 1 | yes | yes |
| [Annotations from Recogito](annotations.md) | yes | no |
| [Place names in a TEI edition](tei.md), TEI P5 or P4 | yes | no |
| [Your own table of places](tables-of-places.md): any CSV, GeoJSON, or a sheet of a workbook (`.xlsx`, `.ods`) that is not the spreadsheet tables | yes, with the columns matched to PLATO's fields | no |

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

**Stopping a run.** **Cancel** stops a run on the page at once, even in the
middle of a long step, and keeps nothing it had half-written: no part of a
file is offered. In a [workflow](#methodos), the step is then *Stopped by
you*, to run again. For a moment afterwards the page may say "The cancelled
run's files are still being released; try again in a moment." On the command
line, Ctrl-C stops a run in the same way, and removes its working files and
any file it had not finished.

(the-kept-file)=
## The file you chose, kept

While **Keep my working data between visits** is on (in the **Permissions**
panel, under *Your working data*), the file you choose on the main page, or
the files, is kept in this browser, with no time limit, so that you need not
choose it again. It stays until you forget it, clear a workflow's files
(**Clear them**), turn the setting off, or choose another file, which takes
its place. It never leaves your computer.

On a new visit, or after a reload, it is offered above the place where you
choose a file, never chosen for you: *Kept from last time: …*, with **Use
it** and **Forget it**. Taking up a [workflow](#methodos) again, or a reload
for a permission while [Chora](#chora) has it open, chooses it again by
itself. The
**Permissions** panel lists it too, with **Forget it**. Like everything else
kept in this browser, it can be read by other pelagios.org pages on this
computer (see [who sees what](#which-map-and-who-sees-what)).

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

**Gzipping the output.** Under *Options*, **Gzip the converted file**
compresses the file as it is written and adds `.gz` to its name; on the
command line, give `--gzip` to `convert` (it is for converting only). The
same data always gives the same bytes. The spreadsheet tables are not
gzipped, as they are a zip already, and the report says so.

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
  it. It is part of what those attestations say, so changing it changes them;
- a pair of places that one contributor now says both are and are not the
  same place, with both answers current: a decision was changed without
  withdrawing the earlier answer (see [reviewing matches](#match-review)).

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

**Changing a decision after Finish.** Every attestation the review writes is
given a web address of its own, made as **Mint** makes one (`#a-` and a hash:
see [addresses](#addresses)), so that a later change can point to it. This
applies only to places under the dataset's base address. Finish again after
changing a decision, on the dataset that Finish wrote, and the earlier answer
is withdrawn: a new attestation retracts it (`plato:Retracts`), and the new
answer, if there is one, is written beside it. Nothing is deleted, so the
dataset still shows what it said before. A decision made again unchanged
writes nothing new. Only your own earlier answers are withdrawn. They are
recognised by your ORCID iD, or by your name alone where either side gives no
ORCID iD, and the report then asks you to check them. PLATO tools never uses
`plato:Supersedes` for this: a superseded answer would come back if the answer
that replaced it were withdrawn later.

In a dataset not yet published, the Finish area also lets you **replace** the
earlier answer: take it out and write the new one, keeping no record of it.
Withdrawing is the default. A published dataset always keeps its earlier
answers, whichever you choose. On the command line this is
`--draft-answers withdraw` or `replace`.

Each Finish is recorded in the work file: what it wrote, and by whom. Save the
review again afterwards, as the page asks. A later Finish can then tell
whether you have given it the dataset it wrote. If you give it the original
file instead, which holds none of the review's answers, it warns you, since a
changed decision cannot withdraw an answer that is not there.

**Looking places up in the World Historical Gazetteer.** The review can also
look your places up in the [World Historical Gazetteer](https://whgazetteer.org/)
(WHG), or another gazetteer that offers the same kind of search, online and
only if you choose. You allow the lookup in the **Permissions** panel of
PLATO tools, and give a WHG token of your own (see
[the WHG token](#the-whg-token), below). A preview shows exactly what will be
sent before anything goes: each place's name, its other names only if you
ask, and its coordinates only if you choose to search near it; and, where a
[Scope](#scope) is set, which of its parts are sent and as what; nothing else
of your dataset. What comes back joins
the review beside your own matches, with each record's licence and its kind of
place, nearest first. A candidate whose kind of place clashes with your
place's own (a lake for a town) comes after the others as near, and says so
("Ranked down: …"). Your place's own kind decides the order only among
records of one place (within 2 km of each other), as when WHG holds one
village several times over, from different gazetteers. WHG's scores rank the
answers to one search only, not how likely a match is, so the decision is
still yours.

**Which places** are looked up is chosen in the lookup panel; **Only places
without a gazetteer link** chooses, in one click, the places that neither
have a gazetteer's address of their own nor are linked to one, and the
preview says how many before anything is sent.

A place whose own address is already a gazetteer's (a WHG, GeoNames, Getty
TGN, Wikidata, OpenStreetMap or Pleiades address, such as a TEI `ref` or a
Recogito link) keeps it: it is never replaced, and WHG's record of it is not
suggested again. It is still looked up, and if WHG's best candidate is more
than 25 km from the record its address names, the place is flagged on its
review screen with both records and the distance. A flagged place is left for
you to decide, and never accepted in bulk. The distance can be changed in the
lookup panel. Where WHG did not return that record, or the record has no
point, the screen says so and nothing is flagged.

**Kind of place.** Each candidate from the World Historical Gazetteer shows
*Kind of place:* with its types: a type from the Getty AAT by WHG's label for
it, with its code, and any other source's type as its code alone (such as
`gn:P.PPL` or `osm:village`), never a label made up for it; or *type unknown*
when the record gives none. Your place's own kind is the types your dataset
gives it (in a table of places, its kind-of-place column). Some kinds never go
together, such as a body of water and a settlement; a settlement, a division
and a landform do (a parish named after its village, a village after its
hill), and a kind these tools do not know decides nothing. Chora's
[*Find in a gazetteer…*](#adopting-a-location-from-a-match) panel shows each
record's kind in the same way, naming by label only the types of
[Scope](#scope)'s shortlist.

**Placeholders.** WHG holds some records whose only name is a cataloguing
placeholder ("Oknoname 037068 Dam" and the like). These are left out of the
candidates, and the lookup says how many, in its summary and on a place left
with nothing.

**WHG's limits.** WHG allows each token a number of requests a day. When it
is reached, the lookup stops, keeps what was answered, and says so: "WHG's
daily limit for this token is reached; it resets at …", in your own time.
Your token is not at fault, and is not asked for again: resume the lookup
once the limit has reset. WHG's limit per minute is waited out by itself.

(the-whg-token)=
**The WHG token.** The field for it, *Your WHG token*, shows only when the
World Historical Gazetteer is the service chosen, in the lookup panel and in
Chora's [*Find in a gazetteer…*](#adopting-a-location-from-a-match) panel,
which share it. Before a token is given, the field is empty, with
**Remember my token** beside it. Press Enter to give the token for this tab
only, or **Remember my token** to keep it in this browser. Once a token is
given, the field shows `••••••••`, never the token itself, with where it is
kept beside it, *Token kept for this tab only* or *Token remembered in this
browser*, and **Forget the token**, which forgets it in this browser at once,
without asking. Forgetting a token does not revoke it: only regenerating it
in your WHG profile does. The field takes only what you type or paste into
it: a password your browser has saved is never taken for a token. The
**Permissions** panel says where the token is kept too, and can forget it.

**The language of the names.** Each name is sent to the World Historical
Gazetteer with its language, so that WHG reads it as a name in that language:
the name's own language tag where it has one (`en-GB` is sent as `en`, `eng`
as `en`), else the language you give for the whole dataset in the lookup
panel (*The dataset's language*, a code such as `en`, `la` or `ang`; on the
command line, `--lang`). You need not know the code: type a language's code
or its name, and the field offers the languages that fit, historical ones
among them, so that *old eng* finds Old English, `ang`. A code the field does not recognise is refused
beside it, and nothing is sent until it is corrected or emptied. A name
tagged `und` or `mis` takes the dataset's language; one tagged `mul` or
`zxx` is sent with none. A name with no language is never sent as
"undetermined", and the preview says how many queries go without one. A
language is not a filter: it leaves nothing out.

**Regions are matched to areas.** In the region review, each region is looked
up among records with an outline only, so that a region is never matched to
a point (a town of the same name), within which nothing could be looked up.
The places themselves are looked up among all records.

(scope)=
## Scope: confining every lookup

A **Scope** confines every lookup in the World Historical Gazetteer to a part
of the world, kinds of place, years and sources. It is sent to WHG only;
another gazetteer is sent nothing of it. **Edit** opens it in the centre of
the page, under *Scope of the lookups*, in four parts:

- **Where**: **Anywhere**; **In these countries**; **Within a place in WHG**,
  found there by name, among records with an outline only (a point cannot
  hold places); or **Within an area drawn on a map**, drawn corner by corner
  on the Natural Earth map, from this site.
- **What kinds of place**: chosen from a shortlist (villages, parishes,
  rivers and so on), or, under **More types…**, from WHG's whole tree of the
  AAT's place types. WHG matches a type exactly, not the narrower types under
  it, so each type chosen is sent with all of them, and its label says how
  many ("Villages (and 1 narrower type)").
- **When**: **From the year** and **To the year**, either or both (a year
  before the common era is negative: `-500` for 500 BCE), with **Include
  places with no dates**. Unticked, a place with no dates is left out
  whenever years are given, and the Scope says so: *Places with no dates are
  left out*.
- **Only these sources**: the WHG sources to look in, sent as their
  namespaces. Nothing chosen means every source. Unlike the other parts,
  the sources narrow WHG's search itself.

**Done** goes back to the step. **Clear the Scope** sets it back to nothing.

**Whose Scope it is.** In a workflow, the Scope is the workflow's: kept with
it, in this browser and in its downloaded record, and used by every WHG
lookup it makes, including Chora's *Find in a gazetteer…* when Chora is
opened for the workflow. It is shown as one line in the
[tracker](#the-tracker), such as *Scope: GB, IE · Villages · 1500 to 1600*,
which opens to its four parts, with **Edit**. Outside a workflow, the lookup
panel has a Scope of its own, for that tab only. A workflow begun while the
tab has one asks whether to use it (**Use it** or **No**), and never takes it
in silently.

**What a row already says comes first.** Once the regions in your table's
region columns are matched, each place is looked up within its own regions,
not within the Scope's Where, and so are the regions below the widest. A
place's own filters in the lookup panel (its countries, near its point) win
too. The kinds of place, the years and the sources still apply to every
place. A place looked up before its regions are settled keeps the Scope's
Where.

**A narrow Scope can leave a place with nothing.** The sources narrow WHG's
search itself, but the Where, the kinds of place and the years are filters:
WHG first takes its best two hundred or so matches by name, from the sources
chosen, then leaves out every one outside them, the right answer too. A place for which nothing was
left says so ("Nothing within the Scope among WHG's best name matches…"), and
offers **Look it up again without Scope**, for that place alone, with nothing
of the Scope sent. Nothing is ever relaxed by itself.

(region-review)=
## Reviewing regions, level by level

Many tables give, beside each place, the regions it lies in: a country, a
county, a parish (the columns read as *within*). **Review the regions level by
level** looks these up in the World Historical Gazetteer before the places,
widest first, each inside the one above it. Every row naming Surrey in England
is one region; a Newport in Shropshire and a Newport in Monmouthshire are two.

**How a match narrows the next search.** A region waits until the region above
it is settled, with a match or with **None of these**. Its search is then kept
within the gazetteer's record for the region above, or within all its records
taken together when it was matched to more than one. Where that cannot be
asked, it is kept to the area they cover. Either way, the match's countries
are added. The widest level, which has no region above it, is kept within
the [Scope](#scope)'s Where, if one is set, and so is a region whose region
above has no match. A constraint only ever takes candidates away: a country filter even
drops one with no country recorded. Each region says what it was looked up
within. A search WHG could not narrow returns nothing, and the review says so:
that is not a finding that there is no match.

**Asking again.** When the right region is missing, ask again, for one region
or a whole level: **Again without the countries**, **Within the area
instead**, within the region above that instead, or **With no constraint**,
which also drops the Scope's Where (its kinds of place, years and sources
still apply). Each button says how many queries and requests it will cost. Changing a
settled region clears the decisions and candidates below it, after asking, and
**Undo** puts them back. Once a place's regions are settled, the places are
looked up within them and reviewed one at a time, as in
[reviewing matches](#match-review). A place still waiting can be looked up
without its regions.

**WHG's guards.** WHG's own page accepts a candidate only when it tops its
answer, its title is an exact match or its score is 90 or more, it is not held
back, and there is no tie. It is held back when WHG gives it a confidence
below 30, or, where WHG gives none, when its names are too unlike the name
sent, by WHG's own measure. It is tied when another candidate scores as high,
unless that one is the same record repeated. In the review of places,
**Accept the N that pass WHG's guards** accepts each place's one passing
candidate, as the kind of match you choose (close match by default). A
candidate too far from the place, in another country, or of another kind of
place than yours (a lake for a town, say), is left out and counted, for you
to decide: a clashing kind is never accepted in bulk. So is a place for which two places of its name
were found where it was looked for, even when WHG's guard lets one of them
through: the place says so ("2 places of this name in …: left for you").
Within a region, every place of that name in it counts, however far off;
otherwise only those within the greatest distance. Records of the name
within 2 km of each other are taken for one place, as WHG often holds one
village several times over, from different gazetteers. Only titles are
compared, not other names. Each acceptance is recorded as your decision,
naming the guard; **Undo** takes them back. Nothing is ever accepted
automatically.

**What is written.** Two separate claims, as in
[regions matched to a gazetteer](json.md#regions-matched-to-a-gazetteer). Your
source's containment stays as it is: each place is `ContainedIn` a region made
from your data, one for each whole chain of regions. Your decision is an
attestation about that region, with you, the date and your certainty,
bundling an identity relation (a close or an exact match, with its basis) to
each gazetteer record you matched it to. When the suggestions are published as
a [candidate set](json.md#candidate-sets), each relation points back to its
suggestion with `promotedFrom`, and the suggestion's `matchParameters` record
what it was looked up within. The containment is never rewritten: a match
changed later is a new attestation. Regions need addresses of their own, so
the dataset needs a
[base address](tables-of-places.md#place-ids-and-the-base-address). The
repository's
[place-centric-regions.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-regions.json)
and
[candidate-set-regions.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/candidate-set-regions.json)
show both claims. Linked Places Format writes them as one `broaderPartitive`
relation.

**Rows set aside.** A place can be marked **Keep without reconciling** (never
looked up, still in the dataset) or **Leave out of the dataset** (and the
version check is told to expect exactly those missing). Notes stay in the work
file, never in the dataset.

**From the command line.** With your WHG token in `WHG_TOKEN`:

```bash
npx github:pelagios/plato-tools lookup --levels --dry-run parishes.csv
npx github:pelagios/plato-tools lookup --levels --reviewer "Your Name" parishes.csv
```

The first shows the plan, level by level, and sends nothing. The second looks
up the first level with regions ready (or `--level N`) and writes a work file,
given back with `--review` to carry on. `--relax` takes `countries`, `area`,
`ancestor` or `all`; `--only` one region or place; `--unconstrained` also
looks up places whose regions are unsettled. The regions are decided on the
page.

(chora)=
## Placing on the map

**Chora**, in the middle of the PLATO tools page (its card among the tools,
**Show on the map** in step 2, or
[straight to it](https://pelagios.org/plato-tools/#chora)), shows a
dataset's places on a map, with everything their attestations say of each
one over time, and lets you add a location you have worked out yourself: a
point, a line or an area, drawn on the map, or traced from a historical map
laid over it. It runs in your browser like the rest of PLATO tools, and
reads the formats in [the table above](#what-it-reads-and-writes). A table
of places of your own is read with its columns matched as PLATO tools
guesses them; to correct the matching, convert the table to PLATO JSON first
and open that.

Chora shows the file chosen in step 1, *Choose your data*, as soon as it
opens, and whatever you choose there while it is open; it has no file
chooser of its own. Step 1 stays above the map, folded to one line with
**Change** once its file is recognised. While the map is shown, the tools
fold away behind **Tools ▸**, which brings them back, and a workflow you are
following stays beside the map. **Leave the map** goes back to the steps.
If the map itself cannot be loaded, the page says so where the map would
be, with **Reload the page**, which comes back to the map.

The map shows every place with a
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

Chora works in one tab at a time: opened in a second tab, the map says that
it is open in another, and the rest of the page works there as usual.

**A place's card** lists what its attestations say: its names, types,
locations, related places (click one the dataset has to go to it) and sources. *Over time*
draws each dated statement as a bar from its start to its end, by year, and
lists those dated only in words. A statement the source makes less than
firmly is labelled: *denied* (the source says it was not so), *doubted*,
*reported* (as said by others) or *tentative*. On the map, a place's
locations are drawn in the same colours: a firm one solid, the others dashed
(a point, hollow), and a denied one, where the place is said *not* to be,
faint.

How well a location is known is drawn too, as PLATO records it, and only
where it does. A point's precision (`spatialPrecision`) is a mark around it:
four ticks for *exact*, a dashed ring for *approximate*, three small rings
for *uncertain* (one of several possible locations), and the dashed ring with
an hourglass for *historical approximate*. A line or an area outline is
edged in the same way: solid, dashed, dotted, or dash and dot. A point's
`precisionKm` is a circle of that radius, drawn to scale on the ground, and
the map zooms out to show it whole when you choose the place. A location
whose precision is not given has no mark, and one without `precisionKm` has
no circle: the map does not invent an uncertainty the data does not give.
**Key: how well a location is known**, folded at the foot of the map once a
place is chosen, shows each mark. The card names the precision with PLATO's
own gloss, and how far out the location may be ("to within 2 km"; for a line
or an area, "boundary to within 2 km"). Where the circle would be too large
to draw, the card adds "(too large to draw)".

A statement that a later one withdraws or replaces is left out, as
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
page: choose the same file again, unchanged, and they come back, with their
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

### Tracing with assistance from the map's ink

Once a map shown has drawn a tile, two more tools are offered beside the
drawing tools, **Trace area** and **Trace line**; until then they say in a
tooltip why not. The tracing itself is loaded when one is first pressed, and
a click made on the map before it has loaded is acted on once it has. With
**Trace area**, click inside an area the map draws, such as a wash or an
outlined field, and its outline is proposed from the map's own ink; with
**Trace line**, click on a line, such as a road or a river, and it is
followed both ways from the click, as far as the ink goes, and proposed.
The proposal is shown on the map, with a panel of settings. For an area:
the colour tolerance, **Bridge gaps in the outline** and how far, and
**Leave out small holes (lettering)**, which keeps holes no bigger than the
map's lettering out of the proposal. For a line: **Match the colour clicked
(else: the darkest ink)**, which follows the colour under the click, within
the colour tolerance, rather than the darkest ink (the tolerance counts only
when this is ticked); the thickness of line to follow; and **Jump gaps in
the line**. For both, how closely to keep to the ink. Moving one proposes
again, from the part of the map already read, so the map's server is asked
nothing more. A proposal is not yet a drawing: **Accept** (or Enter)
makes it one, to edit or remove like any other, and **Let go** (or Esc)
drops it. Accepting before a place is chosen keeps the proposal and asks you
to choose one.

A line may stop where the ink does, or where it meets a fork it cannot judge;
Shift-click further along carries it on, keeping what was proposed and
tracing the new click alone. Whatever holes an area still has are left out
when it is accepted, since a drawing is an outline: the page says how many.
A fill that covers most of the part of the map read is refused in words, as
the area is not closed: bridge its gaps, or lower the tolerance. One that
runs out to the edge of the part read is tried again from a larger part,
and then once at a coarser scale; if it still runs out, the page says it is
too large to trace at once: zoom out, or trace it in parts.

**Snap to ink**, offered while you draw a line or an area by hand (not a
point), once a map shown has drawn a tile, helps tracing by hand: a vertex
you place within 10 screen pixels of the map's ink
goes onto it, the centre of a line or the edge of an area. Hold Alt to
place a vertex where you click.

What is proposed is read from the map's image tiles, fetched from the map's
own image server under the permission you gave it under **Historical
maps**, and nothing else is asked; withdraw that permission and everything
read from that server is let go, the proposal with it. The work is done in
your browser.

A shape traced this way is attested, not computed: you accepted it. Its
notes say so, after the georeference's sentences: that it was proposed from
the map's ink, by filling an area or following a line, with the settings
used; for an area, how many holes were left out; then whether it was
accepted as proposed or edited by hand, counting the vertices moved, added
and removed against those proposed. Moved off its map, it keeps saying how
it was proposed, and that the citation was dropped.

The assistance has limits, which it is better to know than to meet. It
reads the map at the resolution shown, so a fine line is best traced zoomed
in: a line about three pixels wide in the image read, running diagonally,
may be placed a few pixels short at its ends, and a very short stroke of
that width may not be followed at all. A line narrower than six pixels
that ends square-cut, but runs at a slant to the image's pixels, has that
end placed as if rounded, half a line's width short; an end square to the
pixels is placed where the ink stops. A line ending on
a bar twice its width may run on along the bar; on one of its own width it
stops. A map's server that refuses its pixels (one that asks you to log in,
or lets no other site read it) cannot be traced from, and the page says so.
Check every proposal against the map before accepting it, as you would a
drawing of your own.

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
georeferenced historical map at zoom 9 in PLATO tools (Chora)", or, for one
[traced with assistance](#tracing-with-assistance-from-the-maps-ink), how it
was proposed and what was done to it by hand.

It has no web address of its own yet: **Mint** gives it one when you
[publish the dataset](#the-four-parts-in-order).

### Saving

**Save** writes the whole dataset, not the drawings alone: every place and
attestation as it was read, with the drawings added after each place's own
attestations. A dataset read from PLATO JSON Lines is saved as PLATO JSON
Lines (the button says **Save as PLATO JSON Lines**), and the file is named
after yours, ending `.chora.jsonl`. Anything else is saved as one PLATO JSON
document (place-centric), ending `.chora.json` (**Save as PLATO JSON**); a
dataset in another format is converted, and the page lists anything the
conversion reported.

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
complete: let these drawings go**. If you change the drawings before saving
the file, it is no longer offered: save again.

Once the check passes, the saved file is also chosen in step 1, *Choose your
data*, for the other tools, and the page says so under the save. Once its
drawings are let go, Chora carries on with the saved file as its dataset,
keeping the place, the view and any drawings made since, so that what you
draw next is added to it and a later save builds on it. In a
[workflow](#methodos) at Chora's step, the save also does that step, if the
dataset Chora had open is the one that went to the step (see
[Map your data](#methodos-map-your-data), step 8). Saved from another
dataset, the step stays open, and the tracker and the save say why.

### Which map, and who sees what

The map you see first, from [Natural Earth](https://www.naturalearthdata.com/),
comes from this site, so opening Chora sends nothing anywhere else. Its
borders are Natural Earth's borders as they are in practice, not a statement
on any dispute.

Under **Basemap** you can choose another, fetched from its provider:
OpenFreeMap (Liberty, Bright or Positron), OpenStreetMap, CARTO (Positron,
Voyager or Dark Matter), or a style address or tile address of your own,
pasted in, including one with a key. No other site is asked until you allow
it in the page's **Permissions** panel. A basemap not yet allowed is not used: one
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
key in it), your name as the one drawing, the historical maps you add, your
working data, a WHG token you ask to be remembered, and the file you last
chose in step 1 (see [the kept file](#the-kept-file)) are kept in
this browser. PLATO tools is on pelagios.org, which other Pelagios sites
share, so, as the panel says, any Pelagios site can read them, on this
computer only.

### Adopting a location from a match

From a place's card, *Find in a gazetteer…* looks the place up in the World
Historical Gazetteer and adopts a record's location. That records two claims,
kept apart as PLATO keeps them: that this place is that record, and, as a new
attestation citing the gazetteer, where it is. The search looks where the
place lies: within the nearest region your dataset identifies with WHG
records (its `ContainedIn` regions), and in its countries, and the panel says
so before anything is sent. If the right record is not found there, **Search
everywhere** looks without them; it is never done for you. When Chora was
opened for a workflow that has a [Scope](#scope), the search keeps to its
kinds of place, years and sources, and to its Where when the place's own
regions and countries give none. The WHG token is given here as in the
lookup panel (see [the WHG token](#the-whg-token)).

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

1. **Mint** writes a copy of the dataset in which every attestation has a
   permanent address of its own, as PLATO JSON Lines (its name ends
   `-with-ids.jsonl`). This copy is what you publish, and what the other
   parts read. It needs the base address (above).
2. **Report** says what the dataset's description still lacks to be
   [FAIR](index.md#plato-and-fair-data): a title, a description long enough
   for search engines, authors with ORCIDs (whose check digits are tested),
   a licence given as its web address, a version, what the dataset covers,
   and a base address that will last. It counts the checks passed, and
   writes the deposit files (below). Put right what it lists, in the about
   sheet or the `gazetteer` header, and run it again. Run it on the minted
   copy: for a published dataset it refuses attestations without addresses.
   You can run it on the draft first, to see what the description still
   lacks before you mint.
   It also warns of [licences](#licences-that-travel-with-what-you-copy)
   that may not sit under the dataset's own.
3. **Site** makes a website for GitHub Pages from that copy, with the
   workflow that publishes it.
4. **w3id** writes the redirect rules that send your w3id.org addresses to
   the site. Only for a published dataset whose base is a w3id.org address.

```bash
npx github:pelagios/plato-tools publish mint my-tables/ --previous my-gazetteer-1.0.jsonl
npx github:pelagios/plato-tools publish report my-tables-with-ids.jsonl
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

(keep-it-private)=
### Keep it private until it is ready

Everything PLATO tools does to a dataset is done on your own computer:
checking, converting, comparing, matching (Krisis), drawing (Chora) and
preparing it for publishing (Agora). Nothing is uploaded. So the way to keep
work in progress private is to keep it there: prepare, match and review it
locally, and put it anywhere public only when you are ready for it to be
seen.

Nothing else leaves your computer unless you allow it in the **Permissions**
panel, and your dataset itself never does. What can go, once allowed:

- **Looking places up in the World Historical Gazetteer** (Krisis's lookup,
  and Chora's *Find in a gazetteer…*) sends the names you look up, any limits
  you set (such as countries, a region, kinds of place, years or sources), and
  a place's coordinates if you search near it, with your WHG token, which says
  who asked. The preview shows exactly what will be sent. The names of kinds
  of place are fetched from WHG without the token. You never need to upload a
  dataset to WHG to look its places up.
- **Chora's maps** fetch their tiles and images from the sites you allow
  (see [Basemaps](#chora)); nothing of yours is sent with them.
- **A site you upload** is public, even while the dataset is a draft. Every
  page of a draft site says DRAFT and asks search engines not to list it
  (`noindex`), but anyone who has its address can read every page and
  download the whole dataset, and an address is easily passed on. GitHub
  Pages serves a site from a private repository to everyone too (only an
  Enterprise organisation can restrict it), and the workflow Agora writes
  publishes the site on every push that changes the dataset.

So, until the dataset is ready:

- look at the site on your own computer (`npx serve my-tables-with-ids-site`)
  rather than uploading it;
- keep the dataset in a private repository, or in none, and commit the
  site's workflow only when the site may be seen;
- to show a draft to a colleague, send them the files.

The report and the site of any dataset not yet published say so too.

(licences-that-travel-with-what-you-copy)=
### Licences that travel with what you copy

An attestation that copies from a source, such as a location adopted from the
World Historical Gazetteer or a line traced from a historical map, comes under
that source's licence, and a dataset cannot pass it on more freely than the
source allows. Chora records the licence of what it copies: an adopted
location carries the licence of the source WHG had it from, and a traced
drawing the licence of the map, where each is known.

So the report, on the page and on the command line, reads the licence of each
source an attestation cites against the dataset's own, and warns, with a
count and a few examples (the attestation, its source's licence and the
source), of any that may not sit under it:

- a source for non-commercial use only (NC), in a dataset whose licence
  allows commercial use;
- a source whose licence allows no adaptations (ND), even under the same
  licence;
- a share-alike source (such as ODbL or CC BY-SA), in a dataset under
  another licence;
- a source that asks for credit (such as CC BY), in a public-domain dataset
  (CC0, PDDL or the Public Domain Mark).

A rights statement, from [rightsstatements.org](https://rightsstatements.org/)
(such as In Copyright), is not an open licence: it grants nothing, and the
report says that you may need the holder's permission. A licence these tools
do not know, or a location copied from a source that gave none, is reported
as unknown: find out the source's licence and record it on the source, and
the report compares it. A dataset with no licence of its own is not compared
at all, and the report says so.

Each warning says what to do: publish the dataset under a licence compatible
with the source's, remove those attestations (a location can be drawn again
from evidence of your own), or ask the source's holder. Each is a warning,
not a problem, since only you know whether an attestation copied from its
source or only cites it for a fact; and each is a reading of the licences'
terms, "not legal advice".

### The deposit files

**Report** writes a folder (its name ends `-deposit`) of files made from the
dataset's description, for a repository that gives it a DOI. Its
`README.txt` says what to check and fill in before you deposit.

| File | What it is for | Where it goes |
|---|---|---|
| `.zenodo.json` | Zenodo's description of the deposit | At the top of the GitHub repository the dataset is released from, where Zenodo reads it with each release |
| `CITATION.cff` | How to cite the dataset | At the top of the same repository, where GitHub shows *Cite this repository* from it |
| `datacite.json` | DataCite's description, for a repository that registers DOIs itself | Sent to that repository, with the DOI added |

The dataset's licence is given to Zenodo by Zenodo's own id for it (the
Public Domain Mark, for which Zenodo has none, as *Other (Public Domain)*). A
licence these tools do not recognise is left out, for you to choose on the
repository's form, and the report says so.

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

(methodos)=
## Following a workflow: Methodos

**Methodos** is the part of PLATO tools that leads you through a whole
workflow, step by step, with your place kept. It does no work of its own:
each step is one of the tools described above, named with what it does, and
Methodos keeps track of which steps are done. The workflows are named in plain
English; the tools keep their Greek names.

### The three questions

Press **Not sure where to start? Answer three questions**, in the right-hand
column of the page (on a narrow screen, near the top), or choose the
**Methodos** card among the tools. Three questions choose
a workflow:

1. **What do you have?** A list of place names (a spreadsheet or CSV), a text
   that names places, an edition in TEI, annotations from Recogito, a dataset
   already in a PLATO format, a map image, or nothing yet.
2. **What do you want at the end?** Places on a map, each identified in a
   gazetteer; a citable, published dataset; a new version of a published
   dataset, checked; a file in another format; a match of two datasets;
   figures as a Data Cube; or *I am not sure: show me what the tools can do*.
3. **Anything of these?** Only the yes-or-no questions the workflow needs and
   the first two answers left open; and, for a workflow that publishes, or
   that gives regions addresses of their own, the base address they are
   given under (see [below](#methodos-base-address)).

The same answers always give the same workflow. Four workflows exist so far:

| You have | You want | The workflow |
|---|---|---|
| A list of place names | Places on a map, each identified in a gazetteer | [Map your data](#methodos-map-your-data) |
| A list of place names | A citable, published dataset | Map your data, with its publishing steps |
| A dataset already in a PLATO format | A citable, published dataset | [Publish a dataset](#methodos-publish-a-dataset) |
| An edition in TEI | Places on a map, or a citable, published dataset | [Places from an edition (TEI)](#methodos-places-from-tei-or-recogito) |
| Annotations from Recogito | Places on a map, or a citable, published dataset | [Places from Recogito](#methodos-places-from-tei-or-recogito) |

Once the questions are answered, the workflow's steps are listed, with any
steps your answers leave out and, for a workflow that reads an edition or
annotations, what it cannot carry from your files; **Follow** with the
workflow's name begins it. While you follow it, the same list is folded in
the tracker under **What this workflow cannot carry**.
*I am not sure* leads instead to the tools' cards (**Show me the tools**):
each card says what its tool does. Any other answers say that there is no
workflow for this yet, why, and which tools do the work meanwhile, with a
link, **Tell us what you wanted to do** (see [below](#methodos-feedback)).

### The tracker

On a wide screen the main page has three columns: the tools on the left, the
step at hand in the centre, and, on the right, a column that stays in view as
you scroll. A workflow you follow is shown there, under **Your workflow**, as
a list of its steps, each with a checkbox, the tool that does it, and what it
does. A step's box is ticked once the step is done; the step at hand is
marked with a ring; the steps still ahead are greyed until they are reached.
A step the tools cannot do yet has a dashed box, with the reason beside it. It is skipped, not counted among the workflow's steps,
and never refused: the workflow goes on without it, and its end says what was
not done. On a narrower screen the page has two columns, the tools' cards
below the steps; on a narrow one, such as a phone's, a single column, with
the tracker folded into a strip at the top of the window, *Step n of N: …
▾*, that opens to the whole of it. When a [Scope](#scope) is set, it is one
line after the tracker's buttons.

While you follow a workflow, the page's own step numbers are hidden, so that
there is one numbering: the centre is titled with the workflow's, *Step n of
N: …*. The file you choose in *Choose your data* folds to one line, its name
and size, with **Change** to choose another. A step's result stays in view,
labelled *Result of step n: …*, until you act on the next step; it is then
folded into its step's row in the tracker, with **Show its result** to see it
again.

The workflow begins when you choose its file in *Choose your data* (or with
**Choose the file** in the tracker). Steps are of two kinds:

- **Done by the tools.** You run the step's tool on the page, as you would
  without a workflow, and the step is done when the run finishes. The run
  must be on the step's file: a run on another file is not counted, and the
  tracker says which file to choose. A run that finds problems is
  **Stopped**, one that goes wrong **Failed**, and one you stop **Stopped by
  you**; in each case, put it right and run the step again.
- **Yours.** The tracker says what the step waits for (matching the columns,
  deciding on the candidates, drawing in Chora). When you have done it, press
  **This step is done**. Chora's step needs no button: saving there does it
  (see [Map your data](#methodos-map-your-data), step 8).

**Back a step** undoes the last step done, so that it is to do again.
**Leave the workflow** ends it and lets go of everything Methodos kept for it
in this browser. A workflow chosen but not yet begun can be let go with
**Discard this workflow**.

(methodos-map-your-data)=
### Map your data

From a list of place names to places identified in the World Historical
Gazetteer, located, checked and written out, and published if you say so.

**What you need first.** The lookups in the World Historical Gazetteer need an
account of your own with WHG, enrolled in WHG's beta, and a WHG token. That
covers the regions in step 4, the places in step 5, and finding a record whose
location you adopt in Chora. To get the token, sign in at
[whgazetteer.org](https://whgazetteer.org/) with ORCiD, open your **Profile**
and generate an **API Token**. You give the token in the lookup panel (see
[the WHG token](#the-whg-token)). The rest of the workflow needs no account.
A [Scope](#scope), set from the tracker, confines every lookup the workflow
makes.

The questions under 3 are:

- *Does the table say which region each place is in (a parish, a county)?*
- *Will you draw or trace places that the gazetteer cannot locate?*
- *Will you publish the result?* (asked only when you wanted places on a map)
- When the table gives regions, or you will publish, *Under what base address
  will your places, and any regions, have web addresses of their own?* Where
  the table gives regions it is needed, since the regions are given addresses
  under it, so **Follow** waits for it; otherwise it is optional (see
  [the base address](#methodos-base-address)).

The steps, with the tool that does each:

1. **Hermes: Match the columns to PLATO.** Yours: match the table's columns
   to PLATO's fields in the Columns panel (see
   [your own table of places](tables-of-places.md)), then say the step is
   done.
2. **Elenchos: Check the table.** Run the [check](#checking).
3. **Metaphrasis: Make a PLATO dataset of it.** Run the
   [conversion](#converting) to PLATO JSON. Where the table gives regions,
   the conversion uses the base address you gave (it is the one in
   **Options**, *Web address for your identifiers*): the regions are made
   from the table when it is converted, and need it to have addresses of
   their own (see
   [the base address](tables-of-places.md#place-ids-and-the-base-address)).
4. **Krisis: Identify the regions, the widest first.** Only if the table gives
   regions. Yours, in the region review (**Review the regions level by
   level**): the regions are looked up level by level, from the widest, each
   level within the match of the level above. The step is done only when
   every region is settled. The detail of the region review is in
   [reviewing regions, level by level](#region-review).
5. **Krisis: Look the places up in the World Historical Gazetteer.** Where
   the table gives regions, the places are looked up within their regions.
   The workflow's [Scope](#scope), if one is set, applies too: its kinds of
   place, years and sources to every place, and its Where to a place whose
   regions say nothing of where to look. The lookup needs your WHG token and
   your permission (see [reviewing matches](#match-review)).
6. **Krisis: Decide which candidates are the same place.** Yours: review the
   candidates, as in [reviewing matches](#match-review).
7. Recording the decisions, by **Finish** in the review, as one of:
   - **Krisis: Record the decisions in the dataset**, where the table gives
     no regions;
   - **Krisis: Record the decisions, with the region each place is in**,
     where it does. Export the candidates first (**Export the suggestions as
     a candidate set**), so that each identity records the candidate it
     answers (`promotedFrom`). The places stay `ContainedIn` the regions made
     from the table, and each region gets your identification of it with the
     gazetteer's record, as described under
     [what is written](#region-review). If the base address in **Options**
     is no longer the one the review was saved with, **Finish** says so, and
     still writes, for the review's own address: set **Options** back if
     your places keep that address.
8. **Chora: Draw or trace the places still without a location.** Only if you
   said you would. Yours: **Open Chora**, in the tracker or under the step's
   title, opens [Chora](#chora) on the step's dataset, with the workflow
   still beside the map. Draw or trace the places there, or take a location
   from a gazetteer's match (**Adopt**: see
   [adopting a location from a match](#adopting-a-location-from-a-match)),
   and save the dataset. Once the save passes its check, the step is done
   with the file it wrote, which is also chosen in *Choose your data*, and
   Chora says so: **Leave the map** to carry on. A save made from a dataset
   other than the one that went to the step does not do it, and the tracker
   and the save say why. To use a dataset saved some other way, choose it in
   *Choose your data* and press **This step is done**. **This step is done**
   with the dataset that went to Chora, unchanged, is refused, since nothing
   drawn there is in it; if there was nothing to draw, press **Nothing to
   draw: go on with this dataset**.
9. **Elenchos: Check the result.**
10. **Mneme: Compare the result with the dataset made from the table**, as in
    [comparing two versions](#comparing-two-versions).
11. **Metaphrasis: Write it out**, in the format the workflow was given
    (PLATO JSON). The dataset is PLATO JSON by now, and a file is not
    converted into its own format: the step says **Ready to download**, with
    a **Download** button for the file chosen in *Choose your data*, and is done once you
    have downloaded it. A dataset in another format is converted, as any
    step done by the tools.
12. Only if you will publish, the four parts of
    [publishing your dataset](#publishing-your-dataset), by **Agora**:
    **Give every place and source a permanent address**, **Write the FAIR
    report**, **Build the web site** and **Write the permanent-address
    rules**.

(methodos-places-from-tei-or-recogito)=
### Places from an edition (TEI), and Places from Recogito

From the place names of a [TEI edition](tei.md), or the places linked in a
[Recogito export](annotations.md), to places identified in the World
Historical Gazetteer, located, checked and written out, and published if you
say so. Choose the edition, or the export (with the IIIF georeferences of its
maps, and their manifests, if it has regions drawn on maps), in *Choose your
data*. The questions under 3 are Map your data's, less the regions, since
neither an edition nor an export says which region each place is in: *Will
you draw or trace places that the gazetteer cannot locate?*, *Will you
publish the result?* (asked only when you wanted places on a map), and, if
you will publish, the base address, which is optional.

The steps are **Elenchos: Check the edition** (or *the annotations*),
**Metaphrasis: Read its place names into a PLATO dataset** (or *Read the
places they link into a PLATO dataset*), and then Map your data's from step
5, as where the table gives no regions: the lookup, the review, **Record the
decisions in the dataset**, Chora if you said so, the check, the comparison
with the dataset made from the edition (or the annotations), writing it out,
and Agora's four parts if you will publish.

A place's `ref` in the edition, or its link in Recogito, stays its own
address: the lookup looks for it in WHG beside that address, never replaces
it, and flags it when WHG's best candidate is far from it (see
[reviewing matches](#match-review)). Pleiades addresses are read as a
gazetteer's like the others. The tracker lists what each reader cannot carry,
such as a place name with no `ref`, coordinates in a name's own `<geo>`, or a
Recogito region on a map with no georeference.

(methodos-publish-a-dataset)=
### Publish a dataset

For a dataset already in a PLATO format: **Elenchos: Check the dataset**, then
Agora's four parts in order, **Give every place and source a permanent
address**, **Write the FAIR report**, **Build the web site** and **Write the
permanent-address rules** (see [publishing your dataset](#publishing-your-dataset)).
Under 3 it asks only for the base address, which is optional: minting uses it
where the dataset has none of its own (see
[the base address](#methodos-base-address)).

(methodos-base-address)=
### The base address

A workflow that gives places addresses of their own (Map your data when the
table gives regions, and every workflow when you will publish) asks under 3
for the base address they are given under. It is the same question, in the
same field, in every workflow, and optional except where regions need it. The field shows the base address already in **Options**
(*Web address for your identifiers*), and what you type there is written to
**Options** too: there is one base address, used by every tool on the page.

### Saving and resuming

A workflow is kept in this browser at every step: which workflow it is, your
answers, the state of each step, its [Scope](#scope), and references to the
files (each file's name, size and SHA-256). Reload the page, or come back
later, and it is taken up where it was left, with the file the step works on
chosen again in *Choose your data* for you, from what is kept (below). A
workflow chosen before any file is kept too.

Where that file is not kept, the step asks for it to be chosen again in
*Choose your data* (in Chromium, a button **Open** *the file's name*
**again** opens it in one click). The file is checked to be the one the
workflow recorded: a different file is refused, with what differs, and is
not counted. A page closed while a step was running leaves that step failed,
to run again.

If the workflow's recipe has changed since it was saved, the tracker says
so. A change of words only carries on. Otherwise it stays at its last
finished step, and you can **Start the remaining steps under the new
recipe**, or leave it.

### Carrying a workflow elsewhere: the project file

A workflow can be saved whole as one file, a project (ending `.platoproj`),
to carry on in another browser or on another computer, or to give to a
colleague. Under **Save or open the project** in the tracker, **Save the
project** writes the workflow with your answers and its Scope, the files its
steps made, the review open with its decisions, and your own starting file
unless you untick **Put my own file in it**. A file this browser no longer
keeps is left out, and the page names it. Whoever opens the project then
chooses it again where a step needs it. A project never holds your WHG token
or any other key, the permissions you gave, or your other workflows. If any
part of it, your own file included, contains the token or a key this page
knows, the project is not saved. The reviewer's name is in it only where a
review records who decided. Keep it as you would your data.

**Open a project**, in the tracker, or *open a project saved before* at the
top of the page, reads one back. Every part is checked against its size and
SHA-256 before the workflow is taken up at its step, with the review
reopened. Opening a project runs no step and sends nothing anywhere. If a
workflow is already open, the page asks before letting it go. A project whose
files will not fit in the room the browser allows is refused before anything
is written. A project saved by a newer PLATO tools opens with a note that
what the newer version added is not read.

From the command line,
`npx github:pelagios/plato-tools project info my-workflow.platoproj` lists
what a project holds and checks every part, without opening it.

### What is kept in the browser, and clearing it

- **The workflow's record**, with its Scope, in the browser's IndexedDB.
- **A copy of the file you began it with, and the files the steps made**
  (the matching of the columns, the dataset, the review's work file), in the
  browser's private file storage (OPFS), so that after a reload the next
  step takes them without their being chosen again; and,
  where the browser allows, a link to the file you began with. The tracker
  says what is kept and its size, beside **Clear them**. Once cleared, a
  step that takes one asks for it to be chosen. **Clear them** lets go of
  [the kept file](#the-kept-file) too.

None of it leaves your computer, but like everything PLATO tools keeps in
this browser it can be read by other pelagios.org pages on this computer (see
[who sees what](#which-map-and-who-sees-what)). To keep nothing between
visits, turn off **Keep my working data between visits** under *Your working
data* in the **Permissions** panel: the workflow and its files then last only
as long as the tab, and what was kept is cleared at once. **Leave the workflow** lets go
of everything kept for that workflow. A browser that refuses storage (a
private window, say) keeps the workflow for the tab only.

(methodos-feedback)=
### A workflow that is not there

When your answers lead to no workflow, **Tell us what you wanted to do** opens
a new issue on [PLATO tools' GitHub](https://github.com/pelagios/plato-tools/issues),
in a new tab, labelled *Methodos* and titled with your two answers. Nothing
else is put in it: say there what you were trying to do.
