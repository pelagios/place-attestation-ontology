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

## Spreadsheets to RDF

The spreadsheet tables are described in the W3C standard
[CSV on the Web](https://www.w3.org/TR/tabular-data-primer/), so any CSVW
processor converts them. With the reference implementation,
[rdf-tabular](https://github.com/ruby-rdf/rdf-tabular):

```bash
# with csv-metadata.json in the same folder as the ten CSV files
rdf serialize --validate --input-format tabular --minimal --output-format turtle csv-metadata.json
```

Use `serialize --validate` to check a set of tables: rdf-tabular's plain
`validate` command reports broken references as warnings and still says the
input is valid.

Identifiers in the output are relative to the files (`places.csv#bristol`,
`names.csv#row-3`), because CSVW cannot build an address from a cell of
another table. They are for checking the tables, not the dataset's addresses,
which PLATO fixes: a place's is the base, then `place/`, then its
`place_id`; a source's is the base, then `source/`, then its `source_id`; and
the dataset's is its `dataset_uri`, or the base if that is empty. The base is
one given for the conversion, else the about sheet's `base_uri`, with a `/`
added unless it ends in `/` or `#`; every character of an identifier other
than the unreserved characters of RFC 3986 (`A-Z a-z 0-9 - . _ ~`) is
percent-encoded as UTF-8. The attestations have no address of their own. The
dataset node is already named by `dataset_uri` in the output, when it is
given; when it is empty, a CSVW processor names it after the file,
`about.csv`, since a URI template has no fallback value. See
[converting](tools.md#converting) for how PLATO tools applies the rest.
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

## Citing a place in a gazetteer that changes

A place's evidence grows and is corrected while its identity stays the
same, so a citation of it has to say which state was meant. PLATO gives
three pieces for that.

- **A version.** A gazetteer carries a version (`version` in JSON,
  `dcat:version` in RDF). Cite a place as its address plus the gazetteer
  version, as PeriodO is cited. A frozen snapshot published under its own
  address points back with `isVersionOf` and `previousVersion`.
- **Nothing is deleted once published.** When a gazetteer's `status` is
  `published`, its attestations are append-only. A correction is a new
  attestation that supersedes or contradicts the old one, and a withdrawal
  is one that retracts it (`plato:Retracts`). Every attestation carries its
  `created` time, so the state as of any date can be worked out from the
  data itself. Before publishing a new version, check that it keeps this
  rule: [PLATO tools](https://pelagios.org/plato-tools/) compares it with the
  earlier one and lists anything deleted or changed (see
  [comparing two versions](tools.md#comparing-two-versions)). From the
  command line: `npx github:pelagios/plato-tools compare earlier.jsonl later.jsonl`.
- **Addresses for attestations.** An attestation can only be withdrawn or
  replaced by pointing to it, so every attestation in a published dataset
  should have a permanent address of its own (`@id`). This is a
  recommendation for now, and is meant to become a requirement.
- **A state on request.** A platform can offer that state directly through
  datetime negotiation on the place's address ([RFC 7089, "Memento"](https://www.rfc-editor.org/rfc/rfc7089)):
  ask for the address as it stood at a moment, and get the attestations that
  held then. PLATO recommends this to platforms but does not require it.

## JSON to RDF

Add the JSON-LD context to a JSON document, as described under
[JSON formats](json.md), and expand or convert it with any JSON-LD 1.1
processor.
