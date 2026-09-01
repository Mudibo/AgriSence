### Entity Relationship Diagram

The entity relationship diagram models the relational data store underlying the proposed system,
implemented in Supabase (PostgreSQL). The schema separates three functional concerns: user
identity and access control, the data-driven and model-driven forecasting components, and the
marketplace and payment components.

**users**
Stores account records for all three system actors — farmers, buyers, and administrators —
under a single table distinguished by a `role` column, rather than separate tables per actor
type, whereby role is
resolved server-side from the stored record after authentication rather than supplied by the
client. `phone_number` is stored as a unique field, doubling as the destination number for
MPESA STK Push requests where the user is a farmer. `is_disabled` supports the administrator's
account moderation function without requiring deletion of the underlying record.

| Field | Type | Description |
|---|---|---|
| `id` | UUID, PK | |
| `name` | text | |
| `phone_number` | text, unique | |
| `email` | text, unique, nullable | |
| `password_hash` | text | |
| `role` | enum (`farmer`, `buyer`, `admin`) | |
| `is_disabled` | boolean | |
| `created_at` | timestamp | |

**market_locations**
A static lookup table for the five target markets (Nairobi, Nakuru, Mombasa, Kisumu, Eldoret),
storing the coordinates used to join WFP price records with Open-Meteo climate data during the
daily data pipeline run. Referenced by every market-scoped table in the schema.

| Field | Type | Description |
|---|---|---|
| `market_name` | text, PK | |
| `latitude` | numeric | |
| `longitude` | numeric | |

**features**
Stores the engineered model inputs produced by the daily data pipeline, including lag features,
rolling averages, seasonal indicators, and the candidate climate and fuel-price variables subject
to ablation testing. This table feeds the nightly forecast pipeline exclusively and is not
queried by farmer-facing views. The composite primary key enforces one record per
market-crop-month combination, allowing the daily job to upsert rather than duplicate rows.

| Field | Type | Description |
|---|---|---|
| `market` | text, PK, FK → market_locations | |
| `crop` | text, PK | |
| `month` | date, PK | |
| `avg_price` | numeric | |
| `rainfall_mm` | numeric, nullable | |
| `temperature_c` | numeric, nullable | |
| `lag_1_price`, `lag_2_price` | numeric | |
| `rolling_avg_3` | numeric | |
| `month_indicator`, `quarter_indicator` | int | |
| `updated_at` | timestamp | |

**market_prices**
The display-facing counterpart to `features`, storing cleaned, monthly-aggregated price data used
to power the farmer's "View Current Market Prices" and "View Historical Price Trends" functions.
Kept separate from `features` so that changes to the model's feature set do not affect the
simpler price-display query path.

| Field | Type | Description |
|---|---|---|
| `market` | text, PK, FK → market_locations | |
| `crop` | text, PK | |
| `month` | date, PK | |
| `avg_price` | numeric | |
| `updated_at` | timestamp | |

**forecasts**
Stores the latest pre-computed price forecast and accompanying SHAP feature-contribution values
for each of the thirty crop-market-horizon combinations, written by the nightly forecast pipeline
after the trained stacking ensemble and SHAP TreeExplainer are run in batch. This table is read
directly by the Express API in the farmer's live request path, with no on-demand call to the
FastAPI service, enabling sub-100ms response times. Each combination holds only its most recent
forecast, overwritten nightly.

| Field | Type | Description |
|---|---|---|
| `crop` | text, PK | |
| `market` | text, PK, FK → market_locations | |
| `horizon` | enum (`1_month`, `2_month`), PK | |
| `predicted_price` | numeric | |
| `shap_values` | jsonb | |
| `generated_at` | timestamp | |

**produce_listings**
Represents a farmer's produce listing available to buyers. Stores the farmer's asking price,
informed by but not automatically set from the forecast, and a reference to the listing's image
stored in Supabase Storage rather than the image binary itself. `status` distinguishes active,
paid, and removed listings, covering both farmer-initiated deletion and administrator removal.

