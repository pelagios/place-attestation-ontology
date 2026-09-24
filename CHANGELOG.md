# Changelog

All notable changes to PLATO are recorded here. The ontology is an early draft
and the namespace is published, so renamed terms are retained as deprecated
equivalents rather than removed.

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

### Deprecated, not removed

`plato:Thing`, `plato:thing_identifier` and `plato:contains_thing` are retained
as `owl:deprecated` terms, declared `owl:equivalentClass` and
`owl:equivalentProperty` of their replacements. Existing data continues to
describe the same things. New data should use the current terms.

The JSON submission keys are not aliased, because the submission profiles are
not part of the published namespace and the format is still at draft status.

### Unchanged

No relationships, cardinalities or semantics were altered. This release is a
renaming only.

## 0.2.0

Initial public release.
