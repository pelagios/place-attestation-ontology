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
3. If you want more than the place names of the text, choose it in
   **Reading options** (see [below](#reading-options)) before you convert.
4. To see what the first place names will become before you convert a long
   edition, choose **Preview the first 10 records**. It writes nothing: see
   [Previewing the first records](tables-of-places.md#previewing-the-first-records).
5. Read the report. It lists everything that was not carried over, and why.

Nothing leaves your computer: PLATO tools works entirely in your browser.

PLATO tools reads TEI P5, EpiDoc included, and the older TEI P4, such as the
Perseus Digital Library's texts: see [TEI P4](#tei-p4). An entity such as
`&nbsp;` is read when the file declares it, and in some files from the
standard table of character entities: see [Entities](#entities).

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
| A `key`, beside a `ref` | The attestation's **notes** ("Key: …") |
| A `key` with no `ref` | With a pattern you give, what the attestation is **about** (see [Keys](#keys-in-place-of-refs)) |

In an edition with a `<div type="edition">`, the commentary, translation and
notes are the editors' words, and are not converted unless you ask for them:
see [Whose words](#whose-words-the-editors-parts). In an edition without one,
place names in notes, commentary and translations are read too: the source is
the edition, and the locator says where in it the words stand.

The dataset is called "Place names in" followed by the edition's main title.

The full mapping, element by element, for developers, is beside PLATO tools'
[TEI test files](https://github.com/pelagios/plato-tools/blob/main/test/fixtures/tei/README.md#the-mapping).

## Where a ref can point

PLATO identifies places by their web addresses, so every place name must lead
to one.

**A web address.** `ref="https://pleiades.stoa.org/places/579885"` is used as
it is, except that an address of Pleiades, GeoNames or Wikidata is written in
the one form its gazetteer gives it (see
[Gazetteer addresses in one form](#gazetteer-addresses-in-one-form)). A `ref` with several addresses, separated by spaces, gives one
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
coordinates), is not converted unless you ask for it. It is the edition's
description of the place, not a passage of the text that names it, and the
place's web address already leads to the gazetteer's own names and
coordinates. The report names what was left out, once for each place, and
says how to convert it: see [The list of places](#the-list-of-places). A
`<desc>`, a `<note>` or an `<idno>` that is not a web address is reported in
the same way, and is never converted.

**Anything else.** A `ref` into another file (`places.xml#delphi`), a `urn:`,
or a single word cannot be followed from here, and is reported.

## Gazetteer addresses in one form

The same place can be written in several ways. Pleiades' Athens is
`https://pleiades.stoa.org/places/579885`, but older tools write
`http://pleiades.stoa.org/places/579885`, and some add a closing `/`. To a
computer these are different addresses, so one place would become two, and
nothing would join the evidence about it. PLATO tools therefore writes each
address of Pleiades, GeoNames and Wikidata in the one form that gazetteer
itself gives as its place's address:

| Written in the source as | Carried as | Rule |
|---|---|---|
| `http://pleiades.stoa.org/places/579885` | `https://pleiades.stoa.org/places/579885` | `pleiades-https` |
| `https://pleiades.stoa.org/places/579885/` | `https://pleiades.stoa.org/places/579885` | `pleiades-slash` |
| A GeoNames page, such as `https://www.geonames.org/2523083/siracusa.html` | `https://sws.geonames.org/2523083/` | `geonames-page` |
| `https://sws.geonames.org/2523083`, without its closing `/` | `https://sws.geonames.org/2523083/` | `geonames-https` |
| `http://sws.geonames.org/2523083`, with or without its closing `/` | `https://sws.geonames.org/2523083/` | `geonames-sws-https` |
| A Wikidata page, such as `https://www.wikidata.org/wiki/Q1524` | `http://www.wikidata.org/entity/Q1524` | `wikidata-page` |
| `https://www.wikidata.org/entity/Q1524`, or the same without `www.` | `http://www.wikidata.org/entity/Q1524` | `wikidata-https` |

GeoNames' form keeps its closing `/`, and Wikidata's is `http`, not `https`:
in each case it is the address the gazetteer's own linked data uses. An
address already in its gazetteer's form, or of another gazetteer, is carried
as it is written, except the World Historical Gazetteer's
([below](#world-historical-gazetteer-addresses)).

Each attestation whose address was rewritten says so in its notes, with what
the edition wrote and the rule that changed it:

```text
Place address given as http://pleiades.stoa.org/places/462503 (rule pleiades-https, hermes-addresses 1)
```

`hermes-addresses 1` is the version of the rules. If a rule is ever changed or
added, the version changes with it, so you can always tell which rules a
conversion followed. If you compare a new conversion with one made before
these rules, [the version check](tools.md#comparing-two-versions) will show
the rewritten attestations as changed; their notes say why. The rules are
listed for developers in PLATO tools'
[DEVELOPERS.md](https://github.com/pelagios/plato-tools/blob/main/DEVELOPERS.md#address-rules-hermes-addresses-1-2026-10-01).

Because both forms become one, a `ref` that gives both the `http` and the
`https` form of one Pleiades address gives one attestation, not two, and no
warning.

**Parts of a Pleiades record are left as they are.** An address that names
part of a place's record in Pleiades, a location or a name
(`https://pleiades.stoa.org/places/579885/athenae`) or a format
(`…/579885/json`), is not the place itself, so it is not changed to the
place's address: it is carried as written, and the report asks you to check
that it is the place you mean. An address ending `#this`
(`https://pleiades.stoa.org/places/579885#this`) is the place, as Pleiades'
own data names it, but it is a different address from the plain one, and it
too is carried as written and reported, rather than changed silently. In
the output it is then a place of its own, apart from the plain address: if you
mean the same place, write the plain address in the edition.

The same rules apply in every reader: to
[annotations from Recogito](annotations.md) and to
[your own table of places](tables-of-places.md) as well.

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

## Reading options

By default PLATO tools converts only what the edited text attests: the place
names of the text that point to a place. An edition holds more, and four
reading options convert more of it. Each is off until you choose it.

| Reading option | On the page | On the command line |
|---|---|---|
| Place names in the editors' parts: commentary, translation, apparatus, notes | *Read place names in the commentary and notes, as the editors' words* | `--commentary-places` |
| The list of places: each place's first name, and its coordinates on the edition's own site | *Read the list of places, each place's first name as its headword* | `--list-places` |
| Places in the header: where the object was found, and where it was made | *Read the places in the header (found at, made at), as the editors' words* | `--header-places` |
| Keys: a place's address made from its `key`, where it has no `ref` | A row for each prefix of the keys, under *Keys with no web address* | `--key-pattern PREFIX=PATTERN` |

**On the page**, once you have chosen a TEI file, the options are under
**Reading options**, above the **Check** and **Convert** buttons; the table of
keys is shown only when the file has place names with a key and no `ref`.
**On the command line**, give the flags to `check` or `convert`, as in

```text
plato-tools convert --to plato-jsonl --list-places --commentary-places edition.xml
```

A flag for something the input is not (`--list-places` with no TEI edition
among the inputs) is refused, with the reason, and nothing is read.

Each option's report entry, when the option is off, says what it would
convert and how to choose it, so the report of a first conversion tells you
which options are worth a look.

### Whose words: the editors' parts

An EpiDoc edition usually puts the edited text in a `<div type="edition">`,
and the editors' own writing beside it: an apparatus, a translation, a
commentary, a bibliography. A place name in the commentary is evidence of
what the editors think, not of what the inscription says, and PLATO keeps the
two apart.

So, **when the file has a `<div type="edition">`**, every other top-level
division (a commentary, translation, apparatus, bibliography or introduction,
or a division with no type, before the edition or after it), and every
`<note>` anywhere, is the editors' words. The divisions inside the edition
(its `textpart`s) are the edition. **A file with no edition division** is
read as before: its notes, commentary and translations are the edition's
text.

By default, a place name in the editors' words is not converted. The report
lists each, with the part it is in, its words, its `ref` and its line. With
the reading option, it becomes an attestation like any other, except that:

- its name has the form status [*Editorial*](glossary.md), not *Attested*:
  the editors wrote it, the source did not;
- its locator begins with the part, such as "commentary";
- its notes say "The editors' words, not the source's."

To know whether the file has an edition division, PLATO tools may have to
hold back the place names it meets before one. It holds up to 10,000; if the
edition division comes later than that, the report says so, and which names
were converted as the source's words though they were the editors'.

### The list of places

A `<listPlace>` is the editors' index of the places in the edition. By
default only its web addresses are used, to resolve a `ref="#athens"` (see
[above](#where-a-ref-can-point)). With the reading option, each `<place>`
that has a web address in its `<idno>` also becomes an attestation of its
own, citing the edition:

- **about** the place's web address. A place with no web address is reported,
  and not converted; one with several different web addresses is ambiguous,
  reported, and nothing is converted from it (two forms of one address, such
  as `http` and `https` for Pleiades, count as one).
- **name**: its first `<placeName>`, with the form status
  [*Headword*](glossary.md): the form under which the editors list the place,
  an editorial choice rather than a reading. Its other names are reported and
  not converted, as one attestation has one form status for all its names,
  and the others may be variants, translations or modern forms.
- **locator**: "list of places, place" and the place's `xml:id`.
- **coordinates**, from its `<location><geo>`, written "latitude longitude"
  (`37.97 23.72`) or with a comma (`37.08415, 15.27628`), but only where they
  are the editors' own. That is taken to be so only when the place's address
  is on the edition's own site, the host of the edition's `<idno type="URI">`.
  Coordinates beside a Pleiades or Wikidata address are most likely that
  gazetteer's, copied, and the address already leads to them, so they are
  reported and not converted; an edition known only by a DOI therefore never
  has its coordinates converted. PLATO's coordinates are longitude and
  latitude in WGS 84, so they are read only when the header declares no datum
  (TEI's default is WGS 84) or a `<geoDecl datum="WGS84">`; in any other datum
  they are reported. Coordinates that are not two numbers in range are
  reported too.

A list of places in the header waits for the end of the header, so that the
edition's title and address are known; one in the text or in `<back>` is
converted where it stands.

For example, PLATO tools' test file `pointers-constructed.xml` has this list
in its header, and the edition's own address is
`https://example.org/editions/pointers`:

```xml
<place xml:id="athens">
  <placeName>Athenae</placeName>
  <idno type="pleiades">https://pleiades.stoa.org/places/579885</idno>
  <location><geo>37.97 23.72</geo></location>
</place>
<place xml:id="thebes">
  <idno>https://pleiades.stoa.org/places/541138</idno>
  <idno type="URI">https://www.wikidata.org/entity/Q192393</idno>
</place>
<place xml:id="nowhere">
  <placeName>Nephelokokkygia</placeName>
  <idno type="local">N1</idno>
</place>
```

With `--list-places`, Athens becomes an attestation about
`https://pleiades.stoa.org/places/579885` with the headword *Athenae* and the
locator "list of places, place athens", but without the coordinates, which
are reported, since the address is Pleiades', not the edition's. Thebes has
two different addresses, and is reported as ambiguous. Nephelokokkygia has no
web address, and is reported.

### Places in the header

An inscription's header often says where the stone was found, in a
`<provenance type="found">`, and where it was made, in an `<origin>` with an
`<origPlace>`. These are the editors' statements about the object, not words
of the text, so by default they are reported and not converted. With the
reading option, a place name with a `ref` in either becomes an attestation
whose name has the form status [*Editorial*](glossary.md), with the note "The
name is the editors' form, in the edition's header, not words of the source."

- **Where it was found.** The attestation says that the place is the
  *findspot of* the object (PLATO's relation `plato:FindspotOf`), naming the
  object by its web address and its title. The object's address is the
  `<idno type="URI">` in the manuscript's or object's `<msIdentifier>`, or else
  the edition's own `<idno type="URI">`, never its DOI, which names a deposit
  of the edition, not the object. A header with neither gives an attestation
  without the relation, and the report says so. The locator is "teiHeader,
  provenance (found)".
- **Where it was made.** PLATO has no relation for a place of origin, so the
  attestation is a plain one, with the locator "teiHeader, origin" and a note
  that the header gives this as the place of origin; the report says so.

Place names elsewhere in the header are still not converted.

### Keys in place of refs

Some editions name places with a `key` and no `ref`: EpiDoc projects write
`key="pleiades:579885"`, and the Perseus texts `key="tgn,7011179"` (a place in
the Getty Thesaurus of Geographic Names). A key is not a web address, so by
default such a place name is reported, with its key. You can give a
**pattern** that makes the address from the key:

- the **prefix** is what comes before the key's first `:` or `,` (`pleiades`,
  `tgn`); a key with neither has no prefix;
- the rest of the key replaces `{id}` in the pattern:
  `http://vocab.getty.edu/tgn/{id}` makes `tgn,7011179` into
  `http://vocab.getty.edu/tgn/7011179`.

The report lists each prefix once, with how many keys have it and a few of
them, and suggests a pattern where it knows the gazetteer. **On the page**, a
table under *Keys with no web address* has a row for each prefix, with the
suggested pattern filled in, which you can change; a pattern is used only
when you tick *Use* in its row. **On the
command line**, give `--key-pattern PREFIX=PATTERN` once for each prefix, or
`--key-pattern PATTERN` for keys with no prefix.

The rest of each key must have the shape the gazetteer's ids have: digits for
Pleiades and GeoNames, `Q` and digits for Wikidata, and for a pattern of your
own, only letters, digits and `. _ ~ -`. A key of another shape is reported,
and not converted. The address made then follows the
[rules above](#gazetteer-addresses-in-one-form), and the attestation's notes
say how it was made: "Place address made from the key pleiades:579885 with the
pattern https://pleiades.stoa.org/places/{id}". A place name that has a `ref`
uses its `ref`; its key is only noted. A pattern that makes a World Historical
Gazetteer address is refused, as WHG's short codes do not name one record.

For example, PLATO tools' test file
[`keys-constructed.xml`](https://github.com/pelagios/plato-tools/blob/main/test/fixtures/tei/keys-constructed.xml)
has keys of four prefixes. Checked with no patterns, the report suggests

```text
prefix "tgn": 3 keys, such as tgn,7011179, tgn,7010720, tgn,7001393; try --key-pattern tgn=http://vocab.getty.edu/tgn/{id}
prefix "pleiades": 2 keys, such as pleiades:579885, pleiades:athens; try --key-pattern pleiades=https://pleiades.stoa.org/places/{id}
no prefix: 1 key, such as Q1524; try --key-pattern http://www.wikidata.org/entity/{id}
prefix "perseus": 1 key, such as perseus,Argos; give a pattern, such as --key-pattern perseus=https://…/{id}
```

Given those three patterns, five of the key-only place names become
attestations; `pleiades:athens` is reported, as `athens` is not a Pleiades id,
and `perseus,Argos`, with no pattern, is reported again.

## TEI P4

TEI P4 is the version of TEI before P5, and many older editions are in it,
among them the Perseus Digital Library's texts. PLATO tools reads a P4 file as
it reads P5, with P4's own names for things. A file is read as P4 only when
its root element is `<TEI.2>` or `<teiCorpus.2>`, and the report says so once,
as a warning. Everything else on this page applies to it too, with these
differences:

- **Ids and languages.** P4's `id` is read as P5's `xml:id`, and its `lang` as
  `xml:lang`.
- **A language is named in the header.** In P4, `lang` names one of the
  `<language>` elements of the header: `lang="la"` names
  `<language id="la">Latin</language>`. The place name's language is that
  element's `ident`, if it is a language code, or else its `id`, if that is
  one. `<language id="greek">Greek</language>` gives neither, so the name is
  converted without a language, and the report names the `<language>`, so
  that you can give it an `ident`. In a `<teiCorpus.2>`, each `<TEI.2>` has
  its own languages, and the corpus header's hold for every text in it.
- **Numbered divisions.** `<div1>` to `<div7>` are read as `<div>` is, for the
  locator: "book 1, chapter 1, section 2".
- **Notes.** A P4 text has no `<div type="edition">`, so its notes are read as
  the source's words, unless a note is marked as the editors' own, such as
  with `resp="ed"`: see [Whose words](#whose-words-the-editors-parts).
- **A regularised form.** A place name's `reg`, the editors' regularised form,
  as in `<placeName reg="Roma">Romae</placeName>`, is the editors' words, not
  the text's. It is reported and not carried: the name is *Romae*, as the text
  has it.
- **Keys.** Perseus names places with keys such as `key="tgn,7000874"`, a place
  in the Getty Thesaurus of Geographic Names. Give a pattern for them, as for
  any key: see [Keys in place of refs](#keys-in-place-of-refs). The report
  suggests `--key-pattern tgn=http://vocab.getty.edu/tgn/{id}`.

These rules are for P4 only. A file whose root is `<TEI>` with no namespace is
not P4: it is read as P5 written without its `xmlns`, with a warning, and its
`id` and `lang`, which P5 does not have, are reported, not read. Add
`xmlns="http://www.tei-c.org/ns/1.0"` to its root to make it P5 as written.

### Greek in Beta Code

Perseus's P4 texts write Greek in Beta Code, which spells Greek in Latin
letters and signs: `*)aqh=nai` is Ἀθῆναι. PLATO tools does not convert Beta
Code to Greek letters, as a conversion that is not exact would put words in
the source's mouth.

A P4 place name whose language is Greek, written in plain Latin letters with
at least one of Beta Code's signs (`*`, `(`, `)`, `/`, `\`, `=`, `|`, `+` or a
digit), is taken to be Beta Code. It still becomes an attestation, with its
place, its citation and its locator, but with no name; its notes say why, and
the report lists the Beta Code as written, with its line.

A Greek place name in plain Latin letters with none of those signs, such as
`Rwmh`, is **possible Beta Code**: it may be Greek written without accents or
capitals, or a name in another language whose element only inherits Greek from
around it, such as an English note in a Greek passage. Which it is cannot be
told, so the name is carried as written, with no language, and the report
lists it, as a warning. Check each, and give the note or the name its own
`lang` where it is not Greek.

A Greek name written in Greek letters, or with entities for them (below), is
read as any name is.

### An example: a P4 text

PLATO tools' test file `p4-constructed.xml` is a small P4 text, made up in the
manner of a digital library's Latin prose. Its text begins

```xml
<text lang="la">
<body>
<div1 type="book" n="1">
<div2 type="chapter" n="1">
<milestone unit="section" n="1"/>
<p>Primum <placeName key="tgn,7000874" reg="Roma">Romae</placeName> fuimus, deinde
<placeName id="pn-athenae" key="tgn,7001393">Athenas</placeName> navigavimus, ubi Graeci urbem
<foreign lang="greek"><placeName key="tgn,7001393">*)aqh=nai</placeName></foreign> vocant, alii
<foreign lang="greek"><placeName key="tgn,7001393">&Agr;&thgr;&eegr;&ngr;&agr;&igr;</placeName></foreign>
scribunt.</p>
```

Checked with `--key-pattern tgn=http://vocab.getty.edu/tgn/{id}`, it gives
eight attestations. *Romae* is in Latin, about
`http://vocab.getty.edu/tgn/7000874`, with the locator "book 1, chapter 1,
section 1"; *Athenas* has the same locator, with "xml:id pn-athenae" after it.
The Beta Code `*)aqh=nai` gives an attestation about Athens with no name.
The name in entities is read from the ISO sets as *Αθηναι*, with no language,
since `<language id="greek">` is not a language code. The report says, among
other things:

```text
The file is TEI P4 (<TEI.2> or <teiCorpus.2>), which is read as P5 would be …
    <TEI.2> in p4-constructed.xml
… which were read from the ISO entity sets …
    isogrk1: Agr (1), thgr (1), eegr (1), ngr (1), agr (1), igr (1)
    isolat1: aelig (1)
A language (xml:lang) that is not a language tag …
    greek (<language id="greek">Greek</language>)
    latine (<language id="latine">Latin, with no tag</language>)
A place name's reg …
    Romae (reg="Roma") on line 73
A Greek place name written in Beta Code …
    *)aqh=nai (<placeName> on line 75)
```

A place name in the text's footnote, marked `resp="ed"`, is reported as the
editors' words.

## Entities

An entity, such as `&nbsp;` or `&aelig;`, stands for text declared somewhere
else. What PLATO tools does with one depends on where it is declared.

**Declared in the file.** An entity that the file's own DOCTYPE declares with
its text, as in `<!DOCTYPE TEI [<!ENTITY nbsp "&#160;">]>`, is read. One whose
declared text holds markup cannot be read yet, and stops the file where it is
used. An entity declared as another file (with `SYSTEM` or `PUBLIC`) is never
fetched or read, for safety: a file that uses one is refused, and the message
names it.

**From the standard table, in a file that names an outside DTD.** A P4 file
often begins with a DOCTYPE that names TEI's DTD, and the ISO entity sets as
well:

```xml
<!DOCTYPE TEI.2 PUBLIC "-//TEI P4//DTD Main Document Type//EN" "http://www.tei-c.org/Guidelines/DTD/tei2.dtd" [
<!ENTITY % ISOgrk1 PUBLIC "ISO 8879:1986//ENTITIES Greek Letters//EN//XML" "isogrk1.ent">
%ISOgrk1;
]>
```

Such a file relies on entities declared in those other files, which PLATO
tools never fetches. So, for such a file only, an entity the file does not
declare itself is looked up in the standard table of character entities, the
ISO sets as the W3C publishes them
([XML Entity Definitions for Characters](https://www.w3.org/2003/entities/2007/)):
`&aelig;` is *æ*, `&agr;` is *α*. The file's own declarations come first. The
report lists each set used once, with each name and how many times it was
used, as a warning: a few names have stood for different characters over the
years (ISOgrk3's `phiv` and `epsiv`), so check the characters read. This
applies to a P5 file that names an outside DTD as well.

**A publisher's own entities.** A digital library's DTD often declares
entities of its own for its standard wording, such as `&responsibility;` or
`&fund.NEH;`. They are not in the table, and the DTD is never read, so what
they stand for is not known. In a file that names an outside DTD, each is left
out, with nothing in its place, and the report lists them once, with how many
times each was used: words in the header, such as who funded or published the
edition, may be missing. Where leaving one out would make something wrong
rather than shorter:

- a **place name** whose words, `ref` or `key` hold one is not converted, as
  its name or address would be incomplete; the report gives the entity, the
  name as read without it, and its line. So is a place in a list of places
  whose address or name holds one;
- a **number** (`n`) of a division, milestone, page or line that holds one is
  left out of the locators of the place names under it, rather than given
  incomplete, and reported;
- the edition's **title** or its **web address** holding one stops the file,
  as every citation of it would be incomplete.

For example, PLATO tools' test file `p4-boilerplate-constructed.xml` uses
three such entities in its header. Checked with the pattern for its `tgn`
keys, it gives both its place names, and warns:

```text
&responsibility; (2), &fund.NEH; (1), &Perseus.publish; (1): left out, with nothing in their place; the outside DTD that may declare them was never read
```

If its second place name is changed to `Ath&lib.emacr;nas`, that place name is
not converted, and the report says:

```text
&lib.emacr; in "Athnas" (<placeName key="tgn,7001393">) on line 34
```

To keep such a name, declare the entity in the file's DOCTYPE with its text,
or write the text in its place.

**Anything else.** In a file that names no outside DTD, an entity the file
does not declare stops the file where it is used, and the message names it.
Write the character itself, or declare the entity with its text.

## What is left out, and why

**Place names with no ref.** A place name that points to no place has nothing
for an attestation to be about. The report lists each, with its key if it has
one. Give it a `ref` to keep it, or, if it has a key, a pattern for the key
(see [Keys in place of refs](#keys-in-place-of-refs)).

**The editors' words.** In an edition with a `<div type="edition">`, a place
name in the commentary, translation, apparatus or another of the editors'
parts, or in a note, is reported, and converted only with the reading option:
see [Whose words](#whose-words-the-editors-parts).

**Place names outside the text.** A place name in the `teiHeader`, such as
where an inscription was found, or in a `<standOff>` or `<facsimile>`, is the
edition's description of the document, not a name the text attests. It is
reported, not converted, except that the reading option for
[places in the header](#places-in-the-header) converts where the object was
found and where it was made.

**Variant readings.** A place name in an `<rdg>`, or in the part of a
`<choice>` not taken, is listed and not converted: see
[Variant readings](#variant-readings).

**Attributes PLATO has no place for.** `cert`, `resp`, and `type` on a
`<placeName>` are reported, once for each attribute and value. TEI's `cert`
does not say what it is certain of (the reading, or which place is meant), so
it is not taken for the certainty of the attestation.

**Greek in Beta Code.** In a P4 text, a Greek place name in Beta Code is
converted with no name, and one that may be Beta Code is carried as written,
with no language; the report lists each: see
[Greek in Beta Code](#greek-in-beta-code). A P4 place name's `reg` is
reported, not carried.

**Entities no one declares.** In a file that names an outside DTD, an entity
that neither the file nor the standard table declares is left out, and a place
name holding one is not converted: see [Entities](#entities).

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

## A second example: an inscription, with reading options

PLATO tools' tests also use a real EpiDoc file, unchanged: I.Sicily's edition
of the epitaph of Zodoros from Syracuse
([ISic000934](https://github.com/pelagios/plato-tools/blob/main/test/fixtures/tei/isicily-ISic000934.xml),
edited by Jonathan Prag, CC BY 4.0). Its edition division names the village
Zodoros came from, Μάκρης κώμης, over three lines; its commentary names
*Sarepta*; and its header says the stone was made at Syracuse, `<origPlace>`
naming it twice (as Pleiades' *Syracusae*, written
`http://pleiades.stoa.org/places/462503`, and GeoNames' *Siracusa*, written
`http://sws.geonames.org/2523083`), and found in the catacomb of S. Giovanni.

Converted with no reading options, it gives one attestation: Μάκρης κώμης,
attested, in Greek, with the locator "edition, lines 2 to 4". The report lists
*Sarepta* as in the editors' words ("commentary: Sarepta … on line 205") and
the three header names as outside the text.

Converted with `--commentary-places` and `--header-places` (on the page, the
two boxes ticked), it gives five:

- Μάκρης κώμης, as before;
- *Sarepta*, form status *Editorial*, the locator "commentary", the note "The
  editors' words, not the source's.";
- *catacomb of S. Giovanni*, form status *Editorial*, the locator "teiHeader,
  provenance (found)", the *findspot of* the inscription, named by its address
  `http://sicily.classics.ox.ac.uk/inscription/ISic000934` and its title
  *Epitaph of Zodoros*;
- *Syracusae* and *Siracusa*, form status *Editorial*, the locator
  "teiHeader, origin", each with a note that the header gives it as the place
  of origin. Their addresses are carried in their gazetteers' forms,
  `https://pleiades.stoa.org/places/462503` and
  `https://sws.geonames.org/2523083/`, with notes such as "Place address given
  as http://sws.geonames.org/2523083 (rule geonames-sws-https,
  hermes-addresses 1)".
