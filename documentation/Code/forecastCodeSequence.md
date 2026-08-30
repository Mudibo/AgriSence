
sequenceDiagram (Mermaid.live)
    actor F as Farmer
    participant PWA as PWA
    participant API as Express API
    participant SB as Supabase

    F->>PWA: Select crop, market, horizon
    PWA->>API: Request forecast
    API->>SB: Query precomputed forecast
    SB-->>API: Forecast + SHAP values

    

    API-->>PWA: JSON response (Price forecast + SHAPley Values)
    PWA->>PWA: Render forecast and bidirectional SHAP Chart
    PWA-->>F: Display explainable forecast