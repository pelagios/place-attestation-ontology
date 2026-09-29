# Sheet reference

:::{admonition} Where this page fits
:class: note

This is the column-by-column reference for **temPlato**, PLATO's spreadsheet
template. If you are new to it, start with
[Organising data in spreadsheets](index.md), which explains the nine sheets
and the rules that apply to all of them, and where to download the template.

Spreadsheets are one of several formats that comply with PLATO. The same data
can be written as [PLATO JSON](../json.md) or as [linked data](../linked-data.md)
(RDF), and [PLATO tools](https://pelagios.org/plato-tools/) converts between
them, and to and from Linked Places Format.
:::

Every column of every sheet: whether it is needed, what to put in it, an
example, and the values it accepts. This page is generated from the
[table definitions](https://w3id.org/plato/schemas/tables/csv-metadata.json),
so it always matches them.

In every sheet except places, sources and identities, each row becomes one
PLATO attestation, and these columns are shared: `place_id`, `date`, `from`,
`to`, `source_id`, `locator`, `attribution`, `citation_function`,
`certainty`, `certainty_level`, `denied`, `stance` and `notes`.

```{include} ../_generated/sheets.md
```
