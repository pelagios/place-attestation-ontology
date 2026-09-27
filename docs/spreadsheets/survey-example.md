# A place-name survey example

Place-name surveys, cartularies and editions record things a simple list of
places does not: when a manuscript was copied, where on the page a form is
found, whether a form is a reading or an editor's choice. This example shows
how the spreadsheets hold them. It is loosely based on the English Place-Name
Society's surveys; the sources and readings are illustrative, so check an
edition before citing any of them.

{download}`Download the example as CSV files <../_generated/downloads/plato-tables-example-survey.zip>`.

## The sources, and a manuscript copied later

```{include} ../_generated/examples/survey/sources.md
```

Look at the first two rows. The survey's notation "921 (c. 925) ASC (A)"
means an annal for the year 921, read in the A manuscript of the
Anglo-Saxon Chronicle, which was written about 925. That is two sources: the
annal, and the manuscript, which is `derived_from` it and has its own date,
c. 925, with `from` 0915 and `to` 0935. A manuscript's sigil ("A") is simply
its title.

## The names

```{include} ../_generated/examples/survey/names.md
```

Row by row:

- **Grantanbrycg**, dated 921 (the year of the annal) and sourced to the
  manuscript it was read in. The manuscript's date lives on its source row, so
  the two dates never get confused.
- **Bonestou** in Domesday Book, found three times in the passage cited:
  `occurrence_count` 3, the surveys' "(3 X)".
- **Bonestou** again, but only inside a man's name, *Willelmus de Bonestou*:
  `occurrence_context` is `InPersonalName`, the surveys' "(p)". This is
  certain as evidence, so `certainty` stays 1; what differs is the kind of
  evidence, and that is what the column records.
- **Bonestou** in 1254, where the survey gave the source as "ib." and an editor
  worked out that the Close Rolls were meant: `attribution` is `Inferred`. The
  `locator` gives the volume and page.
- **Bunstow(e)**, an ordinary reading, with the edition's brackets kept.
- **Bunsty Hundred**, the form the survey files the entry under:
  `form_status` is `Headword`. It is an editor's decision, not a reading, so
  it is dated to the survey and sourced to it.
- **Bunstowe**, a spelling made up for searching, attested by no source:
  `form_status` is `Normalised`, sourced to the project that made it.

Someone computing "the earliest spelling" or "how many independent spellings"
can now leave out the headword, the search form and the personal name without
having to know the survey's conventions.

## Types and relations

```{include} ../_generated/examples/survey/types.md
```

```{include} ../_generated/examples/survey/relations.md
```

The relation says that Domesday Book, in 1086, places the hundred within
Buckinghamshire. It gives `from` but no `to`, because the source says nothing
about when that stopped being true. Both places must be in the places sheet:

```{include} ../_generated/examples/survey/places.md
```

## What the spreadsheets could not hold here

The surveys also write runs such as "1252 Cl *et passim* to 1346 Harl": one
spelling attested continuously between two sources. That is a single piece of
evidence resting on two sources, which a spreadsheet row cannot express; the
[JSON format](../json.md) can.
