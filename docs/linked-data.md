# Linked data

PLATO is an OWL ontology. Everything in this guide, from the spreadsheets to
the JSON formats, is a way of producing RDF in it.

## Addresses

| What | Permanent address |
|---|---|
| The ontology | <https://w3id.org/plato> (namespace `https://w3id.org/plato#`) |
| Ontology reference documentation | <https://pelagios.org/place-attestation-ontology/> |
| JSON Schemas | `https://w3id.org/plato/schemas/plato.schema.json`, `…/place-centric.schema.json`, `…/attestation-centric.schema.json` |
| JSON-LD context | <https://w3id.org/plato/schemas/plato.context.jsonld> |
| Spreadsheet table definitions (CSVW) | <https://w3id.org/plato/schemas/tables/csv-metadata.json> |

The ontology address answers with HTML in a browser and with RDF to a client
that asks for it. The files themselves are published at
`https://pelagios.org/place-attestation-ontology/ontology.ttl`, and as
`.jsonld`, `.owl` (RDF/XML) and `.nt` (N-Triples). All four are the same
graph: the Turtle is the source file, and the others are generated from it
and checked against it on every release.

:::{note}
The w3id.org redirects are being updated so that `https://w3id.org/plato`
also negotiates JSON-LD, RDF/XML and N-Triples, and so that the schemas and
context are served with JSON media types. Until that change is live, strict
JSON-LD processors such as jsonld.js should load the context from
<https://pelagios.org/place-attestation-ontology/schemas/plato.context.jsonld>.
:::

## Spreadsheets to RDF

The spreadsheet tables are described in the W3C standard
[CSV on the Web](https://www.w3.org/TR/tabular-data-primer/), so any CSVW
processor converts them. With the reference implementation,
[rdf-tabular](https://github.com/ruby-rdf/rdf-tabular):

```bash
# with csv-metadata.json in the same folder as the eight CSV files
rdf serialize --validate --input-format tabular --minimal --output-format turtle csv-metadata.json
```

Use `serialize --validate` to check a set of tables: rdf-tabular's plain
`validate` command reports broken references as warnings and still says the
input is valid.

Identifiers in the output are relative to the files (`places.csv#bristol`,
`names.csv#row-3`); a platform accepting the tables mints permanent ones.
Every node is typed, and every attestation has exactly one subject, source,
date and citation, so the output is complete PLATO without further
processing.

## Without installing anything

[PLATO tools](https://pelagios.org/plato-tools/) converts between PLATO JSON, RDF (it reads N-Triples,
N-Quads and Turtle, and writes N-Triples), the spreadsheet tables and Linked
Places Format, in the browser, and checks RDF against the terms the ontology
declares. The same conversions run [from the command line](https://github.com/pelagios/plato-tools#from-the-command-line) for batch
work, with Node.js 24 or later: for example,
`npx github:pelagios/plato-tools convert --to ntriples data.jsonl`. Large RDF
files are handled through a working database on disk, as in the browser, so
memory stays roughly constant at any size.

## JSON to RDF

Add the JSON-LD context to a JSON document, as described under
[JSON formats](json.md), and expand or convert it with any JSON-LD 1.1
processor.
