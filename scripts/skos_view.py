#!/usr/bin/env python3
"""Make PLATO's SKOS view: every vocabulary of the ontology as plain SKOS.

ontology.ttl is normative and is not changed by this. Its vocabularies are
skos:ConceptSchemes, and every RelationType and CertaintyLevel is a
skos:Concept by entailment (those classes are subclasses of skos:Concept, and
plato:broader_relation a sub-property of skos:broader). Tools that read SKOS
do not reason, and expect what SKOS asks of a concept (a prefLabel, a
definition, narrower links, top concepts) written out, so this view asserts it,
from what the ontology says in its own terms: authority_title becomes the
prefLabel, the comment the definition, relation_label a notation. Nothing in
the view contradicts the ontology or can be inferred false from it; it is
derived and never edited: build it again from the ontology it came from.

Usage: skos_view.py ONTOLOGY.ttl OUT_STEM   writes OUT_STEM.ttl and OUT_STEM.jsonld
       (build_releases.py imports build_view() for each release it publishes).
"""
import sys
from pathlib import Path

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.compare import to_isomorphic
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, SKOS

PL = Namespace("https://w3id.org/plato#")
VIEW = URIRef("https://w3id.org/plato/skos-view")


def _collapse(text) -> Literal:
    return Literal(" ".join(str(text).split()), lang="en")


def build_view(ontology: Graph) -> Graph:
    view = Graph()
    for prefix, ns in (("plato", PL), ("skos", SKOS), ("dcterms", DCTERMS), ("owl", OWL)):
        view.bind(prefix, ns)

    # 1. What the ontology says as SKOS: the schemes, and the concepts in them.
    schemes = set(ontology.subjects(RDF.type, SKOS.ConceptScheme))
    concepts = set(ontology.subjects(SKOS.inScheme, None))
    for s in schemes | concepts:
        for p, o in ontology.predicate_objects(s):
            view.add((s, p, o))

    # 2. Dress the Authority concepts as SKOS tools expect them, written out
    #    because a SKOS tool does not reason.
    for cls in (PL.RelationType, PL.CertaintyLevel):
        for c in ontology.subjects(RDF.type, cls):
            if c not in concepts:
                continue   # an example's own instance is not part of PLATO's vocabulary
            view.add((c, RDF.type, SKOS.Concept))
            title = ontology.value(c, PL.authority_title)
            if title:
                view.add((c, SKOS.prefLabel, title))
            comment = ontology.value(c, RDFS.comment)
            if comment:
                view.add((c, SKOS.definition, _collapse(comment)))
            for v in ontology.objects(c, PL.relation_label):
                view.add((c, SKOS.notation, Literal(str(v))))
            for b in ontology.objects(c, PL.broader_relation):
                view.add((c, SKOS.broader, b))
                view.add((b, SKOS.narrower, c))
            # authority_uri names a property of another ontology (Getty's
            # broaderPartitive), which skos:exactMatch would make a Concept.
            for u in ontology.objects(c, PL.authority_uri):
                view.add((c, RDFS.seeAlso, URIRef(str(u))))

    # Top concepts: in every scheme, those with no broader concept in it.
    for scheme in set(view.subjects(RDF.type, SKOS.ConceptScheme)):
        for c in view.subjects(SKOS.inScheme, scheme):
            if (c, SKOS.broader, None) not in view:
                view.add((c, SKOS.topConceptOf, scheme))
                view.add((scheme, SKOS.hasTopConcept, c))

    # 3. Provenance: which ontology this is a view of.
    onto = next(ontology.subjects(RDF.type, OWL.Ontology), None)
    if onto is not None:
        view.add((VIEW, DCTERMS.title, Literal("PLATO vocabularies as SKOS", lang="en")))
        view.add((VIEW, DCTERMS.description, Literal(
            "A SKOS rendering of the vocabularies of the PLATO ontology, derived from it and not "
            "edited. The ontology is normative.", lang="en")))
        view.add((VIEW, DCTERMS.source, ontology.value(onto, OWL.versionIRI) or onto))
        info = ontology.value(onto, OWL.versionInfo)
        if info:
            view.add((VIEW, OWL.versionInfo, info))
    return view


def check(view: Graph) -> list[str]:
    """Every concept has a label and a scheme; every scheme a label; broader and narrower agree."""
    bad = []
    for c in view.subjects(RDF.type, SKOS.Concept):
        if view.value(c, SKOS.prefLabel) is None:
            bad.append(f"{c}: no skos:prefLabel")
        if view.value(c, SKOS.inScheme) is None:
            bad.append(f"{c}: no skos:inScheme")
    for s in view.subjects(RDF.type, SKOS.ConceptScheme):
        if view.value(s, RDFS.label) is None:
            bad.append(f"{s}: no rdfs:label")
    for c, b in view.subject_objects(SKOS.broader):
        if (b, SKOS.narrower, c) not in view:
            bad.append(f"{c} skos:broader {b}: no matching skos:narrower")
    return bad


def write(view: Graph, stem: Path) -> list[str]:
    """Write STEM.ttl and STEM.jsonld, each read back and checked isomorphic with the view."""
    names, iso = [], to_isomorphic(view)
    for ext, fmt in (("ttl", "turtle"), ("jsonld", "json-ld")):
        path = Path(f"{stem}.{ext}")
        view.serialize(destination=path, format=fmt, encoding="utf-8")
        back = Graph()
        back.parse(path, format=fmt)
        if to_isomorphic(back) != iso:
            raise ValueError(f"{path}: not isomorphic with the view it was written from")
        names.append(path.name)
    return names


def main() -> int:
    src, stem = Path(sys.argv[1]), Path(sys.argv[2])
    ont = Graph()
    ont.parse(src, format="turtle")
    view = build_view(ont)
    problems = check(view)
    for p in problems:
        print(f"::error title=SKOS view::{p}")
    if problems:
        return 1
    try:
        names = write(view, stem)
    except ValueError as e:
        print(f"::error title=SKOS view::{e}")
        return 1
    print(f"{len(view)} triples -> {', '.join(names)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
