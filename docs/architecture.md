# Architecture Documentation

## RM-AgenticAI-LangGraph System Architecture

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture Principles](#architecture-principles)
3. [System Context (C4 Level 1)](#system-context-c4-level-1)
4. [Container Diagram (C4 Level 2)](#container-diagram-c4-level-2)
5. [Component Diagram (C4 Level 3)](#component-diagram-c4-level-3)
6. [LangGraph Workflow Architecture](#langgraph-workflow-architecture)
7. [Data Flow Architecture](#data-flow-architecture)
8. [State Management](#state-management)
9. [Hybrid Intelligence Architecture](#hybrid-intelligence-architecture)
10. [Deployment Architecture](#deployment-architecture)
11. [Security Architecture](#security-architecture)

---

## Overview

RM-AgenticAI-LangGraph follows a **layered architecture** pattern combined with **event-driven agent orchestration**. The system is designed to be:

- **Modular**: Each agent can be developed, tested, and deployed independently
- **Scalable**: Async execution enables high-throughput processing
- **Resilient**: Multi-level fallback mechanisms ensure reliability
- **Observable**: Comprehensive logging and metrics for monitoring

---

## Architecture Principles

### 1. Separation of Concerns
Each layer has a distinct responsibility:
- UI Layer: User interaction only
- Application Layer: Orchestration only
- Intelligence Layer: AI/ML processing only
- Data Layer: Persistence only

### 2. Single Responsibility
Each agent performs exactly one task in the workflow.

### 3. Dependency Inversion
High-level modules don't depend on low-level modules. Both depend on abstractions (interfaces).

### 4. Fail-Safe Design
Every component has fallback mechanisms:
- ML Model → Rule-Based Logic
- LLM → Template-Based Response
- External API → Cached Data

---

## System Context (C4 Level 1)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    SYSTEM CONTEXT                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│    ┌──────────────────────┐                                    ┌──────────────────────┐│
│    │                      │                                    │                      ││
│    │   RELATIONSHIP       │                                    │   COMPLIANCE         ││
│    │   MANAGER (RM)       │                                    │   OFFICER            ││
│    │                      │                                    │                      ││
│    │   Primary User       │                                    │   Audits Reports     ││
│    │   - Analyzes clients │                                    │   Reviews Decisions  ││
│    │   - Reviews insights │                                    │                      ││
│    └──────────┬───────────┘                                    └──────────┬───────────┘│
│               │                                                           │             │
│               │  Web Interface                                            │             │
│               ▼                                                           ▼             │
│    ┌─────────────────────────────────────────────────────────────────────────────────┐ │
│    │                                                                                  │ │
│    │                        RM-AGENTIC-AI-LANGGRAPH                                   │ │
│    │                                                                                  │ │
│    │         Intelligent Investment Advisory Automation Platform                      │ │
│    │                                                                                  │ │
│    │   • Automates client analysis           • Generates recommendations             │ │
│    │   • Ensures compliance                  • Provides explainable AI               │ │
│    │                                                                                  │ │
│    └────────────────────────────────┬────────────────────────────────────────────────┘ │
│                                     │                                                   │
│               ┌─────────────────────┼─────────────────────┐                            │
│               │                     │                     │                            │
│               ▼                     ▼                     ▼                            │
│    ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐                   │
│    │                  │  │                  │  │                  │                   │
│    │   GOOGLE GEMINI  │  │   CLIENT DATA    │  │   PRODUCT        │                   │
│    │   API            │  │   SOURCES        │  │   CATALOG        │                   │
│    │                  │  │                  │  │                  │                   │
│    │   LLM Provider   │  │   CRM/Database   │  │   Investment     │                   │
│    │   for reasoning  │  │   External APIs  │  │   Products DB    │                   │
│    └──────────────────┘  └──────────────────┘  └──────────────────┘                   │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### External Systems Integration

| System | Integration Type | Purpose |
|--------|-----------------|---------|
| Google Gemini API | REST API | LLM reasoning and explainability |
| Client Data Sources | CSV/Database | Prospect information |
| Product Catalog | Database | Investment product details |
| CRM (Future) | REST API | Customer relationship data |

---

## Container Diagram (C4 Level 2)

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                     CONTAINER DIAGRAM                                         │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐│
│  │                                      UI LAYER                                            ││
│  │  ┌───────────────────────────────────────────────────────────────────────────────────┐ ││
│  │  │                           STREAMLIT WEB APPLICATION                                │ ││
│  │  │                                                                                    │ ││
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │ ││
│  │  │  │  Prospect   │  │  Progress   │  │  Results    │  │    Chat     │              │ ││
│  │  │  │  Selector   │  │  Tracker    │  │  Dashboard  │  │  Assistant  │              │ ││
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘              │ ││
│  │  │                                                                                    │ ││
│  │  │  Technology: Streamlit 1.28+                                                       │ ││
│  │  └───────────────────────────────────────────────────────────────────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────────────────────────────────┘│
│                                              │                                               │
│                                              ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐│
│  │                                  APPLICATION LAYER                                       ││
│  │  ┌───────────────────────────────────────────────────────────────────────────────────┐ ││
│  │  │                        LANGGRAPH WORKFLOW ORCHESTRATOR                             │ ││
│  │  │                                                                                    │ ││
│  │  │  ┌─────────────────────────────────────────────────────────────────────────────┐ │ ││
│  │  │  │                           WORKFLOW GRAPH                                     │ │ ││
│  │  │  │                                                                              │ │ ││
│  │  │  │   [START] ──▶ [Node1] ──▶ [Node2] ──▶ [Node3] ──▶ [Node4] ──▶ [Node5] ──▶ [END] ││
│  │  │  │              DataVal    RiskAssess  Persona    Products   Compliance        │ │ ││
│  │  │  │                                                                              │ │ ││
│  │  │  └─────────────────────────────────────────────────────────────────────────────┘ │ ││
│  │  │                                                                                    │ ││
│  │  │  ┌─────────────────────────┐  ┌─────────────────────────┐                        │ ││
│  │  │  │    State Manager        │  │    Error Handler         │                        │ ││
│  │  │  │    (Shared State)       │  │    (Recovery Logic)      │                        │ ││
│  │  │  └─────────────────────────┘  └─────────────────────────┘                        │ ││
│  │  │                                                                                    │ ││
│  │  │  Technology: LangGraph 0.1+, LangChain 0.2+                                        │ ││
│  │  └───────────────────────────────────────────────────────────────────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────────────────────────────────┘│
│                                              │                                               │
│                                              ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐│
│  │                                  INTELLIGENCE LAYER                                      ││
│  │                                                                                          ││
│  │  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐          ││
│  │  │    ML MODELS         │  │    LLM ENGINE        │  │    AGENT POOL        │          ││
│  │  │                      │  │                      │  │                      │          ││
│  │  │  • Risk Classifier   │  │  • Gemini Client     │  │  • DataAnalyst       │          ││
│  │  │    (RandomForest)    │  │  • Prompt Templates  │  │  • RiskAssessment    │          ││
│  │  │  • Goal Predictor    │  │  • Response Parser   │  │  • Persona           │          ││
│  │  │    (Logistic Reg)    │  │  • Fallback Handler  │  │  • ProductSpecialist │          ││
│  │  │                      │  │                      │  │  • GoalPlanning      │          ││
│  │  │  Tech: sklearn       │  │  Tech: LangChain     │  │  • Compliance        │          ││
│  │  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘          ││
│  └─────────────────────────────────────────────────────────────────────────────────────────┘│
│                                              │                                               │
│                                              ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐│
│  │                                      DATA LAYER                                          ││
│  │                                                                                          ││
│  │  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐          ││
│  │  │   PROSPECT DATA      │  │   PRODUCT CATALOG    │  │   MODEL ARTIFACTS    │          ││
│  │  │                      │  │                      │  │                      │          ││
│  │  │  • Client profiles   │  │  • Investment funds  │  │  • risk_model.pkl    │          ││
│  │  │  • Financial data    │  │  • Risk ratings      │  │  • goal_model.pkl    │          ││
│  │  │  • Historical records│  │  • Product features  │  │  • Scaler objects    │          ││
│  │  │                      │  │                      │  │                      │          ││
│  │  │  Format: CSV/DB      │  │  Format: CSV/DB      │  │  Format: Pickle      │          ││
│  │  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘          ││
│  └─────────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                              │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Diagram (C4 Level 3)

### Intelligence Layer Components

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                              INTELLIGENCE LAYER - COMPONENT DETAIL                            │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐│
│  │                                  AGENT POOL                                              ││
│  │                                                                                          ││
│  │    ┌─────────────────────────────────────────────────────────────────────────────────┐ ││
│  │    │                              BASE AGENT (Abstract)                               │ ││
│  │    │                                                                                  │ ││
│  │    │   Properties:                          Methods:                                  │ ││
│  │    │   - name: str                          - execute(state) -> Result               │ ││
│  │    │   - llm_client: GeminiClient           - validate_input(data) -> bool           │ ││
│  │    │   - logger: Logger                     - handle_error(error) -> FallbackResult  │ ││
│  │    │   - metrics: MetricsCollector          - log_execution(metrics) -> None         │ ││
│  │    └──────────────────────────────────┬──────────────────────────────────────────────┘ ││
│  │                                       │                                                 ││
│  │           ┌───────────────────────────┼───────────────────────────┐                    ││
│  │           │                           │                           │                    ││
│  │           ▼                           ▼                           ▼                    ││
│  │  ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐              ││
│  │  │ DataAnalyst     │       │ RiskAssessment  │       │    Persona      │              ││
│  │  │ Agent           │       │ Agent           │       │    Agent        │              ││
│  │  │                 │       │                 │       │                 │              ││
│  │  │ - validate()    │       │ - ml_predict()  │       │ - classify()    │              ││
│  │  │ - score_quality │       │ - llm_analyze() │       │ - get_insights()│              ││
│  │  │ - infer_missing │       │ - rule_fallback │       │ - confidence()  │              ││
│  │  └─────────────────┘       └─────────────────┘       └─────────────────┘              ││
│  │                                                                                         ││
│  │           ┌───────────────────────────┬───────────────────────────┐                    ││
│  │           │                           │                           │                    ││
│  │           ▼                           ▼                           ▼                    ││
│  │  ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐              ││
│  │  │ ProductSpeciali │       │ GoalPlanning    │       │  Compliance     │              ││
│  │  │ st Agent        │       │ Agent           │       │  Agent          │              ││
│  │  │                 │       │                 │       │                 │              ││
│  │  │ - load_products │       │ - predict_goal()│       │ - check_rules() │              ││
│  │  │ - filter_match()│       │ - success_prob()│       │ - disclosures() │              ││
│  │  │ - score_product │       │ - timeline()    │       │ - warnings()    │              ││
│  │  └─────────────────┘       └─────────────────┘       └─────────────────┘              ││
│  │                                                                                         ││
│  └─────────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐│
│  │                                   ML MODELS                                              ││
│  │                                                                                          ││
│  │   ┌─────────────────────────────┐      ┌─────────────────────────────┐                 ││
│  │   │     RISK CLASSIFIER         │      │     GOAL PREDICTOR          │                 ││
│  │   │                             │      │                             │                 ││
│  │   │  Algorithm: RandomForest    │      │  Algorithm: LogisticRegress │                 ││
│  │   │  Features:                  │      │  Features:                  │                 ││
│  │   │  - age                      │      │  - income                   │                 ││
│  │   │  - income                   │      │  - goal_amount              │                 ││
│  │   │  - investment_amount        │      │  - time_horizon             │                 ││
│  │   │  - investment_horizon       │      │  - risk_profile             │                 ││
│  │   │  - risk_tolerance           │      │  - monthly_contribution     │                 ││
│  │   │                             │      │                             │                 ││
│  │   │  Output: LOW/MEDIUM/HIGH    │      │  Output: Probability 0-1    │                 ││
│  │   └─────────────────────────────┘      └─────────────────────────────┘                 ││
│  │                                                                                          ││
│  └─────────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐│
│  │                                   LLM ENGINE                                             ││
│  │                                                                                          ││
│  │   ┌─────────────────────────────────────────────────────────────────────────────────┐  ││
│  │   │                            GEMINI CLIENT                                         │  ││
│  │   │                                                                                  │  ││
│  │   │   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌──────────────┐ │  ││
│  │   │   │   Prompt      │   │   Response    │   │   Fallback    │   │    Rate      │ │  ││
│  │   │   │   Templates   │──▶│   Parser      │──▶│   Handler     │──▶│    Limiter   │ │  ││
│  │   │   └───────────────┘   └───────────────┘   └───────────────┘   └──────────────┘ │  ││
│  │   │                                                                                  │  ││
│  │   └─────────────────────────────────────────────────────────────────────────────────┘  ││
│  └─────────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                               │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## LangGraph Workflow Architecture

### Graph Definition

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                              LANGGRAPH WORKFLOW DEFINITION                                    │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                               │
│                                      ┌─────────┐                                             │
│                                      │  START  │                                             │
│                                      └────┬────┘                                             │
│                                           │                                                  │
│                                           ▼                                                  │
│   ┌───────────────────────────────────────────────────────────────────────────────────────┐ │
│   │                              NODE: data_validation                                     │ │
│   │   ┌─────────────────────────────────────────────────────────────────────────────────┐│ │
│   │   │  Agent: DataAnalystAgent                                                         ││ │
│   │   │  Input: ProspectData                                                             ││ │
│   │   │  Output: ValidatedProspectData + DataQualityScore                                ││ │
│   │   │  Next: risk_assessment                                                           ││ │
│   │   └─────────────────────────────────────────────────────────────────────────────────┘│ │
│   └───────────────────────────────────────────────────────────────────────────────────────┘ │
│                                           │                                                  │
│                                           ▼                                                  │
│   ┌───────────────────────────────────────────────────────────────────────────────────────┐ │
│   │                              NODE: risk_assessment                                    │ │
│   │   ┌─────────────────────────────────────────────────────────────────────────────────┐│ │
│   │   │  Agent: RiskAssessmentAgent                                                      ││ │
│   │   │  Input: ValidatedProspectData                                                    ││ │
│   │   │  Process: ML Prediction → LLM Analysis → Fallback Rules                          ││ │
│   │   │  Output: RiskAssessmentResult                                                    ││ │
│   │   │  Next: persona_classification                                                    ││ │
│   │   └─────────────────────────────────────────────────────────────────────────────────┘│ │
│   └───────────────────────────────────────────────────────────────────────────────────────┘ │
│                                           │                                                  │
│                                           ▼                                                  │
│   ┌───────────────────────────────────────────────────────────────────────────────────────┐ │
│   │                              NODE: persona_classification                             │ │
│   │   ┌─────────────────────────────────────────────────────────────────────────────────┐│ │
│   │   │  Agent: PersonaAgent                                                             ││ │
│   │   │  Input: ValidatedProspectData + RiskAssessmentResult                             ││ │
│   │   │  Classifications: Aggressive Growth | Steady Saver | Cautious Planner            ││ │
│   │   │  Output: PersonaResult + BehavioralInsights                                      ││ │
│   │   │  Next: product_recommendation                                                    ││ │
│   │   └─────────────────────────────────────────────────────────────────────────────────┘│ │
│   └───────────────────────────────────────────────────────────────────────────────────────┘ │
│                                           │                                                  │
│                                           ▼                                                  │
│   ┌───────────────────────────────────────────────────────────────────────────────────────┐ │
│   │                              NODE: product_recommendation                             │ │
│   │   ┌─────────────────────────────────────────────────────────────────────────────────┐│ │
│   │   │  Agent: ProductSpecialistAgent                                                   ││ │
│   │   │  Input: PersonaResult + RiskAssessmentResult + ProductCatalog                    ││ │
│   │   │  Process: Filter → Match → Score → Rank                                          ││ │
│   │   │  Output: Top 5 ProductRecommendations with Justifications                        ││ │
│   │   │  Next: finalization                                                              ││ │
│   │   └─────────────────────────────────────────────────────────────────────────────────┘│ │
│   └───────────────────────────────────────────────────────────────────────────────────────┘ │
│                                           │                                                  │
│                                           ▼                                                  │
│   ┌───────────────────────────────────────────────────────────────────────────────────────┐ │
│   │                              NODE: finalization                                       │ │
│   │   ┌─────────────────────────────────────────────────────────────────────────────────┐│ │
│   │   │  Agents: ComplianceAgent + GoalPlanningAgent                                     ││ │
│   │   │  Input: All previous results                                                     ││ │
│   │   │  Process:                                                                        ││ │
│   │   │    1. Compliance validation                                                      ││ │
│   │   │    2. Goal success prediction                                                    ││ │
│   │   │    3. Aggregate confidence scores                                                ││ │
│   │   │    4. Generate insights and disclosures                                          ││ │
│   │   │    5. Create RM action items                                                     ││ │
│   │   │  Output: WorkflowState (complete)                                                ││ │
│   │   │  Next: END                                                                       ││ │
│   │   └─────────────────────────────────────────────────────────────────────────────────┘│ │
│   └───────────────────────────────────────────────────────────────────────────────────────┘ │
│                                           │                                                  │
│                                           ▼                                                  │
│                                      ┌─────────┐                                             │
│                                      │   END   │                                             │
│                                      └─────────┘                                             │
│                                                                                               │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Graph Code Structure

```python
from langgraph.graph import StateGraph, END
from state import WorkflowState

# Define the workflow graph
workflow = StateGraph(WorkflowState)

# Add nodes (each node is a function that takes state and returns updated state)
workflow.add_node("data_validation", data_validation_node)
workflow.add_node("risk_assessment", risk_assessment_node)
workflow.add_node("persona_classification", persona_classification_node)
workflow.add_node("product_recommendation", product_recommendation_node)
workflow.add_node("finalization", finalization_node)

# Define edges (workflow sequence)
workflow.add_edge("data_validation", "risk_assessment")
workflow.add_edge("risk_assessment", "persona_classification")
workflow.add_edge("persona_classification", "product_recommendation")
workflow.add_edge("product_recommendation", "finalization")
workflow.add_edge("finalization", END)

# Set entry point
workflow.set_entry_point("data_validation")

# Compile the graph
app = workflow.compile()
```

---

## Data Flow Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    DATA FLOW DIAGRAM                                          │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                               │
│  ┌─────────────────┐                                                                         │
│  │  RAW PROSPECT   │                                                                         │
│  │  DATA           │                                                                         │
│  │  ─────────────  │                                                                         │
│  │  • client_id    │                                                                         │
│  │  • name         │                                                                         │
│  │  • age          │                                                                         │
│  │  • income       │                                                                         │
│  │  • investment   │                                                                         │
│  │  • horizon      │                                                                         │
│  │  • risk_tol     │                                                                         │
│  └────────┬────────┘                                                                         │
│           │                                                                                  │
│           ▼                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐│
│  │                           SHARED STATE (WorkflowState)                                   ││
│  │                                                                                          ││
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   ││
│  │  │                 │  │                 │  │                 │  │                 │   ││
│  │  │  prospect_data  │  │ risk_assessment │  │  persona_result │  │recommendations │   ││
│  │  │  (Validated)    │  │                 │  │                 │  │                 │   ││
│  │  │                 │  │  • risk_level   │  │  • persona_type │  │  • products[]   │   ││
│  │  │  • quality_score│  │  • risk_factors │  │  • confidence   │  │  • scores[]     │   ││
│  │  │  • is_complete  │  │  • mitigations  │  │  • insights     │  │  • reasons[]    │   ││
│  │  │  • corrections  │  │  • confidence   │  │                 │  │                 │   ││
│  │  │                 │  │                 │  │                 │  │                 │   ││
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘   ││
│  │                                                                                          ││
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   ││
│  │  │                 │  │                 │  │                 │  │                 │   ││
│  │  │ goal_prediction │  │compliance_check │  │    insights     │  │    metrics      │   ││
│  │  │                 │  │                 │  │                 │  │                 │   ││
│  │  │  • probability  │  │  • is_compliant │  │  • key_points[] │  │  • exec_time    │   ││
│  │  │  • timeline     │  │  • warnings[]   │  │  • actions[]    │  │  • success_rate │   ││
│  │  │  • factors      │  │  • disclosures[]│  │  • next_steps[] │  │  • agent_logs[] │   ││
│  │  │                 │  │                 │  │                 │  │                 │   ││
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘   ││
│  │                                                                                          ││
│  └─────────────────────────────────────────────────────────────────────────────────────────┘│
│           │                                                                                  │
│           ▼                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐│
│  │                                FINAL OUTPUT                                              ││
│  │                                                                                          ││
│  │  ┌─────────────────────────────────────────────────────────────────────────────────┐   ││
│  │  │                                                                                  │   ││
│  │  │  ANALYSIS REPORT                                                                 │   ││
│  │  │  ═══════════════════════════════════════════════════════════════════════════    │   ││
│  │  │                                                                                  │   ││
│  │  │  Client: John Doe (C001)                                                         │   ││
│  │  │  ───────────────────────                                                         │   ││
│  │  │                                                                                  │   ││
│  │  │  Risk Profile: MODERATE (Confidence: 87%)                                        │   ││
│  │  │  Persona: Steady Saver                                                           │   ││
│  │  │  Goal Success Probability: 78%                                                   │   ││
│  │  │                                                                                  │   ││
│  │  │  TOP RECOMMENDATIONS:                                                            │   ││
│  │  │  1. Balanced Growth Fund (Suitability: 92%)                                      │   ││
│  │  │  2. Blue Chip Equity Fund (Suitability: 88%)                                     │   ││
│  │  │  3. Government Bond Fund (Suitability: 85%)                                      │   ││
│  │  │                                                                                  │   ││
│  │  │  COMPLIANCE: ✓ All checks passed                                                 │   ││
│  │  │  DISCLOSURES: [Standard investment risk disclosure]                              │   ││
│  │  │                                                                                  │   ││
│  │  │  RM ACTION ITEMS:                                                                │   ││
│  │  │  • Schedule follow-up call within 5 days                                         │   ││
│  │  │  • Discuss emergency fund allocation                                             │   ││
│  │  │  • Review insurance coverage                                                     │   ││
│  │  │                                                                                  │   ││
│  │  └─────────────────────────────────────────────────────────────────────────────────┘   ││
│  │                                                                                          ││
│  └─────────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                               │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## State Management

### Pydantic State Models

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ProspectData(BaseModel):
    client_id: str
    name: str
    age: int = Field(ge=18, le=100)
    income: float = Field(gt=0)
    investment_amount: float = Field(gt=0)
    investment_horizon: int = Field(ge=1, le=50)
    risk_tolerance: str

class RiskAssessmentResult(BaseModel):
    risk_level: RiskLevel
    risk_factors: List[str]
    mitigations: List[str]
    confidence: float = Field(ge=0, le=1)
    
class WorkflowState(BaseModel):
    prospect: ProspectData
    risk_assessment: Optional[RiskAssessmentResult] = None
    persona: Optional[PersonaResult] = None
    recommendations: List[ProductRecommendation] = []
    compliance: Optional[ComplianceCheck] = None
    insights: List[str] = []
    execution_metrics: dict = {}
```

---

## Hybrid Intelligence Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                              HYBRID INTELLIGENCE DESIGN                                       │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                               │
│                              ┌─────────────────────────┐                                     │
│                              │      INPUT DATA         │                                     │
│                              └────────────┬────────────┘                                     │
│                                           │                                                  │
│              ┌────────────────────────────┼────────────────────────────┐                    │
│              │                            │                            │                    │
│              ▼                            ▼                            ▼                    │
│   ┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐         │
│   │                     │     │                     │     │                     │         │
│   │   MACHINE LEARNING  │     │    LLM REASONING    │     │   RULE-BASED LOGIC  │         │
│   │                     │     │                     │     │                     │         │
│   │   ┌─────────────┐   │     │   ┌─────────────┐   │     │   ┌─────────────┐   │         │
│   │   │RandomForest │   │     │   │   Gemini    │   │     │   │  Business   │   │         │
│   │   │   Risk      │   │     │   │   API       │   │     │   │   Rules     │   │         │
│   │   └─────────────┘   │     │   └─────────────┘   │     │   └─────────────┘   │         │
│   │                     │     │                     │     │                     │         │
│   │   Purpose:          │     │   Purpose:          │     │   Purpose:          │         │
│   │   - Quantitative    │     │   - Qualitative     │     │   - Fallback        │         │
│   │     predictions     │     │     analysis        │     │     mechanism       │         │
│   │   - Risk scoring    │     │   - Explainability  │     │   - Guaranteed      │         │
│   │   - Goal probability│     │   - Context         │     │     output          │         │
│   │                     │     │     understanding   │     │   - Compliance      │         │
│   │   Accuracy: 89%     │     │                     │     │     enforcement     │         │
│   │                     │     │                     │     │                     │         │
│   └──────────┬──────────┘     └──────────┬──────────┘     └──────────┬──────────┘         │
│              │                            │                            │                    │
│              │                            │                            │                    │
│              └────────────────────────────┼────────────────────────────┘                    │
│                                           │                                                  │
│                                           ▼                                                  │
│                              ┌─────────────────────────┐                                     │
│                              │   DECISION FUSION       │                                     │
│                              │                         │                                     │
│                              │   Combines outputs      │                                     │
│                              │   from all three        │                                     │
│                              │   intelligence types    │                                     │
│                              │                         │                                     │
│                              │   Priority:             │                                     │
│                              │   1. ML (if available)  │                                     │
│                              │   2. LLM (if ML fails)  │                                     │
│                              │   3. Rules (fallback)   │                                     │
│                              └────────────┬────────────┘                                     │
│                                           │                                                  │
│                                           ▼                                                  │
│                              ┌─────────────────────────┐                                     │
│                              │     FINAL DECISION      │                                     │
│                              │   with Confidence Score │                                     │
│                              └─────────────────────────┘                                     │
│                                                                                               │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Fallback Mechanism

| Primary | Secondary | Tertiary | Trigger Condition |
|---------|-----------|----------|-------------------|
| ML Model | LLM | Rule-Based | Model file not found |
| ML Model | LLM | Rule-Based | Prediction confidence < 0.5 |
| LLM | Rule-Based | Default | API timeout/error |
| LLM | Rule-Based | Default | Rate limit exceeded |

---

## Deployment Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                              DEPLOYMENT ARCHITECTURE                                          │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐│
│  │                              PRODUCTION ENVIRONMENT                                      ││
│  │                                                                                          ││
│  │   ┌─────────────────────────────────────────────────────────────────────────────────┐  ││
│  │   │                           LOAD BALANCER (nginx/ALB)                              │  ││
│  │   └──────────────────────────────────────┬──────────────────────────────────────────┘  ││
│  │                                          │                                              ││
│  │              ┌───────────────────────────┼───────────────────────────┐                 ││
│  │              │                           │                           │                 ││
│  │              ▼                           ▼                           ▼                 ││
│  │   ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐             ││
│  │   │   APP SERVER    │       │   APP SERVER    │       │   APP SERVER    │             ││
│  │   │   Instance 1    │       │   Instance 2    │       │   Instance 3    │             ││
│  │   │                 │       │                 │       │                 │             ││
│  │   │  ┌───────────┐  │       │  ┌───────────┐  │       │  ┌───────────┐  │             ││
│  │   │  │ Streamlit │  │       │  │ Streamlit │  │       │  │ Streamlit │  │             ││
│  │   │  │ + LangGrph│  │       │  │ + LangGrph│  │       │  │ + LangGrph│  │             ││
│  │   │  └───────────┘  │       │  └───────────┘  │       │  └───────────┘  │             ││
│  │   └────────┬────────┘       └────────┬────────┘       └────────┬────────┘             ││
│  │            │                         │                         │                       ││
│  │            └─────────────────────────┼─────────────────────────┘                       ││
│  │                                      │                                                  ││
│  │                                      ▼                                                  ││
│  │   ┌─────────────────────────────────────────────────────────────────────────────────┐  ││
│  │   │                              SHARED SERVICES                                     │  ││
│  │   │                                                                                  │  ││
│  │   │   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐        │  ││
│  │   │   │   Redis     │   │  Database   │   │    Model    │   │   Logging   │        │  ││
│  │   │   │   Cache     │   │  (Postgres) │   │   Storage   │   │   (ELK)     │        │  ││
│  │   │   └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘        │  ││
│  │   │                                                                                  │  ││
│  │   └─────────────────────────────────────────────────────────────────────────────────┘  ││
│  │                                                                                          ││
│  └─────────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐│
│  │                              EXTERNAL SERVICES                                           ││
│  │                                                                                          ││
│  │   ┌─────────────────┐               ┌─────────────────┐                                 ││
│  │   │   Google Cloud  │               │   Monitoring    │                                 ││
│  │   │   Gemini API    │               │   (Datadog)     │                                 ││
│  │   └─────────────────┘               └─────────────────┘                                 ││
│  │                                                                                          ││
│  └─────────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                               │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Security Architecture

### Security Layers

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  SECURITY ARCHITECTURE                                        │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                               │
│  LAYER 1: NETWORK SECURITY                                                                   │
│  ═════════════════════════                                                                   │
│  • HTTPS/TLS encryption for all traffic                                                      │
│  • WAF (Web Application Firewall)                                                            │
│  • VPC isolation                                                                             │
│  • IP whitelisting for admin access                                                          │
│                                                                                               │
│  LAYER 2: APPLICATION SECURITY                                                               │
│  ═══════════════════════════════                                                             │
│  • Input validation (Pydantic)                                                               │
│  • SQL injection prevention                                                                  │
│  • XSS protection                                                                            │
│  • CSRF tokens                                                                               │
│                                                                                               │
│  LAYER 3: DATA SECURITY                                                                      │
│  ══════════════════════════                                                                  │
│  • Data encryption at rest (AES-256)                                                         │
│  • PII masking in logs                                                                       │
│  • Secure credential storage (Vault/Secrets Manager)                                         │
│  • Data retention policies                                                                   │
│                                                                                               │
│  LAYER 4: ACCESS CONTROL                                                                     │
│  ═════════════════════════                                                                   │
│  • Role-based access control (RBAC)                                                          │
│  • OAuth 2.0 / SSO integration                                                               │
│  • Audit logging                                                                             │
│  • Session management                                                                        │
│                                                                                               │
│  LAYER 5: COMPLIANCE                                                                         │
│  ═══════════════════════                                                                     │
│  • GDPR compliance                                                                           │
│  • Financial regulations (MiFID II, SEC)                                                     │
│  • Data localization requirements                                                            │
│  • Regular security audits                                                                   │
│                                                                                               │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Next Steps

For implementation details of each component, see:
- [Technical Deep Dive](technical-deep-dive.md)
- [API Reference](api-reference.md)
- [Interview Guide](interview-guide.md)
