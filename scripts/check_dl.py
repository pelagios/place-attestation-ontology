#!/usr/bin/env python3
"""Check that ontology.ttl is consistent for a DL reasoner (HermiT), and that this check can fail.

A language-tagged literal is not an xsd:string in OWL 2, and xsd:duration is outside its datatype
map, so an ontology can parse, validate and publish while a DL reasoner finds it inconsistent or
refuses it. That was true of PLATO up to 0.9.0-alpha.1, and nothing noticed. This runs HermiT on
the ontology as published, then on the same ontology with a deliberate contradiction added, and
fails unless the first is consistent AND the second is not: a check that has never failed proves
nothing (a vacuous pass is how the first attempt at this missed the Authority disjointness).

Needs Java and `pip install owlready2` (which carries the HermiT jar). Run from the repository root:
    python3 scripts/check_dl.py [ontology.ttl]
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from rdflib import Graph, Namespace, RDF

PL = Namespace("https://w3id.org/plato#")


def hermit_jar_dir() -> Path:
    import owlready2
    return Path(owlready2.__file__).parent / "hermit"


def consistent(graph: Graph) -> bool:
    """True if HermiT classifies the graph; False if it reports it inconsistent. Anything else raises."""
    jars = hermit_jar_dir()
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "o.owl"
        graph.serialize(destination=path, format="xml")
        r = subprocess.run(
            ["java", "-Xmx2000M", "-cp", f"{jars}:{jars / 'HermiT.jar'}",
             "org.semanticweb.HermiT.cli.CommandLine", "-c", "-O", "-D", path.as_uri()],
            capture_output=True, text=True)
    out = r.stdout + r.stderr
    if "InconsistentOntologyException" in out:
        return False
    if "Exception" in out:
        raise RuntimeError("HermiT could not run on the ontology: " + out.strip().splitlines()[0][:300])
    return True


def main() -> int:
    ont = Graph()
    ont.parse(sys.argv[1] if len(sys.argv) > 1 else "ontology.ttl", format="turtle")

    # The control: a relation type that is also a Source breaks plato:Authority's disjoint union.
    control = Graph()
    for t in ont:
        control.add(t)
    control.add((PL.ContainedIn, RDF.type, PL.Source))
    try:
        detected = not consistent(control)
    except RuntimeError as e:
        print(f"::error title=DL check::{e}")
        return 1
    if not detected:
        print("::error title=DL check::the control contradiction was not detected, so this check proves nothing")
        return 1

    if not consistent(ont):
        print("::error title=DL check::HermiT reports ontology.ttl inconsistent (a language-tagged value in an "
              "xsd:string range, or two disjoint classes sharing an individual)")
        return 1
    print(f"HermiT: ontology.ttl ({len(ont)} triples) is consistent; the control contradiction is detected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
