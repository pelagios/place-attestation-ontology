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

`jsonschema` (4.26, with `referencing`) is installed in the user site-packages, so the JSON examples can be validated against their profile rather than just parsed. The profiles `$ref` the core by the relative name `plato.schema.json`, so register it under `https://w3id.org/plato/schemas/plato.schema.json`:

```bash
python3 - <<'EOF'
import json, glob
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
load = lambda p: json.load(open(p))
reg = Registry().with_resource('https://w3id.org/plato/schemas/plato.schema.json',
                               Resource.from_contents(load('schemas/plato.schema.json')))
profiles = {}
for p in glob.glob('schemas/*-centric.schema.json'):
    s = load(p); profiles[s['$id']] = s; reg = reg.with_resource(s['$id'], Resource.from_contents(s))
for ex in sorted(glob.glob('schemas/examples/*.json')):
    doc = load(ex); errs = list(Draft202012Validator(profiles[doc['$schema']], registry=reg).iter_errors(doc))
    print(ex, 'VALID' if not errs else [list(e.absolute_path) for e in errs])
EOF
```

Two traps: the profiles declare `gazetteer.contributor` as a string (a name or URI), not a contributor object; and years in `isoOrYear` fields must be four digits (`0921`, not `921`).

The spreadsheet tables obey one design rule, forced by CSVW: a non-empty cell yields at most one triple, a virtual column always yields its triple (even when every cell it refers to is empty), and one CSV cannot be read by two table descriptions (rdf-tabular silently ignores the second). So every node a row creates must always exist: each attestation sheet has a required main item and a required `date` (text, 'undated' allowed), and only literals and IRI leaves are optional. A new optional nested node in a row would produce dangling links; give it its own sheet instead. Vocabulary columns take the local name of a declared concept (`Headword`), or its suffix where the template adds a prefix (`Inferred` → `plato:AttributionInferred`); the allowed values are generated from the ontology's schemes, so adding a concept there means regenerating the column's `format` regex.

Check the tables with the reference implementation, rdf-tabular, in a local Docker image (the Ubuntu Ruby lacks the headers its native gems need, so `gem install --user-install` fails):

```bash
# once: an image with rdf-tabular
printf 'FROM ruby:3.3-slim\nRUN apt-get update -qq && apt-get install -y -qq build-essential && gem install --no-document rdf-tabular rdf-turtle linkeddata\nWORKDIR /w\nENTRYPOINT ["rdf"]\n' > Dockerfile && docker build -q -t plato-rdf-tabular .
# copy csv-metadata.json next to an example's CSVs, then:
docker run --rm -v "$PWD":/w plato-rdf-tabular serialize --validate --input-format tabular --minimal --output-format ntriples /w/csv-metadata.json
```

Use `serialize --validate`, not `rdf validate`: the latter prints "Input is valid" even for broken foreign keys, duplicate keys and out-of-range values, which it only warns about. The Python `csvw` package (installed) is a useful second validator but does not detect duplicate primary keys. A useful graph check on the output: every plato: term declared, no object IRI in the file namespace that is not also a subject (dangling), every node typed, and each Attestation with exactly one attests_about, sourced_by, attests_timespan and has_citation.

`pyld` is installed too, so the context can be checked by expansion rather than by inspection: expand each JSON example with the context, convert to N-Quads, parse with rdflib, and confirm every `plato:` predicate and class in the result is declared in the ontology and every key in the schema `$defs` is a context term. Also check what the domains and ranges *imply*: infer each node's plato classes from the `rdfs:domain`/`rdfs:range` of the properties used on it, close under `rdfs:subClassOf`, and flag any node in two classes neither of which subsumes the other. That is how a Gazetteer titled with `plato:authority_title` was found to be inferred an Authority (and so, by `owl:disjointUnionOf`, one of Source, Dataset, Period, RelationType or CertaintyLevel). A context term's IRI must suit the node it is applied to, not just be declared. When sabotaging a term to prove the check can fail, sabotage it inside the scoped context where it is defined (`ctx['attestations']['@context']['notes']`), because a top-level redefinition is shadowed and the check passes for the wrong reason.

