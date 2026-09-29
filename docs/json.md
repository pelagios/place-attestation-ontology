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

[PLATO tools](https://pelagios.org/plato-tools/) checks a JSON document against these schemas and
converts it to RDF, to the spreadsheet tables or to Linked Places Format, in
the browser and at any size. It reads JSON Lines too: a header line, then one
place per line, which is the easiest shape to write and to stream.

For batch jobs and pipelines it also runs [from the command line](https://github.com/pelagios/plato-tools#from-the-command-line),
with Node.js 24 or later. It uses the same engine as the page, so it gives
the same results:

```bash
npx github:pelagios/plato-tools check data/*.jsonl            # a report per file, then a total
npx github:pelagios/plato-tools check --json data/*.json > report.jsonl
npx github:pelagios/plato-tools convert --to ntriples --out rdf/ data/*.jsonl
```

It exits with 0 when no file has problems, 1 when any has, and 2 when a file
cannot be read or the command is wrong, so a script can stop on invalid data.

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
      "timespans": [ { "startEarliest": "1480", "endLatest": "1485", "sourceLabel": "1480-1485" } ],
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

`sourceLabel`, on a name, geometry, timespan, type or property value, is the
source's own wording where the structured value normalises it: a date as
written ('about 1841'), coordinates as printed. A timespan's `label` is for a
named period ('Byzantine period'). Certainty stated in words goes in
`certaintyLevel`, as the URI of a level such as
`https://w3id.org/plato#LessCertain`, rather than as an invented number in
`certainty`. Both are your confidence. How firmly the source itself says
something goes in an attestation's `sourceStance`, such as
`https://w3id.org/plato#StanceReported` for a claim it only passes on ("it is
said"). A source's `licence` is the web address of the licence of the copy you
cite, written as the gazetteer's is.

Routes, journeys and networks use a few more keys (see
[Routes, journeys and networks](routes/index.md)). An attestation that makes a
place a member of a route, with `relationType`
`https://w3id.org/plato#MemberOf`, gives its position in `sequence`, a whole
number. A relation to something that is not a place, such as a person in
Wikidata, gives its web address in `relatesTo` and a name to show it by in
`relatedLabel`. A timespan's `duration` is a length the source states, as an
`xsd:duration` such as `P42D` for six weeks. `computed`, on an attestation or
in a `qualification`, marks a value software worked out, not a source's
statement; data you record from sources never needs it.
