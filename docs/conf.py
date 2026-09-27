"""Sphinx configuration for the PLATO guide, published at
https://pelagios.org/place-attestation-ontology/guide/ beside the Widoco reference.

Reference pages, the template workbook and the download zips are generated at
build time from the normative files (ontology.ttl, schemas/tables/), by
_ext/plato_generate.py, so they cannot drift from them."""
import os, sys
sys.path.insert(0, os.path.abspath("_ext"))

project = "PLATO guide"
author = "Pelagios Network Place Working Group"
copyright = "2026, Pelagios Network Place Working Group (CC BY 4.0)"
language = "en_GB"

extensions = ["myst_parser", "plato_generate"]
myst_enable_extensions = ["colon_fence", "deflist"]
myst_heading_anchors = 3

exclude_patterns = ["_build", "_generated", "_ext", "requirements.txt", "README.md"]
templates_path = []

html_theme = "furo"
html_title = "PLATO guide"
html_static_path = ["_static"]
html_css_files = ["plato.css"]
html_theme_options = {
    "source_repository": "https://github.com/pelagios/place-attestation-ontology/",
    "source_branch": "main",
    "source_directory": "docs/",
}
html_show_sourcelink = False
