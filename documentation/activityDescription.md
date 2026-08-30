### 3.4.X Activity Diagram: Farmer's Core Selling Decision Flow

The activity diagram models the farmer's core decision-making process from viewing market
information through to creating a produce listing, reflecting the "when to sell" and "what price
to accept" dimensions of the selling decision identified in the study's conceptual framework
(Section 2.5). The flow begins once a farmer opens the platform and ends when a produce listing
is created; browsing by buyers and payment initiation are modelled separately in the
corresponding sequence diagrams, as they represent distinct interactions triggered by a different
actor.

**Flow description**

1. **View current market prices** — the farmer views current price data drawn from the system's
   data-driven feature store, populated by the nightly data pipeline.
2. **View historical price trends** — the farmer reviews historical price movement, enabling
   cross-market comparison across the study's five target markets.
3. **Pick crop, market, horizon** — the farmer selects the specific crop, market, and prediction
   horizon (one-month or two-month) for which a forecast is required.
4. **Generate price forecast** — the system retrieves the corresponding pre-computed forecast
   from Supabase, generated in advance by the nightly batch forecast pipeline rather than
   computed live.
5. **View forecast explainability** — the farmer views the SHAP-based feature contribution
   visualization accompanying the forecast, showing which factors most influenced the predicted
   price.
6. **Decision: Is the price forecast favorable?** — the farmer evaluates the forecast and its
   explanation against their own selling goals.
   - **If Yes:** the flow proceeds to determine an asking price informed by the forecast, followed
     by creating a produce listing (crop, quantity, price, market), after which the flow ends.
   - **If No:** the flow loops back to "View current market prices," representing a farmer who
     chooses to wait and re-check market conditions rather than list immediately.

**Design rationale**

The decision node at the center of the diagram is deliberately left to the farmer's own judgment
rather than the system enforcing an outcome — the SHAP explanation informs the decision but does
not automate it, consistent with the study's positioning as a *decision support* model rather than
an autonomous decision-making system. The loop-back on an unfavorable forecast reflects realistic
farmer behavior: a farmer who judges conditions unfavorable does not exit the system, but
continues monitoring prices until conditions change. The "who to sell to" dimension of the
selling decision is intentionally excluded from this diagram, as it only becomes relevant once a
buyer engages with a listing, and is instead addressed in the buyer-facing purchase and payment
sequence diagrams.