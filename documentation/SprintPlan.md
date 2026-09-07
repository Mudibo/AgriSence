# 7-Sprint Development Plan
## SHAP-Based Explainable Decision Support Model for Crop Price Forecasting and Farmer-Buyer Linkage

Each sprint runs for one week and follows the Agile Scrum structure adopted in Chapter 3 (Sprint Planning, Sprint Execution, Sprint Review, Sprint Retrospective). As a solo developer, "Sprint Review" and "Retrospective" is treated as a fixed weekly checkpoint against the deliverable below, rather than a formal ceremony.

---

## Sprint 1: Environment Setup & Data Pipeline Foundation

**Goal:** Establish the project skeleton and get raw data reliably into Supabase.

**Tasks:**
- Set up GitHub repository, project structure (client/server/ml separation), and README.
- Provision Supabase project; create initial schema: `users`, `market_locations` (seed with 5 markets + coordinates).
- Write ETL script: fetch WFP Kenya food prices dataset (HDX), filter to 5 markets × 3 crops.
- Write ETL script: fetch Open-Meteo historical rainfall + temperature data per market coordinates.
- Implement data cleaning: forward-fill short gaps, IQR outlier detection.
- Implement monthly aggregation and market-coordinate join logic.
- Configure GitHub Actions workflow (`cron: '0 23 * * *'`) to run the pipeline daily; test manual trigger.
- Write to `features` and `market_prices` tables (upsert logic, composite keys).

**Deliverable:** A working, scheduled data pipeline that ingests, cleans, aggregates, and stores real WFP + climate data in Supabase, verifiable via manual GitHub Actions run and direct table inspection.

---

## Sprint 2: Exploratory Analysis, Baselines & Feature Validation

**Goal:** Understand the data and establish baseline forecasting performance before building the core model.

**Tasks:**
- Exploratory data analysis: price trends, seasonality, missingness per market/crop.
- Construct lag features, rolling averages, seasonal/month indicators in the feature engineering script.
- Implement chronological train/validation/test split (2014–2023).
- Train and evaluate Linear Regression baseline (MAE, RMSE, MAPE).
- Train and evaluate SARIMA baseline per crop-market series.
- Document baseline results in a working notebook (to feed Chapter 5 evaluation later).
- Confirm feature set is well-formed and free of leakage (no future data in lag/rolling features).

**Deliverable:** Baseline MAE/RMSE/MAPE figures for Linear Regression and SARIMA, and a validated, leakage-free feature set ready for ensemble model training.

---

## Sprint 3: Core Model Training, SHAP & Climate Ablation

**Goal:** Build the study's core contribution: the stacking ensemble and its explainability layer.

**Tasks:**
- Train Random Forest and XGBoost models with k-fold cross-validation and GridSearchCV tuning.
- Build stacking ensemble (RF + XGBoost as base learners, Linear Regression as meta-learner).
- Run climate-variable ablation: train with and without rainfall/temperature, compare against baselines.
- Decide final production feature set based on ablation results.
- Integrate SHAP TreeExplainer against the selected model(s); validate SHAP output makes directional sense.
- Serialize final trained model (and SHAP explainer) for later batch use.
- Write the nightly forecast batch script: loop over 30 crop-market-horizon combinations, predict + compute SHAP, write to `forecasts` table.
- Chain forecast batch script into the GitHub Actions workflow, after the data pipeline step.

**Deliverable:** A trained, evaluated stacking ensemble outperforming baselines, a documented climate-ablation decision, and a working nightly batch job populating the `forecasts` table with predictions and SHAP values for all 30 combinations.

---

## Sprint 4: Backend API & Authentication

**Goal:** Build the Express API layer and secure, role-based access.

