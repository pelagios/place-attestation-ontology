# PLATO: a guide to organising data about places

```{image} _static/plato-thinking.png
:alt: A line drawing of the philosopher Plato, chin in hand, thinking about a network of linked data: Wikidata, GeoNames, the Getty AAT, PeriodO and linked open data.
:class: plato-hero
```

## Why PLATO

Research on historical places produces a great deal of evidence: names read
in documents, positions taken from maps, statements about what kind of place
something was and what it belonged to. That evidence is usually kept in
whatever shape one project needed at the time, which makes it hard to reuse,
to combine with other projects' work, or to hand on to others.

PLATO, the **PL**ace **AT**testation **O**ntology, gives that evidence a
shape. It is a published standard for recording
what sources say about places, designed so that data in its shape can meet the
[FAIR principles](#plato-and-fair-data), and organising your data in its shape
gives you three things.

**A structure to think with.**
: PLATO asks the same few questions of every piece of data: *what is it
  about, what does it say, which source says so, and when does it apply?*
  Answering them is often the most useful step in organising a dataset,
  because it separates what your sources say from your own interpretation of
  them, and shows where your evidence is thin.

  It also leaves room for what historical evidence is really like. Sources
  that disagree are recorded side by side, and nothing forces you to choose
  between them; a scholar's judgement that one statement contradicts,
  supports or supersedes another can be recorded as evidence in its own
  right. And PLATO keeps apart the different ways of not knowing, rather
  than collapsing them all into "uncertain":

  - how sure you are of a statement, which better evidence could change;
  - how firmly the source itself says it: a claim it only reports ("it is
    said"), hedges, or raises and leaves undecided;
  - a date known only within limits, or given only as "c. 925" or "before
    1300";
  - a place with no sharp edge, such as "the Levant", which no evidence will
    make crisp;
  - a location given only relative to somewhere else, such as "two leagues
    north of the ford";
  - evidence that is certain but weaker in kind, such as a name found only
    inside a person's name;
  - a reference an editor has had to work out from "ibid.";
  - a form read from a damaged or misread document, judged for how well it
    was read;
  - a mention that could be one of two places, recorded as alternatives, at
    most one of them right, rather than as two separate claims;
  - a match with a record elsewhere that is close, but perhaps not exact.

  A source can also say that something was *not* so, such as "no market
  here", and that is recorded as a denial, not left out.

**Ready for other systems.**
: Data in PLATO's shape can be read by any software that implements the PLATO
  standard, without a conversion written for your project alone. You do not
  need to know in advance which systems those will be.

  :::{admonition} The World Historical Gazetteer
  :class: tip

  The [World Historical Gazetteer](https://whgazetteer.org) (WHG) is moving
  towards implementing PLATO, so that data organised this way can more easily
  be welcomed there.

  Its *Map your Data* tool, in beta testing and reached from the WHG site,
  *reconciles* your places with established reference gazetteers such as
  Pleiades, GeoNames and Wikidata: it finds the record for the same place,
  so that you can take its coordinates where yours have none. *Map your
  Data* is now migrating out of WHG and into [PLATO tools](https://pelagios.org/plato-tools/),
  where it becomes the first guided workflow in
  {ref}`Methodos <methodos>`: the regions your places lie in are matched
  level by level, then the places themselves, and each place is located from
  its match or drawn, including over a georeferenced historical map, before
  the result is checked and written out in PLATO. Like the rest of PLATO
  tools it is experimental, runs entirely in your browser without uploading
  anything to WHG, and can be used whether or not you contribute to WHG.
  :::

**Nothing is flattened.**
: Every statement keeps its source and its date, so your data can sit
  alongside other people's evidence about the same places without either
  overwriting the other, and a reader can always ask *who says so, and when?*

This guide shows how to put your data into that shape. You do not need to
know anything about ontologies, JSON or linked data: if you can fill in a
spreadsheet, you can use PLATO.

## PLATO and FAIR data

The [FAIR principles](https://www.gofair.foundation/fair-principles) ask that
research data be **Findable, Accessible, Interoperable and Reusable**, by
people and by software. Funders and repositories increasingly expect them.
PLATO is built to help, and here is how, principle by principle.

**Findable.**
: Every place, source and statement in PLATO's shape can have a permanent
  web address of its own, so it can be found, cited and linked to. PLATO
  itself has one, `https://w3id.org/plato`, and each release is archived on
  Zenodo with its own DOI.

**Accessible.**
: PLATO's definitions are openly licensed (CC BY 4.0) and published at that
  address in the standard formats software asks for. Data in PLATO's shape
  is plain spreadsheet tables, JSON or linked data: open formats that anyone
  can read without special software, and that
  [PLATO tools](https://pelagios.org/plato-tools/) checks and converts.

**Interoperable.**
: PLATO is a formal standard (an OWL ontology) built on widely used
  vocabularies, among them PROV for provenance, DCAT for datasets, SKOS for
  vocabularies and CiTO for citations. Your places can be matched to shared
  gazetteers such as Pleiades, GeoNames and Wikidata, so your data joins
  up with other people's.

**Reusable.**
: Every statement keeps its source, its date, how sure anyone is of it, and
  how firmly the source itself says it. That is the provenance someone else
  needs before they can trust and reuse your data. A licence can be stated
  for the dataset and for each source.

PLATO gives the structure; a few steps remain yours when you publish:

- **choose a licence** for your dataset and state it;
- **give it permanent addresses**, under a base you control and will keep,
  such as your own w3id address or a DOI, not a temporary one;
- **deposit it** in a repository that gives it a DOI, such as Zenodo;
- **describe it**: a title, who made it, and what it covers.

In the spreadsheets, the licence, the base of your addresses and the
description all go in one place, the [about sheet](spreadsheets/first-dataset.md#7-say-what-the-dataset-is);
in JSON, in the document's `gazetteer` header.

Taken together, those steps and PLATO's structure make a dataset FAIR.
[PLATO tools](tools.md#publishing-your-dataset) reports what your description
still lacks, writes the files a repository needs, and makes a website and
permanent addresses for your places.

## Where to start

**I have a list of places, or notes about places, to organise.**
: Read [Organising data in spreadsheets](spreadsheets/index.md), then follow
  [a first dataset](spreadsheets/first-dataset.md) step by step.

**I want to understand the ideas first.**
: [The ideas in five minutes](ideas.md) explains places, attestations,
  sources and dates with one example.

**My sources are philological or archival, with copies, editions and "ibid."**
: The [place-name survey example](spreadsheets/survey-example.md) shows how
  to record manuscripts copied later, names found only inside personal names,
  editorial headwords and inferred references.

**I have annotated texts or maps in Recogito.**
: [Annotations from Recogito](annotations.md) shows how the places you linked
  become a PLATO dataset.

**My data is a road, a journey, or a network of rivers or letters.**
: See [Routes, journeys and networks](routes/index.md), with four worked
  examples.

**I want to check a file, or convert it to another format.**
: Use [PLATO tools](https://pelagios.org/plato-tools/): drop the file on the page, and see
  [checking, converting and comparing](tools.md) for what it tells you. It runs in your
  browser, so nothing is uploaded, and it works at any size. To check many
  files at once, it also runs [from the command line](https://github.com/pelagios/plato-tools#from-the-command-line).

**My dataset is ready, and I want to publish it.**
: See [publishing your dataset](tools.md#publishing-your-dataset): a report
  on what its description lacks, the files for depositing it, a website for
  every place, and permanent addresses.

**I produce data with my own software, or work with RDF.**
: See [JSON formats](json.md) and [Linked data](linked-data.md).

**My sources are statistical tables: census volumes, returns.**
: See [Statistical tables](statistics.md).

**I have met a word I do not know.**
: The [glossary](glossary.md) explains the terms used in this guide.

PLATO is developed by the Pelagios Network's Place Working Group and the World
Historical Gazetteer. The formal definition of every term is in the
[ontology reference](https://pelagios.org/place-attestation-ontology/); this
guide is the friendlier way in.

```{toctree}
:hidden:

Why PLATO <self>
PLATO tools <https://pelagios.org/plato-tools/>
```

```{toctree}
:hidden:
:caption: Getting started

ideas
spreadsheets/index
spreadsheets/first-dataset
spreadsheets/survey-example
annotations
tei
tables-of-places
tools
```

```{toctree}
:hidden:
:caption: Routes, journeys and networks

routes/index
routes/antonine
routes/king-john
routes/river-idle
routes/datini
```

```{toctree}
:hidden:
:caption: Reference

spreadsheets/reference
vocabularies
glossary
```

```{toctree}
:hidden:
:caption: For developers

json
statistics
linked-data
```

```{toctree}
:hidden:
:caption: About

about
```
