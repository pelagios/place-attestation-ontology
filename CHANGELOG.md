# Changelog

All notable changes to PLATO are recorded here. The ontology is an early draft
with no implementations yet, so a renamed term is removed outright rather than
retained as a deprecated equivalent. That policy will change once data in the
wild uses the namespace.

## 0.4.0

### Clarified

A SpatialEntity is not a place, and PLATO defines no Place class. The ontology
description, the `plato:SpatialEntity` definition, the README, the JSON schema
and the deposit metadata no longer describe a SpatialEntity as "typically a
place". "Place" carries several meanings in the gazetteer community, and which
of them, if any, corresponds to a SpatialEntity is contested; the ontology now
says so and takes no position. Neither a SpatialEntity nor any set of
attestations or of SpatialEntities is a place by virtue of the ontology. Where
the word still appears it is used informally, for whatever a source is talking
about.

### Added

Two properties on `plato:Source`, closing
[#11](https://github.com/pelagios/place-attestation-ontology/issues/11):

- `plato:source_timespan` (range `plato:Timespan`): when the document, as a
  witness, was produced. An annal for 921 read in a manuscript written c. 925
  has an attested timespan of 921 and a source timespan of c. 925.
- `plato:derived_from` (range `plato:Source`): this document is a copy,
  transcript, edition, calendar or confirmation of that one. A witness is a
  Source in its own right, and a manuscript sigil is its `authority_title`.

Three properties on `plato:Attestation`, in a new "Occurrence and Form Status"
section, closing
[#12](https://github.com/pelagios/place-attestation-ontology/issues/12) and
[#13](https://github.com/pelagios/place-attestation-ontology/issues/13):

- `plato:occurrence_count` (`xsd:nonNegativeInteger`): how many times the form
  occurs in the cited source, the surveys' "(3 X)".
- `plato:occurrence_context` (range `skos:Concept`): the capacity in which the
  form occurs. Starter concepts `plato:Direct`, `plato:InPersonalName` (the
  surveys' "(p)"), `plato:InFieldName`.
- `plato:form_status` (range `skos:Concept`): whether the form was read in the
  source, chosen by the cited authority, or derived by the project. Starter
  concepts `plato:Attested`, `plato:Headword`, `plato:Normalised`,
  `plato:Reconstructed`.

All three sit on the Attestation rather than on the reusable Name node, because
the same string can be direct in one source and a by-name element in another,
a reading in one and a headword in another. The vocabularies are open SKOS
concepts, as with `plato:geometry_role`, rather than closed enumerations.

The JSON `$defs` follow: `source.timespan`, `source.derivedFrom` (a URI or an
inline source object), `attestation.occurrenceCount`,
`attestation.occurrenceContext` and `attestation.formStatus`.

A `plato:Citation` class, closing
[#7](https://github.com/pelagios/place-attestation-ontology/issues/7): the
qualified form of `plato:sourced_by`, reached from the Attestation by
`plato:has_citation` and pointing at its Authority by `plato:cites`. It carries
`plato:locator` (an uninterpreted string: 'p. 412', 'f. 12v', 'Table VI, col.
3, row 88', as in PeriodO) and `plato:attribution_status` (starter concepts
`plato:AttributionStated`, `plato:AttributionInferred` for an *ibidem* resolved
by an editor). A locator on the Source would force a Source per page, and one
on the Attestation could not say which of two sources it locates within; the
surveys' "1252 Cl et passim to 1346 Harl" is one claim resting on two
citations. `sourced_by` is declared as the property chain `has_citation o
cites`, so it follows from a Citation; data for consumers without a reasoner
should assert it directly as well. The *ibidem* concept was briefly a starter
value of `occurrence_context` in this same unreleased batch; it is a statement
about the citation, not the form, and now lives only on the Citation.

The JSON `$defs` gain `citation` (`source` as URI or inline object, `locator`,
`attributionStatus`) and `attestation.citations` beside `sources`.

New examples: `examples/survey-attestations.ttl`,
`schemas/examples/attestation-centric-survey.json`, `examples/citations.ttl`
and `schemas/examples/attestation-centric-citations.json`.

### Changed

`name.nameType` in `plato.schema.json` is no longer a closed enum. The ontology
had always declared `plato:name_type` as an open string with six suggested
values, and the schema closed the same six; the two now agree on an open list,
with the six as documented starter values. Nothing implements the enum, so no
data changes.

### Fixed

The two older JSON examples gave `gazetteer.contributor` as an inline
contributor object, which the submission profiles reject (they declare it as a
name or URI string). Both now give the contributor's ORCID URI, and all three
JSON examples validate against their profiles.

## 0.3.0

### Renamed

`plato:Thing` is now **`plato:SpatialEntity`**.

`Thing` was chosen as a deliberately empty term able to cover every kind of
entity in the model: settlements, routes, networks, administrative units,
regions, periods and collections. All of these are spatial in some sense, so
`SpatialEntity` states the actual scope without committing the ontology to any
single definition of place. `Thing` read as unfinished and gave users no
indication of what belonged in the class.

The class definition now says so explicitly: an entity whose identity is bound
up with space, whether its extent is attested directly, applies notionally (as
with the region to which a period applies), or is derived from its constituents
(as with a collection). A SpatialEntity need not have any attested geometry, so
lost, imagined and unlocated entities are admissible. What kind of entity it is
remains a matter for Type attestations rather than for the class.

Two properties embedding the old name were renamed with it:

| Was | Now |
|---|---|
| `plato:Thing` | `plato:SpatialEntity` |
| `plato:thing_identifier` | `plato:entity_identifier` |
| `plato:contains_thing` | `plato:contains_entity` |

The JSON serialisations follow: `$defs.thing` is now `$defs.spatialEntity`, the
place-centric submission key `things` is now `spatialEntities`, and the
attestation-centric key `newThings` is now `newSpatialEntities`.

### Removed

`plato:Thing`, `plato:thing_identifier` and `plato:contains_thing` are gone
outright, and so are `plato:uncertainty` and `plato:uncertainty_note`, the
0.2.0 facet-level form of `plato:certainty` and `plato:certainty_note`. The
JSON `uncertainty` and `uncertaintyNote` keys go with them. Values need no
conversion: the scale was always 0.0 completely uncertain to 1.0 certain. They were briefly kept as `owl:deprecated` equivalents on the
reasoning that the namespace is published, but nothing implements PLATO yet and
no data anywhere uses them. Carrying two names for one class from the first
week would have taught readers that the old name remains an option. There is
one name for the class and it is `plato:SpatialEntity`.

The JSON submission keys are likewise not aliased.

### Unchanged

No relationships, cardinalities or semantics were altered. This release is a
renaming only.

## 0.2.0

Initial public release.
