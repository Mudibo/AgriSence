erDiagram
    USERS ||--o{ PRODUCE_LISTINGS : creates
    USERS ||--o{ PAYMENTS : initiates
    USERS ||--o{ LISTING_REPORTS : files
    MARKET_LOCATIONS ||--o{ FEATURES : has
    MARKET_LOCATIONS ||--o{ MARKET_PRICES : has
    MARKET_LOCATIONS ||--o{ FORECASTS : has
    MARKET_LOCATIONS ||--o{ PRODUCE_LISTINGS : located_in
    PRODUCE_LISTINGS ||--o| PAYMENTS : paid_via
    PRODUCE_LISTINGS ||--o{ LISTING_REPORTS : flagged_by

    USERS {
        uuid id PK
        string name
        string phone_number UK
        string email UK
        string password_hash
        string role
        boolean is_disabled
        timestamp created_at
    }

    MARKET_LOCATIONS {
        string market_name PK
        numeric latitude
        numeric longitude
    }

    FEATURES {
        string market PK, FK
        string crop PK
        date month PK
        numeric avg_price
        numeric rainfall_mm
        numeric temperature_c
        numeric fuel_price
        numeric lag_1_price
        numeric lag_2_price
        numeric rolling_avg_3
        int month_indicator
        int quarter_indicator
        timestamp updated_at
    }

    MARKET_PRICES {
        string market PK, FK
        string crop PK
        date month PK
        numeric avg_price
        timestamp updated_at
    }

    FORECASTS {
        string crop PK
        string market PK, FK
        string horizon PK
        numeric predicted_price
        json shap_values
        timestamp generated_at
    }

    PRODUCE_LISTINGS {
        uuid id PK
        uuid farmer_id FK
        string crop
        string market FK
        numeric quantity
        string unit
        numeric price_per_unit
        string image_path
        string status
        timestamp created_at
        timestamp updated_at
    }

    PAYMENTS {
        uuid id PK
        uuid listing_id FK
        uuid buyer_id FK
        numeric amount
        string checkout_request_id
        string mpesa_receipt_number
        string status
        timestamp initiated_at
        timestamp completed_at
    }

    LISTING_REPORTS {
        uuid id PK
        uuid listing_id FK
        uuid buyer_id FK
        string reason
        timestamp created_at
    }