| Field | Type | Description |
|---|---|---|
| `id` | UUID, PK | |
| `farmer_id` | UUID, FK → users | |
| `crop` | text | |
| `market` | text, FK → market_locations | |
| `quantity` | numeric | |
| `unit` | text | |
| `price_per_unit` | numeric | |
| `image_path` | text, nullable | |
| `status` | enum (`active`, `paid`, `removed`) | |
| `created_at`, `updated_at` | timestamp | |

**payments**
Represents a single MPESA payment attempt initiated by a buyer against a listing. Payment is
scoped strictly to initiation and status tracking, consistent with the study's delimitation of
delivery logistics and escrow services (Section 1.7.2). `checkout_request_id` stores Daraja's own
reference for the STK Push request, required to reconcile the asynchronous payment callback with
the correct record.

| Field | Type | Description |
|---|---|---|
| `id` | UUID, PK | |
| `listing_id` | UUID, FK → produce_listings | |
| `buyer_id` | UUID, FK → users | |
| `amount` | numeric | |
| `checkout_request_id` | text | |
| `mpesa_receipt_number` | text, nullable | |
| `status` | enum (`initiated`, `completed`, `failed`) | |
| `initiated_at` | timestamp | |
| `completed_at` | timestamp, nullable | |

**listing_reports**
An optional safeguard allowing a buyer to flag a listing or completed payment as undelivered.
Does not resolve disputes automatically; it provides an audit trail visible to the administrator,
who may act on repeated reports against a given farmer account.

| Field | Type | Description |
|---|---|---|
| `id` | UUID, PK | |
| `listing_id` | UUID, FK → produce_listings | |
| `buyer_id` | UUID, FK → users | |
| `reason` | text | |
| `created_at` | timestamp | |
### 3.4.X Entity Relationship Diagram

The entity relationship diagram models the relational data store underlying the proposed system,
implemented in Supabase (PostgreSQL). The schema separates three functional concerns: user
identity and access control, the data-driven and model-driven forecasting components, and the
marketplace and payment components.

**users**
Stores account records for all three system actors — farmers, buyers, and administrators —
under a single table distinguished by a `role` column, rather than separate tables per actor
type. This design underpins the login mechanism described in Section 3.x, whereby role is
resolved server-side from the stored record after authentication rather than supplied by the
client. `phone_number` is stored as a unique field, doubling as the destination number for
MPESA STK Push requests where the user is a farmer. `is_disabled` supports the administrator's
account moderation function without requiring deletion of the underlying record.

| Field | Type | Description |
|---|---|---|
| `id` | UUID, PK | |
| `name` | text | |
| `phone_number` | text, unique | |
| `email` | text, unique, nullable | |
| `password_hash` | text | |
| `role` | enum (`farmer`, `buyer`, `admin`) | |
| `is_disabled` | boolean | |
| `created_at` | timestamp | |

**market_locations**
A static lookup table for the five target markets (Nairobi, Nakuru, Mombasa, Kisumu, Eldoret),
storing the coordinates used to join WFP price records with Open-Meteo climate data during the
daily data pipeline run. Referenced by every market-scoped table in the schema.

| Field | Type | Description |
|---|---|---|
| `market_name` | text, PK | |
| `latitude` | numeric | |
| `longitude` | numeric | |

**features**
Stores the engineered model inputs produced by the daily data pipeline, including lag features,
rolling averages, seasonal indicators, and the candidate climate and fuel-price variables subject
to ablation testing. This table feeds the nightly forecast pipeline exclusively and is not
queried by farmer-facing views. The composite primary key enforces one record per
market-crop-month combination, allowing the daily job to upsert rather than duplicate rows.

