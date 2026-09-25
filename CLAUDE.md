# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A specification repository, not a software project: there is no build system, no dependencies, and no test suite. Everything here is either normative (`ontology.ttl`, `schemas/*.json`) or illustrative (`examples/`, `schemas/examples/`). PLATO formalises the [WHG v4 data model](https://docs.whgazetteer.org/content/v4/data-model/introduction.html) and defines Linked Places Format (LPF) as its single-object-attestation profile; Linked Traces use cases fit within the same model. Do not describe PLATO as superseding LPF.

The namespace is `https://w3id.org/plato#` (prefix `plato:`); published documentation lives at https://pelagios.org/place-attestation-ontology/.

## Checking your work

No linter or validator is configured. `rdflib` (7.6.0) and `jq` are available locally; use them after editing:

```bash
# Turtle syntax check
python3 -c "from rdflib import Graph; g=Graph(); g.parse('ontology.ttl', format='turtle'); print(len(g))"

# JSON Schema files are well-formed JSON
jq empty schemas/*.json schemas/examples/*.json
```

CI never parses `examples/*.ttl`, so nothing but a local check catches syntax errors there. Two traps those files hit before: `/` is illegal unescaped in a Turtle local name, so the illustrative URIs are written `whgx:entity\/bristol` (resolving to `https://whgazetteer.org/example/entity/bristol`) — keep the backslash when adding terms; and each example must declare every prefix it uses, `rdfs:` included.

## Documentation build (CI)

`.github/workflows/widoco.yml` runs on pushes to `main` that touch `ontology.ttl`, `README.md`, `examples/**`, `schemas/**`, or the workflow itself. It downloads the latest [Widoco](https://github.com/dgarijo/Widoco) release, generates HTML docs **from `ontology.ttl` only**, and force-pushes them to `gh-pages`; GitHub's own `pages-build-deployment` then publishes that branch. Changes to schemas or examples trigger a rebuild but are not themselves validated or rendered.

The workflow's fragile parts are already commented in place: the Widoco release lookup must send an `Authorization` header (unauthenticated API calls share a per-IP quota across runners and get rate-limited), while the asset download must **not** (the redirect target rejects it). Widoco also exits non-zero on success, so the run is `|| true` and success is inferred from the output tree.

## Releases

A release bumps the version in four places that must stay in step:

- `ontology.ttl` — `owl:versionInfo`
- `CITATION.cff` — `version` and `date-released`
- `.zenodo.json` — `version`
- the git tag (`v0.1.1` style)

Zenodo archives the repository as it stands at the tag, so **never put a per-version DOI in `README.md` or `CITATION.cff`** — per-version DOIs don't exist until after publication, so quoting one would freeze a placeholder into the archive. Only the concept DOI (`10.5281/zenodo.21688313`, which always resolves to the latest version) is cited in-repo; readers get per-version DOIs from the Zenodo record's Versions panel.

## Architecture

### The attestation-as-bundle pattern

The unit of contributed knowledge is the **Attestation**, not the place record. An `Attestation` is a lightweight node with no substantive content of its own — its meaning comes entirely from its outgoing relationships:

```
Attestation ──attests_about──▶ SpatialEntity        (the stable identity)
            ──attests_name───▶ Name
            ──attests_geometry▶ Geometry
            ──attests_timespan▶ Timespan
            ──attests_type────▶ Type
            ──sourced_by──────▶ Authority   (Source / Dataset / Period / …)
```

Everything on the right is a **reusable node**: one `Name` or `Geometry` can be referenced by attestations about many different SpatialEntities. This is the structural difference from LPF, where names and geometries are properties of a place record. Any subset of these relationships is valid — contributors attest only what their source supports.

Two consequences shape the rest of the model, and new work should preserve them:

- **Attestations are first-class**, so they can be the subject of *meta-attestations* (`meta_attestation_about`, `has_meta_type`) — one scholar recording that an attestation contradicts, supports, or supersedes another.
- **The core stays small while vocabulary grows.** entity-to-entity relationships (`capital_of`, `successor_to`, …) are Attestations linking two SpatialEntities via `attests_about` + `relates_to`, with semantics carried by a `RelationType` authority instance. Do not add new predicates for new relationship kinds; add vocabulary entries.

### Distinctions that are easy to collapse but must not be

- **Attestation vs IdentityRelation vs Candidate.** An `Attestation` claims evidence about a SpatialEntity. An `IdentityRelation` claims two SpatialEntities are the same real-world entity — a separate class with its own provenance, certainty, and basis. A `Candidate` is an *algorithm-generated* match suggestion and is explicitly not an assertion. The lifecycle is: Candidate → human review → IdentityRelation (linked back via `promoted_from`) or rejection.
- **Certainty vs fuzziness vs relativity.** These are orthogonal, not degrees of the same thing. `certainty` is epistemic (better evidence could raise it; 0.0 uncertain, 1.0 certain; `uncertainty` is its deprecated alias on the same scale); `fuzziness` is ontological (the referent genuinely has no sharp boundary); `relative_to` + `relative_bearing`/`relative_distance`/`relative_qualifier` means the facet is defined against an anchor rather than absolutely. The qualification properties deliberately carry **no `rdfs:domain`** so they can be applied to any facet node or to an Attestation as a whole — keep it that way.
- **`SpatialEntity` is not `Place`.** It is deliberately generalised to cover routes, networks, administrative units, and other entities related to place, so that Linked Traces use cases fit the same framework.

### Three representations that must stay in sync

| Layer | File(s) | Role |
|---|---|---|
| RDF/OWL | `ontology.ttl` | Normative; the conceptual model |
| JSON Schema | `schemas/plato.schema.json` | Shared `$defs` for every object type |
| Submission profiles | `schemas/place-centric.schema.json`, `schemas/attestation-centric.schema.json` | Two ingestion shapes composed from those `$defs` |

Adding or renaming a term means touching the ontology, the JSON `$defs`, and usually an example in both `examples/` (Turtle) and `schemas/examples/` (JSON).

Naming conventions differ by layer and are not accidental: RDF uses `snake_case` (`attests_name`, `start_earliest`, `name_type`), JSON uses `camelCase` (`startEarliest`, `nameType`). The JSON schemas also *nest* the qualification properties under a `qualification` object on each facet, whereas in RDF they are applied directly to the facet node.

The two profiles differ only in where the subject lives, and the schemas enforce this: **place-centric** nests attestations under each SpatialEntity and forbids `about` on them (`"not": {"required": ["about"]}`); **attestation-centric** references existing SpatialEntities by URI and requires `about`. Profiles `$ref` the core schema by relative path (`plato.schema.json#/$defs/…`), so the three schema files must remain siblings in `schemas/`.

## Editing conventions

`ontology.ttl` is organised into banner-comment sections (`# ====` for major groups, `# ----` for individual terms). Every term carries an `rdfs:label`, an `@en` triple-quoted `rdfs:comment` that explains the *rationale* and not just the meaning, and often a preceding prose comment block giving the design argument. New terms should match that density — the file doubles as the design document, and Widoco renders the comments as the published documentation.

Prose throughout (ontology comments, README, schema descriptions) uses British spelling: *licence*, *generalised*, *modelling*, *organised*.

Commit messages follow the existing style: a short subject, then a body explaining *why* the change was made and what problem it solves, including any non-obvious constraint discovered along the way.