CI never parses `examples/*.ttl`, so nothing but a local check catches syntax errors there. Two traps those files hit before: `/` is illegal unescaped in a Turtle local name, so the illustrative URIs are written `whgx:entity\/bristol` (resolving to `https://whgazetteer.org/example/entity/bristol`) — keep the backslash when adding terms; and each example must declare every prefix it uses, `rdfs:` included.

## Documentation build (CI)

`.github/workflows/widoco.yml` runs on pushes to `main` that touch `ontology.ttl`, `README.md`, `examples/**`, `schemas/**`, or the workflow itself. It downloads the latest [Widoco](https://github.com/dgarijo/Widoco) release, generates HTML docs **from `ontology.ttl` only**, copies `schemas/` beside them (so the JSON-LD context is served as `application/ld+json`, which raw.githubusercontent.com cannot do and jsonld.js requires), and force-pushes the result to `gh-pages`; GitHub's own `pages-build-deployment` then publishes that branch. Changes to schemas or examples trigger a rebuild but are not themselves validated or rendered.

The workflow's fragile parts are already commented in place: the Widoco release lookup must send an `Authorization` header (unauthenticated API calls share a per-IP quota across runners and get rate-limited), while the asset download must **not** (the redirect target rejects it). Widoco also exits non-zero on success, so the run is `|| true` and success is inferred from the output tree.

## The PLATO guide (Sphinx)

`docs/` is a Sphinx site (MyST Markdown, Furo theme), built by the docs workflow into `guide/` on Pages: https://pelagios.org/place-attestation-ontology/guide/. It is written for non-technical researchers, so keep its prose plain and explain every term (British spelling, as everywhere). It opens with *why* PLATO: a structure that helps researchers think about what their data is and organise it, and reassurance that data in that shape can be consumed by any tool implementing the standard. Frame everything that way. Do not describe using PLATO as "contributing", a "contribution" or a "submission"; say organising data, a dataset, a JSON document. Those words are right only for the ontology's own `Contributor` class and `contributor` key, and for contributing to the PLATO project itself. `docs/_ext/plato_generate.py` generates, at build time and into the git-ignored `docs/_generated/`: the sheet reference from `schemas/tables/csv-metadata.json`, the vocabulary pages from `ontology.ttl`, the template workbook (`.xlsx`, with drop-downs and text-formatted columns), and zips of the template and each worked example. The walkthrough pages `{include}` tables rendered from the example CSVs rather than quoting them, so none of this can drift. Build locally with warnings as errors, as CI does, and run the link checker after changing links:

```bash
python3 -m sphinx -W --keep-going -b html docs docs/_build/html
python3 -m sphinx -b linkcheck docs docs/_build/linkcheck
```

The workflow also inserts a "Start with the guide" banner after the first `</h1>` of Widoco's `index-en.html`, and asserts that it found one.

## PLATO tools (sibling repository)

[pelagios/plato-tools](https://github.com/pelagios/plato-tools), published at https://pelagios.org/plato-tools/, validates and converts PLATO data in the browser. It vendors this repository's normative files (ontology, JSON Schemas, JSON-LD context, `csv-metadata.json`) from a commit pinned in its `package.json`, and its tests encode how the three layers must agree: JSON to RDF must give exactly `jsonld.js`'s graph, RDF to JSON must be lossless, and the table validator must agree with rdf-tabular. So after changing a schema, the context or the table definitions, re-pin there (`npm run vendor`) and run its tests. Its testing surfaced three places where the tables and the JSON Schema disagreed; all were resolved towards the ontology (a type needs only a label; a place may have no attestations; an identity match must state its type, in the tables as in JSON). The smaller gaps are closed too: `ccodes` is in the JSON Schema and the context, and `relationLabel` (the source's wording of a relation) maps to `plato:source_label`, with at most one relation per attestation so that the wording is never ambiguous in RDF. A later round, from converting other projects' data, added `sourceLabel` on every facet, `certaintyLevel`, `entityIdentifier`/`namespace` on SpatialEntities, `plato:Annotates`, `plato:Preferred` and the `unspecified` identity type; see the CHANGELOG.

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
            ──has_citation────▶ Citation ──cites──▶ Authority  (+ locator)
```

Everything on the right except `Citation` is a **reusable node**: one `Name` or `Geometry` can be referenced by attestations about many different SpatialEntities. This is the structural difference from LPF, where names and geometries are properties of a place record. Any subset of these relationships is valid — contributors attest only what their source supports.

Two consequences shape the rest of the model, and new work should preserve them:

- **Attestations are first-class**, so they can be the subject of *meta-attestations* (`meta_attestation_about`, `has_meta_type`) — one scholar recording that an attestation contradicts, supports, or supersedes another.
- **The core stays small while vocabulary grows.** entity-to-entity relationships (`capital_of`, `successor_to`, …) are Attestations linking two SpatialEntities via `attests_about` + `relates_to`, with semantics carried by a `RelationType` authority instance. Do not add new predicates for new relationship kinds; add vocabulary entries.

### Distinctions that are easy to collapse but must not be

- **Attestation vs IdentityRelation vs Candidate.** An `Attestation` claims evidence about a SpatialEntity. An `IdentityRelation` claims two SpatialEntities are the same real-world entity — a separate class with its own provenance, certainty, and basis. A `Candidate` is an *algorithm-generated* match suggestion and is explicitly not an assertion. The lifecycle is: Candidate → human review → IdentityRelation (linked back via `promoted_from`) or rejection.
- **Certainty vs fuzziness vs relativity.** These are orthogonal, not degrees of the same thing. `certainty` is epistemic (better evidence could raise it; 0.0 uncertain, 1.0 certain); `fuzziness` is ontological (the referent genuinely has no sharp boundary); `relative_to` + `relative_bearing`/`relative_distance`/`relative_qualifier` means the facet is defined against an anchor rather than absolutely. The qualification properties deliberately carry **no `rdfs:domain`** so they can be applied to any facet node or to an Attestation as a whole — keep it that way. `plato:transcription_accuracy` and `plato:transcription_completeness` are qualifications too, with no domain. `plato:negated` marks an attestation as a source's denial: any consumer that cannot express a denial must drop and report the attestation, never write it as an assertion, so every converter must handle it explicitly. `plato:citation_function` takes CiTO properties only (the schema lists the 43 under `cito:cites`); producers map their own terms. The same holds for `plato:certainty_level` (certainty in words, as a `CertaintyLevel` such as `plato:LessCertain`) and `plato:source_label` (the source's own wording of any facet: a date as written, coordinates as printed; `timespan_label` is for named periods).
- **`place` has no prescribed meaning in the ontology, and PLATO defines no Place class.** A SpatialEntity is the point on which attestations converge; it is deliberately generalised to cover routes, networks, administrative units, and other entities whose identity is bound up with space, so that Linked Traces use cases fit the same framework. Many SpatialEntities are places in the everyday sense and some are not, and the word means different things to different people (especially across languages), so the ontology must neither equate a SpatialEntity with a place nor define a place in terms of SpatialEntities or their attestations. Do not write "a SpatialEntity is not a place" either: that over-corrects (it was briefly the wording in 0.4.0). User-facing material may say "places" where users expect it, such as the `places` sheet of the spreadsheet tables, provided the documentation says these map to SpatialEntities.

### Three representations that must stay in sync

| Layer | File(s) | Role |
|---|---|---|
| RDF/OWL | `ontology.ttl` | Normative; the conceptual model |
| JSON Schema | `schemas/plato.schema.json` | Shared `$defs` for every object type |
| Submission profiles | `schemas/place-centric.schema.json`, `schemas/attestation-centric.schema.json` | Two ingestion shapes composed from those `$defs` |
| JSON-LD context | `schemas/plato.context.jsonld` | Maps every JSON key to its RDF term; expanding a submission with it yields the graph |
| Spreadsheet tables | `schemas/tables/csv-metadata.json` (+ header-only `*.csv`) | CSVW metadata for eight linked CSV tables; converting them yields the graph |

Adding or renaming a term means touching the ontology, the JSON `$defs`, the JSON-LD context (a key the context does not name is dropped silently on expansion), and usually an example in both `examples/` (Turtle) and `schemas/examples/` (JSON). A property-scoped context in the context file resolves keys that mean different things by parent (`label`, `source`, `contributor`, `identifier`); a new such key goes in the scoped context of its parent, not at the top level, or it will shadow nothing and map wrongly. Starter concepts for SKOS-valued properties are declared in the Starter Vocabularies section of the ontology, not only named in comments.

Naming conventions differ by layer and are not accidental: RDF uses `snake_case` (`attests_name`, `start_earliest`, `name_type`), JSON uses `camelCase` (`startEarliest`, `nameType`). The JSON schemas also *nest* the qualification properties under a `qualification` object on each facet, whereas in RDF they are applied directly to the facet node.

The two profiles differ only in where the subject lives, and the schemas enforce this: **place-centric** nests attestations under each SpatialEntity and forbids `about` on them (`"not": {"required": ["about"]}`); **attestation-centric** references existing SpatialEntities by URI and requires `about`. Identity relations follow the same logic: `subject` is required in the top-level `identityRelations` of both profiles, and optional on relations nested under a SpatialEntity, where the context supplies it (a nested one that repeats it must repeat the enclosing `@id`, which the schema cannot check). Profiles `$ref` the core schema by relative path (`plato.schema.json#/$defs/…`), so the three schema files must remain siblings in `schemas/`.

### Statistical figures (issue #14)

A figure from a statistical table is a `plato:PropertyValue` that is also a `qb:Observation` (RDF Data Cube). Its coordinates and attributes are direct statements keyed by the table's property IRIs: in JSON, absolute-IRI keys under the `dimensions` and `attributes` nesting keys. The measure stays `property_type`/`value_literal`, and the area and date stay on the attestation; nothing is written twice, so a PLATO document is not Data Cube as written, and plato-tools' `--cube` export derives the rest. `plato:universe` is asserted only from the source. PLATO mints no currency, no code lists and no units: those are the encoding project's.

### Versions and the append-only rule

A Gazetteer is versioned with DCAT 3 (`dcat:version`, `dcat:isVersionOf`, `dcat:previousVersion`), not with `plato:authority_version`, whose domain would make it an Authority. Once a Gazetteer's status is `published`, its attestations are append-only, and this is normative: never deleted or changed; corrections are new attestations with a meta-attestation (Supersedes, Contradicts, Retracts). Any tool that shows the current state must leave retracted and superseded attestations out, and any tool that writes to a published gazetteer must not edit in place.

## Editing conventions

`ontology.ttl` is organised into banner-comment sections (`# ====` for major groups, `# ----` for individual terms). Every term carries an `rdfs:label`, an `@en` triple-quoted `rdfs:comment` that explains the *rationale* and not just the meaning, and often a preceding prose comment block giving the design argument. New terms should match that density — the file doubles as the design document, and Widoco renders the comments as the published documentation.

Prose throughout (ontology comments, README, schema descriptions) uses British spelling: *licence*, *generalised*, *modelling*, *organised*.

Commit messages follow the existing style: a short subject, then a body explaining *why* the change was made and what problem it solves, including any non-obvious constraint discovered along the way.