| Field | Type | Description |
|---|---|---|
| `market` | text, PK, FK → market_locations | |
| `crop` | text, PK | |
| `month` | date, PK | |
| `avg_price` | numeric | |
| `rainfall_mm` | numeric, nullable | |
| `temperature_c` | numeric, nullable | |
| `fuel_price` | numeric, nullable | |
| `lag_1_price`, `lag_2_price` | numeric | |
| `rolling_avg_3` | numeric | |
| `month_indicator`, `quarter_indicator` | int | |
| `updated_at` | timestamp | |

**market_prices**
The display-facing counterpart to `features`, storing cleaned, monthly-aggregated price data used
to power the farmer's "View Current Market Prices" and "View Historical Price Trends" functions.
Kept separate from `features` so that changes to the model's feature set do not affect the
simpler price-display query path.

| Field | Type | Description |
|---|---|---|
| `market` | text, PK, FK → market_locations | |
| `crop` | text, PK | |
| `month` | date, PK | |
| `avg_price` | numeric | |
| `updated_at` | timestamp | |

**forecasts**
Stores the latest pre-computed price forecast and accompanying SHAP feature-contribution values
for each of the thirty crop-market-horizon combinations, written by the nightly forecast pipeline
after the trained stacking ensemble and SHAP TreeExplainer are run in batch. This table is read
directly by the Express API in the farmer's live request path, with no on-demand call to the
FastAPI service, enabling sub-100ms response times. Each combination holds only its most recent
forecast, overwritten nightly.

| Field | Type | Description |
|---|---|---|
| `crop` | text, PK | |
| `market` | text, PK, FK → market_locations | |
| `horizon` | enum (`1_month`, `2_month`), PK | |
| `predicted_price` | numeric | |
| `shap_values` | jsonb | |
| `generated_at` | timestamp | |

**produce_listings**
Represents a farmer's produce listing available to buyers. Stores the farmer's asking price,
informed by but not automatically set from the forecast, and a reference to the listing's image
stored in Supabase Storage rather than the image binary itself. `status` distinguishes active,
paid, and removed listings, covering both farmer-initiated deletion and administrator removal.

| Field | Type | Description |
|---|---|---|
| `id` | UUID, PK | |
| `farmer_id` | UUID, FK → users | |
| `crop` | text | |
| `market` | text, FK → market_locations | |
| `quantity` | numeric | |
| `unit` | text | |
| `price_per_unit` | numeric | |
| `image_path` | text, nullable | |
| `status` | enum (`active`, `paid`, `removed`) | |
| `created_at`, `updated_at` | timestamp | |

**payments**
Represents a single MPESA payment attempt initiated by a buyer against a listing. Payment is
scoped strictly to initiation and status tracking, consistent with the study's delimitation of
delivery logistics and escrow services (Section 1.7.2). `checkout_request_id` stores Daraja's own
reference for the STK Push request, required to reconcile the asynchronous payment callback with
the correct record.

| Field | Type | Description |
|---|---|---|
| `id` | UUID, PK | |
| `listing_id` | UUID, FK → produce_listings | |
| `buyer_id` | UUID, FK → users | |
| `amount` | numeric | |
| `checkout_request_id` | text | |
| `mpesa_receipt_number` | text, nullable | |
| `status` | enum (`initiated`, `completed`, `failed`) | |
| `initiated_at` | timestamp | |
| `completed_at` | timestamp, nullable | |

**listing_reports**
An optional safeguard allowing a buyer to flag a listing or completed payment as undelivered.
Does not resolve disputes automatically; it provides an audit trail visible to the administrator,
who may act on repeated reports against a given farmer account.

| Field | Type | Description |
|---|---|---|
| `id` | UUID, PK | |
| `listing_id` | UUID, FK → produce_listings | |
| `buyer_id` | UUID, FK → users | |
| `reason` | text | |
| `created_at` | timestamp | |

**Relationship summary**

