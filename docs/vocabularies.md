# Vocabularies

Some columns in the spreadsheets, and some fields in JSON, take a word from a
fixed list rather than free text. This page lists every such word, what it
means, and the full identifier it stands for in PLATO. It is generated from
the ontology, so it always matches it.

In the spreadsheets, write the word in the *Value* column exactly as shown,
with the same capital letters. Four columns are exceptions, because the
table definitions add the start of the word for you:

- `attribution`: write `Stated` or `Inferred` (not `AttributionStated`);
- `stance`: write `Reported`, `Tentative`, `Doubted` or `Asserted` (not
  `StanceReported`);
- `transcription_accuracy`: write `Accurate`, `Inaccurate` or `False`;
- `transcription_completeness`: write `Complete`, `Reconstructable` or
  `NonReconstructable`.

The kinds of spatial entity (`TypeRoute` and the others) are not written as
words in any column: give the full identifier in a type row's `type_uri`, as
[Routes, journeys and networks](routes/index.md) shows. In JSON and RDF, use
the full identifier.

The lists are open: if you need a value that is not here, ask for it by
[opening an issue](https://github.com/pelagios/place-attestation-ontology/issues).

## The vocabularies as SKOS

If you already use SKOS (Simple Knowledge Organization System, the format
most thesaurus and vocabulary tools read), every list on this page is also
published as a SKOS file, so that your tools can load PLATO's words like any
other vocabulary:

- the current version: `https://w3id.org/plato/schemas/plato.skos.ttl`
  (or `.jsonld`);
- a fixed copy for each release, from 0.9.0-alpha.2 on:
  `https://pelagios.org/place-attestation-ontology/releases/<version>/vocabularies.skos.ttl`.

PLATO's own lists of words (form status, source stance, relation types,
certainty levels and the rest) are SKOS concept schemes in the ontology
itself. The SKOS file writes out what SKOS tools expect of each concept
(its label, definition and narrower or broader concepts), and a project's own
narrower relation type, declared with `broader_relation`, is a SKOS "broader"
link by definition. The file is made from the ontology at each release and is
never edited; the ontology is the authority. It is also not a way to use your own SKOS vocabulary in PLATO: for
that, name the vocabulary's concept as a type's identifier, and say which
scheme it belongs to.

```{include} _generated/vocabularies.md
```
