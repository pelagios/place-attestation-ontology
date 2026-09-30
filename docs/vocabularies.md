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

```{include} _generated/vocabularies.md
```
