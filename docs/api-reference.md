# API Reference

## RM-AgenticAI-LangGraph API Documentation

---

## Table of Contents

1. [State Models](#state-models)
2. [Agents API](#agents-api)
3. [Workflow API](#workflow-api)
4. [Configuration](#configuration)
5. [Utilities](#utilities)

---

## State Models

### ProspectData

Client/Prospect input data model.

```python
from pydantic import BaseModel, Field

class ProspectData(BaseModel):
    client_id: str
    name: str
    age: int = Field(ge=18, le=100)
    income: float = Field(gt=0)
    investment_amount: float = Field(gt=0)
    investment_horizon: int = Field(ge=1, le=50)
    risk_tolerance: str  # "low", "medium", "high"
    monthly_contribution: Optional[float] = 0
    existing_investments: Optional[float] = 0
    financial_goals: Optional[List[str]] = []
```

**Example:**
```python
prospect = ProspectData(
    client_id="C001",
    name="John Doe",
    age=35,
    income=150000,
    investment_amount=50000,
    investment_horizon=10,
    risk_tolerance="medium"
)
```

---

### RiskAssessmentResult

Output from risk assessment agent.

```python
class RiskAssessmentResult(BaseModel):
    risk_level: RiskLevel  # LOW, MEDIUM, HIGH
    risk_score: float      # 0.0 - 1.0
    risk_factors: List[str]
    mitigation_suggestions: List[str]
    confidence: float      # 0.0 - 1.0
    reasoning: str
    method_used: str       # "ml", "llm", "rule_based"
```

**Example Response:**
```json
{
    "risk_level": "MEDIUM",
    "risk_score": 0.72,
    "risk_factors": [
        "Moderate income-to-investment ratio",
        "10-year horizon provides recovery time",
        "Stated medium risk tolerance"
    ],
    "mitigation_suggestions": [
        "Maintain 6-month emergency fund",
        "Diversify across asset classes",
        "Review allocation annually"
    ],
    "confidence": 0.87,
    "reasoning": "Based on age (35), income ($150K), and 10-year horizon...",
    "method_used": "ml"
}
```

---

### PersonaResult

Investor persona classification output.

```python
class PersonaResult(BaseModel):
    persona_type: PersonaType  # AGGRESSIVE_GROWTH, STEADY_SAVER, CAUTIOUS_PLANNER
    confidence: float
    behavioral_insights: List[str]
    investment_preferences: Dict[str, Any]
    communication_style: str
```

---

### ProductRecommendation

Single product recommendation.

```python
class ProductRecommendation(BaseModel):
    product_id: str
    product_name: str
    product_type: str      # "equity", "fixed_income", "balanced"
    risk_rating: str       # "low", "medium", "high"
    expected_return: float
    suitability_score: float  # 0.0 - 1.0
    allocation_percentage: float  # 0 - 100
    justification: str
    warnings: List[str]
```

---

### WorkflowState

Complete workflow state container.

```python
class WorkflowState(BaseModel):
    # Input
    prospect: ProspectData
    
    # Processing results
    data_quality_score: Optional[float] = None
    risk_assessment: Optional[RiskAssessmentResult] = None
    persona: Optional[PersonaResult] = None
    goal_prediction: Optional[GoalPredictionResult] = None
    recommendations: List[ProductRecommendation] = []
    compliance: Optional[ComplianceCheck] = None
    
    # Insights
    key_insights: List[str] = []
    action_items: List[str] = []
    disclosures: List[str] = []
    
    # Metrics
    overall_confidence: float = 0.0
    execution_metrics: List[ExecutionMetrics] = []
```

---

## Agents API

### BaseAgent

Abstract base class for all agents.

```python
class BaseAgent(ABC):
    def __init__(self, name: str):
        """Initialize agent with name"""
        
    @abstractmethod
    async def _execute(self, **kwargs) -> Any:
        """Core execution logic - implemented by subclasses"""
        
    @abstractmethod
    def _fallback(self, **kwargs) -> Any:
        """Fallback logic when primary execution fails"""
        
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute agent with error handling and metrics.
        
        Returns:
            {
                "result": <agent result>,
                "metrics": ExecutionMetrics,
                "log_entry": str
            }
        """
```

---

### DataAnalystAgent

Validates and scores input data quality.

```python
class DataAnalystAgent(BaseAgent):
    async def execute(self, prospect: ProspectData) -> Dict:
        """
        Validate prospect data and generate quality score.
        
        Args:
            prospect: ProspectData object
            
        Returns:
            {
                "result": {
                    "validated_data": ProspectData,
                    "quality_score": float,
                    "issues": List[str],
                    "corrections": List[str]
                },
                "metrics": ExecutionMetrics
            }
        """
```

**Usage:**
```python
agent = DataAnalystAgent()
result = await agent.execute(prospect=prospect_data)
print(f"Quality Score: {result['result']['quality_score']}")
```

---

### RiskAssessmentAgent

Assesses investor risk profile using ML + LLM.

```python
class RiskAssessmentAgent(BaseAgent):
    async def execute(self, prospect: ProspectData) -> Dict:
        """
        Assess risk profile using ML model and LLM analysis.
        
        Args:
            prospect: Validated prospect data
            
        Returns:
            {
                "result": RiskAssessmentResult,
                "metrics": ExecutionMetrics
            }
        """
```

**Methods:**

| Method | Description |
|--------|-------------|
| `_ml_predict(prospect)` | ML model prediction |
| `_llm_analyze(prospect, risk_level)` | LLM explanation generation |
| `_rule_based_assessment(prospect)` | Fallback rule-based logic |

---

### PersonaAgent

Classifies investor behavioral persona.

```python
class PersonaAgent(BaseAgent):
    async def execute(
        self, 
        prospect: ProspectData, 
        risk_profile: RiskAssessmentResult
    ) -> Dict:
        """
        Classify investor persona based on profile and risk.
        
        Args:
            prospect: Prospect data
            risk_profile: Risk assessment result
            
        Returns:
            {
                "result": PersonaResult,
                "metrics": ExecutionMetrics
            }
        """
```

---

### ProductSpecialistAgent

Generates product recommendations.

```python
class ProductSpecialistAgent(BaseAgent):
    async def execute(
        self,
        persona: PersonaResult,
        risk_profile: RiskAssessmentResult
    ) -> Dict:
        """
        Generate product recommendations.
        
        Args:
            persona: Investor persona
            risk_profile: Risk assessment
            
        Returns:
            {
                "result": {
                    "products": List[ProductRecommendation]
                },
                "metrics": ExecutionMetrics
            }
        """
```

**Scoring Algorithm:**
```python
score = (
    persona_match * 0.4 +    # Persona alignment (40%)
    risk_alignment * 0.3 +   # Risk compatibility (30%)
    return_score * 0.2 +     # Return optimization (20%)
    diversification * 0.1    # Portfolio diversity (10%)
)
```

---

### ComplianceAgent

Validates regulatory compliance.

```python
class ComplianceAgent(BaseAgent):
    async def execute(self, state: WorkflowState) -> Dict:
        """
        Validate compliance of recommendations.
        
        Args:
            state: Complete workflow state
            
        Returns:
            {
                "result": ComplianceCheck,
                "metrics": ExecutionMetrics
            }
        """
```

**Checks Performed:**
- Suitability validation
- Concentration risk check
- KYC completeness
- Regulatory disclosure requirements

---

## Workflow API

### create_workflow()

Create and compile the LangGraph workflow.

```python
def create_workflow() -> CompiledGraph:
    """
    Create the complete advisory workflow.
    
    Returns:
        Compiled LangGraph workflow ready for execution
        
    Example:
        workflow = create_workflow()
        result = await workflow.ainvoke({"prospect": prospect_data.dict()})
    """
```

---

### Workflow Execution

**Synchronous Execution:**
```python
workflow = create_workflow()
result = workflow.invoke({"prospect": prospect_data.dict()})
```

**Asynchronous Execution:**
```python
workflow = create_workflow()
result = await workflow.ainvoke({"prospect": prospect_data.dict()})
```

**Batch Processing:**
```python
from utils.async_utils import AsyncBatchProcessor

processor = AsyncBatchProcessor(max_concurrent=5)
results = await processor.process_batch(prospects, workflow.ainvoke)
```

---

### Workflow Configuration

```python
# Custom configuration
workflow = create_workflow(
    config={
        "checkpoint": True,          # Enable state checkpointing
        "max_retries": 3,           # Retry failed nodes
        "timeout_seconds": 60,      # Node execution timeout
        "fallback_enabled": True    # Use fallback logic
    }
)
```

---

## Configuration

### Settings

```python
# config/settings.py

class Settings:
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    
    # Model Paths
    RISK_MODEL_PATH: str = "data/models/risk_model.pkl"
    GOAL_MODEL_PATH: str = "data/models/goal_model.pkl"
    
    # Data Paths
    PRODUCT_CATALOG_PATH: str = "data/products.csv"
    PROSPECT_DATA_PATH: str = "data/prospects.csv"
    
    # LLM Configuration
    LLM_MODEL: str = "gemini-pro"
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 2048
    LLM_TIMEOUT: int = 30
    
    # Processing
    MAX_CONCURRENT_REQUESTS: int = 5
    CACHE_TTL_SECONDS: int = 300
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_PATH: str = "logs"
```

---

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Cloud API key for Gemini | Required |
| `LOG_LEVEL` | Logging level | INFO |
| `MAX_CONCURRENT` | Max concurrent analyses | 5 |
| `MODEL_PATH` | Path to ML models | data/models |

---

## Utilities

### CacheManager

```python
class CacheManager:
    def __init__(self):
        self.llm_cache = TTLCache(maxsize=100, ttl=300)
        self.prediction_cache = TTLCache(maxsize=500, ttl=3600)
    
    def get_cached_llm(self, prompt_key: str) -> Any
    def set_cached_llm(self, prompt_key: str, response: Any)
    def get_cached_prediction(self, features: dict) -> Any
    def set_cached_prediction(self, features: dict, prediction: Any)
```

---

### MetricsCollector

```python
class MetricsCollector:
    def record(
        self, 
        agent_name: str, 
        duration_ms: float, 
        success: bool, 
        fallback: bool = False
    )
    
    def get_summary(self) -> Dict:
        """
        Returns:
            {
                "total_executions": int,
                "success_rate": float,
                "fallback_rate": float,
                "avg_duration_ms": float,
                "by_agent": Dict[str, Dict]
            }
        """
```

---

### Error Handling Decorators

```python
# Retry with exponential backoff
@with_retry(max_retries=3, delay=1.0, backoff=2.0)
async def my_function():
    pass

# Timeout wrapper
@with_timeout(30.0)
async def my_function():
    pass

# Fallback on failure
@with_fallback(fallback_func)
async def my_function():
    pass
```

---

## Response Codes

| Code | Description |
|------|-------------|
| SUCCESS | Operation completed successfully |
| FALLBACK_USED | Primary method failed, fallback used |
| VALIDATION_ERROR | Input validation failed |
| ML_ERROR | ML model error |
| LLM_ERROR | LLM API error |
| TIMEOUT | Operation timed out |
| COMPLIANCE_FAIL | Compliance check failed |

---

## Rate Limits

| Component | Limit | Window |
|-----------|-------|--------|
| Gemini API | 60 requests | per minute |
| Batch Processing | 5 concurrent | per instance |
| Cache Size | 100 LLM / 500 ML | entries |

---

## Examples

### Complete Workflow Example

```python
import asyncio
from graph import create_workflow
from state import ProspectData

async def main():
    # Create workflow
    workflow = create_workflow()
    
    # Prepare prospect data
    prospect = ProspectData(
        client_id="C001",
        name="John Doe",
        age=35,
        income=150000,
        investment_amount=50000,
        investment_horizon=10,
        risk_tolerance="medium"
    )
    
    # Execute workflow
    result = await workflow.ainvoke({"prospect": prospect.dict()})
    
    # Access results
    print(f"Risk Level: {result['risk_assessment']['risk_level']}")
    print(f"Persona: {result['persona']['persona_type']}")
    print(f"Top Recommendation: {result['recommendations'][0]['product_name']}")
    print(f"Compliance: {result['compliance']['status']}")
    
    return result

# Run
result = asyncio.run(main())
```

### Custom Agent Execution

```python
from agents import RiskAssessmentAgent

async def assess_risk(prospect_data):
    agent = RiskAssessmentAgent()
    result = await agent.execute(prospect=prospect_data)
    
    if result['metrics'].fallback_used:
        print("Warning: Fallback logic was used")
    
    return result['result']
```

---

## Changelog

### Version 1.0.0
- Initial release
- 5 specialized agents
- ML + LLM hybrid intelligence
- LangGraph orchestration
- Streamlit UI
