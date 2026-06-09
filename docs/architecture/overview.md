# System Overview

REI has five main components:

```mermaid
flowchart TD
    A[\"Repo Ingestor\"] --> B[\"Static Graph Builder\"]
    A --> C[\"Commit Graph Builder\"]
    C --> D[\"Noise Filter\"]
    B --> E[\"Prediction Engine\"]
    D --> E
    E --> F[\"Explainer\"]
    F --> G[\"Eval Runner\"]
    G --> H[\"Metrics Reporter\"]
```

!!! note "Design principle"
Each component has a single responsibility. Data flows through SQLite between
stages so the pipeline is debuggable and resumable.

## High-level flow

1. **Ingestor**
2. **Static graph builder**
3. **Commit graph builder**
4. **Noise filter**
5. **Prediction engine**
6. **Explainer**
7. **Eval runner**