- `users` (1) → `produce_listings` (many): a farmer creates multiple listings.
- `users` (1) → `payments` (many): a buyer initiates multiple payments.
- `users` (1) → `listing_reports` (many): a buyer may file multiple reports.
- `market_locations` (1) → `features`, `market_prices`, `forecasts`, `produce_listings` (many
  each): every market-scoped record references one of the five target markets.
- `produce_listings` (1) → `payments` (0 or 1): a listing may have no payment yet; the
  relationship is deliberately not enforced as one-to-one, since payment does not automatically
  lock a listing, consistent with its non-custodial scope.
- `produce_listings` (1) → `listing_reports` (many): a listing may accumulate multiple reports
  over time.### 3.4.X Entity Relationship Diagram

The entity relationship diagram models the relational data store underlying the proposed system,
implemented in Supabase (PostgreSQL). The schema separates three functional concerns: user
identity and access control, the data-driven and model-driven forecasting components, and the
marketplace and payment components.

**users**
Stores account records for all three system actors — farmers, buyers, and administrators —
under a single table distinguished by a `role` column, rather than separate tables per actor
type. This design underpins the login mechanism described in Section 3.x, whereby role is
resolved server-side from the stored record after authentication rather than supplied by the
client. `phone_number` is stored as a unique field, doubling as the destination number for
MPESA STK Push requests where the user is a farmer. `is_disabled` supports the administrator's
account moderation function without requiring deletion of the underlying record.

| Field | Type | Description |
|---|---|---|
| `id` | UUID, PK | |
| `name` | text | |
| `phone_number` | text, unique | |
| `email` | text, unique, nullable | |
| `password_hash` | text | |
| `role` | enum (`farmer`, `buyer`, `admin`) | |
| `is_disabled` | boolean | |
| `created_at` | timestamp | |

**market_locations**
A static lookup table for the five target markets (Nairobi, Nakuru, Mombasa, Kisumu, Eldoret),
storing the coordinates used to join WFP price records with Open-Meteo climate data during the
daily data pipeline run. Referenced by every market-scoped table in the schema.

| Field | Type | Description |
|---|---|---|
| `market_name` | text, PK | |
| `latitude` | numeric | |
| `longitude` | numeric | |

**features**
Stores the engineered model inputs produced by the daily data pipeline, including lag features,
rolling averages, seasonal indicators, and the candidate climate and fuel-price variables subject
to ablation testing. This table feeds the nightly forecast pipeline exclusively and is not
queried by farmer-facing views. The composite primary key enforces one record per
market-crop-month combination, allowing the daily job to upsert rather than duplicate rows.

| Field | Type | Description |
|---|---|---|
| `market` | text, PK, FK → market_locations | |
| `crop` | text, PK | |
| `month` | date, PK | |
| `avg_price` | numeric | |
| `rainfall_mm` | numeric, nullable | |
| `temperature_c` | numeric, nullable | |
| `fuel_price` | numeric, nullable | |
| `lag_1_price`, `lag_2_price` | numeric | |
| `rolling_avg_3` | numeric | |
| `month_indicator`, `quarter_indicator` | int | |
| `updated_at` | timestamp | |

**market_prices**
The display-facing counterpart to `features`, storing cleaned, monthly-aggregated price data used
to power the farmer's "View Current Market Prices" and "View Historical Price Trends" functions.
Kept separate from `features` so that changes to the model's feature set do not affect the
simpler price-display query path.

| Field | Type | Description |
|---|---|---|
| `market` | text, PK, FK → market_locations | |
| `crop` | text, PK | |
| `month` | date, PK | |
| `avg_price` | numeric | |
| `updated_at` | timestamp | |

**forecasts**
Stores the latest pre-computed price forecast and accompanying SHAP feature-contribution values
for each of the thirty crop-market-horizon combinations, written by the nightly forecast pipeline
after the trained stacking ensemble and SHAP TreeExplainer are run in batch. This table is read
directly by the Express API in the farmer's live request path, with no on-demand call to the
FastAPI service, enabling sub-100ms response times. Each combination holds only its most recent
forecast, overwritten nightly.

