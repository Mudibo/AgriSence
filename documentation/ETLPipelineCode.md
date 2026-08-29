sequenceDiagram (Mermaid.live code)
    participant GHA as GitHub Actions
    participant DP as Data pipeline
    participant Ext as WFP API
    participant SB as Supabase
    participant FE as Forecast engine (FastAPI)

    GHA->>DP: Trigger daily run 
    DP->>Ext: Fetch prices
    Ext-->>DP: Raw datasets
    DP->>DP: Clean, aggregate, engineer features
    DP->>SB: Upsert features table
    GHA->>FE: Trigger forecast job
    FE->>SB: Read latest features
    SB-->>FE: Feature vectors

    loop 
        FE->>FE: model.predict()  +  SHAP TreeExplainer
    end

    FE->>SB: Upsert forecasts table
    SB-->>FE: Write confirmed