### 3.4.1 Class Diagram

The class diagram models the core domain objects of the proposed system and their relationships,
following Object-Oriented Analysis and Design (OOAD) principles. An abstract `User` class
generalizes shared authentication behaviour across all account types, while `Farmer`, `Buyer`,
and `Administrator` extend `User` with role-specific responsibilities. Three supporting domain
classes — `ProduceListing`, `Forecast`, and `Payment` — represent the marketplace, forecasting,
and payment-tracking components of the system respectively.

**User (abstract)**
Represents the shared identity and authentication behaviour common to all account types in the
system. `Farmer`, `Buyer`, and `Administrator` all inherit from this class, ensuring `register()`
and `login()` are defined once rather than duplicated across roles.
- Attributes: `id`, `name`, `phoneNumber`, `passwordHash`
- Methods: `register()`, `login()`

**Farmer** (extends `User`)
Represents a smallholder farmer who manages produce listings and requests explainable price
forecasts.
- Methods: `createListing()`, `editListing()`, `deleteListing()`, `viewMyListings()`,
  `generateForecast()`, `viewForecastExplainability()`

**Buyer** (extends `User`)
Represents a produce buyer who browses listings and initiates payment.
- Methods: `browseListings()`, `viewListingDetails()`, `payWithMpesa()`,
  `viewPurchaseHistory()`

**Administrator** (extends `User`)
Represents the platform manager responsible for user and listing moderation, and payment
oversight.
- Methods: `viewUserAccounts()`, `disableUserAccount()`, `removeListing()`,
  `viewDashboardStatistics()`

**ProduceListing**
Represents a farmer's produce listing available for purchase within a specific crop and market.
- Attributes: `id`, `crop`, `market`, `quantity`, `pricePerUnit`, `status`
- Methods: `updateStatus()`

**Forecast**
Represents a system-generated, pre-computed price forecast with an accompanying SHAP
explanation, produced by the nightly batch forecast pipeline rather than modified directly by
any user-facing class.
- Attributes: `id`, `crop`, `market`, `horizon`, `predictedPrice`, `shapValues`

**Payment**
Represents an MPESA payment record tracked by the system from initiation through completion.
- Attributes: `id`, `mpesaReceiptNumber`, `amount`, `status`
- Methods: `initiateSTKPush()`, `handleCallback()`

**Relationships**

| Relationship | Cardinality | Description |
|---|---|---|
| `User` ◁— `Farmer`, `Buyer`, `Administrator` | Generalization | All three roles inherit shared authentication behaviour from the abstract `User` class. |
| `Farmer` → `ProduceListing` | 1 to many | A farmer creates and manages multiple produce listings. |
| `Farmer` → `Forecast` | 1 to many | A farmer requests forecasts across different crop, market, and horizon combinations. |
| `Buyer` → `Payment` | 1 to many | A buyer may initiate multiple payments across different listings. |
| `ProduceListing` → `Payment` | 1 to 0..1 | A listing has at most one associated payment, reflecting payment initiation rather than a full transaction ledger. |
| `Administrator` ⇢ `ProduceListing` | Dependency | The administrator moderates listings without owning them. |
| `Administrator` ⇢ `Payment` | Dependency | The administrator monitors payment records without owning them. |

The design deliberately keeps `Forecast` independent of `ProduceListing`, since a farmer requests
a forecast for a given crop, market, and horizon rather than for a specific listing. This reflects
the system's architecture, in which forecasts are pre-computed in batch across all 30
crop-market-horizon combinations rather than generated per listing.