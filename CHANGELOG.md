# Changelog

All notable changes to PLATO are recorded here. The ontology is an early draft
with no implementations yet, so a renamed term is removed outright rather than
retained as a deprecated equivalent. That policy will change once data in the
wild uses the namespace.

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
outright. They were briefly kept as `owl:deprecated` equivalents on the
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
