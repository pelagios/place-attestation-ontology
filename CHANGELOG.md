# Changelog

All notable changes to PLATO are recorded here. The ontology is an early draft.

Until 0.5.0 it had no implementations and no data published in its namespace,
so a renamed term was removed outright rather than kept as a deprecated
equivalent. That is no longer so: PLATO tools implements it, and DEEP (the
digitised English Place-Name Society survey) publishes its data in PLATO's
namespace. So from 0.5.0 on, a term that is renamed or withdrawn is kept,
marked `owl:deprecated` with a pointer to its replacement, for at least one
release before it is removed. The changes recorded under 0.5.0 and earlier
were made under the earlier policy.

## Unreleased

### Changed

- The append-only rule of a published Gazetteer now says what an
  attestation's content is: its facets and citations, whether or not they
  have IRIs of their own. A Name shared under its IRI is not re-spelt once
  published, since that would change every attestation pointing to it. The
  SpatialEntities and Authorities attestations are about or cite may still be
  corrected and enriched. Found while building PLATO tools' version check,
  which treats them so.
- Every attestation in a published Gazetteer should have a permanent IRI
  (`@id`): a correction or withdrawal must point to its target. A
  recommendation for now, in the ontology, the JSON Schema's description and
  the guide, meant to become a requirement. The spreadsheet tables have no
  column for one, so it applies to data published as JSON or RDF. The
  examples that say they are published now give every attestation one.
