# About PLATO

PLATO, the Place Attestation Ontology, is developed by the
[Pelagios Network](https://pelagios.org)'s Place Working Group, led by the
[Institute for Spatial History Innovation](https://www.ishi.pitt.edu/) at the
University of Pittsburgh, and formalises the data model of the
[World Historical Gazetteer](https://whgazetteer.org).

## Under development

PLATO is developed in the open. It is an early draft, published for
discussion and review, and not yet stable: its terms, its JSON schemas and
its spreadsheet tables may still change between releases.

A term or JSON key that is renamed or withdrawn is not removed at once. It
is kept, marked as deprecated and pointing to its replacement, for at least
one release before it is removed. The
[changelog](https://github.com/pelagios/place-attestation-ontology/blob/main/CHANGELOG.md)
states this policy and records every change, release by release.

Each release is archived on Zenodo with its own DOI (see
[Citing PLATO](#citing-plato)), so data organised against one release can
always name the exact version it follows.

[PLATO tools](https://pelagios.org/plato-tools/), which checks and converts
data in PLATO's shape, is developed separately and carries its own badge.

## PLATO and Linked Places Format

Linked Places Format (LPF) is PLATO's single-attestation profile: every LPF
element corresponds to one attestation linking one place to one name, type,
geometry or related place. Existing LPF files remain valid. PLATO does not
replace LPF; the simple interchange format and the richer model are meant to
coexist, and LPF's development continues in its own
[repository](https://github.com/LinkedPasts/linked-places-format).

## Taking part

Questions, suggestions and problems are welcome as
[issues](https://github.com/pelagios/place-attestation-ontology/issues) on the
repository. The Working Group can be reached at gazetteers@pelagios.org.

## Citing PLATO

Cite the concept DOI, which always resolves to the latest version:
[10.5281/zenodo.21688313](https://doi.org/10.5281/zenodo.21688313).

## Licence

PLATO and this guide are published under the
[Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)
licence.
