# JSON formats

If you produce data with your own software, PLATO has two JSON formats for
a dataset, each defined by a JSON Schema. They carry everything the
spreadsheets do and more: several facts or several sources in one
attestation, shared names and geometries, comments on other people's
evidence. A third format, the candidate set, holds the matches that
matching software suggests, kept beside a dataset rather than in it (see
[Candidate sets](#candidate-sets)).

| Format | Use it when… | Schema |
|---|---|---|
| **place-centric** | you are describing your own places: each place carries its attestations inside it | [place-centric.schema.json](https://w3id.org/plato/schemas/place-centric.schema.json) |
| **attestation-centric** | you are adding evidence about places that already exist elsewhere, referring to them by URI | [attestation-centric.schema.json](https://w3id.org/plato/schemas/attestation-centric.schema.json) |
| **candidate set** | you are publishing the matches your matching software suggested for a dataset, for people to review | [candidate-set.schema.json](https://w3id.org/plato/schemas/candidate-set.schema.json) |

The two dataset formats say the same thing. Whichever you choose, what you
record is attestations (a name, a type, a relation, a figure, each with its
source), and each attestation is about one place. Expanded with the JSON-LD
context, a place-centric document and an attestation-centric one give the same
attestations in RDF, with the same content and provenance. They differ only
in where the place is written, and so in a few bookkeeping statements (which
places the document contains, and their labels): inside the document, with
its label and its attestations nested under it (place-centric), or by
reference to a place described elsewhere (attestation-centric). So choose by
whether the places are new in this document. If they are all new, as in the
[Valor Ecclesiasticus example](#worked-examples), place-centric is the natural
shape, and it is the only one that gives each place a label; the
attestation-centric format carries a place's label only through
`newSpatialEntities`, which nests its attestations anyway.

All three are built from the shared definitions in
[plato.schema.json](https://w3id.org/plato/schemas/plato.schema.json), which
they refer to by relative path, so keep the files together when
validating. Worked examples are in the repository's
[schemas/examples](https://github.com/pelagios/place-attestation-ontology/tree/main/schemas/examples)
folder, and are listed under [Worked examples](#worked-examples) below.

## Checking and converting

[PLATO tools](https://pelagios.org/plato-tools/) checks a JSON document against these schemas and
converts it to RDF, to the spreadsheet tables or to Linked Places Format, in
the browser and at any size. It reads JSON Lines too: a header line, then one
place per line, which is the easiest shape to write and to stream.

For batch jobs and pipelines it also runs [from the command line](https://github.com/pelagios/plato-tools#from-the-command-line),
with Node.js 24 or later. It uses the same engine as the page, so it gives
the same results:

```bash
npx github:pelagios/plato-tools check data/*.jsonl            # a report per file, then a total
npx github:pelagios/plato-tools check --json data/*.json > report.jsonl
npx github:pelagios/plato-tools convert --to ntriples --out rdf/ data/*.jsonl
```

It exits with 0 when no file has problems, 1 when any has, and 2 when a file
cannot be read or the command is wrong, so a script can stop on invalid data.

## From JSON to linked data

Add the PLATO JSON-LD context to a JSON document and any JSON-LD processor turns
it into RDF in the PLATO ontology:

```json
{
  "@context": "https://w3id.org/plato/schemas/plato.context.jsonld",
  "$schema": "https://w3id.org/plato/schemas/attestation-centric.schema.json",
  "profile": "attestation-centric",
  "gazetteer": { "title": "My dataset" },
  "attestations": [
    {
      "about": "https://www.geonames.org/2654675/",
      "names": [ { "toponym": "Bristowe", "language": "enm" } ],
      "timespans": [ { "startEarliest": "1480", "endLatest": "1485", "sourceLabel": "1480-1485" } ],
      "sources": [ { "title": "TNA E 122/19/10" } ]
    }
  ]
}
```

The context's own opening comment explains how the formats are read and
what a triplifier must add itself. See [Linked data](linked-data.md) for the
URLs.

## Keys and terms

JSON keys are camelCase (`startEarliest`, `formStatus`); the ontology's
properties are snake_case (`start_earliest`, `form_status`). The context maps
one to the other. The fixed values for keys such as `formStatus` are the full
identifiers listed under [Vocabularies](vocabularies.md).

`sourceLabel`, on a name, geometry, timespan, type or property value, is the
source's own wording where the structured value normalises it: a date as
written ('about 1841'), coordinates as printed. A timespan's `label` is for a
named period ('Byzantine period'). Certainty stated in words goes in
`certaintyLevel`, as the URI of a level such as
`https://w3id.org/plato#LessCertain`, rather than as an invented number in
`certainty`. Both are your confidence. `certainty` is a number from 0 to 1,
written as a JSON number (`0.8`, or `1`), not as text; any kind of number
is accepted in RDF (see [Numbers](linked-data.md#numbers)). How firmly the
source itself says
something goes in an attestation's `sourceStance`, such as
`https://w3id.org/plato#StanceReported` for a claim it only passes on ("it is
said"). A source's `licence` is the web address of the licence of the copy you
cite, written as the gazetteer's is.

A name's `toponym` is the name as the source gives it: in its original script
where that is known and can be written, otherwise in a scholarly
transliteration. `script` says which script the form is written in (`Grek`;
`Latn` for a transliteration), `transliterationSystem` names the system a
transliteration follows, and `romanized` can give a romanised form beside a
name in another script. A Demotic name known only in Egyptological
transliteration is still a toponym, with the language `egy-Latn-t-egy-egyd`.

An attestation's timespans normally say when what it records held, according
to the source. Many gazetteers date a place instead by the earliest and latest
documents that mention it, which is not the same thing: a town mentioned from
144 BC to AD 99 existed before the first of those texts and after the last.
Such a window is recorded as one attestation about the place carrying only a
timespan, with `timespanRole` set to `https://w3id.org/plato#EvidenceSpan`;
it is never repeated on each name. The default role, `WhenTrue`, is usually
left out. Both are listed under [Timespan role](vocabularies.md#timespan-role).
Software that cannot carry the role should report the loss rather than show
the window as the dates of the place; the spreadsheets have no column for it.

A location given only relative to somewhere else puts the anchor's address in
`relativeTo`, in the geometry's `qualification`, with a `relativeQualifier`
from the [Relative qualifier](vocabularies.md#relative-qualifier) list.
`https://w3id.org/plato#BetweenXAndY` takes a list of exactly two anchors, in
no particular order; a `relativeBearing` or `relativeDistance` goes with one
anchor only. A place located relative to several others at once is several
attestations, not one with many anchors.

Routes, journeys and networks use a few more keys (see
[Routes, journeys and networks](routes/index.md)). An attestation that makes a
place a member of a route, with `relationType`
`https://w3id.org/plato#MemberOf`, gives its position in `sequence`, a whole
number. A relation to something that is not a place, such as a person in
Wikidata, gives its web address in `relatesTo` and a name to show it by in
`relatedLabel`. `relatedLabel` on its own, with no `relatesTo`, names
something the source gives no address for ("in the Delta"); a unit that
recurs, such as a province, is better made a place of the dataset, so that its
places can be found together. Places that were merged, absorbed into a
neighbour or divided use the succession relation types, `MergedInto`,
`AbsorbedBy`, `SplitInto`, `SucceededBy` and `TransferredTo`, as
[Places that replace one another](routes/index.md#places-that-replace-one-another)
explains. A timespan's `duration` is a length the source states, as an
`xsd:duration` such as `P42D` for six weeks. `computed`, on an attestation or
in a `qualification`, marks a value software worked out, not a source's
statement; data you record from sources never needs it.

A document describes itself in its `gazetteer` header, so that it can be
found and cited: `title` (required), `description`, `creator` (the authors
to cite, each an ORCID or other address, a name, or both), `licence`
(required once `status` is `published`), `version`, `keywords`, `spatial`
(the regions it covers, as addresses), `temporal` (`startDate` and
`endDate`), `landingPage`, and `uriSpace`, the base of its entities' web
addresses. `contributor` is whoever owns or maintains it, who need not be
an author.

A type's `identifier` should be the concept's full web address in a
published vocabulary (an AAT, Wikidata or GeoNames concept; for an
OpenStreetMap tag, its address with the key, such as
`https://wiki.openstreetmap.org/wiki/Tag:waterway=stream`), never a bare
code such as `PPL` or `stream`. A category of your source's own that no
vocabulary holds goes in `label` and `sourceLabel`, with no identifier.
Where a vocabulary has no such addresses, or changes what its terms mean
from one version to the next, give its address in `scheme` and the version
you used in `schemeVersion`. A type's own `@id`, if you give one, is your
dataset's address for it, never the vocabulary's: otherwise every dataset's
labels and versions would pile up on the one shared concept.

Saying that records elsewhere are the same place is evidence like any other,
never a settled fact. Identity relations asserted together, as when someone
accepts a group of suggested matches, go in one attestation's `identities`,
which gives them one source, date and author, and lets them be withdrawn
together. The same attestation with `negated` set, and one `exactMatch`,
says two records are *not* the same place. Software may join matches up
(A is B and B is C, so A is C) only within one such attestation: two people's
separate matches are not anyone's claim about the third pair.

A project may need a relation PLATO does not name, such as "flows into" for a
river. A document declares it once, in a `relationTypes` array beside its
`gazetteer`, and then uses its address as any relation's `relationType`:

```json
"relationTypes": [
  {
    "@id": "https://example.org/vocab/flows-into",
    "label": "flows into",
    "inverseLabel": "receives",
    "broaderRelation": "https://w3id.org/plato#LeadsTo"
  }
]
```

`broaderRelation` names the PLATO relation it narrows, so software that knows
only `LeadsTo` still reads "flows into" as a connection running one way.

## Worked examples

Each JSON example in the repository's
[schemas/examples](https://github.com/pelagios/place-attestation-ontology/tree/main/schemas/examples)
folder is valid against its profile and shows one part of the model. The
examples that belong to a page of this guide are explained there.

- [place-centric-constantinople.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-constantinople.json):
  one place with three attestations from three periods, each giving a name,
  a type and dates.
- [attestation-centric-customs.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/attestation-centric-customs.json):
  evidence from customs accounts about places that already exist elsewhere,
  referred to by address.
- [attestation-centric-citations.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/attestation-centric-citations.json)
  and
  [attestation-centric-survey.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/attestation-centric-survey.json):
  citations with locators, an attribution worked out from "ibid.", an
  editorial form, a copy derived from an earlier source, and a name found
  only inside a personal name, as in the
  [place-name survey example](spreadsheets/survey-example.md).
- [place-centric-judgements.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-judgements.json):
  denials, a source's stance, alternative readings, transcription judgements
  and a withdrawn import.
- [candidate-set-judgements.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/candidate-set-judgements.json)
  and
  [attestation-centric-judgements.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/attestation-centric-judgements.json):
  matches suggested by software, and a person's answers to them (see
  [Candidate sets](#candidate-sets)).
- [place-centric-regions.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-regions.json)
  and
  [candidate-set-regions.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/candidate-set-regions.json):
  a parish in Surrey in England, its regions made from the list itself and
  matched to a gazetteer (see
  [Regions matched to a gazetteer](#regions-matched-to-a-gazetteer)).
- [place-centric-trismegistos.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-trismegistos.json):
  three places from Trismegistos Places (CC BY-SA 4.0, credited in the
  file): a date window that is the span of the evidence
  (`timespanRole`), a position between two places (`BetweenXAndY` with two
  anchors), a containment known only by name (`relatedLabel` alone), a
  Demotic name known only in transliteration, and the land of a people,
  whose names are typed both toponym and ethnonym.
- [place-centric-succession.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-succession.json):
  invented municipalities that merge, absorb, divide and transfer land (see
  [Places that replace one another](routes/index.md#places-that-replace-one-another)).
- [place-centric-georeference.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-georeference.json):
  locations traced from a historical map, citing the map and the
  georeference they were placed through.
- [place-centric-statistics.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-statistics.json):
  figures from a statistical table, with their dimensions (see
  [Statistical tables](statistics.md)).
- [place-centric-valor.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-valor.json):
  a sample of the Valor Ecclesiasticus dataset (the 1535 survey of Church of
  England benefices, as printed in 1810-1834; CC BY-NC 4.0, credited in the
  file): an index entry kept as printed beside its editorial head-name, a
  place nested in a deanery and a diocese that skip an unprinted
  archdeaconry, a link to a historical parish, a religious house with its
  possessions, and the King's Books value and tenths that Ecton printed in
  pounds, shillings and pence, with the printed figures as the source's
  wording and the value in pence derived.
- [place-centric-antonine.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-antonine.json),
  [place-centric-king-john.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-king-john.json),
  [place-centric-river-idle.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-river-idle.json)
  and
  [place-centric-datini.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-datini.json):
  the four worked examples of
  [Routes, journeys and networks](routes/index.md), whole.

The same models are shown in RDF in the repository's
[examples](https://github.com/pelagios/place-attestation-ontology/tree/main/examples)
folder.

## Candidate sets

Matching software, such as a reconciliation service, suggests that a place in
your dataset may be the same as a record elsewhere. Such a suggestion is a
*candidate*. It is not anyone's claim: it records what the software
suggested, with its score and the settings that produced it, so that a
reviewer, or a later reader, can see why the match was offered.

Candidates are published in a document of their own, a *candidate set*,
beside the dataset and never inside it, because a dataset holds claims and a
candidate is a claim by no one. A candidate set has a header,
`candidateSet`, with its address (`@id`), a `title`, the date it was
`issued`, and `candidatesFor`, the address of the dataset the matches were
sought for; and a `candidates` list. Each candidate gives its `subject` (the
place in your dataset), its `object` (the suggested match), the
`similarityScore`, the `algorithmVersion`, the `matchParameters` if any, the
time it was `generatedAt`, and its `status`, which is always `suggested`.

Once issued, a candidate set never changes: no candidate in it is altered or
removed, and a later run of the software is a new set, which leaves out any
candidate an earlier set has already published. Each candidate's address is
the set's address followed by `#c-` and a short code worked out from what the
candidate says, so the same suggestion always gets the same address.

A candidate's score therefore records what the software said when it first
suggested the pair. If the places' names change and the same algorithm, run
with the same settings, would now score the pair differently, the first
score stands. To record a new score, publish it under a new
`algorithmVersion` or new `matchParameters`, which gives the candidate a new
address.

A person's answer to a candidate goes in the dataset, as an attestation like
any other identity match, whose identity relation points back to the
candidate with `promotedFrom`. A yes is an ordinary attestation; a no is an
attestation with `negated` set, saying the two are *not* the same place. What
became of a candidate is read from these attestations, never from the
candidate, so a decision can be withdrawn and made again without changing
the published set. Software that accepts matches with no one reviewing them
should publish its own attestations in the same way, not mark candidates as
confirmed. A dataset can list its candidate sets in its `gazetteer` header,
in `candidateSets`, and should be published together with them, so that
anyone can follow `promotedFrom` to the suggestion it answers.

Candidate sets are written by software, so they are published as JSON (or
RDF) only: the spreadsheet template has no sheet for them. The repository's
[candidate-set-judgements.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/candidate-set-judgements.json)
is a small candidate set, and
[attestation-centric-judgements.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/attestation-centric-judgements.json)
answers it.

### Regions matched to a gazetteer

A table of places often gives, beside each place, the regions it lies in: a
parish, its county, its country. When those regions are matched to a
gazetteer, two different things have been said, and PLATO keeps them apart.

- **What your source says.** The parish is *contained in* the county, and the
  county in the country. Each of these is a relation with `relationType`
  `ContainedIn`, and it points at a region made from your own data, with the
  name as your source writes it. Make one region for each whole chain of
  containers (England, then Surrey), not one for each name, so that a Newport
  in Shropshire and a Newport in Monmouthshire stay two regions.
  The region's name goes in that region's own name attestation. Use
  `relationLabel` only when your source words the relation itself ("in the
  county of Surrey"); `relatedLabel` is not needed, since the region is a
  place in your dataset.
- **What the reviewer decided.** That your Surrey is the gazetteer's Surrey
  is an identity match, made like any other: an attestation with the
  reviewer's source and certainty, whose identity relation points back with
  `promotedFrom` to the suggestion it answers. The matching software's score
  stays on that suggestion, in the candidate set. It is not a certainty, so
  it is never written on the containment.

If the match is later changed, that is a new identity attestation, and what
your source said is untouched. A region you assign by hand, with no
suggestion from software, may simply point its `ContainedIn` at the
gazetteer's address.

Linked Places Format (LPF) writes the two claims as one: a
`gvp:broaderPartitive` relation for each container, whose `relationTo` is the
identity match's gazetteer address, whose `certainty` is the reviewer's
certainty level, whose `whg_match_score` is the suggestion's score and whose
`label` is the region's name. Reading such LPF back gives the simpler
shape, a containment straight to the gazetteer's address: the region made from
your data, the separate match and the score are not in LPF to be recovered. The
repository's
[place-centric-regions.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/place-centric-regions.json)
shows a parish in Surrey in England, and
[candidate-set-regions.json](https://github.com/pelagios/place-attestation-ontology/blob/main/schemas/examples/candidate-set-regions.json)
holds the suggestions it answers.
