"""Build PLATO's logo files into docs/_static/logo/.

The mark is a map pin (a place) whose head carries the rings of the Mediterranean eye charm,
with PLATO's gold, the guide's colour for an attestation, as the ring between white and blue:
a place, witnessed and kept. The lockup sets "PLATO" in Alegreya and "Place Attestation
Ontology" in Alegreya Sans, the guide's type, converted to outlines so that the files need no
font. Both fonts are under the SIL Open Font Licence, which allows this.

    python3 scripts/build_logo.py FONT_DIR

FONT_DIR holds alegreya-latin-500-normal.woff2 and alegreya-sans-latin-500-normal.woff2
(from @fontsource/alegreya and @fontsource/alegreya-sans). Needs fontTools, brotli and, for
the PNG favicons, cairosvg.
"""
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

OUT = Path(__file__).resolve().parent.parent / "docs" / "_static" / "logo"

# The palette, defined once.
PIN = "#1f45b8"      # cobalt: the place
WHITE = "#ffffff"
GOLD = "#f3c969"     # the guide's attestation gold
IRIS = "#7cc4f2"     # the charm's light blue
PUPIL = "#101a3a"
INK = "#1f2330"      # text in the lockup

PIN_PATH = "M50 96 C50 96 16 60 16 38 A34 34 0 0 1 84 38 C84 60 50 96 50 96 Z"
RINGS = [(22, WHITE), (17, GOLD), (14, IRIS), (7, PUPIL)]


def mark_body(dx=0):
    t = f' transform="translate({dx} 0)"' if dx else ""
    circles = "".join(f'<circle cx="50" cy="38" r="{r}" fill="{c}"/>' for r, c in RINGS)
    return f'<g{t}><path d="{PIN_PATH}" fill="{PIN}"/>{circles}</g>'


def mono_body():
    # One ink: the pin, then alternately cut out and filled rings, so the white and the
    # light blue become the background and the gold and the pupil stay ink.
    def circle(r, sweep):
        return f"M{50 - r} 38 a{r} {r} 0 1 {sweep} {2 * r} 0 a{r} {r} 0 1 {sweep} {-2 * r} 0 Z"
    d = PIN_PATH + " " + circle(22, 1) + " " + circle(17, 1) + " " + circle(14, 1) + " " + circle(7, 1)
    return f'<path fill-rule="evenodd" d="{d}" fill="currentColor"/>'


def svg(view_box, body, title, desc, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}" role="img" '
            f'aria-labelledby="t d"{extra}>\n<title id="t">{title}</title>\n<desc id="d">{desc}</desc>\n'
            f"{body}\n</svg>\n")


def text_path(font, text, size, x, baseline, tracking=0.0):
    """Outline `text` at `size` units, starting at x on baseline; returns (path d, end x)."""
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = size / font["head"].unitsPerEm
    parts = []
    for ch in text:
        name = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, baseline)))
        parts.append(pen.getCommands())
        x += gs[name].width * scale + tracking * size
    return " ".join(p for p in parts if p), x - tracking * size


def main(font_dir):
    font_dir = Path(font_dir)
    serif = TTFont(font_dir / "alegreya-latin-500-normal.woff2")
    sans = TTFont(font_dir / "alegreya-sans-latin-500-normal.woff2")
    OUT.mkdir(parents=True, exist_ok=True)
    desc = ("A blue map pin whose head holds white, gold, light blue and dark rings, "
            "like the Mediterranean eye charm: a place, witnessed and kept.")

    # The mark alone, cropped to the pin (x 16 to 84, y 4 to 96).
    (OUT / "plato-mark.svg").write_text(svg("14 2 72 96", mark_body(), "PLATO", desc))
    (OUT / "plato-mark-mono.svg").write_text(svg("14 2 72 96", mono_body(), "PLATO", desc + " One colour."))

    # The lockup: the mark, then the name and what it stands for.
    word, x1 = text_path(serif, "PLATO", 52, 82, 60, tracking=0.04)
    tag, x2 = text_path(sans, "Place Attestation Ontology", 15.5, 83, 84)
    width = max(x1, x2) + 4
    body = (mark_body(dx=-14) + f'<path d="{word}" fill="{INK}"/>'
            f'<path d="{tag}" fill="#5b6070"/>')
    (OUT / "plato-logo.svg").write_text(svg(f"0 2 {width:.1f} 96", body, "PLATO: Place Attestation Ontology", desc))
    body_dark = (mark_body(dx=-14) + f'<path d="{word}" fill="#eceae4"/>'
                 f'<path d="{tag}" fill="#b9b6ad"/>')
    (OUT / "plato-logo-dark.svg").write_text(svg(f"0 2 {width:.1f} 96", body_dark,
                                                 "PLATO: Place Attestation Ontology", desc + " For dark grounds."))

    # Favicons: square, the pin centred.
    square = svg("0 0 100 100", f'<g transform="translate(2 0)">{mark_body(dx=-2)}</g>', "PLATO", desc)
    (OUT / "favicon.svg").write_text(square)
    import cairosvg
    for px in (32, 180, 512):
        cairosvg.svg2png(bytestring=square.encode(), write_to=str(OUT / f"plato-{px}.png"),
                         output_width=px, output_height=px)
    # A card for social-media previews (GitHub's repository preview is 1280 by 640): the lockup
    # centred on white, with PLATO's address beneath, clear of the edges that services crop.
    url, x3 = text_path(sans, "w3id.org/plato", 15.5, 0, 0)
    scale = 780 / width
    left = (1280 - 780) / 2
    card = (f'<rect width="1280" height="640" fill="#ffffff"/>'
            f'<g transform="translate({left:.1f} {300 - 50 * scale:.1f}) scale({scale:.4f}) translate(0 -2)">{body}</g>'
            f'<g transform="translate({640 - x3 * 1.6 / 2:.1f} 520) scale(1.6)"><path d="{url}" fill="#5b6070"/></g>')
    social = svg("0 0 1280 640", card, "PLATO: Place Attestation Ontology", desc)
    cairosvg.svg2png(bytestring=social.encode(), write_to=str(OUT / "plato-social.png"),
                     output_width=1280, output_height=640)
    print("wrote", ", ".join(sorted(p.name for p in OUT.iterdir())))


if __name__ == "__main__":
    main(sys.argv[1])
