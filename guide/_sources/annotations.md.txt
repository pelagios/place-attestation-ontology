# Annotations from Recogito

If you have read a text, a map or a table in
[Recogito](https://recogito.pelagios.org/) or
[Recogito Studio](https://recogitostudio.org/) and linked the places it
mentions to a gazetteer, you have already done most of the work of organising
that evidence in PLATO's shape. Each link says: *this passage, in this
document, names this place*. That is an attestation.

[PLATO tools](https://pelagios.org/plato-tools/) turns a Recogito download
into a PLATO dataset, which you can then check, convert to the spreadsheet
tables or to Linked Places Format, and add to.

## How to do it

1. In Recogito, download your document's annotations in the **W3C Web
   Annotation** format (a JSON-LD file).
2. Open [PLATO tools](https://pelagios.org/plato-tools/), drop the file on
   it, and choose **Convert**, with the format you want.
3. Read the report. It lists everything that was not carried over, and why.

Nothing leaves your computer: PLATO tools works entirely in your browser.

## What each part of an annotation becomes

| In Recogito | In PLATO |
|---|---|
| The place you linked the passage to (a Pleiades, GeoNames, Wikidata or WHG address) | What the attestation is **about** |
| The words you marked | The **name** the source uses, recorded as attested |
| For a map or image, your transcription of the label | The **name** |
| The document | The **source** |
| Where in the document: the characters, the paragraph of a TEI text, the region of an image, the page, the row of a table | The citation's **locator**, written out in words ("characters 1083 to 1092", "row 2") |
| Who made the link, and when | The attestation's **contributor** and dates |
| Comments, notes and free tags | The attestation's **notes** |
| A tag from a vocabulary (an AAT or Wikidata concept) | A **type** |

A passage linked to two places becomes two attestations, each with a note
naming the other.

## Gazetteer addresses in one form

Recogito's first version writes Pleiades and GeoNames addresses with `http`
(`http://pleiades.stoa.org/places/423025`, `http://sws.geonames.org/2629833`),
while the gazetteers themselves, and many other datasets, write
`https://pleiades.stoa.org/places/423025` and
`https://sws.geonames.org/2629833/`. To a computer these are different
addresses, so the same place would become two, and your evidence would not
meet anyone else's. PLATO tools therefore writes each Pleiades, GeoNames and
Wikidata address in the one form its gazetteer gives it, by the rules listed
in [Place names in a TEI edition](tei.md#gazetteer-addresses-in-one-form),
and says so in the attestation's notes, with what Recogito wrote, the rule,
and the version of the rules:

```text
Place address given as http://sws.geonames.org/2629833 (rule geonames-sws-https, hermes-addresses 1)
```

In PLATO tools' test file of a Recogito download of Pliny's text, 48 of its 55
attestations have their address rewritten so. A Pleiades address that names
part of a place's record (a location, a name, `/json`), or ends `#this`, is
carried as written, and the report asks you to check it.

If you converted the same download before these rules, the
[version check](tools.md#comparing-two-versions) will show the rewritten
attestations as changed; the version in their notes says why.

## What is left out, and why

**Links a person never confirmed.** Recogito can suggest place links by
itself, by recognising place names in a text. A suggestion is not anyone's
statement, so PLATO tools leaves it out rather than record it as evidence,
and the report counts what was left out. Review the suggestions in Recogito
before you download, and confirm or delete each one.

There is one case PLATO tools cannot detect. In Recogito's first version, a
place added with the automatic best match, and never checked, looks in the
download exactly like a confirmed one. If you worked that way, check those
links before you download; the report reminds you of this.

**Mentions never linked.** A passage marked as a place but not linked to any
gazetteer has nothing to be evidence *about*. People and events are left out
too: PLATO records evidence about places, routes and other things whose
identity is bound up with space, not about people or events.

**The gazetteer's own coordinates and titles.** A Recogito download can
include coordinates or a title taken from the matched gazetteer. They are
the gazetteer's, not your document's evidence, so they are not recorded as
your attestation. The place's own gazetteer still has them.

**Shapes drawn on an image.** A rectangle is kept as a region in the
locator; a freely drawn shape is reported, and only its presence is noted.

**Recogito Studio documents.** Studio's download names the project rather
than the document, so annotations from several documents cannot be told
apart. Download one document at a time.

## Identifiers

Each attestation's notes give the address of the annotation it came from
("From annotation …"), so you can always find your way back to Recogito. The
annotation's address is not used as the attestation's own identifier: you
may edit an annotation and download it again, but an attestation in a
published dataset must never change. See [PLATO and FAIR data](index.md#plato-and-fair-data).

The full mapping, for developers, is beside PLATO tools'
[annotation test files](https://github.com/pelagios/plato-tools/blob/main/test/fixtures/annotations/README.md#the-mapping).
