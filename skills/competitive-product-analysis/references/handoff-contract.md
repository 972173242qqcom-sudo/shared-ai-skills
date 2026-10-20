# Collection To Analysis Handoff

The collection package and the analysis package are separate deliverables joined by stable identifiers and traceable evidence.

## Required Competitor Fields

- `competitor_id`: stable, unique, filesystem-safe identifier.
- `offering_type`, `category`, `brand`, and `product` or `offering_name`.
- `market_status`, `status_date`, `region`.
- `reference_price`, `price_date`, `currency`.
- `target_segment`, `core_task`, `value_proposition`, and `core_interaction` when interaction is material.
- `business_model`, `key_risk`.
- `primary_source`, `retrieved_at`.

Legacy or smaller packages may use localized column names, but normalize them before repeated analysis.

## Required Asset Fields

- `competitor_id` and `file`.
- `image_role`: `hero`, `detail`, `ui`, `scenario`, or `historical`.
- `source_url`, `source_page`, `source_type`.
- `width`, `height`, `bytes`, and content hash when downloaded.
- `license_note`, `decision`, and `created_at`.

For an image-led report, one selected `hero` image per deep-dive competitor is the minimum. Contact sheets do not replace per-product mappings. For nonvisual services or B2B solutions, replace hero-image coverage with relevant proof such as workflow screens, service blueprints, pricing evidence, architecture, or case results.

## Required Evidence Fields

For facts stored outside the competitor table, use:

- `competitor_id`;
- `claim`;
- `value`;
- `source_url`;
- `source_type`;
- `region`;
- `observed_at`;
- `confidence`;
- `notes`.

## Analysis Gap Request

When evidence is missing, return a narrow request:

```text
Missing competitor IDs:
Required fields or image roles:
Preferred sources:
Region and freshness date:
Reason the evidence affects the decision:
```

Do not ask the collection workflow to repeat already verified items.