- The IRIs of a dataset made from the spreadsheet tables are now normative,
  taken from the ones PLATO tools makes. The base is the one given for a
  conversion, else the about sheet's `base_uri`, with a `/` added when it
  ends in neither `/` nor `#`. A place is `<base>place/<place_id>` and a
  source `<base>source/<source_id>`, with every character of the identifier
  other than RFC 3986's unreserved characters (`A-Z a-z 0-9 - . _ ~`)
  percent-encoded as UTF-8, so `! ' ( ) *` too; identifiers SHOULD use
  unreserved characters only. The Gazetteer is named by `dataset_uri`, or by
  the base (with its `/`) when that is empty. Until now the table
  definitions left minting them to the platform, so two tools could give the
  same tables different IRIs. CSVW cannot build an IRI from a cell of
  another table, so a CSVW processor alone still gives places and sources
  IRIs relative to their files (`places.csv#bristol`); that graph is for
  validating the tables, and the table definitions, the sheet reference and
  the guide now say so. In it, the Gazetteer is now named by `dataset_uri`
  (the about table's `aboutUrl`) rather than `about.csv#dataset`; with
  `dataset_uri` empty, it is named `about.csv` itself, since a URI template
  has no fallback value.
- The table definitions no longer write `dataset_uri` as a
  `dcterms:identifier` literal on the Gazetteer, as they have since 0.7.0:
  it is the Gazetteer's IRI instead, so the literal only repeated it.

- The about sheet's `creator` cell now takes an author's name and address
  together, as `Name <address>` (`Stephen Gadd
  <https://orcid.org/0000-0003-3060-0181>`), as well as an address alone or
  a name alone, several separated by `;` as before. Until now a name and its
  ORCID could not be paired in the tables: names went in `creator_name`, so
  converting gave a name-only author and an address-only author where the
  JSON has one author with both. The column is now text with a pattern
  (`format`) rather than `anyURI`, since `Name <address>` is not an address.
  CSV on the Web can split the cell but not parse it, so a CSVW processor
  writes each author as the text of the cell (`dcterms:creator "Stephen Gadd
  <https://orcid.org/…>"`); PLATO tools writes `dcterms:creator` with the
  address as a link, and that link's `foaf:name`, as from JSON. The customs
  and survey examples now give their author in this form. JSON is unchanged:
  a creator object already pairs `@id` and `name`.

- `plato:certainty`, `plato:fuzziness`, `plato:relative_bearing`,
  `plato:relative_distance`, `plato:identity_certainty`, `plato:precision_km`
  and `plato:similarity_score` no longer declare `rdfs:range xsd:float`. No
  one XSD type fits what writes PLATO: JSON-LD gives a whole number
  `xsd:integer` and any other `xsd:double`, the spreadsheet tables give
  `xsd:decimal`, and the examples used decimals and, once, `xsd:float`. In
  OWL 2 those value spaces are disjoint, so the declared range made data
  giving these numbers inconsistent for a reasoner that applied it. Any XSD
  numeric datatype is now accepted, within the bounds each property states
  (0 to 1 for the certainties and fuzziness), and each comment and the
  guide's linked-data page (*Numbers*) say so. PLATO tools writes a whole
  number as `xsd:integer` and any other as `xsd:double`. `plato:similarity_score`
  gains a comment, and `plato:precision_km` is labelled in kilometres.

- `plato:derived_from` now says what it already meant in `plato:computed`: a
  Source may be derived from another as a copy or edition of it, or as a
  work made from it (a count taken from a register, the georeference of a
  map). How it is cited says which: a copy as the evidence, a georeference as
  the method used.

- The georeference pattern in `plato:Geometry` now says which role a traced
  map symbol takes: its position is a `plato:RepresentativePoint`, unless the
  map shows the specific feature (a church drawn as such), when it is a
  `plato:FeaturePoint`. A fort's symbol on a small-scale map stands for the
  fort rather than depicting any part of it, so the traced Fort Duquesne in
  `schemas/examples/place-centric-georeference.json` is now a
  `RepresentativePoint` (still of approximate precision), not a
  `FeaturePoint`. The `geometry_role` column's description says so too.

### Added

- **An editorial form.** `plato:Editorial` joins the FormStatusScheme: a form
  written by the editors of the cited edition in their own words
  (commentary, apparatus, notes), not one the edited source contains. A
  scope note says to use it when the citation is to an edition and the name
  occurs in the editors' text; it says nothing about whether the name is
  attested elsewhere, and `Attested` remains the default. Without it, a name
  converted from an editor's note, with no form status, read as the source's
  own, and no existing concept fitted: a headword is the form an entry is
  filed under, not a mention. The tables' `form_status` accepts it, the
  JSON Schema's `formStatus` description names it, the citations examples
  (Turtle and attestation-centric JSON) show it on an invented edition's
  commentary, and the guide's glossary and survey example explain it. The
  guide's vocabulary pages now show a concept's scope note after its
  definition.

- Both profiles take an optional `@context` (an address, which may be
  relative, an object, or a list of them), so a document can carry PLATO's
  context, as the guide and the README tell readers to do; any other unknown
  key is still refused. Without it, the guide's own JSON example failed
  validation.
- A guide page, *Checking, converting and comparing*, on what PLATO tools
  checks, what each format keeps when converting, and what the version check
  reports.
- A section of that page, *Publishing your dataset*, on preparing a dataset
  for publishing with PLATO tools: the report on its description and the
  deposit files (`.zenodo.json`, `CITATION.cff`, DataCite JSON), permanent
  addresses for attestations (`<base>place/<id>#a-<hash>`), a website for
  GitHub Pages with the workflow that publishes it, and the rules for a
  w3id.org address; what `published` commits a dataset to; and why a
  github.io base is not a permanent address. The linked-data page and the
  guide's home page point to it.

- How a geometry traced from a historical map records the georeference it
  was placed through (issue #15), with no new term. The attestation cites the
  map as the evidence (`cito:citesAsEvidence`), with the canvas as the
  locator (and `#xywh=` for a region), and cites the IIIF Georeference
  Annotation as a Source of its own, `derivedFrom` the map, with
  `cito:usesMethodIn`. The transformation and the number of control points go
  in the attestation's notes, since the annotation can be edited later. Such
  a geometry is attested, not `computed`: software fits the transformation,
  but the geometry is evidence of what the map shows. The pattern is given in
  `plato:Geometry`, and shown in a new example,
  `schemas/examples/place-centric-georeference.json`, on a real map and a
  real Allmaps annotation. A structured property for the transformation can
  follow if a consumer needs to query by it.

### Deprecated

- The about sheet's `creator_name` column, replaced by `creator`, which now
  takes a name alone as well as a name with its address. It stays for one
  release under the deprecation policy and is to be withdrawn in the release
  after; the survey example keeps one name in it, so that both stay tested.

### Fixed

- The profiles were titled "Submission Profile", and the place-centric one
  called itself "the successor to LPF". They are now the place-centric and
  attestation-centric profiles, describing a document, and LPF is described as
  PLATO's single-object-attestation profile, still valid as it is. The
  attestation-centric description gives the meta-attestation exception to
  `about`. Descriptions only.
- The vocabularies page named the attribution column as the only one whose
  start the table definitions add. So do `stance`,
  `transcription_accuracy` and `transcription_completeness`.

- The invented ORCIDs in the examples failed ORCID's check digit (ISO 7064
  MOD 11-2), so any checker that tests it rightly rejected them. They are now `0000-0002-1825-0097`, the fictitious
  Josiah Carberry whom ORCID's own documentation uses, in the Turtle and the
  JSON examples alike.
- The relation example (`examples/relation.ttl`) named two real historians as the contributors making its claims; they are now fictitious (Josiah Carberry, with ORCID's test ORCID, and Wilhelmina Placeholder, with none), and Allsen's book stays cited only as a source.
- The relation example no longer attributes its meta-attestation's argument about Shangdu to Allsen: it is now the fictitious Wilhelmina Placeholder's, marked as a hypothetical example and citing Allsen (2001) as its source; and the contributor carrying ORCID's test ORCID in the simple-attestation and Constantinople examples is now named Josiah Carberry, the fictitious person it belongs to, rather than another invented name.
- The core schema's description of `about` still said it was required in
  every attestation-centric attestation; it now gives the meta-attestation
  exception that 0.7.1 made in the attestation-centric schema. Description
  only: validation is unchanged.

## 0.7.1

Found by WHG's final pass on its documentation against 0.7.0, and a logo.

### Added

- A logo: a map pin (a place) whose head carries the rings of the
  Mediterranean eye charm, with the guide's attestation gold as the ring
  between white and blue. `docs/_static/logo/` holds the mark, a one-colour
  version, the lockup with the name for light and dark grounds (lettering
  as outlines, so no font is needed), and favicons;
  `scripts/build_logo.py` builds them from the guide's fonts. The README
  opens with it, and the guide uses it as its favicon and in its sidebar.

### Fixed

- A meta-attestation need not say what it is about: its target does. 0.7.0
  said so only here; the attestation-centric schema still required `about`
  on every attestation. It now requires `about` or `meta`, and
  `plato:meta_attestation_about` states the rule.
- `plato:attests_timespan` says that the attested timespan is no wider than
  the source can witness, so for a source that shows a name in use only in
  its own day it coincides with the source's date while remaining the
  claim's. The Constantinople example's notes said the timespan was "not the
  span in which the name was used", which read as contradicting that.
- The Constantinople example's Turtle and JSON now agree on their creation
  dates and the GeoNames identity's basis.
- `examples/identity-judgements.ttl` shared the IRI of its denial with the
  different denial in `place-centric-judgements.json`, so a combined graph
  gave one attestation two sources; its IRI is now its own, and its header
  no longer claims the JSON holds the same judgements.

## 0.7.0

Dataset metadata, from a review of PLATO against the FAIR principles, and a
licence correction.

### Added

- Describing a dataset, in the vocabularies catalogues read: `creator`
  (`dcterms:creator`, the authors to cite, each an address, a name or both;
  `contributor`, `plato:gazetteer_owner`, stays the owner), `keywords`
  (`dcat:keyword`), `spatial` (`dcterms:spatial`), `temporal`
  (`dcterms:temporal`, a `dcterms:PeriodOfTime` with `dcat:startDate` and
  `dcat:endDate`), `landingPage` (`dcat:landingPage`) and `uriSpace`
  (`void:uriSpace`, the base of the dataset's entity addresses). All
  optional. No new PLATO terms.
- A tenth sheet, `about`: one row describing the dataset, with those fields,
  its title, licence, version and status, and `base_uri`, from which PLATO
  tools makes every place's permanent address. In the tables, `creator` and
  `spatial` hold addresses as text, since CSV on the Web cannot make several
  links from one cell; PLATO tools turns them into links. Exactly one row,
  which PLATO tools checks.
- The ontology describes itself for FAIR: `owl:versionIRI`,
  `owl:priorVersion`, `dcterms:issued`, the concept DOI and a citation,
  keywords, and `rdfs:isDefinedBy` on every term.
- `plato:DepictedIn` and `plato:SubjectOf`: a place shown in a photograph,
  map or drawing, or the subject of an archival file, report or
  publication, each named by its address as an outside target. Linking a
  place to what a collection holds about it is what lets the collection be
  explored by place; it is a statement with its own source, not a citation.
  Raised by the draft Pelagios partnership with the British Institute at
  Ankara, whose archives and photographic collections need it. Each release's ontology is
  published at `releases/X.Y.Z/`, where `https://w3id.org/plato/X.Y.Z`
  resolves.

- `plato:attests_identity` (JSON `identities` on an attestation): identity
  relations asserted in one act, such as accepting a cluster of matches, are
  bundled by one attestation, which gives them one provenance and is
  withdrawn or amended as a unit by the existing Retracts and Supersedes.
  With `negated`, bundling one `exactMatch`, it says two entities are not
  the same, so that disagreement accumulates as well as agreement. Decided
  by Stephen with the WHG team: clusters stay out of PLATO (they are query
  results), and accepting one is evidence.
- A type's vocabulary and version: JSON `scheme` (`skos:inScheme`, a Type
  being a `skos:Concept`) and `schemeVersion` (new `plato:scheme_version`),
  tables `type_scheme` and `type_scheme_version`. For vocabularies without
  IRIs of their own, and for those whose terms change meaning between
  versions (ecoregions of 2001 and 2017), as WHG's regions work needs. The
  version sits on the Type, not the scheme: a scheme's IRI is shared by
  every dataset, and versions recorded on it could not be told apart.
  A Type node stands for one dataset's use of a concept: its IRI is the
  dataset's own or none, never the concept's, which would merge every
  dataset's versions onto it one level down (found by the WHG review). The
  four route and network kinds, declared in 0.6.0 as Type instances, are
  therefore concepts in `plato:EntityKindScheme` instead, with the same IRIs.
  `type_identifier` now says it should be a full IRI, never a bare code
  (WHG's index held 54 million of those), with a source's own category
  left as a label.
- `plato:match_parameters`: the settings that produced a Candidate's score,
  so it can be reproduced.

### Clarified

- An IdentityRelation is one attributed claim among many, never a canonical
  fact: platforms must not materialise identity relations into merged
  records or minted identifiers, nor let one outweigh contrary evidence. A
  consumer may chain `exactMatch` relations only within one attestation, and
  never chain `closeMatch`, `related` or `unspecified`: A~B and B~C asserted
  by different people is nobody's assertion that A~C.
- A Gazetteer may attest evidence about SpatialEntities defined in other
  Gazetteers, by IRI, without redefining them; that changes neither the
  entity's identity nor its owner, and in JSON uses the attestation-centric
  profile. A place-centric document lists only its own entities
  (`plato:contains_entity` now says "defines"). A published Gazetteer's
  append-only rule covers its own attestations only.
- A curated collection of places is a Gazetteer, not a SpatialEntity; the
  SpatialEntity comment's "(as with a collection)" now reads "(as with a
  route or a network)".
- `plato:Candidate` covers suggested matches in general, such as
  reconciliation review, not only the retired PLACE clustering pipeline.
- A meta-attestation need not say what it is about: its target does.

### Changed

- A published dataset (`status` `published`) must state its licence, in
  JSON and in the about sheet. Drafts need not. DEEP already does.
- Sets of tables made with the 0.6.0 template need an `about.csv` with at
  least a title.
- `LICENSE.md` held the CC BY-NC 4.0 legal code, contradicting every other
  statement of PLATO's licence; it is now CC BY 4.0, as PLATO has always
  been declared.
- `plato:geo_json` has range `rdf:JSON`, not `xsd:string`. The JSON-LD
  context has always mapped `geojson` with `@type: @json`, the only way a
  GeoJSON object becomes a literal, so every converted dataset already
  carries `rdf:JSON`; the ontology now says so.

### Fixed

Found by WHG's rewrite of its documentation against PLATO:

- `type_identifier` is written as a literal typed `xsd:anyURI`, never an
  IRI object, as the context and the tables produce it; the comment says
  so, and `examples/constantinople.ttl` now uses that form.
- `start_precision` and `end_precision` list `day` and `month`, as the JSON
  Schema always has.
- `name_embedding` no longer says "typically 256-dimensional": the model and
  dimension are the producer's, and must be stated in the gazetteer's
  description, since vectors from different models cannot be compared.
- The Constantinople example dated each name to a whole historical period
  (330 to 1453, 1453 to 1923) while citing sources that cannot witness such
  spans, and its Turtle and JSON versions disagreed. Both now use the same
  three sources (Herodotus, the Notitia Urbis Constantinopolitanae,
  GeoNames), each dated to what it witnesses, with only the geometry a
  source gives; the Notitia's Latin form is attested as written.
- `plato:Geometry` said to put different kinds of geometry in separate
  attestations, which the schema (an array of geometries) and
  `examples/geometry-roles.ttl` never required. It now says what they do: one
  attestation may attest several geometries when one source gives them all,
  each with a role where they depict different things; a geometry from
  another source is another attestation. A GeometryCollection is not
  accepted, and the schema now says so plainly rather than "not supported in
  some implementations".
- `examples/relation.ttl` uses `plato:Refines` rather than a concept of its
  own, and the customs example `https://w3id.org/plato#Near` rather than
  the retired `http://w3id.org/plato/vocab#` namespace.

### Examples

- `examples/identity-judgements.ttl`: a cluster of suggested matches
  accepted in one act (`plato:attests_identity`, `promoted_from` Candidates
  with `match_parameters`), that act withdrawn with `plato:Retracts`, the
  corrected matches, and a denial (`plato:negated`).

### Guide

- A page on bringing Recogito annotations into PLATO, with PLATO tools: what
  each part of an annotation becomes, and what is left out and why.

## 0.6.0

Two gaps found in encoding the markets corpus (the CAMPOP market and fair
records: Blome's Britannia of 1673, Everitt's survey of 1967, and the
project's register of sources), both checked against 0.5.0.

Routes, itineraries and networks, which WHG will support and for which it
needs modelling examples, following the WHG v4 patterns and agreed with the
WHG documentation. PLATO had `plato:sequence` and `plato:connection_metadata`
for them, but no relation types to use them with, and nothing had tested
either. The same change lets a place be related to people, objects and events
described elsewhere, which is what Linked Traces records.

### Added

- `plato:source_stance` (JSON `sourceStance`, tables `stance`): how firmly
  the source itself asserts what an attestation records, with a starter
  scheme `plato:SourceStanceScheme` of `plato:StanceAsserted` (the default),
  `plato:StanceReported` (passed on without vouching: "it is said", "as
  Cambden noteth"), `plato:StanceTentative` (hedged) and `plato:StanceDoubted`
  (raised and left unsettled). Blome passes on 118 of 7,435 statements and
  hedges 27; Everitt leaves 65 places undecided. Nothing could record this.
  `certainty` is the encoder's confidence, and an editor may be quite sure a
  source hedged; `attribution_status` is about whether the source is named;
  `negated` is a denial, and doubt is not one. Like `negated` it qualifies the
  whole attestation. Unlike it, no consumer is required to drop an attestation
  it cannot express, since reading a report as an assertion overstates the
  source but does not invert it; converters should report the loss.
- A licence on a source (JSON `licence` on `source`, tables `licence` on
  sources), as `dcterms:license`, exactly as on the gazetteer. The markets
  project admits evidence by its licence (13 sources under three licences),
  and the licence could not travel with the data, so a consumer could not see
  that a cited source was licence-restricted.
- Relation types for routes, itineraries and networks: `plato:MemberOf` (a
  station, stop or member of a route, itinerary or network, ordered by
  `plato:sequence`), `plato:ConnectedTo` (undirected) and `plato:LeadsTo`
  (directed, from the attestation's subject to its target);
  `plato:BeginsAt` and `plato:EndsAt` for the ends of a directed segment, and
  `plato:HasEnd` for those of an undirected one. A segment's ends never use
  `ConnectedTo`, which always joins two places, so a walk across a network
  never takes two steps for one. Direction is
  carried by the relation type alone, never by a qualifier, so that a consumer
  filtering on the type cannot misread a one-way connection as two-way.
- `plato:broader_relation`: a project's own relation type ('flows into',
  'carries post to') names the starter type it narrows, so a consumer that
  knows only `LeadsTo` still follows it the right way. `skos:broader` could
  not be used, because a RelationType is an Authority, not a skos:Concept.
- `plato:declares_relation_type` (JSON `relationTypes`, a document-level
  array beside `dataSets`): the relation types a document declares for its
  own use, each with `label`, `inverseLabel` and `broaderRelation`. Without
  it a project could use its own relation type in JSON but not declare it,
  although the guide said it could; only RDF could. The WHG documentation
  review found the gap. It gets a link of its own, not `dcterms:hasPart`,
  which already joins a gazetteer to its statistical tables.
- Four Types, `plato:TypeRoute`, `plato:TypeItinerary`, `plato:TypeNetwork` and
  `plato:TypeSegment`, so that any consumer can tell these entities from
  places. A segment (a leg of a road, a reach of a river) is a SpatialEntity
  of its own, and platforms may leave segments out of lists of places.
- Relation types for places in the history of people, objects and events, as
  Linked Traces records them: `plato:BirthplaceOf`, `plato:DeathplaceOf`,
  `plato:ResidenceOf`, `plato:FindspotOf`, `plato:SettingOf` and
  `plato:WorkplaceOf` (the relational keywords WHG's own collections use;
  the rest of their keywords are themes, not relations), with
  `plato:related_label` (JSON `relatedLabel`, tables `related_label`) to name
  a target described elsewhere.
- `plato:duration` (JSON `duration` on a timespan, tables `duration` on the
  relations sheet): how long something lasted, as an `xsd:duration`, with or
  without dates. A source often gives a length and no dates ("where I staid
  6 weekes"), and an itinerary needs it to tell a long stay from a night's
  lodging. `xsd:duration` has no weeks, so six weeks is `P42D`.
- `plato:computed` (JSON `computed`, on an attestation or in any
  `qualification`): a value worked out by software, such as an itinerary's
  span from its stops. It is not evidence, and a consumer must not import it
  as an attestation. WHG will export such values, and without the marker a
  re-import would turn them into evidence no source gave.
  It marks what can be derived again from the same data; a figure a project
  works out from its sources and publishes (a count of letters) is attested,
  citing that work as a source derived from the material.

### Deprecated

- `plato:licence`, replaced by `dcterms:license` (`dcterms:isReplacedBy`). It
  could be given only to a Dataset, had no route in PLATO JSON, and was a
  literal where the gazetteer's licence is an IRI. It stays for one release
  under the deprecation policy. No published data uses it.

### Removed

- `plato:connection_metadata`, removed outright, as a deliberate exception to
  the deprecation policy. It was an opaque string whose format each project
  chose, with no JSON key and no spreadsheet column, and no data, tool or
  platform used it (WHG never implemented it). What it was for is now carried
  in the open: the kind of connection and its direction by the relation type,
  and figures such as goods, frequency or journey time as PropertyValues, each
  with its own source and date.

### Clarified

- `plato:certainty_level` is the same confidence as `plato:certainty`, the
  contributor's or editor's. Its comment had said "when a source or a dataset
  states certainty in words", which left open whose certainty it was.
- `plato:sequence` sits on the attestation about a member, which relates_to
  the route, itinerary or network with `plato:MemberOf`, as in WHG v4. Its
  comment had said the attestation was about the route, which leaves the
  number nothing to order. Equal numbers are alternatives; no number means no
  order is given.
- `plato:relates_to` no longer has `rdfs:range plato:SpatialEntity`. Its
  target may be a person, object or event described elsewhere, which the range
  would have inferred to be a SpatialEntity.

### Changed

- The spreadsheet tables gain two columns: `stance` after `denied` on every
  attestation sheet, and `licence` after `derived_from` on sources. Sheets
  made with the earlier template need the two columns added, empty if unused.
- The relations sheet gains `related_uri`, `related_label` and `sequence`
  after `related_place_id` (which is now optional), and `duration` after
  `to`. A row relates its place either to another place or, in
  `related_uri`, to something described elsewhere, and must fill in exactly
  one of the two. CSVW cannot state that rule, so rdf-tabular does not check
  it; PLATO tools does, as an error. `relation_type` takes the new relation
  types.
- A ninth sheet, `connections`, for figures about a connection between two
  places (letters sent from one city to another, a journey time): one link
  and one figure per row, becoming a `ConnectedTo` or `LeadsTo` attestation
  with one PropertyValue. A relations row cannot carry a figure, because a
  row may not create an optional node. Sets of tables made with the earlier
  template need an empty `connections.csv`, headings only, and the four new
  relations columns. The sheets take only PLATO's own relation types; a
  project's own, declared with `broader_relation`, need JSON or RDF.

## 0.5.0

### Added

The guide, the README and the linked-data and JSON pages point to
[PLATO tools](https://pelagios.org/plato-tools/), which checks and converts PLATO data in the browser
(spreadsheet tables, PLATO JSON and JSON Lines, RDF, Linked Places Format v1). PLATO tools also runs from the command line, for checking and converting
many files at once; the guide's spreadsheet, JSON and linked-data pages and
the README say how.

A guide to PLATO, published at
https://pelagios.org/place-attestation-ontology/guide/ beside the ontology
reference, and linked from the top of it. Built with Sphinx from `docs/`, it
is written for people with no background in ontologies or linked data: the
ideas in plain language, how to organise data in spreadsheets (a first
dataset step by step, and a place-name survey example for copies,
editions, "ibid." and headwords), a reference for every sheet and column, the
vocabularies, the JSON formats, the linked-data addresses, and a glossary.
The sheet reference, vocabulary pages, template workbook and download zips
are generated from `ontology.ttl` and `schemas/tables/` during the build, so
they cannot drift from the normative files.

Spreadsheet tables for contributors who work in Excel, LibreOffice or Google
Sheets: `schemas/tables/`, eight linked CSV tables (places, sources, names,
locations, types, relations, properties, identities) described by a CSV on
the Web (CSVW) metadata file, `schemas/tables/csv-metadata.json`, which states
the columns, their allowed values, the references between tables and how each
row becomes PLATO RDF. Header-only templates sit beside it and two worked
examples under `schemas/tables/examples/`. The sheet of entities is called
`places` because that is what contributors expect; its rows are
SpatialEntities.

The tables follow one rule, forced by how CSVW works: a cell yields at most
one triple, so every node a row creates must always exist. Each attestation
sheet therefore has a required main item (the name, the location, the type),
and a required `date` column holding the date as the source gives it
('undated' is allowed), with optional `from` and `to`. Tested with the
reference implementation (rdf-tabular) in strict mode and with the Python
`csvw` package; the converted graphs use only declared terms and contain no
dangling or untyped nodes. What the tables cannot express (several facets or
several sources in one attestation, shared Name or Geometry nodes, meta-
attestations) needs the JSON submission formats.

`schemas/plato.context.jsonld`, a JSON-LD 1.1 context mapping every key of
`plato.schema.json` and of both submission profiles to its ontology term, so
that a conformant submission expands to the RDF graph the ontology describes.
The document node is the Gazetteer; place-centric nesting is read through the
reverse of `attests_about`; `qualification`, `relations` and `meta` are nesting
keys; `authorityType` becomes `rdf:type`. Keys that mean different things by
parent are resolved with property-scoped contexts. What a context cannot do is
listed in the file's `$comment`.

Starter concepts declared as `skos:Concept`s in six `skos:ConceptScheme`s
(`FormStatusScheme`, `OccurrenceContextScheme`, `AttributionStatusScheme`,
`GeometryRoleScheme`, `RelativeQualifierScheme`, `MetaTypeScheme`), so that the
IRIs named in property comments (`plato:Headword`, `plato:InPersonalName`,
`plato:Extent`, `plato:Near`, `plato:Supersedes`, ...) are terms of the ontology
rather than only mentions. `plato:DerivedFrom` is added to the meta-attestation
types for a value derived from another attestation's.

`plato:ContainedIn`, a `RelationType` instance for containment (`contained_in`
/ `contains`), aligned to Getty `broaderPartitive` by `authority_uri`.

`plato:contains_identity_relation` (Gazetteer to IdentityRelation), the
property the profiles' top-level `identityRelations` maps to.

### Changed

A relation's wording now reaches RDF. `relationLabel` was mapped to null in the
context, so every relation label (DEEP's 539,306 among them) was lost in RDF,
and the schema described it, wrongly for how it is used, as a label for the
relation type. It is now the source's own wording of the relation before it is
mapped to a relation type ("part of Berkshire", "within Buckingham"), as in
LPF, and maps to `plato:source_label`, which no longer has a domain (see
below). The JSON key is unchanged.

An attestation now asserts at most one relation (`relations` has `maxItems:
1`). In RDF a relation's target, type and wording sit on the attestation
itself, so with two relations which wording went with which target was lost;
two relations are two attestations. Nothing in DEEP or the examples had more
than one.

`metaTypeLabel` is removed from the JSON Schema and the context. A meta type
is a concept whose label is the concept's own, and the key was dropped in RDF.

Country codes are now in PLATO JSON. `ccodes`, an array of ISO 3166-1 alpha-2
codes, is added to `spatialEntity` in `plato.schema.json` and mapped to the
existing `plato:ccodes` in the context, so the JSON, the spreadsheet tables and
Linked Places Format all carry them and LPF's `ccodes` round-trip. Their
meaning is now stated, as in LPF: the modern countries whose territory contains
or overlaps the place. Like the label they are a finding aid, not evidence,
and need no source; a historical claim about a country belongs in a relation
attestation.

The guide's "Ready for other systems" gains a panel on the World Historical
Gazetteer: that it is moving towards implementing PLATO, and that its Map your
Data tool, in beta testing, reconciles places with Pleiades, GeoNames and
Wikidata in the browser, for anyone.

Three places where the spreadsheet tables and the JSON Schema disagreed are
resolved, each towards the ontology, which set none of these constraints:

- A type needs only a label. `type.identifier` is no longer required in
  `plato.schema.json`, though still strongly encouraged: a source's own type
  word with no vocabulary match (the survey's "hundred") is recorded as a
  label alone, as the tables and the ontology already allowed.
- A place may have no attestations. The place-centric profile no longer
  requires `attestations` or sets a minimum of one. Such a place is only a
  referent, such as the target of a relation, and its label is not evidence.
- An identity match must say what kind of match it is. `match_type` is now
  required in the identities sheet, as `identityType` already was in JSON.
  Where the source does not say how strong the match is, the value is
  `unspecified` (see below), so that the strength is never guessed.

A place can now be cited in a state that reproduces (issue #9). A Gazetteer
is documented as versioned but had no version, so a citation of a place
could not say which state was meant, and `plato:authority_version` could
not be reused: its domain would have made every Gazetteer an Authority.
Instead, as a `dcat:Dataset`, a Gazetteer uses DCAT 3's `dcat:version`,
`dcat:isVersionOf` and `dcat:previousVersion` (JSON `version`,
`isVersionOf`, `previousVersion`), and a place is cited as its IRI plus the
gazetteer version. JSON also gains the gazetteer's `status`, mapped to the
existing `plato:gazetteer_status`. Once a gazetteer is published its
attestations are append-only, normatively: never deleted or changed, only
superseded, contradicted or retracted, so the state as of any date is a
filter over the data. `plato:Retracts` joins the meta types for a claim its
maker withdraws. A retraction or supersession takes effect only while it
holds itself, so retracting a retraction restores its target. Datetime negotiation (RFC 7089) is recommended to
platforms in the guide, not required. Decided by Stephen Gadd.

A survey of four corpora (Pleiades, Vision of Britain, Vision of Ireland and
DEEP, with the markets data) found the following, each measured and each
decided by Stephen Gadd:

- **Why a source is cited.** `plato:citation_function` on a Citation (JSON
  `citationFunction`, tables `citation_function`), valued by a property of
  CiTO, the Citation Typing Ontology: `cito:citesAsEvidence`,
  `cito:citesAsDataSource`, `cito:citesAsRelated` and the rest of the 43
  properties below `cito:cites` in CiTO 2.9.0, which the JSON Schema and the
  tables list exactly. Only CiTO terms are accepted; a vocabulary's own terms,
  such as Pleiades' `seeFurther` (143,418 of its 244,759 references), are
  mapped to CiTO by the producer. Pleiades writes them as `cito:seeFurther`
  and `cito:seeAlso`, IRIs in CiTO's namespace that CiTO does not define,
  which is why the accepted properties are listed exactly rather than
  matched by namespace. (The survey first gave 218,324 references; it had
  missed the 22,311 names that carry their own.)
- **How well a form was read.** `plato:transcription_accuracy` (Accurate,
  Inaccurate, False) and `plato:transcription_completeness` (Complete,
  Reconstructable, NonReconstructable), two new concept schemes. Like the
  other qualification properties they have no `rdfs:domain`; in JSON they go in
  a facet's `qualification`, and the tables' names sheet has a column for each.
  Pleiades judges all 44,079 of its names this way.
- **A source's denial.** `plato:negated` (JSON `negated`, tables `denied`):
  the source states that what the attestation bundles is not so, as 1,000 of
  the 1,813 rows of the 1886 return of market rights do. The attestation is
  about the real place, so no market that never existed is invented. A tool
  that cannot express a denial must leave the attestation out and report it.
- **Alternative readings.** `plato:AlternativeTo` joins the meta types: this
  attestation and its target are alternative readings of the same evidence,
  at most one of them right, to be counted as one piece of evidence. None of
  the four corpora records either-or readings, so this was added on the
  argument, ahead of data that uses it.
- **Identifiers that are IRIs.** The JSON Schema's `uri` definition now has
  format `iri`, so identifiers with non-ASCII characters (Pleiades'
  `#André-1980`, 1,410 citations) validate as they are, as JSON-LD and RDF
  allow; every ASCII URI still validates.
- **Deep time.** Years in the structured date fields, JSON and tables, may
  have more than four digits (`-12000`), as `xsd:gYear` allows; four is still
  the minimum. Pleiades has 199 endpoints before 9999 BCE.
- **People and organisations connected to a place** (a grantee, an owner) need
  no new term: the `plato:PropertyValue` comment now documents the pattern,
  the agent's IRI as the value with the property naming the role.

A new example, `schemas/examples/place-centric-judgements.json`, shows a
denial, a pair of alternatives, a judged reading, a deep-time date and an IRI
with an accented letter; the citations examples cite with `citesAsEvidence`.

Figures from statistical tables (issue #14), designed on the W3C RDF Data
Cube vocabulary and tested on three corpora (Vision of Britain, Vision of
Ireland and the 1886 markets return): every round trip rebuilt its source
exactly, and every integrity check passed. Decided by Stephen Gadd:

- A figure is a `plato:PropertyValue` that is also a `qb:Observation`: JSON
  `dataSet` (its table), `dimensions` and `attributes` (objects keyed by the
  IRIs of the table's dimension and attribute properties, each entry a direct
  statement on the figure) and `universe`, and a header array `dataSets`
  describing the tables and their structures. The county is no longer said to
  have "class 1": the observation is.
- `plato:universe`, the one new property: the figure this one is a part or
  share of, asserted only from the source, never inferred.
- Nothing is written twice. The measure stays `property` and `value`, and the
  area and date stay on the attestation; plato-tools' cube export
  (`convert --to ntriples --cube`) adds the measure statement, refArea and
  refPeriod, and declares them in each table's structure, so that the export
  is standard Data Cube while a PLATO document is not, and need not be.
- A printed dash is a figure with `sdmx-attribute:obsStatus` and no value,
  never 0; a blank cell is no figure. Money is an exact integer in the
  smallest unit of its system of account, the unit's IRI from a fitting
  authority or minted by the encoding project: PLATO mints no currency and
  converts nothing. A coordinate the source does not give is an explicit
  "unknown" code. A table mixing measures is one data set per measure.
- Dimension values are concepts, published by the encoding project where no
  code list exists (almost none do). Statistical tables in spreadsheet form
  keep their own CSVW description; the eight PLATO sheets do not change.
- A figure needs a value unless its attributes give an `obsStatus`.

A new example, `schemas/examples/place-centric-statistics.json`, and a guide
page, "Statistical tables", show the pattern.

An identity relation nested under its SpatialEntity no longer needs a
`subject`. The JSON-LD context already took the subject from the nesting
(the reverse of `plato:identity_subject`), as it takes a nested
attestation's `about`, but the schema still required it everywhere. It is
now required only in the top-level `identityRelations` of both profiles,
where nothing else supplies it. A nested relation may still repeat it; if it
does, it must be the enclosing SpatialEntity's `@id`. The Constantinople
examples gain such a relation, to GeoNames.

Seven gaps found while converting other projects' data to PLATO are closed:

- **A source's own wording on any facet.** `sourceLabel` is added to names,
  geometries and timespans in JSON, and `plato:source_label` loses its
  `rdfs:domain`, so it applies to any facet or attestation, as the
  qualification properties do: the form as printed, coordinates as printed
  ('03-47S/13038E'), a date as written ('about 1841'). In the tables, the
  `date` column of every sheet now writes `plato:source_label`;
  `plato:timespan_label` keeps its meaning of a named period ('Byzantine
  period'). The examples' written dates move with it. Closes #8.
- **A neutral meta type.** `plato:Annotates` joins the MetaTypeScheme: a
  meta-attestation that remarks on another, with its own source, without
  supporting, contradicting or refining it. The remark is its `notes`.
- **A record's own identifier.** `entityIdentifier` and `namespace` are added
  to `spatialEntity` in JSON, mapped to the existing `plato:entity_identifier`
  and `plato:namespace`, which is restated as an identifier other than the
  IRI: a project's own record id, or an authority's. A finding aid, not a
  claim about the place. The tables' `place_id` is now written to it rather
  than only minted into the IRI.
- **A latitude alone.** `plato:PropertyValue` documents that a latitude
  without a longitude is a property value, not a geometry, with property
  `http://www.w3.org/2003/01/geo/wgs84_pos#lat`.
- **Certainty in words.** `plato:certainty_level` (no domain, range
  `plato:CertaintyLevel`) and three starter levels, `plato:Certain`,
  `plato:LessCertain` and `plato:Uncertain`, the words of Linked Places
  Format, whose `certainty` now round-trips. `certaintyLevel` (a URI) is
  added to attestations and to `qualification` in JSON, and a
  `certainty_level` column to every attestation sheet. The number stays
  optional, and a producer should not invent one from a word.
- **A preferred form.** `plato:Preferred` joins the FormStatusScheme: the form
  the contributing project prefers for display and search, a project decision
  that the cited source may not show. The tables' `form_status` accepts it.
- **An identity of unstated strength.** `identityType` and the tables'
  `match_type` accept `unspecified`, for a source that links two records
  without saying how strongly. The value is still required.

The spreadsheet template is named temPlato in the guide, the glossary and the
workbook's own title sheet (the download filenames are unchanged, so existing
links keep working). The sheet reference opens by saying where it fits: that it
belongs to "Organising data in spreadsheets", and that spreadsheets are one of
several formats that comply with PLATO, beside PLATO JSON and linked data.

The guide's "Data that tools can rely on" is now "Ready for other systems",
so that it is not confused with PLATO tools, and says that the World
Historical Gazetteer is moving towards implementing PLATO.

`plato:bibliographic_string` now has domain `plato:Authority`, not
`plato:Source`. The JSON `source` object allows a `citation` whatever its
`authorityType`, so a cited dataset was inferred to be both a Source and a
Dataset, which the disjoint union of Authority forbids. Conversely, the JSON
schema now allows `timespan` and `derivedFrom` only on sources (an omitted
`authorityType` counts as a source), matching the domains of
`source_timespan` and `derived_from`. The schema and the context both note
that JSON-LD does not apply the `authorityType` default, so producers
targeting RDF should state it. Found by the DEEP/EPNS triplification.

In the JSON-LD context, a gazetteer's `title` and `licence` now map to
`dcterms:title` and `dcterms:license`. They mapped to `plato:authority_title`
and `plato:licence`, whose domains are `plato:Authority` and `plato:Dataset`, so
every Gazetteer was inferred to be an Authority, and so one of the five
disjoint kinds of Authority. The Turtle example that did the same is
corrected, and the Gazetteer definition now says which properties to use.
Found by the DEEP/EPNS triplification.

The wording on "place" is corrected. 0.4.0 said that a SpatialEntity is not a
place; that over-corrected. Many SpatialEntities are places in the everyday
sense and some are not, so PLATO defines no Place class and gives "place" no
prescribed meaning. It neither equates a SpatialEntity with a place nor
defines a place in terms of SpatialEntities or their attestations.

The range of `plato:start_earliest`, `start_latest`, `end_earliest` and
`end_latest` is `rdfs:Literal` rather than `xsd:string`, so that a producer may
emit `xsd:gYear`, `xsd:date` or `xsd:dateTime` by shape and a store can index
the bounds; plain strings remain conformant.

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
