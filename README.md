<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/_static/logo/plato-logo-dark.svg">
  <img src="docs/_static/logo/plato-logo.svg" alt="PLATO: Place Attestation Ontology" width="320">
</picture>

# PLATO — Place Attestation Ontology

[![DOI: 10.5281/zenodo.21688313](badges/doi.svg)](https://doi.org/10.5281/zenodo.21688313)
[![status: experimental](badges/status.svg)](#status)
[![version](badges/version.svg)](CITATION.cff)

<a id="status"></a>**Status: experimental — published for discussion and review; not yet stable.**

## What is this?

An OWL ontology for representing historical place knowledge as **attestations**: bundles of evidence linking SpatialEntities (settlements, routes, networks, administrative units, regions and other entities whose identity is bound up with space) to names, geometries, timespans, types, and sources with full provenance.

The central idea is that the fundamental unit of recorded knowledge is not a *place record* but an *attestation* — a claim that a particular entity had a particular name, geometry, or classification, during a particular period, according to a particular source. SpatialEntities are stable identities, the points on which attestations converge; everything we know about them is layered on through attestations from different people, sources, and periods. Many SpatialEntities are places in the everyday sense and some are not; PLATO defines no Place class and gives the word no prescribed meaning.

➤ **Check or convert a file: [PLATO tools](https://pelagios.org/plato-tools/)**, in your browser; nothing is uploaded. For batch checking, it also runs [from the command line](https://github.com/pelagios/plato-tools#from-the-command-line).

➤ **New to PLATO? [Start with the guide](https://pelagios.org/place-attestation-ontology/guide/)**: why PLATO, the ideas in plain language, and how to organise data about places in an ordinary spreadsheet so that tools implementing PLATO can use it.

➤ **[Read the full ontology documentation](https://pelagios.org/place-attestation-ontology/)**, a generated reference for every class and property.

## Why a new ontology?

This work grows out of the [World Historical Gazetteer](https://whgazetteer.org) project's experience building and maintaining a collaborative historical gazetteer platform. Two earlier formats developed within the [Pelagios Network](https://pelagios.org) — **Linked Places Format (LPF)** and **Linked Traces** — have served the community well but face structural limitations:

- **LPF** is place-centric and GeoJSON-based. It works well for describing places, but it treats names, geometries, and timespans as properties of a place record rather than as independent, reusable, provenance-bearing entities. It cannot natively represent the same name or geometry being shared across multiple places, nor can it model attestations as first-class objects with their own certainty, provenance, and temporal scope.

- **Linked Traces** extended LPF to handle events, routes, and journeys — things that aren't places but involve places. Its use cases are real, but the attestation-based model proposed here accommodates them within a single unified framework rather than requiring a separate format.

PLATO grounds everything in the attestation-as-bundle pattern and defines LPF as its **single-object-attestation profile**: every LPF element corresponds to one attestation linking one entity to one name, type, geometry or related entity. Existing LPF files remain valid, and the simple interchange format and the richer model coexist without either superseding the other. The use cases of Linked Traces are accommodated within the same model. LPF's development continues in its own [repository](https://github.com/LinkedPasts/linked-places-format), under the Pelagios Network's Place Working Group.

For the broader discussion of the architectural and conceptual motivations, see [WHG Discussion #98](https://github.com/WorldHistoricalGazetteer/place/discussions/98).

## Core concepts

The ontology defines a small number of classes and a bundling mechanism that connects them.

### Classes

| Class | Description |
|-------|-------------|
| **SpatialEntity** | A stable, persistent identity: the point on which attestations converge. Covers settlements, routes, networks, administrative units, regions and other entities whose identity is bound up with space; what kind it is comes from Type attestations. Many are places in the everyday sense; PLATO gives "place" no prescribed meaning. |
| **Attestation** | A lightweight bundle node linking a SpatialEntity to a Name, Geometry, Timespan, Type, PropertyValue and/or Source. Carries metadata (certainty, contributor, notes) but no substantive content of its own — its meaning is defined entirely by its outgoing relationships. |
| **Name** | A toponym or appellation. Reusable: the same Name can appear in attestations for different SpatialEntities. |
| **Geometry** | A spatial representation (point, polygon, line). Reusable across attestations and SpatialEntities. |
| **Timespan** | A temporal interval with start/end bounds and precision metadata. Reusable. |
| **Type** | A classification from a controlled vocabulary (typically AAT). Reusable. |
| **PropertyValue** | An attribute that is none of the above — a population, a valuation, a market day. The property is identified by URI in an external vocabulary; the value may be a literal or a structured object. Reusable. |
| **Authority** | Abstract superclass for provenance entities, with subtypes: **Source** (a citable document), **Dataset** (a collection-level authority), **Period** (a named historical period), **RelationType** (a vocabulary entry for entity-to-entity relationships), and **CertaintyLevel**. |
| **Citation** | One attestation's use of one source: the qualified form of `sourced_by`, carrying a locator (page, folio, cell) and whether the attribution was stated or inferred. An attestation resting on two sources has two Citations. |
| **Gazetteer** | A mutable workspace of SpatialEntities and Attestations, owned by a person or team. |
| **Candidate** | A match between two SpatialEntities suggested by software, published in a candidate set and never changed: a claim by no one. A person's answer is an attestation whose identity relation points back to it (`promoted_from`), a match or, in a negated attestation, a denial. |
| **CandidateSet** | The matches one run of matching software suggested for a dataset (`candidates_for`), published together beside the dataset rather than inside it, and frozen once issued. |

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
            ──has_citation────▶ Citation ──cites──▶ Authority, with locator
```

Not every relationship is required in every attestation. A dataset might attest only a name and timespan, or only a geometry, depending on what their source provides.

### Meta-attestations

Because Attestations are first-class entities, they can themselves be the subject of other Attestations. This allows scholars to record that one attestation contradicts, supports, or supersedes another — modelling scholarly discourse and the evolution of historical understanding without special-case logic.

### Entity-to-entity relations

Relationships like "capital_of", "successor_to", or "connected_by_trade_route_to" are modelled as Attestations that link two SpatialEntities via `attests_about` and `relates_to`, with the semantic type specified by a RelationType authority. This keeps the core ontology stable while allowing the vocabulary of historical relationships to grow.

## Examples

The `examples/` directory contains worked examples in Turtle (RDF) format:

- **[constantinople.ttl](examples/constantinople.ttl)** — Constantinople/Istanbul through three historical periods, demonstrating how multiple attestations with different names, geometries, and timespans converge on a single SpatialEntity.
- **[simple-attestation.ttl](examples/simple-attestation.ttl)** — A minimal example: a scholar attesting that a known place appears in their source with a particular name and date.
- **[relation.ttl](examples/relation.ttl)** — An entity-to-entity relationship: attesting that a city was the capital of a political entity during a particular period.
- **[geometry-roles.ttl](examples/geometry-roles.ttl)** — Four geometries for one SpatialEntity — a built extent, a market-place feature point, a proxy locator and a map label anchor — distinguished by `plato:geometry_role`.
- **[property-values.ttl](examples/property-values.ttl)** — Attributes that are neither name, geometry, timespan nor type: a census population, and a fair's trading days as a structured recurrence rule anchored to a moveable feast.
- **[citations.ttl](examples/citations.ttl)** — Reified citations: one printed gazetteer cited at different pages, one claim resting on two sources with a locator in each, an attribution resolved editorially from an *ibidem* (`plato:Citation`, `plato:locator`, `plato:attribution_status`), and a name found only in an edition's commentary (`plato:form_status` `plato:Editorial`).
- **[identity-judgements.ttl](examples/identity-judgements.ttl)** — Identity judgements: a cluster of matches accepted together, then withdrawn, corrected and denied, each with its own provenance, and the candidate set of software suggestions they answer through `promoted_from`.
- **[antonine-routes.ttl](examples/antonine-routes.ttl)**, **[king-john-itinerary.ttl](examples/king-john-itinerary.ttl)**, **[river-idle-network.ttl](examples/river-idle-network.ttl)**, **[datini-network.ttl](examples/datini-network.ttl)** — Parts of the four worked examples of routes, a journey and networks, explained in the guide's [Routes, journeys and networks](https://pelagios.org/place-attestation-ontology/guide/routes/index.html); each whole example is in the JSON examples below and as spreadsheet tables in `schemas/tables/examples/`.
- **[survey-attestations.ttl](examples/survey-attestations.ttl)** — Place-name survey data: a witness dated separately from the text it transmits (`plato:source_timespan`, `plato:derived_from`), a form found only inside a personal name (`plato:occurrence_context`, `plato:occurrence_count`), and an editorial headword and a derived search form distinguished from attested spellings (`plato:form_status`).

The `schemas/examples/` directory contains corresponding examples in JSON format, following the JSON Schema profiles:

- **[place-centric-constantinople.json](schemas/examples/place-centric-constantinople.json)** — Constantinople/Istanbul in place-centric JSON format, with three attestations nested under a single SpatialEntity.
- **[attestation-centric-customs.json](schemas/examples/attestation-centric-customs.json)** — Two attestations from London customs accounts in attestation-centric JSON format, demonstrating how to add evidence about places that already exist elsewhere.
- **[attestation-centric-citations.json](schemas/examples/attestation-centric-citations.json)** — The citations example in attestation-centric JSON format: `citations` with `locator` and `attributionStatus`, and a `formStatus` of `Editorial`.
- **[attestation-centric-survey.json](schemas/examples/attestation-centric-survey.json)** — The survey-attestations example in attestation-centric JSON format: a dated witness with `derivedFrom`, `occurrenceCount`, `occurrenceContext` and `formStatus`.
- **[place-centric-judgements.json](schemas/examples/place-centric-judgements.json)** — Denials, a source's stance, alternative readings and transcription judgements, and a withdrawn import.
- **[candidate-set-judgements.json](schemas/examples/candidate-set-judgements.json)** — The candidate set of the identity-judgements example, in the candidate set profile: two matches suggested by software, each with its minted `#c-` IRI.
- **[attestation-centric-judgements.json](schemas/examples/attestation-centric-judgements.json)** — Two answers to that candidate set, a match and a denial, each pointing at its candidate with `promotedFrom`, from a dataset that lists the set in `candidateSets`.
- **[place-centric-statistics.json](schemas/examples/place-centric-statistics.json)** — Figures from a statistical table, with their dimensions, as explained in the guide's [Statistical tables](https://pelagios.org/place-attestation-ontology/guide/statistics.html).
- **[place-centric-georeference.json](schemas/examples/place-centric-georeference.json)** — Geometries traced from a historical map, citing the map and the georeference they were placed through.
- **[place-centric-antonine.json](schemas/examples/place-centric-antonine.json)**, **[place-centric-king-john.json](schemas/examples/place-centric-king-john.json)**, **[place-centric-river-idle.json](schemas/examples/place-centric-river-idle.json)**, **[place-centric-datini.json](schemas/examples/place-centric-datini.json)** — The four worked examples of routes, a journey and networks, whole.

## JSON Schemas and the JSON-LD context

`schemas/plato.schema.json` holds the shared `$defs` for every object type, and the profiles compose them: the two dataset profiles (`place-centric.schema.json`, `attestation-centric.schema.json`) and the candidate set profile (`candidate-set.schema.json`), which publishes matches suggested by software beside a dataset, never inside it. All are JSON Schema, and they validate a document's shape.

`schemas/plato.context.jsonld` is the JSON-LD 1.1 context that connects those keys to the ontology: it maps every key in the `$defs` and the profiles to its `plato:` term, so that expanding a conformant document with the context yields the RDF graph the ontology describes. Add it as the document's `@context` (intended URL `https://w3id.org/plato/schemas/plato.context.jsonld`) and any JSON-LD processor produces the triples. The document node is the Gazetteer (in a candidate set, the CandidateSet); in place-centric documents, attestations nested under a SpatialEntity are linked by the reverse of `attests_about`. The context's own `$comment` lists what a context cannot do (it adds no `rdf:type` to untyped objects, and it cannot type timespan bounds or convert coordinate arrays to WKT), which a triplifier covers itself.

The starter concepts named by the SKOS-valued properties (`form_status`, `occurrence_context`, `attribution_status`, `geometry_role`, `relative_qualifier`, `has_meta_type`, `source_stance`, `transcription_accuracy`, `transcription_completeness`, `timespan_role`) are declared in the ontology as `skos:Concept`s in concept schemes, so the IRIs data points at resolve to a definition. `RelationType` instances are declared for containment (`plato:ContainedIn`); for routes, itineraries and networks (`plato:MemberOf`, `plato:ConnectedTo`, the directed `plato:LeadsTo`, `plato:BeginsAt`/`plato:EndsAt` for the ends of a directed segment, and `plato:HasEnd` for those of an undirected one); and for the part a place plays in the history of a person, an object or an event, as Linked Traces records it (`plato:BirthplaceOf`, `plato:DeathplaceOf`, `plato:ResidenceOf`, `plato:FindspotOf`, `plato:SettingOf`, `plato:WorkplaceOf`), and for the images and records about it (`plato:DepictedIn`, `plato:SubjectOf`); and for the land of a people (`plato:HomelandOf`). A project declares its own relation types under these with `plato:broader_relation`. Four concepts in `plato:EntityKindScheme` (`plato:TypeRoute`, `plato:TypeItinerary`, `plato:TypeNetwork`, `plato:TypeSegment`), named in a Type's identifier, let any consumer tell those entities from places.

## Relationship to the WHG v4 data model

PLATO formalises the data model developed for [WHG v4](https://docs.whgazetteer.org/content/v4/data-model/introduction.html), which is built on the attestation-as-bundle pattern. The ontology is intended to be platform-independent — it defines the conceptual model from which platform-specific implementations (graph databases, JSON schemas, spreadsheet formats, RDF serialisations) are derived as projections.

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

## Acknowledgements

Development has been supported by the [Institute for Spatial History Innovation (ISHI)](https://www.ishi.pitt.edu/) at the University of Pittsburgh.

## Licence

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