**Tasks:**
- Design and implement `produce_listings`, `payments`, `listing_reports` tables in Supabase.
- Implement shared registration endpoint (farmer/buyer only; admin provisioned manually via seed script).
- Implement shared login endpoint; issue token with `role` claim resolved server-side.
- Implement Express middleware for role-based route protection (farmer/buyer/admin).
- Implement endpoints: current price lookup, historical price trend, forecast retrieval (reads `forecasts` table directly, no FastAPI call).
- Implement endpoints: create/edit/delete listing, view my listings, browse listings, view listing details.
- Set up Supabase Storage bucket (`listing-images`, public, RLS-restricted writes) and image upload flow.
- Write basic API tests for auth and core read/write endpoints.

**Deliverable:** A functioning, authenticated backend API covering authentication, decision support reads, and core marketplace CRUD, testable via Postman.

---

## Sprint 5: Farmer-Facing PWA

**Goal:** Build the farmer's complete experience: prices, forecasts, explainability, and listings.

**Tasks:**
- Set up React PWA project structure and routing (role-based views).
- Build registration/login screens.
- Build "Current Prices" and "Historical Trends" views (Recharts line/bar charts).
- Build forecast request flow (crop/market/horizon selectors) and forecast display.
- Build SHAP feature-contribution bar chart component.
- Build "Create/Edit/Delete Listing" forms, including image upload.
- Build "My Listings" view with status indicators.
- Connect all farmer-facing screens to the Sprint 4 API endpoints; handle loading/error states.

**Deliverable:** A fully functional farmer journey, from viewing prices through requesting an explainable forecast to publishing a produce listing with a photo.

---

## Sprint 6: Buyer & Admin PWA, MPESA Integration

**Goal:** Complete the marketplace loop and platform oversight functions.

**Tasks:**
- Build buyer registration/login (shared components from Sprint 5).
- Build "Browse Listings" and "Listing Details" views.
- Register Daraja Sandbox credentials; implement STK Push initiation endpoint (Express → Daraja).
- Implement Daraja callback endpoint; update `payments` status on confirmation (`initiated → completed/failed`).
- Build "Pay with MPESA" button and payment status feedback in the PWA.
- Build "View Purchase History" for buyers.
- Build Admin dashboard: view users, disable user, view listings, remove listing, view payments, summary statistics.
- (If time permits) Build "Report Listing" flow for buyers and corresponding admin view.

**Deliverable:** A complete, testable transaction loop — buyer browses, pays via Daraja Sandbox STK Push, payment status updates and is visible to both buyer and admin — plus a working admin panel.

---

## Sprint 7: Integration Testing, Evaluation & Documentation

**Goal:** Harden the system, finalize model evaluation, and prepare for submission and defense.

**Tasks:**
- End-to-end testing of all three user journeys (farmer, buyer, admin); fix critical bugs.
- Verify GitHub Actions pipeline reliability over the sprint (check logs, handle failure cases gracefully).
- Finalize model evaluation tables and figures (MAE/RMSE/MAPE across all models, ablation results) for Chapter 5.
- Capture screenshots/recordings of key flows (forecast + SHAP chart, listing creation, MPESA payment) for the report and defense.
- Deploy PWA (e.g., Vercel/Netlify) and backend (e.g., Render/Railway) for live demonstration.
- Finalize and proofread Chapters 4 and 5; reconcile any remaining inconsistencies between chapters (e.g., data split figures, scope wording).
- Prepare defense walkthrough script mapped to the three sequence diagrams and the architecture diagram.

**Deliverable:** A fully deployed, end-to-end working system; finalized evaluation results; a submission-ready document; and a rehearsed defense walkthrough.

---

## Risk Notes

- **Sprint 3 is the highest-risk sprint** — model tuning and SHAP integration can overrun. If behind schedule, deprioritize exhaustive GridSearchCV tuning before deprioritizing SHAP integration, since explainability is the study's core contribution.
- **Sprint 6's MPESA integration** depends on Daraja Sandbox registration lead time — register for sandbox credentials as early as Sprint 4 to avoid a bottleneck in Sprint 6.
- Keep the optional `listing_reports` feature and admin statistics dashboard as the first items to cut if any sprint runs over, since neither blocks the core forecasting-to-marketplace flow that the study is evaluated on.
