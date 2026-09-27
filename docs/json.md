# JSON formats

If you produce data with your own software, PLATO has two JSON formats,
each defined by a JSON Schema. They carry everything the spreadsheets do and
more: several facts or several sources in one attestation, shared names and
geometries, comments on other people's evidence.

| Format | Use it when… | Schema |
|---|---|---|
| **place-centric** | you are describing your own places: each place carries its attestations inside it | [place-centric.schema.json](https://w3id.org/plato/schemas/place-centric.schema.json) |
| **attestation-centric** | you are adding evidence about places that already exist elsewhere, referring to them by URI | [attestation-centric.schema.json](https://w3id.org/plato/schemas/attestation-centric.schema.json) |

Both are built from the shared definitions in
[plato.schema.json](https://w3id.org/plato/schemas/plato.schema.json), which
they refer to by relative path, so keep the three files together when
validating. Worked examples are in the repository's
[schemas/examples](https://github.com/pelagios/place-attestation-ontology/tree/main/schemas/examples)
folder.

## Checking and converting

[PLATO tools](https://pelagios.org/plato-tools/) checks a JSON submission against these schemas and
converts it to RDF, to the spreadsheet tables or to Linked Places Format, in
the browser and at any size. It reads JSON Lines too: a header line, then one
place per line, which is the easiest shape to write and to stream.

## From JSON to linked data

Add the PLATO JSON-LD context to a JSON document and any JSON-LD processor turns
it into RDF in the PLATO ontology:

```json
{
  "@context": "https://w3id.org/plato/schemas/plato.context.jsonld",
  "$schema": "https://w3id.org/plato/schemas/attestation-centric.schema.json",
  "profile": "attestation-centric",
  "gazetteer": { "title": "My dataset" },
  "attestations": [
    {
      "about": "https://www.geonames.org/2654675/",
      "names": [ { "toponym": "Bristowe", "language": "enm" } ],
      "timespans": [ { "startEarliest": "1480", "endLatest": "1485", "label": "1480-1485" } ],
      "sources": [ { "title": "TNA E 122/19/10" } ]
    }
  ]
}
```

The context's own opening comment explains how the two formats are read and
what a triplifier must add itself. See [Linked data](linked-data.md) for the
URLs.

## Keys and terms

JSON keys are camelCase (`startEarliest`, `formStatus`); the ontology's
properties are snake_case (`start_earliest`, `form_status`). The context maps
one to the other. The fixed values for keys such as `formStatus` are the full
identifiers listed under [Vocabularies](vocabularies.md).
