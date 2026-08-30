---
config:
  layout: fixed
---
flowchart TB
    Start((" ")) --> A["<b>View current market prices</b><br>Data-driven component"]
    A --> B["<b>View historical price trends</b><br>Cross-market comparison"]
    B --> C["<b>Pick crop, market, horizon</b><br>1-month or 2-month forecast"]
    C --> D["<b>Generate price forecast</b><br>Reads computed forecast"]
    D --> E["<b>View forecast explainability</b><br>SHAP feature contribution chart"]
    E --> Dec{"<b>Price forecast<br>favorable?</b>"}
    Dec -- No --> A
    Dec -- Yes --> F["<b>Determine asking price</b><br>Informed by forecast"]
    F --> G["<b>Create produce listing</b><br>Crop, quantity, price, market"]
    G --> End((" "))

     Start:::startEnd
     A:::action
     B:::action
     C:::action
     D:::action
     E:::action
     Dec:::decision
     F:::action
     G:::action
     End:::startEnd
    classDef action fill:#0a4d3c,stroke:#26a69a,color:#ffffff
    classDef decision fill:#663300,stroke:#ff9800,color:#ffffff
    classDef startEnd fill:#424242,stroke:#a6a6a6,color:#ffffff