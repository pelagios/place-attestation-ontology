# The ideas in five minutes

PLATO rests on one idea: **what we know about a place is a collection of
statements made by sources, and each statement should keep its source and its
date.** Everything else follows from that.

## An example

A customs account of 1480 to 1485, now in The National Archives (UK), mentions a
port it spells *Bristowe*. In PLATO that is recorded as one **attestation**:

```{figure} _static/attestation.svg
:class: plato-figure
:alt: An attestation links the place Bristol to the name Bristowe, the dates 1480 to 1485, and the source TNA E 122/19/10.

One attestation: this source, for these dates, gives this name for this place.
```

An attestation is a single piece of evidence: *this source says that this
place had this name at this time*. Another source might give *Bristoll* in
1540, and a gazetteer might give modern coordinates. Each of those is another
attestation about the same place. None of them overwrites the others.

## Places

The thing the attestations are about is, most of the time, what anyone would
call a place: a town, a parish, a river, a region. PLATO's own word for it is
**SpatialEntity**, because not everything a gazetteer records is what everyone
would call a place (a road, a trade route, the region a historical period
applies to), and because "place" means rather different things in different
languages and disciplines. PLATO does not give the word "place" any special
meaning of its own.

In the spreadsheets the first sheet is called **places**, because that is what
most people expect. Each row in it becomes a SpatialEntity.

A place in PLATO has very little of its own: an identifier and a label to list
it under. Its names, locations and types all come from attestations, because
all of them can change over time and all of them depend on a source.

## Sources and where in them

Every attestation names its **source**: a document, a map, a book, a dataset.
You list each source once, in the sources sheet, and refer to it from as many
rows as you need.

If you want to say *where* in the source the evidence is, such as a page, a
folio or an entry number, that goes in the row's **locator**, not in the
source. One book cited at twenty different pages is still one source.

A source can also be a copy of another. A charter known only from a later
cartulary is two sources, each with its own date, one derived from the other.
Your attestation cites the one you actually read.

## Dates

Every attestation has a **date**: the date the statement applies to, written
as the source gives it ("1086", "c. 925", "1480–1485", "a. 1300"), or
"undated". If you can, you also give the earliest and latest years it could
mean, in **from** and **to**. That way the original wording is kept and
computers can still sort and compare.

The date of the statement is not the same as the date of the source. An annal
for the year 921 read in a manuscript written around 925 is dated 921; the
manuscript's own date, c. 925, belongs to the source.

## How sure, and what kind of evidence

You can say how **certain** you are of a row, from 0 (not at all) to 1
(certain). That is about the evidence: better evidence could change it.

Some evidence is certain but of a weaker kind. A place-name found only inside
a person's name (*Willelmus de Bonestou*) proves the name existed, but not
that anyone was using it for the place. PLATO lets you mark such cases rather
than lowering your certainty, so that the reason is kept.

## Why this way

Because every statement keeps its source and date, datasets from
different projects can be combined without anyone's evidence being flattened
into someone else's. A user can always ask *who says so, and when?* And
because a place's names and locations are evidence rather than fixed
properties, disagreements between sources can be recorded instead of resolved
by deletion.

Next: [Organising data in spreadsheets](spreadsheets/index.md).
