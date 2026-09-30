# Glossary


Attestation
: One piece of evidence: a statement that a source, for a date, gives a name,
  location, type, relation or other fact for a place. Each evidence row of the
  spreadsheets becomes one attestation.

Certainty
: How sure whoever recorded a statement is of it, from 0 to 1. It reflects the
  evidence: better evidence could change it. Not the same as fuzziness. Where
  a dataset gives certainty in words, the *certainty level* records the word
  ('Certain', 'LessCertain', 'Uncertain') instead of a number. Certainty is
  never the source's own hedging: that is its *stance*.

Citation
: One attestation's use of one source, with the locator saying where in the
  source the evidence is, and, where known, why the source is cited: as the
  evidence, as a source of data, as related reading.

Computed value
: A value software worked out from other data, such as a journey's overall
  dates from the dates of its stops. Platforms mark such values when they
  export them, because they are not evidence; they should never be entered as
  if a source had given them.

Connection
: Two places joined directly: `ConnectedTo` either way, `LeadsTo` one way.
  Figures about a connection, such as the number of letters sent, go in the
  connections sheet.

CSVW (CSV on the Web)
: The W3C standard used to describe the spreadsheet tables: their columns,
  allowed values, how they refer to one another and how rows become RDF.

Date, from, to
: *Date* is the date as the source gives it, or "undated", kept in the
  source's own words. *From* and *to* are
  the earliest and latest years or days it can mean, written with at least four-digit
  years.

Denial
: A source's statement that something was not so, such as "no market here".
  It is recorded as an attestation marked as denied, about the real place,
  so that nothing that never existed has to be invented.

Duration
: How long something lasted, where the source says so: a stay of six weeks,
  written `P42D`. It may be given with dates or without them.

Fuzziness
: The sense in which something genuinely has no sharp edge, such as "the
  Levant" or a gradual change of rule. It is a property of the thing, not of
  our knowledge of it, so it is different from certainty.

Gazetteer
: In PLATO, a dataset of places and the evidence about them, such as
  yours: the about sheet of the spreadsheets, and the `gazetteer` header of
  a JSON document, describe it. In everyday use, also a reference list of
  places, such as GeoNames or Pleiades.

Headword
: The form of a name under which an editor or survey files an entry. An
  editorial decision rather than a reading.

Ibid. (ibidem), idem
: "The same (source) as before". Where an editor has worked out which source
  was meant, the attribution is *inferred*.

Identity match
: A statement that a place in your data is the same as a record elsewhere,
  such as in Pleiades or Wikidata, and how closely: an exact match, a close
  match, or only related. The spreadsheets record it in the identities sheet,
  JSON in `identityRelations`.

Itinerary
: A journey someone actually made, through places in order, with each stop
  dated as far as the source allows. Compare *route*.

JSON-LD
: A way of writing linked data as JSON. PLATO's JSON-LD context turns a JSON
  document into RDF.

Locator
: Where in a source the evidence is: a page, folio, column or entry number.

Member
: A place that belongs to a route, journey or network, recorded with the
  relation `MemberOf`. Its position in the order is its *sequence*.

Meta-attestation
: An attestation about another attestation rather than about a place: one
  scholar recording that another's evidence is supported, contradicted,
  replaced or withdrawn. It lets corrections and disagreements be kept, not
  written over.

Network
: A set of places and the connections between them, in no single order: a
  river system, a canal network, a web of correspondents.

Normalised form
: A spelling made up for searching or matching, attested by no source.

Place
: In this guide, as in everyday speech, somewhere a source talks about. PLATO
  gives the word no special meaning: its own term is SpatialEntity. The
  spreadsheets' places sheet holds SpatialEntities.

RDF
: The W3C standard data model for linked data, in which the PLATO ontology is
  written.

Route
: A way through places in order, such as a road or a pilgrimage route. Its
  dates, if any, are when it was in use, not when anyone travelled it.
  Compare *itinerary*.

Segment
: The stretch between two places on a route or in a network, such as a leg
  of a road or a reach of a river, when the source says something about it. It
  is a row in the places sheet of its own, typed `segment`, with its ends given
  by `BeginsAt` and `EndsAt` (or `HasEnd`, if it has no direction).

Sequence
: A member's position on a route or journey, as the source orders it. Equal
  numbers are alternatives; no number means the source gives no order.

Source
: A document, map, book or dataset that evidence comes from. A source can be
  derived from another, as a copy or an edition. It can carry its licence, the
  licence of the copy you cite, so that anyone using your data can see which
  sources may be reused.

SpatialEntity
: PLATO's term for the thing attestations are about. Many SpatialEntities are
  places in the everyday sense; others are routes, networks, administrative
  units or the regions historical periods apply to. What kind each is comes
  from type attestations.

Stance
: How firmly a source itself says something. Most sources simply assert, but
  some pass a claim on without vouching for it ("it is said"), hedge it, or
  raise it and leave it undecided. That is recorded as the source's stance,
  separately from how sure you are: you can be quite certain that a source
  hedged. Leaving a thing undecided is not denying it (see Denial).

temPlato
: PLATO's spreadsheet template: ten linked sheets, as an Excel workbook or
  as CSV files, for putting data into PLATO's shape without software.

Type
: What kind of thing a place is, such as a market town, a river or a road,
  usually taken from a published vocabulary such as the Getty Art &
  Architecture Thesaurus, with the vocabulary's web address. The spreadsheets
  record it in the types sheet.

URI
: A web address used as a permanent identifier, such as
  `https://www.geonames.org/2654675/`.
