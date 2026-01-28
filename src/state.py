"""
State Models for RM-AgenticAI-LangGraph

This module defines all Pydantic models used for state management
across the multi-agent workflow.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Annotated
from enum import Enum
from datetime import datetime
import operator


# =============================================================================
# ENUMS
# =============================================================================

class RiskLevel(str, Enum):
    """Risk classification levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class PersonaType(str, Enum):
    """Investor persona classifications"""
    AGGRESSIVE_GROWTH = "aggressive_growth"
    STEADY_SAVER = "steady_saver"
    CAUTIOUS_PLANNER = "cautious_planner"


class ComplianceStatus(str, Enum):
    """Compliance check status"""
    PASSED = "passed"
    WARNING = "warning"
    FAILED = "failed"


# =============================================================================
# INPUT MODELS
# =============================================================================

class ProspectData(BaseModel):
    """
    Client/Prospect input data model.
    
    This model captures all necessary information about a prospect
    for the advisory workflow.
    """
    client_id: str = Field(..., description="Unique client identifier")
    name: str = Field(..., min_length=2, max_length=100, description="Client full name")
    age: int = Field(..., ge=18, le=100, description="Client age (must be 18-100)")
    income: float = Field(..., gt=0, description="Annual income in USD")
    investment_amount: float = Field(..., gt=0, description="Amount to invest in USD")
    investment_horizon: int = Field(..., ge=1, le=50, description="Investment horizon in years")
    risk_tolerance: str = Field(..., description="Stated risk tolerance: low/medium/high")
    monthly_contribution: Optional[float] = Field(default=0, ge=0, description="Monthly contribution amount")
    existing_investments: Optional[float] = Field(default=0, ge=0, description="Existing investment value")
    financial_goals: Optional[List[str]] = Field(default_factory=list, description="List of financial goals")
    
    @validator('risk_tolerance')
    def validate_risk_tolerance(cls, v):
        """Ensure risk tolerance is valid"""
        allowed = ['low', 'medium', 'high']
        if v.lower() not in allowed:
            raise ValueError(f'risk_tolerance must be one of {allowed}')
        return v.lower()
    
    @validator('financial_goals', pre=True)
    def ensure_list(cls, v):
        """Ensure financial_goals is a list"""
        if v is None:
            return []
        if isinstance(v, str):
            return [v]
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "client_id": "C001",
                "name": "John Doe",
                "age": 35,
                "income": 150000,
                "investment_amount": 50000,
                "investment_horizon": 10,
                "risk_tolerance": "medium",
                "monthly_contribution": 1000,
                "financial_goals": ["retirement", "education"]
            }
        }


# =============================================================================
# RESULT MODELS
# =============================================================================

class RiskAssessmentResult(BaseModel):
    """
    Output from the Risk Assessment Agent.
    
    Contains the risk classification, supporting factors,
    and confidence metrics.
    """
    risk_level: RiskLevel = Field(..., description="Classified risk level")
    risk_score: float = Field(..., ge=0, le=1, description="Numeric risk score (0-1)")
    risk_factors: List[str] = Field(default_factory=list, description="Key risk factors identified")
    mitigation_suggestions: List[str] = Field(default_factory=list, description="Suggested risk mitigations")
    confidence: float = Field(..., ge=0, le=1, description="Model confidence (0-1)")
    reasoning: str = Field(default="", description="Explanation of risk classification")
    method_used: str = Field(default="ml", description="Method used: ml/llm/rule_based")
    
    @property
    def is_high_risk(self) -> bool:
        """Check if client is high risk"""
        return self.risk_level == RiskLevel.HIGH
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for state updates"""
        return {
            "risk_level": self.risk_level.value,
            "risk_score": self.risk_score,
            "risk_factors": self.risk_factors,
            "mitigation_suggestions": self.mitigation_suggestions,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "method_used": self.method_used
        }


class PersonaResult(BaseModel):
    """
    Output from the Persona Classification Agent.
    
    Contains investor classification and behavioral insights.
    """
    persona_type: PersonaType = Field(..., description="Classified persona type")
    confidence: float = Field(..., ge=0, le=1, description="Classification confidence")
    behavioral_insights: List[str] = Field(default_factory=list, description="Behavioral observations")
    investment_preferences: Dict[str, Any] = Field(default_factory=dict, description="Preferred investment types")
    communication_style: str = Field(default="", description="Recommended communication approach")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for state updates"""
        return {
            "persona_type": self.persona_type.value,
            "confidence": self.confidence,
            "behavioral_insights": self.behavioral_insights,
            "investment_preferences": self.investment_preferences,
            "communication_style": self.communication_style
        }


