# Place names in a TEI edition

If you have edited a text in [TEI](https://tei-c.org/) XML, EpiDoc included,
and pointed the place names in it at a gazetteer, you have already recorded
evidence in PLATO's shape. A place name such as

```xml
<placeName ref="https://pleiades.stoa.org/places/579885">Athenae</placeName>
```

says: *this edition, at this point, names this place, in these words*. That
is an attestation.

[PLATO tools](https://pelagios.org/plato-tools/) turns a TEI edition into a
PLATO dataset, which you can then check, convert to the spreadsheet tables or
to Linked Places Format, and add to. It reads TEI; it does not write it.

## How to do it

1. Save your edition as UTF-8, which is the usual encoding for TEI. A file
   that says it is in another encoding is refused, rather than read with its
   letters wrong.
2. Open [PLATO tools](https://pelagios.org/plato-tools/), drop the file on
   it, and choose **Convert**, with the format you want. It also runs
   [from the command line](https://github.com/pelagios/plato-tools#from-the-command-line),
   for many editions at a time.
3. Read the report. It lists everything that was not carried over, and why.

Nothing leaves your computer: PLATO tools works entirely in your browser.

**Entities.** An entity such as `&nbsp;` is read when the file's own DOCTYPE
declares it with its text, as in `<!DOCTYPE TEI [<!ENTITY nbsp "&#160;">]>`.
An entity the file does not declare, or one whose declared text holds markup,
cannot be read yet, and stops the file where it is used. An entity declared
as another file (with `SYSTEM` or `PUBLIC`, as from an external DTD) is never
fetched or read, for safety: a file that uses one is refused, and the message
names it. Write the character itself, or declare the entity with its text.

## What each part of the edition becomes

PLATO tools reads the place names in the `<text>` of the edition. Each place
name whose `ref` points to a place becomes one attestation about that place.

| In the TEI edition | In PLATO |
|---|---|
| A `<placeName>`, `<settlement>`, `<region>`, `<country>`, `<bloc>`, `<district>` or `<geogName>`, or an `<rs>` or `<name>` with `type="place"` | One attestation for each place its `ref` points to |
| The place its `ref` points to: a web address, directly or through the header's `<prefixDef>` or a `<listPlace>` (see below) | What the attestation is **about** |
| The words inside the element, with notes inside it left out and a word broken over a line (`break="no"`) joined up | The **name** the source uses, recorded as attested |
| In a `<choice>`, the regularised, expanded or corrected form; in an `<app>`, the lemma | The **name** |
| The form as the original has it, where a `<choice>` changed it (`orig`, `abbr`, `sic`) | The name's **source label**: the source's own wording |
| A place name wholly inside an `<rdg>`, or in the part of a `<choice>` not taken | Nothing: a variant reading (see [below](#variant-readings)) |
| The nearest `xml:lang`, on the element or around it | The name's **language** |
| The edition itself, as its `teiHeader` describes it: title, author or editor, publisher, date, licence, and its web address or DOI | The **source** |
| The original the edition was made from (the `sourceDesc`'s bibliographic description, or a manuscript's or inscribed object's identifier) | The source it is **derived from** |
| Where in the edition: divisions, milestones, pages, lines, a note, the element's `xml:id` | The citation's **locator**, in words ("book 2, chapter 1, section 1, page 12", "line 6", "in a note") |
| A `key` | The attestation's **notes** ("Key: …") |

Place names in notes, commentary and translations are read too: the source is
the edition, and the locator says where in it the words stand.

The dataset is called "Place names in" followed by the edition's main title.

The full mapping, element by element, for developers, is beside PLATO tools'
[TEI test files](https://github.com/pelagios/plato-tools/blob/main/test/fixtures/tei/README.md#the-mapping).

## Where a ref can point

PLATO identifies places by their web addresses, so every place name must lead
to one.

**A web address.** `ref="https://pleiades.stoa.org/places/579885"` is used as
it is. A `ref` with several addresses, separated by spaces, gives one
attestation for each, with a note naming them all, and the report warns you.
That the addresses may be the same place in two gazetteers is not recorded:
PLATO says that with an identity match, not with a place name.

**A prefixed pointer.** `ref="pl:579885"` is expanded through a `<prefixDef>`
in the header, such as

```xml
<prefixDef ident="pl" matchPattern="([0-9]+)"
           replacementPattern="https://pleiades.stoa.org/places/$1"/>
```

The pattern must match everything after the prefix. A prefix with no
`<prefixDef>`, or one that expands to something other than a web address
(such as a `urn:`), is reported and not converted.

**A place in a list of places.** `ref="#athens"` points to
`<place xml:id="athens">` in a `<listPlace>` in the same file, in the header
or in the text. PLATO tools takes that place's web address from its `<idno>`:

- one web address: the attestation is about it;
- several different web addresses: which one is meant cannot be told, so the
  place name is reported as ambiguous and nothing is converted from it;
- none, or no place with that `xml:id`: reported, and not converted.

A list of places later in the file than the place name, such as one in
`<back>`, is waited for.

The list's own description of each place, its names and its location (its
coordinates), is not converted, for now. It is the edition's description of the
place, not a passage of the text that names it: converting it raises the
question of whom such an attestation cites (the edition, or its editors), which
is still to be decided. Meanwhile the place's web address leads to the
gazetteer's own names and coordinates. The report names what was left out,
once for each place. A `<desc>`, a `<note>` or an `<idno>` that is not a web
address is reported in the same way.

**Anything else.** A `ref` into another file (`places.xml#delphi`), a `urn:`,
or a single word cannot be followed from here, and is reported.

## World Historical Gazetteer addresses

Addresses of the [World Historical Gazetteer](https://whgazetteer.org) (WHG)
come in several forms, and PLATO tools writes them in the one form that will
keep working, `https://w3id.org/whg/id/place:…`, with a note giving the form
the edition used:

- a reconciliation id, such as `place:gn:2988507` (when no `<prefixDef>`
  declares the prefix `place`; one that does is used instead);
- an entity page, such as `https://whgazetteer.org/entity/place:gn:2995469/api`.

This holds wherever the address is found: in a `ref`, from a `<prefixDef>`,
or in a list of places' `<idno>`. Two kinds of address are refused, and the
report says so:

- an address of the form `https://whgazetteer.org/places/<number>/portal/` with
  a number below 12,345,678, which names one of WHG's database records rather
  than a place, and which WHG answers with the wrong place or an error;
- an address on `dev.whgazetteer.org`, WHG's staging copy, which changes
  without notice.

A `/portal/` address with a larger number names one of WHG's place clusters,
and is kept as it is.

## Variant readings

The edition's text at any point is its lemma or its edited form, so a place
name wholly inside an `<rdg>`, or in the part of a `<choice>` that is not
taken (an `orig`, `abbr` or `sic` beside a `reg`, `expan` or `corr`), is not
an attestation: a variant is not what the text says. The report lists each,
with its words and its line. A `<choice>` with only one part takes that part.

Where both parts of a `<choice>` hold a place name with the same `ref`, such as

```xml
<choice>
  <orig><placeName ref="https://pleiades.stoa.org/places/579885">Athenas</placeName></orig>
  <reg><placeName ref="https://pleiades.stoa.org/places/579885">Athenae</placeName></reg>
</choice>
```

there is one attestation, not two: its name is the part taken ("Athenae"), and
its source label the part as printed ("Athenas"). Nothing is reported.

## What is left out, and why

**Place names with no ref.** A place name that points to no place has nothing
for an attestation to be about. The report lists each, with its key if it has
one. Give it a `ref` to keep it.

**Place names outside the text.** A place name in the `teiHeader`, such as
where an inscription was found, or in a `<standOff>` or `<facsimile>`, is the
edition's description of the document, not a name the text attests. It is
reported, not converted.

**Variant readings.** A place name in an `<rdg>`, or in the part of a
`<choice>` not taken, is listed and not converted: see
[Variant readings](#variant-readings).

**Attributes PLATO has no place for.** `cert`, `resp`, and `type` on a
`<placeName>` are reported, once for each attribute and value. TEI's `cert`
does not say what it is certain of (the reading, or which place is meant), so
it is not taken for the certainty of the attestation.

**A language that is not a language code.** `xml:lang="grc"` is carried;
`xml:lang="Latin"` is reported, and the name converted without a language.

**A licence in words only.** The edition's licence is carried only when it
has a web address (a `<licence target="…">`).

**Further originals.** Where the `sourceDesc` names several originals, only
the first is carried; the others are reported.

**The rest of the header.** Who encoded the file, its revision history and its
taxonomies describe the file, not the edition as a source, and are not read.

If the edition has no web address in its header (an `<idno type="URI">` or
`type="DOI"` in the `publicationStmt`), the report warns you: the source is
then known only by its title. Give it an address, so that the attestations can
be traced to it.

## Identifiers

Each attestation's notes say where it came from ("From TEI element
`<placeName>` on line 32 of …"), so you can always find your way back to
the edition. An element's `xml:id` is given there and in the locator, but is
not used as the attestation's own identifier: an edition can be revised under
the same ids, but an attestation in a published dataset must never change. See
[PLATO and FAIR data](index.md#plato-and-fair-data).

The edition names each place but does not give it a label, so when the
attestations are gathered by place, the report warns that each place's
address is used as its label.

## An example

This passage is from a small edition made up for PLATO tools' tests:

```xml
<div type="book" n="2">
  <div type="chapter" n="1">
    <pb n="12"/>
    <p>
      <milestone unit="section" n="1"/>The land of
      <placeName ref="https://pleiades.stoa.org/places/570182"
                 key="corinth">Corinth<note>The city, not the gulf.</note></placeName>
      is a part of the Argive land.
```

The edition's header gives its title, *A Journey through Achaia*, an author,
a publisher, a date, a DOI and a CC BY licence, and in its `sourceDesc` the
text it was made from. The place name becomes one attestation:

- **about** `https://pleiades.stoa.org/places/570182`;
- **name** "Corinth", attested, in English (the edition's `xml:lang="en"`),
  without the words of the note inside it;
- **source** *A Journey through Achaia*, with its DOI as its address, its
  licence, a citation built from the header, and derived from *Pausanias,
  Description of Greece, book 2 (Teubner, 1903)*;
- **locator** "book 2, chapter 1, section 1, page 12";
- **notes** "Key: corinth" and where in the file the place name stands.

A second place name in the same passage, `<placeName ref="… …">Kenchreai</placeName>`
with two addresses, becomes two attestations and a warning; a third,
`<placeName>Lechaeum</placeName>`, has no `ref`, and the report lists it.
