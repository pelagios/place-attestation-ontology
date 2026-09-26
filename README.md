# PLATO — Place Attestation Ontology

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21688313.svg)](https://doi.org/10.5281/zenodo.21688313)

**Status: Early draft — published for discussion and review. Not yet stable.**

## What is this?

An OWL ontology for representing historical place knowledge as **attestations**: bundles of evidence linking SpatialEntities (settlements, routes, networks, administrative units, regions and other entities whose identity is bound up with space) to names, geometries, timespans, types, and sources with full provenance.

The central idea is that the fundamental unit of contributed knowledge is not a *place record* but an *attestation* — a claim that a particular entity had a particular name, geometry, or classification, during a particular period, according to a particular source. SpatialEntities are stable identities, the points on which attestations converge; everything we know about them is layered on through attestations from different contributors, sources, and periods. A SpatialEntity is not a place: PLATO defines no Place class and does not define the word, which carries several contested meanings in the gazetteer community.

➤ **[Read the full ontology documentation](https://pelagios.org/place-attestation-ontology/)**, a generated reference for every class and property.

## Why a new ontology?

This work grows out of the [World Historical Gazetteer](https://whgazetteer.org) project's experience building and maintaining a collaborative historical gazetteer platform. Two earlier formats developed within the [Pelagios Network](https://pelagios.org) — **Linked Places Format (LPF)** and **Linked Traces** — have served the community well but face structural limitations:

- **LPF** is place-centric and GeoJSON-based. It works well for describing places, but it treats names, geometries, and timespans as properties of a place record rather than as independent, reusable, provenance-bearing entities. It cannot natively represent the same name or geometry being shared across multiple places, nor can it model attestations as first-class objects with their own certainty, provenance, and temporal scope.

- **Linked Traces** extended LPF to handle events, routes, and journeys — things that aren't places but involve places. Its use cases are real, but the attestation-based model proposed here accommodates them within a single unified framework rather than requiring a separate format.

PLATO grounds everything in the attestation-as-bundle pattern and defines LPF as its **single-object-attestation profile**: every LPF element corresponds to one attestation linking one entity to one name, type, geometry or related entity. Existing LPF files remain valid, and the simple interchange format and the richer model coexist without either superseding the other. The use cases of Linked Traces are accommodated within the same model. LPF development sits with the Pelagios Network's Place Working Group.

For the broader discussion of the architectural and conceptual motivations, see [WHG Discussion #98](https://github.com/WorldHistoricalGazetteer/place/discussions/98).

## Core concepts

The ontology defines a small number of classes and a bundling mechanism that connects them.

### Classes

| Class | Description |
|-------|-------------|
| **SpatialEntity** | A stable, persistent identity: the point on which attestations converge. Covers settlements, routes, networks, administrative units, regions and other entities whose identity is bound up with space; what kind it is comes from Type attestations. Not a place — PLATO defines no Place class. |
| **Attestation** | A lightweight bundle node linking a SpatialEntity to a Name, Geometry, Timespan, Type, and/or Source. Carries metadata (certainty, contributor, notes) but no substantive content of its own — its meaning is defined entirely by its outgoing relationships. |
| **Name** | A toponym or appellation. Reusable: the same Name can appear in attestations for different SpatialEntities. |
| **Geometry** | A spatial representation (point, polygon, line). Reusable across attestations and SpatialEntities. |
| **Timespan** | A temporal interval with start/end bounds and precision metadata. Reusable. |
| **Type** | A classification from a controlled vocabulary (typically AAT). Reusable. |
| **PropertyValue** | An attribute that is none of the above — a population, a valuation, a market day. The property is identified by URI in an external vocabulary; the value may be a literal or a structured object. Reusable. |
| **Authority** | Abstract superclass for provenance entities, with subtypes: **Source** (a citable document), **Dataset** (a collection-level authority), **Period** (a named historical period), **RelationType** (a vocabulary entry for entity-to-entity relationships), and **CertaintyLevel**. |
| **Gazetteer** | A mutable workspace of SpatialEntities and Attestations, owned by a contributor or team. |
| **Candidate** | An algorithm-generated match candidate between two SpatialEntities — explicitly *not* an Attestation until confirmed by a human reviewer. |

### The bundling mechanism

An Attestation bundles entities together through outgoing relationships:

```
Attestation ──attests_about──▶ SpatialEntity
            ──attests_name───▶ Name
            ──attests_geometry▶ Geometry
            ──attests_timespan▶ Timespan
            ──attests_type────▶ Type
            ──attests_property▶ PropertyValue
            ──sourced_by──────▶ Authority (Source)
```

Not every relationship is required in every attestation. A contributor might attest only a name and timespan, or only a geometry, depending on what their source provides.

### Meta-attestations

Because Attestations are first-class entities, they can themselves be the subject of other Attestations. This allows scholars to record that one attestation contradicts, supports, or supersedes another — modelling scholarly discourse and the evolution of historical understanding without special-case logic.

### entity-to-entity relations

Relationships like "capital_of", "successor_to", or "connected_by_trade_route_to" are modelled as Attestations that link two SpatialEntities via `attests_about` and `relates_to`, with the semantic type specified by a RelationType authority. This keeps the core ontology stable while allowing the vocabulary of historical relationships to grow.

## Examples

The `examples/` directory contains worked examples in Turtle (RDF) format:

- **[constantinople.ttl](examples/constantinople.ttl)** — Constantinople/Istanbul through three historical periods, demonstrating how multiple attestations with different names, geometries, and timespans converge on a single SpatialEntity.
- **[simple-attestation.ttl](examples/simple-attestation.ttl)** — A minimal example: a scholar attesting that a known place appears in their source with a particular name and date.
- **[relation.ttl](examples/relation.ttl)** — A entity-to-entity relationship: attesting that a city was the capital of a political entity during a particular period.
- **[geometry-roles.ttl](examples/geometry-roles.ttl)** — Four geometries for one SpatialEntity — a built extent, a market-place feature point, a proxy locator and a map label anchor — distinguished by `plato:geometry_role`.
- **[property-values.ttl](examples/property-values.ttl)** — Attributes that are neither name, geometry, timespan nor type: a census population, and a fair's trading days as a structured recurrence rule anchored to a moveable feast.
- **[survey-attestations.ttl](examples/survey-attestations.ttl)** — Place-name survey data: a witness dated separately from the text it transmits (`plato:source_timespan`, `plato:derived_from`), a form found only inside a personal name (`plato:occurrence_context`, `plato:occurrence_count`), and an editorial headword and a derived search form distinguished from attested spellings (`plato:form_status`).

The `schemas/examples/` directory contains corresponding examples in JSON format, following the JSON Schema submission profiles:

- **[place-centric-constantinople.json](schemas/examples/place-centric-constantinople.json)** — Constantinople/Istanbul in place-centric JSON format, with three attestations nested under a single SpatialEntity.
- **[attestation-centric-customs.json](schemas/examples/attestation-centric-customs.json)** — Two attestations from London customs accounts in attestation-centric JSON format, demonstrating the flexible model for contributing evidence about existing SpatialEntities.
- **[attestation-centric-survey.json](schemas/examples/attestation-centric-survey.json)** — The survey-attestations example in attestation-centric JSON format: a dated witness with `derivedFrom`, `occurrenceCount`, `occurrenceContext` and `formStatus`.

## Relationship to the WHG v4 data model

PLATO formalises the data model developed for [WHG v4](https://docs.whgazetteer.org/content/v4/data-model/introduction.html), which implements the attestation-as-bundle pattern in ArangoDB. The ontology is intended to be platform-independent — it defines the conceptual model from which platform-specific implementations (graph databases, JSON schemas, spreadsheet formats, RDF serialisations) are derived as projections.

## How to contribute

PLATO is at an early stage. We welcome review, critique, and contributions:

- **Open an Issue** for questions, suggestions, or problems.
- **Start a Discussion** for broader conceptual questions.
- **Submit a Pull Request** for concrete changes to the ontology or examples.

## How to cite

Every tagged release is archived on Zenodo. To cite PLATO, use the **concept DOI**, which always resolves to the latest version:

> Gadd, Stephen, and Pelagios Network Place Working Group. 2026. *PLATO — Place Attestation Ontology*. Zenodo. https://doi.org/10.5281/zenodo.21688313

To cite one specific release instead, take that version's own DOI from the **Versions** panel of the [Zenodo record](https://doi.org/10.5281/zenodo.21688313). Per-version DOIs are deliberately not listed here: they don't exist until the release is published, so quoting them in the README would archive a placeholder in every release.

Machine-readable citation metadata is in [CITATION.cff](CITATION.cff).

## Developed by

The [Pelagios Network](https://pelagios.org) Place Working Group, led by the [Institute for Spatial History Innovation (ISHI)](https://www.ishi.pitt.edu/) at the University of Pittsburgh.

## Licence

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
