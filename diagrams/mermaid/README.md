# Diagrams as code (Mermaid)

GitHub renders these diagrams directly. PNG versions (rendered from Graphviz) are in [`../png`](../png), and their sources are in [`../source`](../source).

## 1. To-be process flow (BPMN-style)

```mermaid
flowchart TD
    subgraph C[Customer - Web / Mobile]
        S((Start)) --> A1[Start application<br/>and give consent]
        A1 --> A2[Enter personal,<br/>KYC and income data]
        FIX[Fix missing /<br/>invalid data]
        EA(((Pre-approved<br/>notice)))
        ED(((Declined +<br/>adverse action notice)))
    end
    subgraph SYS[Onboarding System - Decision Engine]
        G0{Complete?}
        T3[Log consent<br/>to Audit Log]
        T4[Verify identity<br/>KYC Service]
        G1{KYC result?}
        T5[Soft credit pull<br/>retry x3 on timeout]
        G2{Credit decision<br/>rules}
        T6[Auto pre-approve:<br/>create offer]
        T7[Auto decline:<br/>record reasons]
        T8[Notify customer<br/>email / SMS / in-app]
    end
    subgraph OPS[Operations - Manual Review]
        Q[Manual review queue<br/>SLA 4 business hours]
        G3{Agent decision}
    end
    A2 --> G0
    G0 -- No --> FIX --> A2
    G0 -- Yes --> T3 --> T4 --> G1
    G1 -- Pass --> T5 --> G2
    G1 -- Partial match --> Q
    G1 -- Fail --> T7
    G2 -- "Score >= 680 and DTI <= 40%" --> T6
    G2 -- "Borderline or API failure" --> Q
    G2 -- "Score < 600" --> T7
    Q --> G3
    G3 -- Approve --> T6
    G3 -- Decline --> T7
    T6 --> T8
    T7 --> T8
    T8 -- approved --> EA
    T8 -- declined --> ED
```

## 2. Component and data flow

```mermaid
flowchart TD
    WEB[Web app] -- "application + consent (HTTPS)" --> GW
    MOB[Mobile app] -- "application + consent (HTTPS)" --> GW
    GW[API Gateway<br/>auth, rate limit, TLS] -- "validated request + token" --> ORCH
    ORCH[Onboarding Orchestrator<br/>+ Decision Engine]
    ORCH -- "KYC request" --> KYC[KYC Service]
    KYC -. "verification result" .-> ORCH
    ORCH -- "soft-pull request (consent ref)" --> CB[Credit Bureau API<br/>external]
    CB -. "credit score" .-> ORCH
    ORCH -- "application data and decision" --> CORE[Core Banking System]
    ORCH -- "case for review" --> MRQ[Manual Review Queue]
    ORCH -- "decision event" --> NOTIF[Notification Service]
    ORCH -- "consent, pull, decision" --> AUD[(Audit Logging Service<br/>immutable)]
    KYC --> AUD
    CORE --> AUD
    MRQ -- "agent actions" --> AUD
    NOTIF -- "notice sent" --> AUD
```

## 3. Entity model

```mermaid
erDiagram
    CUSTOMER ||--o{ APPLICATION : submits
    APPLICATION ||--|{ CONSENT : records
    APPLICATION ||--o{ KYC_CHECK : triggers
    APPLICATION ||--o{ CREDIT_PULL : requests
    APPLICATION ||--|{ AUDIT_LOG : "logged by"

    CUSTOMER {
        uuid customer_id PK
        string full_name
        date date_of_birth
        string email
        string phone
        string residential_address
        string ssn_token "tokenized"
        timestamp created_at
    }
    APPLICATION {
        uuid application_id PK
        uuid customer_id FK
        decimal loan_amount
        int term_months
        decimal annual_income
        string channel "web or mobile"
        string status
        string decision "approve, decline, review"
        string reason_codes
        string rule_version
        timestamp submitted_at
        timestamp decided_at
    }
    CONSENT {
        uuid consent_id PK
        uuid application_id FK
        string consent_type "soft_pull, esign, privacy"
        string disclosure_version
        timestamp granted_at
        string device_id
    }
    KYC_CHECK {
        uuid kyc_check_id PK
        uuid application_id FK
        string provider_ref
        string result "pass, review, fail"
        decimal match_score
        boolean watchlist_hit
        timestamp checked_at
    }
    CREDIT_PULL {
        uuid credit_pull_id PK
        uuid application_id FK
        string pull_type "soft"
        int credit_score
        decimal dti_ratio
        string response_status
        int retry_count
        timestamp pulled_at
    }
    AUDIT_LOG {
        uuid audit_id PK
        uuid application_id FK
        string actor
        string action
        string details_hash
        timestamp created_at
    }
```