class GoalPredictionResult(BaseModel):
    """
    Output from the Goal Planning Agent.
    
    Predicts probability of achieving investment goals.
    """
    success_probability: float = Field(..., ge=0, le=1, description="Probability of goal achievement")
    projected_value: float = Field(..., ge=0, description="Projected portfolio value at horizon")
    goal_amount: float = Field(..., ge=0, description="Target goal amount")
    shortfall_amount: Optional[float] = Field(default=None, description="Projected shortfall if any")
    key_factors: List[str] = Field(default_factory=list, description="Key factors affecting success")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations to improve odds")
    
    @property
    def on_track(self) -> bool:
        """Check if client is on track to meet goals"""
        return self.success_probability >= 0.7
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for state updates"""
        return {
            "success_probability": self.success_probability,
            "projected_value": self.projected_value,
            "goal_amount": self.goal_amount,
            "shortfall_amount": self.shortfall_amount,
            "key_factors": self.key_factors,
            "recommendations": self.recommendations
        }


class ProductRecommendation(BaseModel):
    """
    Single investment product recommendation.
    
    Includes product details, suitability scoring, and justification.
    """
    product_id: str = Field(..., description="Unique product identifier")
    product_name: str = Field(..., description="Product display name")
    product_type: str = Field(..., description="Product category: equity/fixed_income/balanced")
    risk_rating: str = Field(..., description="Product risk rating: low/medium/high")
    expected_return: float = Field(..., ge=0, le=1, description="Expected annual return")
    suitability_score: float = Field(..., ge=0, le=1, description="Suitability for this client (0-1)")
    allocation_percentage: float = Field(..., ge=0, le=100, description="Recommended allocation %")
    justification: str = Field(default="", description="Why this product is recommended")
    warnings: List[str] = Field(default_factory=list, description="Any warnings about this product")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for state updates"""
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_type": self.product_type,
            "risk_rating": self.risk_rating,
            "expected_return": self.expected_return,
            "suitability_score": self.suitability_score,
            "allocation_percentage": self.allocation_percentage,
            "justification": self.justification,
            "warnings": self.warnings
        }


