# Rothschild Research Graph

This namespace stores entity-level research objects for the `ROTHSCHILD / FINANCE & INTELLIGENCE` cluster.

## Purpose

The family tree is a research graph, not a guilt graph.

Genealogical relationships establish identity and lineage only. They do not transfer allegations, intelligence relevance, political influence, culpability, or evidentiary weight between relatives.

Every non-genealogical edge requires its own source and provenance.

## Graph model

Preferred relationship pattern:

`Person → Parent/Spouse → Bank → Government → Intelligence Agency → Political Office → Company → Event → Document`

Supported edge classes should include:

- `parent_of`
- `child_of`
- `spouse_of`
- `member_of_family_branch`
- `employed_by`
- `served_in`
- `advised`
- `directed`
- `business_relationship`
- `political_relationship`
- `intelligence_relationship`
- `associated_with`
- `mentioned_in`
- `investigated_by`
- `alleged_by`
- `corroborated_by`
- `conflicted_by`

`associated_with` must never be silently upgraded into an operational relationship.

## Person record

Each person should capture, where available:

- `person_id`
- `canonical_name`
- `alternate_names`
- `birth_date`
- `death_date`
- `family_branch`
- `parents`
- `spouses`
- `children`
- `business_roles`
- `government_roles`
- `intelligence_roles`
- `political_contacts`
- `major_transactions_events`
- `documents`
- `allegations`
- `corroborating_sources`
- `conflicting_sources`
- `identity_confidence`
- `source_genealogy`

## Source genealogy — mandatory

For every material assertion:

`earliest available primary source → direct reproductions → later official interpretation → independent analysis → derivative retellings`

Repeated derivative claims count as one source lineage, not multiple independent sources.

## Identity control

The Rothschild Archive notes that unrelated families have also used the Rothschild name. Identity must therefore be established before linking a person or document hit into this family graph.

No surname-only linkage.

## Baseline

`genealogy-baseline.json` contains the initial source-verified founder/five-branch structure from Mayer Amschel Rothschild and a London-branch path to Victor Rothschild.

Sources:
- https://www.rothschildarchive.org/family/
- https://www.rothschildarchive.org/business/
- https://family.rothschildarchive.org/people/21-mayer-amschel-rothschild-1744-1812
- https://family.rothschildarchive.org/people/124-nathaniel-mayer-victor-rothschild-1910-1990

## Hard rule

**No inherited guilt or association scoring.**

A family relationship is genealogy. Any intelligence, political, corporate, financial, or operational connection requires independent documentary support.