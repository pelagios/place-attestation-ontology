# Glossary

Attestation
: One piece of evidence: a statement that a source, for a date, gives a name,
  location, type, relation or other fact for a place. Each evidence row of the
  spreadsheets becomes one attestation.

Certainty
: How sure whoever recorded a statement is of it, from 0 to 1. It reflects the
  evidence: better evidence could change it. Not the same as fuzziness. Where
  a source or a dataset gives certainty in words, the *certainty level*
  records the word ('Certain', 'LessCertain', 'Uncertain') instead of a
  number.

Citation
: One attestation's use of one source, with the locator saying where in the
  source the evidence is, and, where known, why the source is cited: as the
  evidence, as a source of data, as related reading.

CSVW (CSV on the Web)
: The W3C standard used to describe the spreadsheet tables: their columns,
  allowed values, how they refer to one another and how rows become RDF.

Date, from, to
: *Date* is the date as the source gives it, or "undated", kept in the
  source's own words. *From* and *to* are
  the earliest and latest years or days it can mean, written with at least four-digit
  years.

Denial
: A source's statement that something was not so, such as "no market here".
  It is recorded as an attestation marked as denied, about the real place,
  so that nothing that never existed has to be invented.

Fuzziness
: The sense in which something genuinely has no sharp edge, such as "the
  Levant" or a gradual change of rule. It is a property of the thing, not of
  our knowledge of it, so it is different from certainty.

Headword
: The form of a name under which an editor or survey files an entry. An
  editorial decision rather than a reading.

Ibid. (ibidem), idem
: "The same (source) as before". Where an editor has worked out which source
  was meant, the attribution is *inferred*.

JSON-LD
: A way of writing linked data as JSON. PLATO's JSON-LD context turns a JSON
  document into RDF.

Locator
: Where in a source the evidence is: a page, folio, column or entry number.

Normalised form
: A spelling made up for searching or matching, attested by no source.

Place
: In this guide, as in everyday speech, somewhere a source talks about. PLATO
  gives the word no special meaning: its own term is SpatialEntity. The
  spreadsheets' places sheet holds SpatialEntities.

RDF
: The W3C standard data model for linked data, in which the PLATO ontology is
  written.

Source
: A document, map, book or dataset that evidence comes from. A source can be
  derived from another, as a copy or an edition.

SpatialEntity
: PLATO's term for the thing attestations are about. Many SpatialEntities are
  places in the everyday sense; others are routes, networks, administrative
  units or the regions historical periods apply to. What kind each is comes
  from type attestations.

temPlato
: PLATO's spreadsheet template: eight linked sheets, as an Excel workbook or
  as CSV files, for putting data into PLATO's shape without software.

URI
: A web address used as a permanent identifier, such as
  `https://www.geonames.org/2654675/`.