class ComplianceCheck(BaseModel):
    """
    Output from the Compliance Agent.
    
    Contains results of regulatory compliance validation.
    """
    status: ComplianceStatus = Field(..., description="Overall compliance status")
    checks_performed: List[str] = Field(default_factory=list, description="List of checks performed")
    passed_checks: List[str] = Field(default_factory=list, description="Checks that passed")
    failed_checks: List[str] = Field(default_factory=list, description="Checks that failed")
    warnings: List[str] = Field(default_factory=list, description="Compliance warnings")
    disclosures: List[str] = Field(default_factory=list, description="Required disclosures")
    regulatory_notes: List[str] = Field(default_factory=list, description="Regulatory notes")
    
    @property
    def is_compliant(self) -> bool:
        """Check if fully compliant"""
        return self.status == ComplianceStatus.PASSED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for state updates"""
        return {
            "status": self.status.value,
            "checks_performed": self.checks_performed,
            "passed_checks": self.passed_checks,
            "failed_checks": self.failed_checks,
            "warnings": self.warnings,
            "disclosures": self.disclosures,
            "regulatory_notes": self.regulatory_notes
        }


# =============================================================================
# METRICS MODELS
# =============================================================================

class ExecutionMetrics(BaseModel):
    """
    Agent execution metrics for monitoring and debugging.
    """
    agent_name: str = Field(..., description="Name of the agent")
    start_time: datetime = Field(..., description="Execution start time")
    end_time: datetime = Field(..., description="Execution end time")
    duration_ms: float = Field(..., ge=0, description="Duration in milliseconds")
    success: bool = Field(..., description="Whether execution succeeded")
    error_message: Optional[str] = Field(default=None, description="Error message if failed")
    fallback_used: bool = Field(default=False, description="Whether fallback logic was used")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "agent_name": self.agent_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_ms": self.duration_ms,
            "success": self.success,
            "error_message": self.error_message,
            "fallback_used": self.fallback_used
        }


# =============================================================================
# WORKFLOW STATE
# =============================================================================

class WorkflowState(BaseModel):
    """
    Complete workflow state container.
    
    This is the main state object passed between LangGraph nodes.
    Each agent reads from and writes to this shared state.
    """
    # Input data
    prospect: ProspectData = Field(..., description="Input prospect data")
    
    # Data validation results
    data_quality_score: Optional[float] = Field(default=None, description="Data quality score (0-1)")
    data_issues: List[str] = Field(default_factory=list, description="Data quality issues found")
    
    # Processing results
    risk_assessment: Optional[RiskAssessmentResult] = Field(default=None, description="Risk assessment output")
    persona: Optional[PersonaResult] = Field(default=None, description="Persona classification output")
    goal_prediction: Optional[GoalPredictionResult] = Field(default=None, description="Goal prediction output")
    recommendations: List[ProductRecommendation] = Field(default_factory=list, description="Product recommendations")
    compliance: Optional[ComplianceCheck] = Field(default=None, description="Compliance check output")
    
    # Insights and actions
    key_insights: List[str] = Field(default_factory=list, description="Key insights generated")
    action_items: List[str] = Field(default_factory=list, description="Recommended action items for RM")
    disclosures: List[str] = Field(default_factory=list, description="Required disclosures")
    
    # Aggregated metrics
    overall_confidence: float = Field(default=0.0, description="Overall confidence score")
    execution_metrics: List[ExecutionMetrics] = Field(default_factory=list, description="Per-agent metrics")
    
    # Status tracking
    current_node: str = Field(default="", description="Currently executing node")
    completed_nodes: List[str] = Field(default_factory=list, description="List of completed nodes")
    errors: List[str] = Field(default_factory=list, description="Errors encountered")
    
    # Messages for append-only logging (LangGraph pattern)
    messages: Annotated[List[str], operator.add] = Field(default_factory=list)
    
    def add_metric(self, metric: ExecutionMetrics) -> None:
        """Add execution metric"""
        self.execution_metrics.append(metric)
    
    def mark_node_complete(self, node_name: str) -> None:
        """Mark a node as completed"""
        if node_name not in self.completed_nodes:
            self.completed_nodes.append(node_name)
    
    def add_error(self, error: str) -> None:
        """Add error message"""
        self.errors.append(error)
    
    def calculate_overall_confidence(self) -> float:
        """
        Calculate weighted average confidence across all components.
        
        Weights:
        - Risk Assessment: 30%
        - Persona: 20%
        - Goal Prediction: 30%
        - Recommendations: 20%
        """
        confidences = []
        weights = []
        
        if self.risk_assessment:
            confidences.append(self.risk_assessment.confidence)
            weights.append(0.3)
        
        if self.persona:
            confidences.append(self.persona.confidence)
            weights.append(0.2)
        
        if self.goal_prediction:
            confidences.append(self.goal_prediction.success_probability)
            weights.append(0.3)
        
        if self.recommendations:
            avg_suitability = sum(r.suitability_score for r in self.recommendations) / len(self.recommendations)
            confidences.append(avg_suitability)
            weights.append(0.2)
        
        if not confidences:
            return 0.0
        
        total_weight = sum(weights)
        weighted_sum = sum(c * w for c, w in zip(confidences, weights))
        
        self.overall_confidence = weighted_sum / total_weight
        return self.overall_confidence
    
    def get_summary(self) -> Dict[str, Any]:
        """Get workflow summary"""
        return {
            "client_id": self.prospect.client_id,
            "client_name": self.prospect.name,
            "risk_level": self.risk_assessment.risk_level.value if self.risk_assessment else None,
            "persona": self.persona.persona_type.value if self.persona else None,
            "num_recommendations": len(self.recommendations),
            "compliance_status": self.compliance.status.value if self.compliance else None,
            "overall_confidence": self.overall_confidence,
            "completed_nodes": self.completed_nodes,
            "has_errors": len(self.errors) > 0
        }
    
    class Config:
        arbitrary_types_allowed = True


# =============================================================================
# TYPE DEFINITIONS FOR LANGGRAPH
# =============================================================================

# For LangGraph StateGraph initialization
from typing import TypedDict

class GraphState(TypedDict):
    """TypedDict version for LangGraph compatibility"""
    prospect: dict
    data_quality_score: Optional[float]
    risk_assessment: Optional[dict]
    persona: Optional[dict]
    goal_prediction: Optional[dict]
    recommendations: List[dict]
    compliance: Optional[dict]
    key_insights: List[str]
    action_items: List[str]
    overall_confidence: float
    execution_log: Annotated[List[str], operator.add]
