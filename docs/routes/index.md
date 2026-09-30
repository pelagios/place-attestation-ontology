# Routes, journeys and networks

Not everything a gazetteer holds is a place in the everyday sense. A Roman
road, a pilgrimage way, a king's progress through his realm, a river and its
tributaries, the cities a merchant wrote to: each is made of places, in an
order or in a pattern, and each has a history of its own. PLATO records all
of them with the same few ideas, and the World Historical Gazetteer will
show them as routes, journeys and networks.

This page explains those ideas. The worked examples then show each one on
real sources:

- [the Antonine Itinerary](antonine.md): two Roman roads from London to the
  Kent ports, a **route**;
- [King John in 1215](king-john.md): the King's movements around the sealing
  of Magna Carta, a dated **journey**;
- [the lower Idle](river-idle.md): a river from Mattersey to the Trent, a
  **network** with a direction;
- [the Datini letters](datini.md): the post between a merchant's offices, a
  **network** of correspondence between cities.

## Three kinds of thing

A **route** is a way through places in order: a road, a sea lane, a
pilgrimage route. If it has dates, they say when it was in use, not when
anyone travelled it.

A **journey** (PLATO and the World Historical Gazetteer call it an
*itinerary*) is a route someone actually travelled, with each stop dated as
the source allows: arrived on this day, left on that one.

A **network** is a set of places and the connections between them, in no
single order: a river system, a canal network, the cities that exchanged
letters.

Each of these is itself a row in the places sheet, with a row in the types
sheet saying which kind it is. The kinds have fixed identifiers, listed on the
[vocabularies](../vocabularies.md) page: put `route`, `itinerary`, `network`
or `segment` in `type_label`, and the matching identifier in `type_uri`.

## Members, in order

A place on a route is a **member** of it. In the relations sheet, a row with
`relation_type` `MemberOf` says so: the place in `place_id` is a member of the
route in `related_place_id`. Its position goes in `sequence`, as your source
orders it: 1, 2, 3.

The order belongs to the source, not to the place. Two itineraries of the same
road can list its stations differently, and one town can be the third stop on
one route and the ninth on another; each row keeps its own source's order.
Two members with the same number are alternatives at that point (two branches
of a road). A member with no number is in an order the source does not give.
The members of a network usually have none; a river's reaches, which the water
puts in order, can be numbered downstream.

## The stretch between two places

The road between two stations, or a reach of a river between two
confluences, is often something your source describes in its own right: it
gives its length, or says when it was built, or when it silted up. Such a
stretch is a **segment**: a row of its own in the places sheet, typed
`segment`, and a member of its route or network like the stations.

Its ends are relations too: `BeginsAt` and `EndsAt` for a segment with a
direction (the way the itinerary runs, the way the water flows), or `HasEnd`
twice for one without. Its length and anything else your source says about it
go in the properties sheet, like any other fact.

Platforms may leave segments out of lists and searches of places, so that
"Road from Londinium to Durobrivae" is not offered as a place to visit.

## Connections

Sometimes two places are simply connected, with nothing to say about the
stretch between them: two cities that exchanged letters, two ports with a
regular crossing. Then a relations row joins them directly: `ConnectedTo` if
the connection runs either way, `LeadsTo` if it runs one way, from the place
in `place_id` to the other.

Direction is always in the word you choose, never in a separate column. If a
connection is known in both directions but from different sources, record two
`LeadsTo` rows, each with its own source, not one `ConnectedTo`.

A source may give figures about a connection: how many letters went from one
city to another, how many days they took. Those go in the **connections**
sheet, one figure per row, so that the figure is about the connection and not
about either city.

Your project may need a more particular word, such as "flows into" for a
river. The spreadsheets take only PLATO's own words, so a project's own kinds
of connection need the [JSON format](../json.md). There a document declares
each one once, in `relationTypes`, with the PLATO word it narrows, so that
any software that knows only PLATO's words still follows it the right way.

## How long

A source often says how long without saying when: "where I stayed six weeks".
The relations sheet's `duration` column holds that length, written in a
standard form: `P42D` for six weeks (the form has no weeks, so write them as
days), `P1D` for a day, `PT12H` for twelve hours. Put the source's own words
in `date` as usual. It may be given with dates or without them.

## People, objects, events, images and records

A place also has a part in things that are not places: the town where someone
was born, the field where a hoard was found, the site of a battle. The person,
object or event is usually described somewhere else already, such as in
Wikidata or a museum catalogue. So a relations row can point to it by its web
address, in `related_uri`, with a name to show it by in `related_label`, and
`relation_type` `BirthplaceOf`, `DeathplaceOf`, `ResidenceOf`, `WorkplaceOf`,
`FindspotOf` or `SettingOf`.

The same goes for what an archive or collection holds about a place: a
photograph, map or drawing that shows it (`DepictedIn`), or a file, site
record, report or publication about it (`SubjectOf`). That is what lets a
collection be explored by place. It is different from citing a source: a
source you cite is the evidence for a statement, while "this photograph
shows the site" is a statement in its own right, with its own source,
usually the catalogue that identified it.

Each relations row names exactly one thing it relates the place to: either a
place in `related_place_id` or an address in `related_uri`, never both and
never neither. [PLATO tools](https://pelagios.org/plato-tools/) reports a row
that breaks this rule.

## What not to enter

Platforms work some things out for themselves: a journey's overall dates from
the dates of its stops, a route's line from its stations. When they export
data they mark such values as *computed*, because they are not evidence.
Record what your sources say; do not copy a computed value back into your
own data as if a source had said it.
