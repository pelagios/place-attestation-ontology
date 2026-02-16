# PLATO — Place Attestation Ontology

**Status: Early draft — published for discussion and review. Not yet stable.**

## What is this?

An OWL ontology for representing historical place knowledge as **attestations**: bundles of evidence linking places (and other historical entities) to names, geometries, timespans, types, and sources with full provenance.

The central idea is that the fundamental unit of contributed knowledge is not a *place record* but an *attestation* — a claim that a particular place had a particular name, geometry, or classification, during a particular period, according to a particular source. Places are stable identities; everything we know about them is layered on through attestations from different contributors, sources, and periods.

## Why a new ontology?

This work grows out of the [World Historical Gazetteer](https://whgazetteer.org) project's experience building and maintaining a collaborative historical gazetteer platform. Two earlier formats developed within the [Pelagios Network](https://pelagios.org) — **Linked Places Format (LPF)** and **Linked Traces** — have served the community well but face structural limitations:

- **LPF** is place-centric and GeoJSON-based. It works well for describing places, but it treats names, geometries, and timespans as properties of a place record rather than as independent, reusable, provenance-bearing entities. It cannot natively represent the same name or geometry being shared across multiple places, nor can it model attestations as first-class objects with their own certainty, provenance, and temporal scope.

- **Linked Traces** extended LPF to handle events, routes, and journeys — things that aren't places but involve places. Its use cases are real, but the attestation-based model proposed here accommodates them within a single unified framework rather than requiring a separate format.

PLATO aims to **unify and supersede both LPF and Linked Traces** by grounding everything in the attestation-as-bundle pattern.

For the broader discussion of the architectural and conceptual motivations, see [WHG Discussion #98](https://github.com/WorldHistoricalGazetteer/place/discussions/98).

## Core concepts

The ontology defines a small number of classes and a bundling mechanism that connects them.

### Classes

| Class | Description |
|-------|-------------|
| **Thing** | A stable, persistent identity — typically a place, but generalised to accommodate routes, networks, administrative units, and other historical entities related to place. |
| **Attestation** | A lightweight bundle node linking a Thing to a Name, Geometry, Timespan, Type, and/or Source. Carries metadata (certainty, contributor, notes) but no substantive content of its own — its meaning is defined entirely by its outgoing relationships. |
| **Name** | A toponym or appellation. Reusable: the same Name can appear in attestations for different Things. |
| **Geometry** | A spatial representation (point, polygon, line). Reusable across attestations and Things. |
| **Timespan** | A temporal interval with start/end bounds and precision metadata. Reusable. |
| **Type** | A classification from a controlled vocabulary (typically AAT). Reusable. |
| **Authority** | Abstract superclass for provenance entities, with subtypes: **Source** (a citable document), **Dataset** (a collection-level authority), **Period** (a named historical period), **RelationType** (a vocabulary entry for Thing-to-Thing relationships), and **CertaintyLevel**. |
| **Gazetteer** | A mutable workspace of Things and Attestations, owned by a contributor or team. |
| **SoftLink** | An algorithm-generated match candidate between two Things — explicitly *not* an Attestation until confirmed by a human reviewer. |

### The bundling mechanism

An Attestation bundles entities together through outgoing relationships:

```
Attestation ──attests_about──▶ Thing
            ──attests_name───▶ Name
            ──attests_geometry▶ Geometry
            ──attests_timespan▶ Timespan
            ──attests_type────▶ Type
            ──sourced_by──────▶ Authority (Source)
```

Not every relationship is required in every attestation. A contributor might attest only a name and timespan, or only a geometry, depending on what their source provides.

### Meta-attestations

Because Attestations are first-class entities, they can themselves be the subject of other Attestations. This allows scholars to record that one attestation contradicts, supports, or supersedes another — modelling scholarly discourse and the evolution of historical understanding without special-case logic.

### Thing-to-Thing relations

Relationships like "capital_of", "successor_to", or "connected_by_trade_route_to" are modelled as Attestations that link two Things via `attests_about` and `relates_to`, with the semantic type specified by a RelationType authority. This keeps the core ontology stable while allowing the vocabulary of historical relationships to grow.

## Examples

The `examples/` directory contains worked examples in Turtle (RDF) format:

- **[constantinople.ttl](examples/constantinople.ttl)** — Constantinople/Istanbul through three historical periods, demonstrating how multiple attestations with different names, geometries, and timespans converge on a single Thing.
- **[simple-attestation.ttl](examples/simple-attestation.ttl)** — A minimal example: a scholar attesting that a known place appears in their source with a particular name and date.
- **[relation.ttl](examples/relation.ttl)** — A Thing-to-Thing relationship: attesting that a city was the capital of a political entity during a particular period.

The `schemas/examples/` directory contains corresponding examples in JSON format, following the JSON Schema submission profiles:

- **[place-centric-constantinople.json](schemas/examples/place-centric-constantinople.json)** — Constantinople/Istanbul in place-centric JSON format, with three attestations nested under a single Thing.
- **[attestation-centric-customs.json](schemas/examples/attestation-centric-customs.json)** — Two attestations from London customs accounts in attestation-centric JSON format, demonstrating the flexible model for contributing evidence about existing places.

## Relationship to the WHG v4 data model

PLATO formalises the data model developed for [WHG v4](https://docs.whgazetteer.org/content/v4/data-model/introduction.html), which implements the attestation-as-bundle pattern in ArangoDB. The ontology is intended to be platform-independent — it defines the conceptual model from which platform-specific implementations (graph databases, JSON schemas, spreadsheet formats, RDF serialisations) are derived as projections.

## How to contribute

PLATO is at an early stage. We welcome review, critique, and contributions:

- **Open an Issue** for questions, suggestions, or problems.
- **Start a Discussion** for broader conceptual questions.
- **Submit a Pull Request** for concrete changes to the ontology or examples.

## Developed by

The [Pelagios Network](https://pelagios.org) Place Working Group, led by the [Institute for Spatial History Innovation (ISHI)](https://www.ishi.pitt.edu/) at the University of Pittsburgh.

## Licence

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
