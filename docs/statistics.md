# Statistical tables

Census volumes, returns and other statistical sources give figures, not
statements: a count of agricultural labourers who were men, in one county,
in 1851. Each figure is a number *at an address*: the county, the occupation,
the sex. PLATO records such a figure as evidence about the place, like any
other attestation, and keeps its address with the figure, so that the county
is never said to "have" an occupation or a sex.

PLATO does this with the W3C [RDF Data Cube](https://www.w3.org/TR/vocab-data-cube/)
vocabulary, the standard for statistical data on the web. The design, and its
testing on Vision of Britain, Vision of Ireland and the 1886 return of market
rights, is recorded in
[issue #14](https://github.com/pelagios/place-attestation-ontology/issues/14).

## A figure in JSON

A figure is a property value in an attestation about the place, with four
things added:

- `dataSet`: the table it belongs to;
- `dimensions`: its address in the table, one entry per coordinate, keyed by
  the web address of the table's dimension (occupation, sex, class);
- `attributes`: facts about the figure itself, such as that the source
  printed a dash, or that an amount is approximate;
- `universe`: the figure it is a part or share of, where the source says so.

```json
{
  "@id": "https://example.org/occ1851/county-a/agri/m",
  "property": "https://example.org/measure/persons",
  "value": 280,
  "dataSet": "https://example.org/occ1851",
  "dimensions": {
    "https://example.org/dim/occupation": { "@id": "https://example.org/code/agricultural-labourer" },
    "http://purl.org/linked-data/sdmx/2009/dimension#sex": { "@id": "http://purl.org/linked-data/sdmx/2009/code#sex-M" }
  },
  "universe": "https://example.org/occ1851/county-a/agri/total"
}
```

The place and the date are not repeated: they are the attestation's, which
also carries the source and the table and cell in `locator`. The table itself
is described once, in the document's `dataSets`: its title, what it covers,
the source it is part of, and its structure (which dimensions, measures and
attributes it has). The full example is
[place-centric-statistics.json](https://w3id.org/plato/schemas/examples/place-centric-statistics.json).

## Rules

- **Give the universe only where the source does.** A total printed beside
  its parts is a universe; a figure that merely looks like one is not. In
  Vision of Ireland, three of seven plausible denominators, chosen by name,
  turned out to be wrong when their parts were summed.
- **A printed dash is not a zero.** Record it as a figure with no value and
  an `sdmx-attribute:obsStatus` saying "nil or not applicable". A blank cell
  is no figure at all.
- **Money is a whole number in the smallest unit of its system**, so it stays
  exact: farthings for sterling amounts that include halfpennies. Name the
  unit with a web address from a suitable authority, or mint your own, and
  keep the amount as printed ("2,909 12 1") in `sourceLabel`. PLATO converts
  nothing between currencies or periods.
- **A coordinate the source does not give is "unknown", stated.** Give it an
  explicit "unknown" code rather than leaving the dimension out.
- **A table that mixes measures** (money amounts beside other answers) is one
  data set per measure.
- **Dimension values are concepts** with the source's own label. Almost no
  published code lists exist for historical tables, so you will usually
  publish your own.
- **Totals need a code too.** A total over both sexes has the sex code for
  "total", or it cannot be told apart from its own parts.

## Spreadsheets

PLATO's nine sheets are for evidence about places. A statistical table keeps
its own shape: describe it with its own [CSV on the Web](https://www.w3.org/TR/tabular-data-primer/)
metadata, and link its rows to the places in your PLATO sheets by `place_id`.

## Checking, and standard Data Cube

[PLATO tools](https://pelagios.org/plato-tools/) checks a document with
figures like any other. A PLATO document is not written as standard Data
Cube, because nothing in it is written twice; the tools produce standard Data
Cube from it, and check that:

```bash
npx github:pelagios/plato-tools convert --to ntriples --cube figures.json
npx github:pelagios/plato-tools datacube figures.nt
```

The first adds what Data Cube expects: each figure's measure as a direct
statement, and its place and date as `refArea` and `refPeriod`, declared in
each table's structure. A figure whose date is not one year or one day gets
no `refPeriod`; it is reported, not guessed. The second runs Data Cube's
integrity checks on the result, at any size, and says which passed, which
failed, and which had nothing to check.

If you run the W3C's own integrity queries instead, normalise the cube first,
as the [specification](https://www.w3.org/TR/vocab-data-cube/#normalize)
requires. The export writes each table's structure in the short form
(`qb:dimension`, `qb:measure`, `qb:attribute`), which normalisation expands.
The queries assume the expanded form, so without that step IC-11, IC-12 and
IC-14 find nothing to check and pass without testing anything.
`plato-tools datacube` normalises as it reads.
