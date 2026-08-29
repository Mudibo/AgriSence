# AgriSence System Architecture

## Overview

AgriSence adopts a modular three-tier architecture consisting of a Presentation Layer, Application Layer, Service Layer, and Data Layer. The system integrates a hybrid Decision Support System (DSS) with an agricultural marketplace. The hybrid DSS combines both a data-driven component, which provides farmers with current and historical market price information, and a model-driven component, which generates future price forecasts using a machine learning model with SHAP explainability.

The architecture also incorporates an automated data acquisition pipeline that periodically updates market and climatic datasets without requiring manual intervention.

---

## Architecture Components

### 1. Presentation Layer

The Presentation Layer provides interfaces for all system users.

Actors include:

- Farmer
- Buyer
- Administrator

The frontend is developed using React and Vite and deployed on Vercel.

The frontend is responsible for:

- User authentication
- Displaying market prices
- Displaying historical price trends
- Displaying machine learning forecasts
- Visualizing SHAP feature contributions
- Managing produce listings
- Processing buyer purchases
- Providing administrator functionality

All communication between the frontend and backend occurs via secure REST APIs over HTTPS.

---

### 2. Application Layer

The Application Layer is implemented using Express.js and serves as the central API gateway for the system.

It is responsible for:

- User authentication
- Authorization
- Marketplace management
- Decision support orchestration
- MPESA payment integration
- Administrative operations
- Communication with external services

Within the application layer, the system is logically divided into three functional modules.

#### Data-Driven Decision Support Module

This module retrieves stored market information from the database.

Its responsibilities include:

- Retrieving current market prices
- Retrieving historical market prices
- Displaying market trends across supported markets

This component does not perform prediction but provides descriptive market intelligence to assist farmers in making informed decisions.

---

#### Model-Driven Decision Support Module

This module is responsible for generating price forecasts.

When a farmer requests a forecast, the module:

1. Retrieves historical market and climatic data from the database.
2. Performs feature preparation.
3. Sends the processed features to the Machine Learning Service.
4. Receives the predicted market price.
5. Receives SHAP feature contribution values.
6. Returns both the prediction and explainability information to the frontend.

This component forms the predictive aspect of the hybrid Decision Support System.

---

#### Marketplace Module

The Marketplace Module enables agricultural trading between farmers and buyers.

Its responsibilities include:

- Creating produce listings
- Updating listings
- Deleting listings
- Browsing listings
- Purchasing produce
- Initiating MPESA payments
- Recording completed payment transactions

The marketplace focuses solely on facilitating listing publication and payment to the platform.

Delivery logistics and escrow services are outside the scope of this project.

---

### 3. Machine Learning Service

The forecasting model is deployed as an independent FastAPI service.

Responsibilities include:

- Loading the trained forecasting model
- Receiving prepared feature vectors
- Generating crop price forecasts
- Computing SHAP values
- Returning prediction results and feature contributions

Separating the Machine Learning Service from the main backend improves modularity, maintainability, and future scalability.

---

### 4. Payment Service

The system integrates with Safaricom's Daraja API for MPESA payments.

The payment process is as follows:

1. Buyer initiates purchase.
2. Express backend sends an STK Push request.
3. Buyer authorizes payment on their phone.
4. Daraja sends a callback to the backend.
5. Backend validates the transaction.
6. Payment information is stored in the database.

Payments are made to the platform only.

Funds are not automatically transferred to farmers.

---

### 5. Data Layer

The system uses Supabase PostgreSQL as its primary database.

The database stores:

- User accounts
- Produce listings
- Payment records
- Historical market prices
- Climatic observations
- System metadata

The database serves as the central repository for both marketplace operations and decision support.

---

## Automated Data Acquisition Pipeline

The system includes an automated ETL (Extract, Transform and Load) pipeline.

The pipeline executes on a scheduled basis using GitHub Actions.

The workflow is as follows:

1. Download the latest market prices from the World Food Programme (WFP) dataset.
2. Download historical climatic observations from the Open-Meteo API.
3. Clean and preprocess the downloaded data.
4. Transform the data into the required schema.
5. Insert the processed records into the Supabase database.

This ensures that both the data-driven and model-driven components always operate on up-to-date information while avoiding runtime calls to external data providers.

---

## Decision Support Workflow

When a farmer requests a forecast:

1. The request is submitted from the frontend.
2. The backend retrieves the required historical market and climatic information from Supabase.
3. Features are engineered.
4. The feature vector is sent to the Machine Learning Service.
5. The forecasting model generates the predicted price.
6. SHAP values are computed.
7. The prediction and feature contributions are returned to the frontend.
8. The frontend displays the predicted price together with a feature contribution visualization.

No external APIs are contacted during prediction.

All prediction inputs originate from the locally maintained database.

---

## Marketplace Workflow

When a buyer purchases produce:

1. The buyer selects a listing.
2. The backend initiates an MPESA STK Push request through the Daraja API.
3. The buyer authorizes the payment.
4. Daraja sends a payment callback to the backend.
5. The backend verifies the transaction.
6. Payment records are stored in Supabase.
7. The buyer receives payment confirmation.

---

## Architectural Benefits

The proposed architecture provides several advantages:

- Clear separation of concerns between marketplace, prediction, and data acquisition.
- Modular machine learning deployment through a dedicated FastAPI service.
- Independent automated data acquisition using scheduled ETL jobs.
- Elimination of runtime dependence on external market and weather APIs.
- Improved maintainability through layered architecture.
- Scalability by allowing independent deployment of frontend, backend, and machine learning services.
- Support for a hybrid Decision Support System by combining descriptive market intelligence with predictive machine learning forecasts.
