#!/usr/bin/env python3
"""Publish a fixed copy of the ontology for every PLATO release tag.

For each git tag vX.Y.Z (or vX.Y.Z-pre) this writes <publish_dir>/releases/X.Y.Z[-pre]/ with

    ontology.ttl     byte-identical to `git show vX.Y.Z:ontology.ttl`
    ontology.nt      N-Triples  } serialised from that Turtle by rdflib and
    ontology.owl     RDF/XML    } checked isomorphic with it, exactly as the
    ontology.jsonld  JSON-LD    } workflow does for the current ontology

and then <publish_dir>/releases/index.json listing every release built.
w3id.org/plato/X.Y.Z redirects to these paths, so they must never change
once published: everything is regenerated from the tag, not from main.

A tag whose ontology.ttl is missing, does not parse, or does not round-trip
is skipped with a GitHub Actions ::warning:: and left out of index.json. It
must not fail the build: one broken historical tag would otherwise block
every later documentation deploy.

Usage: build_releases.py PUBLISH_DIR   (run from the repository root, in a
checkout that has the tags: actions/checkout needs fetch-depth: 0)
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from rdflib import Graph
from rdflib.compare import to_isomorphic

# vX.Y.Z, or a SemVer pre-release such as v0.9.0-alpha.1 (PLATO's releases
# from 0.9.0 on are alphas, then betas). Build metadata (+...) is not used.
TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$")
FORMATS = [("ontology.nt", "nt"), ("ontology.owl", "xml"), ("ontology.jsonld", "json-ld")]


def git(*args: str) -> bytes:
    return subprocess.run(["git", *args], check=True, capture_output=True).stdout


def warn(msg: str) -> None:
    # One line: a workflow command must not contain a raw newline.
    print(f"::warning title=Release copy skipped::{msg}".replace("\n", " "), flush=True)


def build(tag: str, version: str, releases: Path) -> list[str] | None:
    """Write releases/<version>/; return its file names, or None if skipped."""
    try:
        ttl = git("show", f"{tag}:ontology.ttl")
    except subprocess.CalledProcessError:
        warn(f"{tag}: no ontology.ttl at this tag")
        return None

    # Build in a scratch directory and move it into place only when every
    # file has passed, so a failing tag never leaves a partial release.
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        (work / "ontology.ttl").write_bytes(ttl)
        g = Graph()
        try:
            g.parse(data=ttl, format="turtle")
        except Exception as e:  # rdflib raises several unrelated types
            warn(f"{tag}: ontology.ttl does not parse as Turtle ({type(e).__name__}: {e})")
            return None
        iso = to_isomorphic(g)
        for name, fmt in FORMATS:
            try:
                # encoding only silences rdflib's warning that N-Triples is
                # always UTF-8; the other serialisers default to UTF-8 anyway.
                g.serialize(destination=work / name, format=fmt, encoding="utf-8")
                h = Graph()
                h.parse(work / name, format=fmt)
            except Exception as e:
                warn(f"{tag}: could not write {name} ({type(e).__name__}: {e})")
                return None
            if to_isomorphic(h) != iso:
                warn(f"{tag}: {name} is not isomorphic with ontology.ttl")
                return None
        dest = releases / version
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(work, dest)
    print(f"{tag}: {len(g)} triples -> releases/{version}/ (ttl, nt, owl, jsonld; all isomorphic)")
    return ["ontology.ttl"] + [name for name, _ in FORMATS]


def precedence(tag: str) -> tuple:
    """SemVer 2.0.0 precedence: 0.9.0-alpha.1 < 0.9.0-alpha.2 < 0.9.0-beta.1
    < 0.9.0. Numeric identifiers sort as numbers and below alphanumeric ones;
    a release sorts after all its pre-releases."""
    major, minor, patch, pre = TAG.match(tag).groups()
    if pre is None:
        return (int(major), int(minor), int(patch), 1, ())
    ids = tuple((0, int(p), "") if p.isdigit() else (1, 0, p) for p in pre.split("."))
    return (int(major), int(minor), int(patch), 0, ids)


def main() -> int:
    publish = Path(sys.argv[1])
    releases = publish / "releases"
    releases.mkdir(parents=True, exist_ok=True)

    tags = [t for t in git("tag", "-l", "v*").decode().split() if TAG.match(t)]
    if not tags:
        # Almost always a shallow checkout rather than a repository with no
        # releases: say so rather than publish an empty index silently.
        warn("no vX.Y.Z release tags found; is the checkout shallow (fetch-depth: 0)?")
    tags.sort(key=precedence)

    index, skipped = [], []
    for tag in tags:
        version = tag[1:]
        files = build(tag, version, releases)
        if files is None:
            skipped.append(tag)
            continue
        # ^{commit} peels an annotated tag to the commit it points at.
        commit = git("rev-parse", f"{tag}^{{commit}}").decode().strip()
        index.append({"version": version, "tag": tag, "commit": commit,
                      "files": [f"{version}/{f}" for f in files]})

    (releases / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print(f"releases/index.json: {len(index)} built"
          + (f", skipped {' '.join(skipped)}" if skipped else ", none skipped"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