| Field | Type | Description |
|---|---|---|
| `crop` | text, PK | |
| `market` | text, PK, FK → market_locations | |
| `horizon` | enum (`1_month`, `2_month`), PK | |
| `predicted_price` | numeric | |
| `shap_values` | jsonb | |
| `generated_at` | timestamp | |

**produce_listings**
Represents a farmer's produce listing available to buyers. Stores the farmer's asking price,
informed by but not automatically set from the forecast, and a reference to the listing's image
stored in Supabase Storage rather than the image binary itself. `status` distinguishes active,
paid, and removed listings, covering both farmer-initiated deletion and administrator removal.

| Field | Type | Description |
|---|---|---|
| `id` | UUID, PK | |
| `farmer_id` | UUID, FK → users | |
| `crop` | text | |
| `market` | text, FK → market_locations | |
| `quantity` | numeric | |
| `unit` | text | |
| `price_per_unit` | numeric | |
| `image_path` | text, nullable | |
| `status` | enum (`active`, `paid`, `removed`) | |
| `created_at`, `updated_at` | timestamp | |

**payments**
Represents a single MPESA payment attempt initiated by a buyer against a listing. Payment is
scoped strictly to initiation and status tracking, consistent with the study's delimitation of
delivery logistics and escrow services (Section 1.7.2). `checkout_request_id` stores Daraja's own
reference for the STK Push request, required to reconcile the asynchronous payment callback with
the correct record.

| Field | Type | Description |
|---|---|---|
| `id` | UUID, PK | |
| `listing_id` | UUID, FK → produce_listings | |
| `buyer_id` | UUID, FK → users | |
| `amount` | numeric | |
| `checkout_request_id` | text | |
| `mpesa_receipt_number` | text, nullable | |
| `status` | enum (`initiated`, `completed`, `failed`) | |
| `initiated_at` | timestamp | |
| `completed_at` | timestamp, nullable | |

**listing_reports**
An optional safeguard allowing a buyer to flag a listing or completed payment as undelivered.
Does not resolve disputes automatically; it provides an audit trail visible to the administrator,
who may act on repeated reports against a given farmer account.

| Field | Type | Description |
|---|---|---|
| `id` | UUID, PK | |
| `listing_id` | UUID, FK → produce_listings | |
| `buyer_id` | UUID, FK → users | |
| `reason` | text | |
| `created_at` | timestamp | |

**Relationship summary**

- `users` (1) → `produce_listings` (many): a farmer creates multiple listings.
- `users` (1) → `payments` (many): a buyer initiates multiple payments.
- `users` (1) → `listing_reports` (many): a buyer may file multiple reports.
- `market_locations` (1) → `features`, `market_prices`, `forecasts`, `produce_listings` (many
  each): every market-scoped record references one of the five target markets.
- `produce_listings` (1) → `payments` (0 or 1): a listing may have no payment yet; the
  relationship is deliberately not enforced as one-to-one, since payment does not automatically
  lock a listing, consistent with its non-custodial scope.
- `produce_listings` (1) → `listing_reports` (many): a listing may accumulate multiple reports
  over time.
**Relationship summary**

- `users` (1) → `produce_listings` (many): a farmer creates multiple listings.
- `users` (1) → `payments` (many): a buyer initiates multiple payments.
- `users` (1) → `listing_reports` (many): a buyer may file multiple reports.
- `market_locations` (1) → `features`, `market_prices`, `forecasts`, `produce_listings` (many
  each): every market-scoped record references one of the five target markets.
- `produce_listings` (1) → `payments` (0 or 1): a listing may have no payment yet; the
  relationship is deliberately not enforced as one-to-one, since payment does not automatically
  lock a listing, consistent with its non-custodial scope.
- `produce_listings` (1) → `listing_reports` (many): a listing may accumulate multiple reports
  over time.