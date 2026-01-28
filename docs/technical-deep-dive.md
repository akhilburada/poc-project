# Technical Deep Dive

## RM-AgenticAI-LangGraph Implementation Details

---

## Table of Contents

1. [LangGraph Orchestration](#langgraph-orchestration)
2. [State Management with Pydantic](#state-management-with-pydantic)
3. [Agent Implementation](#agent-implementation)
4. [Machine Learning Pipeline](#machine-learning-pipeline)
5. [LLM Integration](#llm-integration)
6. [Error Handling & Fallbacks](#error-handling--fallbacks)
7. [Async Processing](#async-processing)
8. [Logging & Monitoring](#logging--monitoring)
9. [Testing Strategy](#testing-strategy)
10. [Performance Optimization](#performance-optimization)

---

## 1. LangGraph Orchestration

### What is LangGraph?

LangGraph is a library for building stateful, multi-actor applications with LLMs. It extends LangChain Expression Language with the ability to coordinate multiple chains (or actors) across multiple steps of computation in a cyclic manner.

### Key Concepts

#### StateGraph
A graph where each node represents a computation step and edges define the flow between steps.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# Define state structure
class WorkflowState(TypedDict):
    prospect: dict
    risk_assessment: dict
    persona: dict
    recommendations: list
    messages: Annotated[list, operator.add]  # Append-only field

# Create graph
workflow = StateGraph(WorkflowState)
```

#### Nodes
Functions that receive the current state and return updates to the state.

```python
def data_validation_node(state: WorkflowState) -> dict:
    """
    Node 1: Validate and clean input data
    """
    prospect = state["prospect"]
    
    # Run validation
    agent = DataAnalystAgent()
    result = agent.execute(prospect)
    
    # Return state updates
    return {
        "prospect": result.validated_data,
        "messages": [f"Data validation complete. Quality score: {result.quality_score}"]
    }
```

#### Edges
Define the flow between nodes. Can be:
- **Static**: Always go to the same next node
- **Conditional**: Choose next node based on state

```python
# Static edges
workflow.add_edge("data_validation", "risk_assessment")
workflow.add_edge("risk_assessment", "persona_classification")

# Conditional edge example
def should_continue(state: WorkflowState) -> str:
    """Route based on risk level"""
    if state["risk_assessment"]["risk_level"] == "HIGH":
        return "compliance_check"  # Additional validation for high risk
    return "persona_classification"

workflow.add_conditional_edges(
    "risk_assessment",
    should_continue,
    {
        "compliance_check": "compliance_check",
        "persona_classification": "persona_classification"
    }
)
```

### Complete Graph Definition

```python
# graph.py - Complete implementation

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from state import WorkflowState
from agents import (
    DataAnalystAgent,
    RiskAssessmentAgent,
    PersonaAgent,
    ProductSpecialistAgent,
    ComplianceAgent
)

def create_workflow():
    """Create and compile the LangGraph workflow"""
    
    # Initialize graph with state schema
    workflow = StateGraph(WorkflowState)
    
    # Define node functions
    async def data_validation(state: WorkflowState) -> dict:
        agent = DataAnalystAgent()
        result = await agent.execute(state["prospect"])
        return {
            "data_quality": result.quality_score,
            "prospect": result.validated_data,
            "execution_log": [result.log_entry]
        }
    
    async def risk_assessment(state: WorkflowState) -> dict:
        agent = RiskAssessmentAgent()
        result = await agent.execute(state["prospect"])
        return {
            "risk_assessment": result.to_dict(),
            "execution_log": [result.log_entry]
        }
    
    async def persona_classification(state: WorkflowState) -> dict:
        agent = PersonaAgent()
        result = await agent.execute(
            prospect=state["prospect"],
            risk_profile=state["risk_assessment"]
        )
        return {
            "persona": result.to_dict(),
            "execution_log": [result.log_entry]
        }
    
    async def product_recommendation(state: WorkflowState) -> dict:
        agent = ProductSpecialistAgent()
        result = await agent.execute(
            persona=state["persona"],
            risk_profile=state["risk_assessment"]
        )
        return {
            "recommendations": [r.to_dict() for r in result.products],
            "execution_log": [result.log_entry]
        }
    
    async def finalization(state: WorkflowState) -> dict:
        compliance_agent = ComplianceAgent()
        compliance_result = await compliance_agent.execute(state)
        
        # Aggregate insights
        insights = generate_insights(state)
        action_items = generate_action_items(state)
        
        return {
            "compliance": compliance_result.to_dict(),
            "insights": insights,
            "action_items": action_items,
            "overall_confidence": calculate_confidence(state),
            "execution_log": [compliance_result.log_entry]
        }
    
    # Add nodes to graph
    workflow.add_node("data_validation", data_validation)
    workflow.add_node("risk_assessment", risk_assessment)
    workflow.add_node("persona_classification", persona_classification)
    workflow.add_node("product_recommendation", product_recommendation)
    workflow.add_node("finalization", finalization)
    
    # Define edges
    workflow.add_edge("data_validation", "risk_assessment")
    workflow.add_edge("risk_assessment", "persona_classification")
    workflow.add_edge("persona_classification", "product_recommendation")
    workflow.add_edge("product_recommendation", "finalization")
    workflow.add_edge("finalization", END)
    
    # Set entry point
    workflow.set_entry_point("data_validation")
    
    # Add checkpointing for state persistence (optional)
    memory = SqliteSaver.from_conn_string(":memory:")
    
    # Compile and return
    return workflow.compile(checkpointer=memory)
```

---

## 2. State Management with Pydantic

### Why Pydantic?

- **Type Safety**: Catch errors at runtime before they propagate
- **Validation**: Automatic validation of data types and constraints
- **Serialization**: Easy JSON serialization/deserialization
- **Documentation**: Self-documenting schemas

### Complete State Models

```python
# state.py - Complete state definitions

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

# Enums for type safety
class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class PersonaType(str, Enum):
    AGGRESSIVE_GROWTH = "aggressive_growth"
    STEADY_SAVER = "steady_saver"
    CAUTIOUS_PLANNER = "cautious_planner"

class ComplianceStatus(str, Enum):
    PASSED = "passed"
    WARNING = "warning"
    FAILED = "failed"

# Input Models
class ProspectData(BaseModel):
    """Client/Prospect input data"""
    client_id: str = Field(..., description="Unique client identifier")
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=18, le=100, description="Client age (18-100)")
    income: float = Field(..., gt=0, description="Annual income in USD")
    investment_amount: float = Field(..., gt=0, description="Amount to invest")
    investment_horizon: int = Field(..., ge=1, le=50, description="Years")
    risk_tolerance: str = Field(..., description="low/medium/high")
    monthly_contribution: Optional[float] = Field(default=0)
    existing_investments: Optional[float] = Field(default=0)
    financial_goals: Optional[List[str]] = Field(default_factory=list)
    
    @validator('risk_tolerance')
    def validate_risk_tolerance(cls, v):
        allowed = ['low', 'medium', 'high']
        if v.lower() not in allowed:
            raise ValueError(f'risk_tolerance must be one of {allowed}')
        return v.lower()
    
    class Config:
        json_schema_extra = {
            "example": {
                "client_id": "C001",
                "name": "John Doe",
                "age": 35,
                "income": 150000,
                "investment_amount": 50000,
                "investment_horizon": 10,
                "risk_tolerance": "medium"
            }
        }

# Result Models
class RiskAssessmentResult(BaseModel):
    """Output from risk assessment agent"""
    risk_level: RiskLevel
    risk_score: float = Field(..., ge=0, le=1)
    risk_factors: List[str] = Field(default_factory=list)
    mitigation_suggestions: List[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0, le=1)
    reasoning: str = Field(default="")
    method_used: str = Field(default="ml")  # ml, llm, or rule_based
    
    @property
    def is_high_risk(self) -> bool:
        return self.risk_level == RiskLevel.HIGH

class PersonaResult(BaseModel):
    """Output from persona classification agent"""
    persona_type: PersonaType
    confidence: float = Field(..., ge=0, le=1)
    behavioral_insights: List[str] = Field(default_factory=list)
    investment_preferences: Dict[str, Any] = Field(default_factory=dict)
    communication_style: str = Field(default="")

class GoalPredictionResult(BaseModel):
    """Output from goal planning agent"""
    success_probability: float = Field(..., ge=0, le=1)
    projected_value: float
    shortfall_amount: Optional[float] = None
    key_factors: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)

class ProductRecommendation(BaseModel):
    """Single product recommendation"""
    product_id: str
    product_name: str
    product_type: str
    risk_rating: str
    expected_return: float
    suitability_score: float = Field(..., ge=0, le=1)
    allocation_percentage: float = Field(..., ge=0, le=100)
    justification: str
    warnings: List[str] = Field(default_factory=list)

class ComplianceCheck(BaseModel):
    """Output from compliance agent"""
    status: ComplianceStatus
    checks_performed: List[str] = Field(default_factory=list)
    passed_checks: List[str] = Field(default_factory=list)
    failed_checks: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    disclosures: List[str] = Field(default_factory=list)
    regulatory_notes: List[str] = Field(default_factory=list)

class ExecutionMetrics(BaseModel):
    """Agent execution metrics"""
    agent_name: str
    start_time: datetime
    end_time: datetime
    duration_ms: float
    success: bool
    error_message: Optional[str] = None
    fallback_used: bool = False

# Aggregate State Model
class WorkflowState(BaseModel):
    """Complete workflow state container"""
    # Input
    prospect: ProspectData
    
    # Processing results
    data_quality_score: Optional[float] = None
    risk_assessment: Optional[RiskAssessmentResult] = None
    persona: Optional[PersonaResult] = None
    goal_prediction: Optional[GoalPredictionResult] = None
    recommendations: List[ProductRecommendation] = Field(default_factory=list)
    compliance: Optional[ComplianceCheck] = None
    
    # Insights and actions
    key_insights: List[str] = Field(default_factory=list)
    action_items: List[str] = Field(default_factory=list)
    disclosures: List[str] = Field(default_factory=list)
    
    # Metrics
    overall_confidence: float = Field(default=0.0)
    execution_metrics: List[ExecutionMetrics] = Field(default_factory=list)
    
    # Status tracking
    current_node: str = Field(default="")
    completed_nodes: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    
    def add_metric(self, metric: ExecutionMetrics):
        self.execution_metrics.append(metric)
        
    def mark_node_complete(self, node_name: str):
        self.completed_nodes.append(node_name)
        
    def calculate_overall_confidence(self) -> float:
        """Calculate weighted average confidence across all components"""
        confidences = []
        weights = []
        
        if self.risk_assessment:
            confidences.append(self.risk_assessment.confidence)
            weights.append(0.3)  # 30% weight
            
        if self.persona:
            confidences.append(self.persona.confidence)
            weights.append(0.2)  # 20% weight
            
        if self.goal_prediction:
            confidences.append(self.goal_prediction.success_probability)
            weights.append(0.3)  # 30% weight
            
        if self.recommendations:
            avg_suitability = sum(r.suitability_score for r in self.recommendations) / len(self.recommendations)
            confidences.append(avg_suitability)
            weights.append(0.2)  # 20% weight
            
        if not confidences:
            return 0.0
            
        total_weight = sum(weights)
        return sum(c * w for c, w in zip(confidences, weights)) / total_weight
```

---

## 3. Agent Implementation

### Base Agent Pattern

```python
# agents/base_agent.py

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime
from loguru import logger
from state import ExecutionMetrics

class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logger.bind(agent=name)
        self._start_time: Optional[datetime] = None
        
    @abstractmethod
    async def _execute(self, **kwargs) -> Any:
        """Core execution logic - implemented by subclasses"""
        pass
    
    @abstractmethod
    def _fallback(self, **kwargs) -> Any:
        """Fallback logic when primary execution fails"""
        pass
    
    async def execute(self, **kwargs) -> Any:
        """
        Execute agent with error handling and metrics
        """
        self._start_time = datetime.now()
        self.logger.info(f"Starting execution with inputs: {list(kwargs.keys())}")
        
        try:
            # Primary execution
            result = await self._execute(**kwargs)
            self.logger.info("Execution completed successfully")
            return self._wrap_result(result, success=True)
            
        except Exception as e:
            self.logger.warning(f"Primary execution failed: {e}, attempting fallback")
            
            try:
                # Fallback execution
                result = self._fallback(**kwargs)
                self.logger.info("Fallback execution completed")
                return self._wrap_result(result, success=True, fallback_used=True)
                
            except Exception as fallback_error:
                self.logger.error(f"Fallback also failed: {fallback_error}")
                return self._wrap_result(None, success=False, error=str(fallback_error))
    
    def _wrap_result(
        self, 
        result: Any, 
        success: bool, 
        fallback_used: bool = False,
        error: Optional[str] = None
    ) -> Dict[str, Any]:
        """Wrap result with execution metrics"""
        end_time = datetime.now()
        duration = (end_time - self._start_time).total_seconds() * 1000
        
        metrics = ExecutionMetrics(
            agent_name=self.name,
            start_time=self._start_time,
            end_time=end_time,
            duration_ms=duration,
            success=success,
            error_message=error,
            fallback_used=fallback_used
        )
        
        return {
            "result": result,
            "metrics": metrics,
            "log_entry": f"{self.name}: {'SUCCESS' if success else 'FAILED'} in {duration:.2f}ms"
        }
```

### Risk Assessment Agent Implementation

```python
# agents/risk_assessment_agent.py

import pickle
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from state import ProspectData, RiskAssessmentResult, RiskLevel
from .base_agent import BaseAgent
from config.settings import Settings

class RiskAssessmentAgent(BaseAgent):
    """
    Agent responsible for assessing investor risk profile
    Uses: ML Model (primary) + LLM (explanation) + Rules (fallback)
    """
    
    def __init__(self):
        super().__init__("RiskAssessmentAgent")
        self.settings = Settings()
        self.model = self._load_model()
        self.llm = self._init_llm()
        
    def _load_model(self) -> Optional[Any]:
        """Load trained ML model"""
        model_path = Path(self.settings.RISK_MODEL_PATH)
        if model_path.exists():
            with open(model_path, 'rb') as f:
                return pickle.load(f)
        self.logger.warning("Risk model not found, will use fallback")
        return None
    
    def _init_llm(self) -> Optional[ChatGoogleGenerativeAI]:
        """Initialize Gemini LLM client"""
        try:
            return ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=self.settings.GOOGLE_API_KEY,
                temperature=0.3
            )
        except Exception as e:
            self.logger.warning(f"Failed to init LLM: {e}")
            return None
    
    async def _execute(self, prospect: ProspectData) -> RiskAssessmentResult:
        """
        Primary execution: ML prediction + LLM explanation
        """
        # Step 1: ML Prediction
        if self.model:
            risk_level, risk_score = self._ml_predict(prospect)
            method = "ml"
        else:
            # If no ML model, use rule-based
            risk_level, risk_score = self._rule_based_assessment(prospect)
            method = "rule_based"
        
        # Step 2: LLM Analysis for explanation and factors
        risk_factors, mitigations, reasoning = await self._llm_analyze(prospect, risk_level)
        
        # Step 3: Calculate confidence
        confidence = self._calculate_confidence(risk_score, method)
        
        return RiskAssessmentResult(
            risk_level=risk_level,
            risk_score=risk_score,
            risk_factors=risk_factors,
            mitigation_suggestions=mitigations,
            confidence=confidence,
            reasoning=reasoning,
            method_used=method
        )
    
    def _ml_predict(self, prospect: ProspectData) -> tuple[RiskLevel, float]:
        """Make prediction using trained ML model"""
        # Prepare features
        features = np.array([[
            prospect.age,
            prospect.income,
            prospect.investment_amount,
            prospect.investment_horizon,
            self._encode_risk_tolerance(prospect.risk_tolerance)
        ]])
        
        # Get prediction and probability
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        
        risk_map = {0: RiskLevel.LOW, 1: RiskLevel.MEDIUM, 2: RiskLevel.HIGH}
        risk_level = risk_map[prediction]
        risk_score = probabilities[prediction]
        
        return risk_level, risk_score
    
    def _encode_risk_tolerance(self, tolerance: str) -> int:
        """Encode risk tolerance string to numeric"""
        encoding = {'low': 0, 'medium': 1, 'high': 2}
        return encoding.get(tolerance.lower(), 1)
    
    async def _llm_analyze(
        self, 
        prospect: ProspectData, 
        risk_level: RiskLevel
    ) -> tuple[list, list, str]:
        """Use LLM to generate risk factors and explanations"""
        if not self.llm:
            return self._template_analysis(prospect, risk_level)
        
        prompt = PromptTemplate(
            template="""
            Analyze the following investor profile for risk factors:
            
            Age: {age}
            Annual Income: ${income:,.0f}
            Investment Amount: ${investment_amount:,.0f}
            Investment Horizon: {horizon} years
            Risk Tolerance: {risk_tolerance}
            Predicted Risk Level: {risk_level}
            
            Provide:
            1. Key risk factors (3-5 bullet points)
            2. Mitigation suggestions (3-5 bullet points)
            3. Brief reasoning for the risk classification (2-3 sentences)
            
            Format your response as JSON with keys: risk_factors, mitigations, reasoning
            """,
            input_variables=["age", "income", "investment_amount", "horizon", 
                           "risk_tolerance", "risk_level"]
        )
        
        try:
            response = await self.llm.ainvoke(
                prompt.format(
                    age=prospect.age,
                    income=prospect.income,
                    investment_amount=prospect.investment_amount,
                    horizon=prospect.investment_horizon,
                    risk_tolerance=prospect.risk_tolerance,
                    risk_level=risk_level.value
                )
            )
            
            # Parse JSON response
            import json
            data = json.loads(response.content)
            return data['risk_factors'], data['mitigations'], data['reasoning']
            
        except Exception as e:
            self.logger.warning(f"LLM analysis failed: {e}")
            return self._template_analysis(prospect, risk_level)
    
    def _template_analysis(
        self, 
        prospect: ProspectData, 
        risk_level: RiskLevel
    ) -> tuple[list, list, str]:
        """Template-based analysis when LLM is unavailable"""
        risk_factors = []
        mitigations = []
        
        # Age-based factors
        if prospect.age < 30:
            risk_factors.append("Young age allows for higher risk tolerance")
            mitigations.append("Consider growth-oriented investments")
        elif prospect.age > 55:
            risk_factors.append("Approaching retirement requires capital preservation")
            mitigations.append("Shift towards fixed-income investments")
        
        # Income-based factors
        income_to_investment = prospect.investment_amount / prospect.income
        if income_to_investment > 0.5:
            risk_factors.append("High investment ratio relative to income")
            mitigations.append("Ensure adequate emergency fund before investing")
        
        # Horizon-based factors
        if prospect.investment_horizon < 5:
            risk_factors.append("Short investment horizon limits recovery time")
            mitigations.append("Focus on lower-volatility investments")
        
        reasoning = f"Based on profile analysis, {risk_level.value} risk classification is appropriate."
        
        return risk_factors, mitigations, reasoning
    
    def _rule_based_assessment(self, prospect: ProspectData) -> tuple[RiskLevel, float]:
        """Rule-based fallback when ML model is unavailable"""
        score = 0
        
        # Age scoring (younger = higher risk capacity)
        if prospect.age < 35:
            score += 2
        elif prospect.age < 50:
            score += 1
        
        # Income scoring (higher = more risk capacity)
        if prospect.income > 200000:
            score += 2
        elif prospect.income > 100000:
            score += 1
        
        # Horizon scoring (longer = more risk capacity)
        if prospect.investment_horizon > 15:
            score += 2
        elif prospect.investment_horizon > 7:
            score += 1
        
        # Risk tolerance
        tolerance_score = {'low': 0, 'medium': 1, 'high': 2}
        score += tolerance_score.get(prospect.risk_tolerance.lower(), 1)
        
        # Determine risk level
        if score <= 2:
            return RiskLevel.LOW, 0.7
        elif score <= 5:
            return RiskLevel.MEDIUM, 0.75
        else:
            return RiskLevel.HIGH, 0.8
    
    def _calculate_confidence(self, score: float, method: str) -> float:
        """Calculate confidence based on method and score"""
        base_confidence = score
        
        # Adjust based on method
        method_adjustment = {
            'ml': 1.0,        # Full confidence in ML
            'llm': 0.9,       # Slightly less for LLM
            'rule_based': 0.7  # Lower for rules
        }
        
        return min(1.0, base_confidence * method_adjustment.get(method, 0.7))
    
    def _fallback(self, prospect: ProspectData) -> RiskAssessmentResult:
        """Complete fallback when all else fails"""
        risk_level, risk_score = self._rule_based_assessment(prospect)
        risk_factors, mitigations, reasoning = self._template_analysis(prospect, risk_level)
        
        return RiskAssessmentResult(
            risk_level=risk_level,
            risk_score=risk_score,
            risk_factors=risk_factors,
            mitigation_suggestions=mitigations,
            confidence=0.5,  # Low confidence for fallback
            reasoning=reasoning,
            method_used="rule_based"
        )
```

### Product Specialist Agent Implementation

```python
# agents/product_specialist_agent.py

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from state import (
    PersonaResult, RiskAssessmentResult, ProductRecommendation, 
    RiskLevel, PersonaType
)
from .base_agent import BaseAgent
from config.settings import Settings

class ProductSpecialistAgent(BaseAgent):
    """
    Agent responsible for matching and recommending investment products
    """
    
    def __init__(self):
        super().__init__("ProductSpecialistAgent")
        self.settings = Settings()
        self.products = self._load_products()
        
    def _load_products(self) -> pd.DataFrame:
        """Load product catalog"""
        product_path = Path(self.settings.PRODUCT_CATALOG_PATH)
        if product_path.exists():
            return pd.read_csv(product_path)
        return self._get_default_products()
    
    def _get_default_products(self) -> pd.DataFrame:
        """Default products when catalog unavailable"""
        return pd.DataFrame([
            {"id": "P001", "name": "Conservative Bond Fund", "type": "fixed_income", 
             "risk": "low", "expected_return": 0.04, "min_investment": 1000},
            {"id": "P002", "name": "Balanced Growth Fund", "type": "balanced", 
             "risk": "medium", "expected_return": 0.07, "min_investment": 5000},
            {"id": "P003", "name": "Aggressive Equity Fund", "type": "equity", 
             "risk": "high", "expected_return": 0.12, "min_investment": 10000},
            {"id": "P004", "name": "Blue Chip Dividend Fund", "type": "equity", 
             "risk": "medium", "expected_return": 0.08, "min_investment": 5000},
            {"id": "P005", "name": "Government Securities Fund", "type": "fixed_income", 
             "risk": "low", "expected_return": 0.035, "min_investment": 1000},
        ])
    
    async def _execute(
        self, 
        persona: PersonaResult, 
        risk_profile: RiskAssessmentResult
    ) -> Dict[str, Any]:
        """Generate product recommendations based on persona and risk"""
        
        # Step 1: Filter products by risk compatibility
        filtered_products = self._filter_by_risk(risk_profile.risk_level)
        
        # Step 2: Score products based on persona match
        scored_products = self._score_products(filtered_products, persona, risk_profile)
        
        # Step 3: Generate optimal allocation
        recommendations = self._generate_recommendations(scored_products, persona)
        
        # Step 4: Add justifications
        recommendations = self._add_justifications(recommendations, persona, risk_profile)
        
        return {"products": recommendations[:5]}  # Top 5 recommendations
    
    def _filter_by_risk(self, risk_level: RiskLevel) -> pd.DataFrame:
        """Filter products compatible with risk level"""
        risk_compatibility = {
            RiskLevel.LOW: ['low'],
            RiskLevel.MEDIUM: ['low', 'medium'],
            RiskLevel.HIGH: ['low', 'medium', 'high']
        }
        
        allowed_risks = risk_compatibility[risk_level]
        return self.products[self.products['risk'].isin(allowed_risks)]
    
    def _score_products(
        self, 
        products: pd.DataFrame,
        persona: PersonaResult,
        risk_profile: RiskAssessmentResult
    ) -> pd.DataFrame:
        """Score each product based on multiple factors"""
        
        scored = products.copy()
        scored['suitability_score'] = 0.0
        
        for idx, product in scored.iterrows():
            score = 0.0
            
            # Persona match (40% weight)
            persona_score = self._calculate_persona_match(product, persona)
            score += persona_score * 0.4
            
            # Risk alignment (30% weight)
            risk_score = self._calculate_risk_alignment(product, risk_profile)
            score += risk_score * 0.3
            
            # Return optimization (20% weight)
            return_score = min(1.0, product['expected_return'] / 0.12)
            score += return_score * 0.2
            
            # Diversification bonus (10% weight)
            score += 0.1  # Base diversification score
            
            scored.at[idx, 'suitability_score'] = min(1.0, score)
        
        return scored.sort_values('suitability_score', ascending=False)
    
    def _calculate_persona_match(
        self, 
        product: pd.Series, 
        persona: PersonaResult
    ) -> float:
        """Calculate how well product matches investor persona"""
        
        persona_preferences = {
            PersonaType.AGGRESSIVE_GROWTH: {
                'equity': 1.0, 'balanced': 0.7, 'fixed_income': 0.3
            },
            PersonaType.STEADY_SAVER: {
                'balanced': 1.0, 'fixed_income': 0.8, 'equity': 0.5
            },
            PersonaType.CAUTIOUS_PLANNER: {
                'fixed_income': 1.0, 'balanced': 0.6, 'equity': 0.2
            }
        }
        
        preferences = persona_preferences.get(persona.persona_type, {})
        return preferences.get(product['type'], 0.5)
    
    def _calculate_risk_alignment(
        self, 
        product: pd.Series, 
        risk_profile: RiskAssessmentResult
    ) -> float:
        """Calculate risk alignment score"""
        
        risk_scores = {
            (RiskLevel.LOW, 'low'): 1.0,
            (RiskLevel.LOW, 'medium'): 0.5,
            (RiskLevel.LOW, 'high'): 0.0,
            (RiskLevel.MEDIUM, 'low'): 0.8,
            (RiskLevel.MEDIUM, 'medium'): 1.0,
            (RiskLevel.MEDIUM, 'high'): 0.6,
            (RiskLevel.HIGH, 'low'): 0.6,
            (RiskLevel.HIGH, 'medium'): 0.8,
            (RiskLevel.HIGH, 'high'): 1.0,
        }
        
        return risk_scores.get((risk_profile.risk_level, product['risk']), 0.5)
    
    def _generate_recommendations(
        self, 
        scored_products: pd.DataFrame,
        persona: PersonaResult
    ) -> List[ProductRecommendation]:
        """Generate recommendation objects with allocations"""
        
        recommendations = []
        total_allocation = 100
        
        for idx, (_, product) in enumerate(scored_products.head(5).iterrows()):
            # Allocate based on score and position
            base_allocation = max(10, 40 - (idx * 10))
            
            rec = ProductRecommendation(
                product_id=product['id'],
                product_name=product['name'],
                product_type=product['type'],
                risk_rating=product['risk'],
                expected_return=product['expected_return'],
                suitability_score=product['suitability_score'],
                allocation_percentage=base_allocation,
                justification="",  # Added later
                warnings=[]
            )
            recommendations.append(rec)
        
        # Normalize allocations to 100%
        total = sum(r.allocation_percentage for r in recommendations)
        for rec in recommendations:
            rec.allocation_percentage = (rec.allocation_percentage / total) * 100
            
        return recommendations
    
    def _add_justifications(
        self, 
        recommendations: List[ProductRecommendation],
        persona: PersonaResult,
        risk_profile: RiskAssessmentResult
    ) -> List[ProductRecommendation]:
        """Add justification text to each recommendation"""
        
        for rec in recommendations:
            justification_parts = []
            
            # Score-based justification
            if rec.suitability_score > 0.8:
                justification_parts.append(f"Excellent match ({rec.suitability_score:.0%} suitability)")
            elif rec.suitability_score > 0.6:
                justification_parts.append(f"Good match ({rec.suitability_score:.0%} suitability)")
            else:
                justification_parts.append(f"Moderate match ({rec.suitability_score:.0%} suitability)")
            
            # Persona alignment
            justification_parts.append(
                f"Aligns with {persona.persona_type.value.replace('_', ' ')} profile"
            )
            
            # Risk alignment
            if rec.risk_rating == risk_profile.risk_level.value:
                justification_parts.append("Risk level perfectly matches profile")
            
            # Return expectation
            justification_parts.append(
                f"Expected annual return: {rec.expected_return:.1%}"
            )
            
            rec.justification = ". ".join(justification_parts) + "."
            
            # Add warnings if applicable
            if rec.risk_rating == 'high' and risk_profile.risk_level != RiskLevel.HIGH:
                rec.warnings.append("Higher risk than profile suggests - monitor closely")
        
        return recommendations
    
    def _fallback(
        self, 
        persona: PersonaResult, 
        risk_profile: RiskAssessmentResult
    ) -> Dict[str, Any]:
        """Fallback: return safe default recommendations"""
        
        default_recs = [
            ProductRecommendation(
                product_id="DEFAULT-1",
                product_name="Diversified Index Fund",
                product_type="balanced",
                risk_rating="medium",
                expected_return=0.07,
                suitability_score=0.7,
                allocation_percentage=60,
                justification="Default recommendation for diversified exposure",
                warnings=["Based on fallback logic - verify suitability"]
            ),
            ProductRecommendation(
                product_id="DEFAULT-2",
                product_name="Government Bond Fund",
                product_type="fixed_income",
                risk_rating="low",
                expected_return=0.035,
                suitability_score=0.6,
                allocation_percentage=40,
                justification="Conservative component for stability",
                warnings=["Based on fallback logic - verify suitability"]
            )
        ]
        
        return {"products": default_recs}
```

---

## 4. Machine Learning Pipeline

### Model Training

```python
# models/train_models.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import pickle
from pathlib import Path
from loguru import logger

class ModelTrainer:
    """Train and persist ML models for risk and goal prediction"""
    
    def __init__(self, data_path: str, model_dir: str):
        self.data_path = Path(data_path)
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
    def train_risk_model(self) -> dict:
        """Train risk classification model"""
        logger.info("Training risk classification model...")
        
        # Load data
        df = pd.read_csv(self.data_path / "training_data.csv")
        
        # Feature engineering
        features = ['age', 'income', 'investment_amount', 
                   'investment_horizon', 'risk_tolerance_encoded']
        
        # Encode risk tolerance
        le = LabelEncoder()
        df['risk_tolerance_encoded'] = le.fit_transform(df['risk_tolerance'])
        
        X = df[features]
        y = df['risk_level']  # target: low/medium/high
        
        # Encode target
        y_encoded = LabelEncoder().fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            class_weight='balanced'
        )
        
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
        
        logger.info(f"Risk model accuracy: {accuracy:.2%}")
        logger.info(f"Cross-validation: {cv_scores.mean():.2%} (+/- {cv_scores.std() * 2:.2%})")
        
        # Save model and scaler
        with open(self.model_dir / "risk_model.pkl", 'wb') as f:
            pickle.dump(model, f)
        with open(self.model_dir / "risk_scaler.pkl", 'wb') as f:
            pickle.dump(scaler, f)
        with open(self.model_dir / "risk_encoder.pkl", 'wb') as f:
            pickle.dump(le, f)
            
        return {
            "accuracy": accuracy,
            "cv_mean": cv_scores.mean(),
            "cv_std": cv_scores.std(),
            "feature_importance": dict(zip(features, model.feature_importances_))
        }
    
    def train_goal_model(self) -> dict:
        """Train goal success prediction model"""
        logger.info("Training goal success prediction model...")
        
        # Load data
        df = pd.read_csv(self.data_path / "goal_data.csv")
        
        # Feature engineering
        features = ['income', 'goal_amount', 'time_horizon', 
                   'monthly_contribution', 'risk_profile_encoded', 
                   'current_savings']
        
        # Calculate derived features
        df['savings_rate'] = df['monthly_contribution'] / (df['income'] / 12)
        df['goal_income_ratio'] = df['goal_amount'] / df['income']
        
        # Encode risk profile
        le = LabelEncoder()
        df['risk_profile_encoded'] = le.fit_transform(df['risk_profile'])
        
        X = df[features]
        y = df['goal_achieved']  # binary: 0 or 1
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = LogisticRegression(
            C=1.0,
            max_iter=1000,
            class_weight='balanced',
            random_state=42
        )
        
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test_scaled)
        y_prob = model.predict_proba(X_test_scaled)[:, 1]
        accuracy = accuracy_score(y_test, y_pred)
        
        logger.info(f"Goal model accuracy: {accuracy:.2%}")
        
        # Save model
        with open(self.model_dir / "goal_model.pkl", 'wb') as f:
            pickle.dump(model, f)
        with open(self.model_dir / "goal_scaler.pkl", 'wb') as f:
            pickle.dump(scaler, f)
            
        return {
            "accuracy": accuracy,
            "coefficients": dict(zip(features, model.coef_[0]))
        }

# Usage
if __name__ == "__main__":
    trainer = ModelTrainer(
        data_path="data/training",
        model_dir="data/models"
    )
    
    risk_metrics = trainer.train_risk_model()
    goal_metrics = trainer.train_goal_model()
    
    print("Training complete!")
    print(f"Risk Model Accuracy: {risk_metrics['accuracy']:.2%}")
    print(f"Goal Model Accuracy: {goal_metrics['accuracy']:.2%}")
```

---

## 5. LLM Integration

### Gemini Client Setup

```python
# config/llm_config.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from typing import Optional
from pydantic import BaseModel
import os

class LLMConfig:
    """Configuration and utilities for LLM integration"""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model_name = "gemini-pro"
        self.temperature = 0.3
        self.max_tokens = 2048
        
    def get_client(self) -> Optional[ChatGoogleGenerativeAI]:
        """Get configured Gemini client"""
        if not self.api_key:
            return None
            
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=self.api_key,
            temperature=self.temperature,
            max_output_tokens=self.max_tokens
        )

# Prompt Templates
RISK_ANALYSIS_PROMPT = PromptTemplate(
    template="""
    You are a financial risk analyst. Analyze the following investor profile:
    
    ## Investor Profile
    - Age: {age} years
    - Annual Income: ${income:,.0f}
    - Investment Amount: ${investment_amount:,.0f}
    - Investment Horizon: {horizon} years
    - Stated Risk Tolerance: {risk_tolerance}
    
    ## Task
    Based on this profile, provide:
    
    1. **Risk Assessment**: Classify as LOW, MEDIUM, or HIGH risk
    2. **Key Risk Factors**: List 3-5 specific factors affecting risk
    3. **Mitigation Strategies**: Provide 3-5 actionable suggestions
    4. **Reasoning**: Explain your classification in 2-3 sentences
    
    ## Output Format
    Respond in JSON format:
    {{
        "risk_level": "LOW|MEDIUM|HIGH",
        "risk_factors": ["factor1", "factor2", ...],
        "mitigations": ["suggestion1", "suggestion2", ...],
        "reasoning": "Your explanation here"
    }}
    """,
    input_variables=["age", "income", "investment_amount", "horizon", "risk_tolerance"]
)

PERSONA_CLASSIFICATION_PROMPT = PromptTemplate(
    template="""
    You are an investment behavioral analyst. Classify the following investor:
    
    ## Investor Data
    - Age: {age}
    - Income: ${income:,.0f}
    - Investment Amount: ${investment_amount:,.0f}
    - Risk Profile: {risk_level}
    - Investment Goals: {goals}
    
    ## Persona Types
    1. **Aggressive Growth**: High-risk tolerance, focus on capital appreciation
    2. **Steady Saver**: Balanced approach, consistent contributions
    3. **Cautious Planner**: Risk-averse, focus on capital preservation
    
    ## Task
    Classify this investor and provide behavioral insights.
    
    ## Output Format
    {{
        "persona_type": "AGGRESSIVE_GROWTH|STEADY_SAVER|CAUTIOUS_PLANNER",
        "confidence": 0.0-1.0,
        "behavioral_insights": ["insight1", "insight2", ...],
        "investment_preferences": {{
            "preferred_asset_types": [...],
            "time_horizon_preference": "short|medium|long",
            "volatility_tolerance": "low|medium|high"
        }},
        "communication_style": "Description of how to communicate with this investor"
    }}
    """,
    input_variables=["age", "income", "investment_amount", "risk_level", "goals"]
)
```

---

## 6. Error Handling & Fallbacks

### Comprehensive Error Handling Strategy

```python
# utils/error_handling.py

from enum import Enum
from typing import Callable, Any, Optional
from functools import wraps
import asyncio
from loguru import logger

class ErrorType(Enum):
    ML_MODEL_ERROR = "ml_model_error"
    LLM_API_ERROR = "llm_api_error"
    DATA_VALIDATION_ERROR = "data_validation_error"
    TIMEOUT_ERROR = "timeout_error"
    UNKNOWN_ERROR = "unknown_error"

class AgentError(Exception):
    """Custom exception for agent errors"""
    def __init__(self, error_type: ErrorType, message: str, original_error: Optional[Exception] = None):
        self.error_type = error_type
        self.message = message
        self.original_error = original_error
        super().__init__(message)

def with_fallback(fallback_func: Callable):
    """Decorator to add fallback logic to async functions"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Primary function failed: {e}, using fallback")
                return fallback_func(*args, **kwargs)
        return wrapper
    return decorator

def with_retry(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator to add retry logic with exponential backoff"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None
            current_delay = delay
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    
                    if attempt < max_retries - 1:
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
            
            raise AgentError(
                ErrorType.UNKNOWN_ERROR,
                f"All {max_retries} attempts failed",
                last_error
            )
        return wrapper
    return decorator

def with_timeout(seconds: float):
    """Decorator to add timeout to async functions"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=seconds
                )
            except asyncio.TimeoutError:
                raise AgentError(
                    ErrorType.TIMEOUT_ERROR,
                    f"Function timed out after {seconds} seconds"
                )
        return wrapper
    return decorator

# Usage example in agent
class RobustAgent:
    """Example agent with comprehensive error handling"""
    
    @with_timeout(30.0)
    @with_retry(max_retries=3, delay=1.0)
    async def call_llm(self, prompt: str) -> str:
        """Call LLM with retry and timeout"""
        # LLM call implementation
        pass
    
    @with_fallback(lambda self, data: self._rule_based_prediction(data))
    async def predict(self, data: dict) -> dict:
        """Prediction with fallback"""
        # ML prediction implementation
        pass
```

---

## 7. Async Processing

### Async Workflow Execution

```python
# utils/async_utils.py

import asyncio
from typing import List, Callable, Any, Dict
from loguru import logger

class AsyncBatchProcessor:
    """Process multiple items concurrently"""
    
    def __init__(self, max_concurrent: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
    async def process_batch(
        self, 
        items: List[Any], 
        processor: Callable
    ) -> List[Dict[str, Any]]:
        """Process items with concurrency control"""
        
        async def process_with_semaphore(item):
            async with self.semaphore:
                try:
                    result = await processor(item)
                    return {"success": True, "result": result, "item": item}
                except Exception as e:
                    logger.error(f"Error processing item: {e}")
                    return {"success": False, "error": str(e), "item": item}
        
        tasks = [process_with_semaphore(item) for item in items]
        return await asyncio.gather(*tasks)

# Example: Process multiple prospects
async def analyze_prospects_batch(prospects: List[dict]) -> List[dict]:
    """Analyze multiple prospects concurrently"""
    
    from graph import create_workflow
    workflow = create_workflow()
    
    processor = AsyncBatchProcessor(max_concurrent=3)
    
    async def analyze_single(prospect):
        result = await workflow.ainvoke({"prospect": prospect})
        return result
    
    results = await processor.process_batch(prospects, analyze_single)
    return results
```

---

## 8. Logging & Monitoring

### Structured Logging Configuration

```python
# config/logging_config.py

import sys
from loguru import logger
from pathlib import Path
from datetime import datetime

def setup_logging(
    log_dir: str = "logs",
    app_name: str = "rm_agentic_ai"
) -> None:
    """Configure structured logging with Loguru"""
    
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Remove default handler
    logger.remove()
    
    # Console handler (human-readable)
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
               "<level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    # File handler - Application logs
    logger.add(
        log_path / "app.log",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
               "{name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="30 days",
        compression="gz"
    )
    
    # File handler - Agent-specific logs
    logger.add(
        log_path / "agents.log",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
               "{extra[agent]} | {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="30 days",
        compression="gz",
        filter=lambda record: "agent" in record["extra"]
    )
    
    # JSON structured logs for monitoring
    logger.add(
        log_path / "structured.json",
        format="{message}",
        serialize=True,
        level="INFO",
        rotation="50 MB",
        retention="7 days"
    )
    
    logger.info(f"Logging initialized for {app_name}")

# Metrics collector
class MetricsCollector:
    """Collect and report agent metrics"""
    
    def __init__(self):
        self.metrics = {
            "executions": 0,
            "successes": 0,
            "failures": 0,
            "fallbacks": 0,
            "total_duration_ms": 0,
            "by_agent": {}
        }
    
    def record(self, agent_name: str, duration_ms: float, success: bool, fallback: bool = False):
        """Record a single execution"""
        self.metrics["executions"] += 1
        self.metrics["total_duration_ms"] += duration_ms
        
        if success:
            self.metrics["successes"] += 1
        else:
            self.metrics["failures"] += 1
            
        if fallback:
            self.metrics["fallbacks"] += 1
        
        # By agent
        if agent_name not in self.metrics["by_agent"]:
            self.metrics["by_agent"][agent_name] = {
                "executions": 0,
                "successes": 0,
                "avg_duration_ms": 0
            }
        
        agent_metrics = self.metrics["by_agent"][agent_name]
        agent_metrics["executions"] += 1
        if success:
            agent_metrics["successes"] += 1
        
        # Update average
        total_duration = agent_metrics["avg_duration_ms"] * (agent_metrics["executions"] - 1)
        agent_metrics["avg_duration_ms"] = (total_duration + duration_ms) / agent_metrics["executions"]
    
    def get_summary(self) -> dict:
        """Get metrics summary"""
        total = self.metrics["executions"]
        return {
            "total_executions": total,
            "success_rate": self.metrics["successes"] / total if total > 0 else 0,
            "fallback_rate": self.metrics["fallbacks"] / total if total > 0 else 0,
            "avg_duration_ms": self.metrics["total_duration_ms"] / total if total > 0 else 0,
            "by_agent": self.metrics["by_agent"]
        }
```

---

## 9. Testing Strategy

### Test Implementation

```python
# tests/test_workflow.py

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from state import ProspectData, RiskLevel, PersonaType
from agents.risk_assessment_agent import RiskAssessmentAgent
from agents.product_specialist_agent import ProductSpecialistAgent
from graph import create_workflow

# Fixtures
@pytest.fixture
def sample_prospect():
    return ProspectData(
        client_id="TEST001",
        name="Test User",
        age=35,
        income=150000,
        investment_amount=50000,
        investment_horizon=10,
        risk_tolerance="medium"
    )

@pytest.fixture
def mock_llm():
    with patch('agents.risk_assessment_agent.ChatGoogleGenerativeAI') as mock:
        mock_instance = AsyncMock()
        mock_instance.ainvoke.return_value = Mock(content='{"risk_level": "MEDIUM"}')
        mock.return_value = mock_instance
        yield mock

# Unit Tests
class TestRiskAssessmentAgent:
    """Tests for risk assessment agent"""
    
    def test_rule_based_assessment(self, sample_prospect):
        """Test rule-based fallback"""
        agent = RiskAssessmentAgent()
        agent.model = None  # Force rule-based
        
        result = agent._rule_based_assessment(sample_prospect)
        
        assert result[0] in [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH]
        assert 0 <= result[1] <= 1
    
    @pytest.mark.asyncio
    async def test_execute_with_fallback(self, sample_prospect, mock_llm):
        """Test execution with LLM fallback"""
        agent = RiskAssessmentAgent()
        agent.model = None  # Force fallback path
        
        result = await agent.execute(prospect=sample_prospect)
        
        assert result["result"] is not None
        assert result["metrics"].agent_name == "RiskAssessmentAgent"
    
    def test_risk_encoding(self):
        """Test risk tolerance encoding"""
        agent = RiskAssessmentAgent()
        
        assert agent._encode_risk_tolerance("low") == 0
        assert agent._encode_risk_tolerance("medium") == 1
        assert agent._encode_risk_tolerance("high") == 2

class TestProductSpecialistAgent:
    """Tests for product specialist agent"""
    
    def test_risk_filtering(self):
        """Test product filtering by risk level"""
        agent = ProductSpecialistAgent()
        
        low_risk = agent._filter_by_risk(RiskLevel.LOW)
        high_risk = agent._filter_by_risk(RiskLevel.HIGH)
        
        assert all(p['risk'] == 'low' for _, p in low_risk.iterrows())
        assert len(high_risk) >= len(low_risk)
    
    def test_suitability_scoring(self, sample_prospect):
        """Test product suitability scoring"""
        from state import PersonaResult, RiskAssessmentResult
        
        agent = ProductSpecialistAgent()
        persona = PersonaResult(
            persona_type=PersonaType.STEADY_SAVER,
            confidence=0.85,
            behavioral_insights=[]
        )
        risk = RiskAssessmentResult(
            risk_level=RiskLevel.MEDIUM,
            risk_score=0.7,
            confidence=0.85,
            risk_factors=[],
            mitigation_suggestions=[]
        )
        
        products = agent._filter_by_risk(risk.risk_level)
        scored = agent._score_products(products, persona, risk)
        
        assert all(0 <= s <= 1 for s in scored['suitability_score'])
        assert scored['suitability_score'].is_monotonic_decreasing

# Integration Tests
class TestWorkflowIntegration:
    """End-to-end workflow tests"""
    
    @pytest.mark.asyncio
    async def test_full_workflow(self, sample_prospect):
        """Test complete workflow execution"""
        workflow = create_workflow()
        
        result = await workflow.ainvoke({"prospect": sample_prospect.dict()})
        
        assert "risk_assessment" in result
        assert "persona" in result
        assert "recommendations" in result
        assert len(result["recommendations"]) > 0
    
    @pytest.mark.asyncio
    async def test_workflow_with_high_risk_prospect(self):
        """Test workflow with high-risk profile"""
        high_risk_prospect = ProspectData(
            client_id="TEST002",
            name="High Risk User",
            age=25,
            income=200000,
            investment_amount=100000,
            investment_horizon=20,
            risk_tolerance="high"
        )
        
        workflow = create_workflow()
        result = await workflow.ainvoke({"prospect": high_risk_prospect.dict()})
        
        assert result["risk_assessment"]["risk_level"] in ["medium", "high"]

# Performance Tests
class TestPerformance:
    """Performance benchmarks"""
    
    @pytest.mark.asyncio
    async def test_workflow_execution_time(self, sample_prospect):
        """Test that workflow completes within timeout"""
        import time
        
        workflow = create_workflow()
        
        start = time.time()
        await workflow.ainvoke({"prospect": sample_prospect.dict()})
        duration = time.time() - start
        
        assert duration < 60  # Should complete within 60 seconds
```

---

## 10. Performance Optimization

### Optimization Techniques

```python
# utils/optimization.py

import functools
from typing import Any, Callable
import asyncio
from cachetools import TTLCache
import hashlib
import json

# In-memory caching for expensive operations
class CacheManager:
    """Manage various caches for optimization"""
    
    def __init__(self):
        # LLM response cache (5 minute TTL)
        self.llm_cache = TTLCache(maxsize=100, ttl=300)
        
        # Model prediction cache (1 hour TTL)
        self.prediction_cache = TTLCache(maxsize=500, ttl=3600)
        
        # Product catalog cache (24 hour TTL)
        self.product_cache = TTLCache(maxsize=10, ttl=86400)
    
    def _hash_key(self, data: Any) -> str:
        """Generate hash key from data"""
        json_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(json_str.encode()).hexdigest()
    
    def get_cached_llm(self, prompt_key: str) -> Any:
        return self.llm_cache.get(prompt_key)
    
    def set_cached_llm(self, prompt_key: str, response: Any):
        self.llm_cache[prompt_key] = response
    
    def get_cached_prediction(self, features: dict) -> Any:
        key = self._hash_key(features)
        return self.prediction_cache.get(key)
    
    def set_cached_prediction(self, features: dict, prediction: Any):
        key = self._hash_key(features)
        self.prediction_cache[key] = prediction

# Decorator for caching
def cached_llm_call(cache_manager: CacheManager):
    """Decorator to cache LLM calls"""
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(self, prompt: str, *args, **kwargs):
            # Check cache
            cache_key = hashlib.md5(prompt.encode()).hexdigest()
            cached = cache_manager.get_cached_llm(cache_key)
            
            if cached is not None:
                return cached
            
            # Call function
            result = await func(self, prompt, *args, **kwargs)
            
            # Cache result
            cache_manager.set_cached_llm(cache_key, result)
            
            return result
        return wrapper
    return decorator

# Lazy loading for models
class LazyModelLoader:
    """Load ML models lazily on first use"""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self._model = None
    
    @property
    def model(self):
        if self._model is None:
            import pickle
            with open(self.model_path, 'rb') as f:
                self._model = pickle.load(f)
        return self._model

# Connection pooling for database
class ConnectionPool:
    """Manage database connections efficiently"""
    
    def __init__(self, max_connections: int = 10):
        self.semaphore = asyncio.Semaphore(max_connections)
        self.connections = []
    
    async def get_connection(self):
        async with self.semaphore:
            # Return connection from pool or create new
            pass
```

---

## Summary

This technical deep dive covers the core implementation details of the RM-AgenticAI-LangGraph system:

1. **LangGraph** orchestrates the multi-agent workflow
2. **Pydantic** ensures type safety and validation
3. **Agents** follow a consistent pattern with fallback mechanisms
4. **ML Pipeline** provides quantitative predictions
5. **LLM Integration** enables qualitative analysis
6. **Error Handling** ensures reliability
7. **Async Processing** enables high throughput
8. **Logging** provides observability
9. **Testing** ensures quality
10. **Optimization** maintains performance

For interview preparation, see [interview-guide.md](interview-guide.md).
