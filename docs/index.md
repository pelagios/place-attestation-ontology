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
what sources say about places, and organising your data in its shape gives
you three things.

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

  Its **Map your Data** tool, now in beta testing and reached from the WHG
  site, *reconciles* your places with established reference gazetteers such
  as Pleiades, GeoNames and Wikidata: it finds the record for the same place,
  so that you can take its coordinates where yours have none. It reads many
  formats, PLATO's among them, and runs entirely in your browser without
  uploading anything to WHG. You can use it whether or not you contribute
  to WHG.
  :::

**Nothing is flattened.**
: Every statement keeps its source and its date, so your data can sit
  alongside other people's evidence about the same places without either
  overwriting the other, and a reader can always ask *who says so, and when?*

This guide shows how to put your data into that shape. You do not need to
know anything about ontologies, JSON or linked data: if you can fill in a
spreadsheet, you can use PLATO.

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

**I want to check a file, or convert it to another format.**
: Use [PLATO tools](https://pelagios.org/plato-tools/): drop the file on the page. It runs in your
  browser, so nothing is uploaded, and it works at any size. To check many
  files at once, it also runs [from the command line](https://github.com/pelagios/plato-tools#from-the-command-line).

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
:caption: Getting started

ideas
spreadsheets/index
spreadsheets/first-dataset
spreadsheets/survey-example
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
