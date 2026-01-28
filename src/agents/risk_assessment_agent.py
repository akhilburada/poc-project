"""
Risk Assessment Agent

This agent is responsible for assessing investor risk profiles
using a combination of:
1. Machine Learning models (primary)
2. LLM reasoning (for explanations)
3. Rule-based logic (fallback)
"""

import pickle
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass
import numpy as np

from .base_agent import BaseAgent, with_retry, with_timeout


@dataclass
class RiskAssessmentOutput:
    """Output structure for risk assessment"""
    risk_level: str  # "low", "medium", "high"
    risk_score: float  # 0.0 - 1.0
    risk_factors: List[str]
    mitigation_suggestions: List[str]
    confidence: float
    reasoning: str
    method_used: str  # "ml", "llm", "rule_based"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "risk_level": self.risk_level,
            "risk_score": self.risk_score,
            "risk_factors": self.risk_factors,
            "mitigation_suggestions": self.mitigation_suggestions,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "method_used": self.method_used
        }


class RiskAssessmentAgent(BaseAgent):
    """
    Agent for assessing investor risk profiles.
    
    Uses:
    - ML Model (RandomForest) for numerical prediction
    - LLM (Gemini) for explanation generation
    - Rule-based logic as fallback
    
    Example:
        agent = RiskAssessmentAgent()
        result = await agent.execute(prospect=prospect_data)
        print(result.result.risk_level)  # "medium"
    """
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        llm_api_key: Optional[str] = None
    ):
        """
        Initialize the Risk Assessment Agent.
        
        Args:
            model_path: Path to trained ML model (.pkl file)
            llm_api_key: Google API key for Gemini
        """
        super().__init__("RiskAssessmentAgent")
        
        self.model_path = model_path or "data/models/risk_model.pkl"
        self.llm_api_key = llm_api_key
        
        # Lazy loading
        self._model = None
        self._llm = None
    
    @property
    def model(self):
        """Lazy load ML model"""
        if self._model is None:
            self._model = self._load_model()
        return self._model
    
    def _load_model(self) -> Optional[Any]:
        """Load trained ML model from disk."""
        model_path = Path(self.model_path)
        if model_path.exists():
            try:
                with open(model_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                self._log(f"Failed to load model: {e}")
        return None
    
    def _init_llm(self):
        """Initialize LLM client (would use actual LangChain in production)."""
        # In production, this would be:
        # from langchain_google_genai import ChatGoogleGenerativeAI
        # return ChatGoogleGenerativeAI(model="gemini-pro", ...)
        return None
    
    # =========================================================================
    # MAIN EXECUTION
    # =========================================================================
    
    async def _execute(self, prospect: Dict[str, Any]) -> RiskAssessmentOutput:
        """
        Primary execution: ML prediction + LLM explanation.
        
        Args:
            prospect: Dictionary with prospect data including:
                - age: int
                - income: float
                - investment_amount: float
                - investment_horizon: int
                - risk_tolerance: str
                
        Returns:
            RiskAssessmentOutput with complete risk analysis
        """
        # Step 1: ML Prediction
        if self.model is not None:
            risk_level, risk_score = self._ml_predict(prospect)
            method = "ml"
            self._log("ML prediction successful")
        else:
            # If no ML model, use rule-based
            risk_level, risk_score = self._rule_based_assessment(prospect)
            method = "rule_based"
            self._log("Using rule-based assessment (no ML model)")
        
        # Step 2: Generate risk factors and mitigations
        risk_factors, mitigations = self._analyze_risk_factors(prospect, risk_level)
        
        # Step 3: Generate reasoning
        reasoning = self._generate_reasoning(prospect, risk_level, risk_factors)
        
        # Step 4: Calculate confidence
        confidence = self._calculate_confidence(risk_score, method)
        
        return RiskAssessmentOutput(
            risk_level=risk_level,
            risk_score=risk_score,
            risk_factors=risk_factors,
            mitigation_suggestions=mitigations,
            confidence=confidence,
            reasoning=reasoning,
            method_used=method
        )
    
    def _fallback(self, prospect: Dict[str, Any]) -> RiskAssessmentOutput:
        """
        Fallback: Complete rule-based assessment when all else fails.
        
        Args:
            prospect: Prospect data dictionary
            
        Returns:
            Safe default RiskAssessmentOutput
        """
        risk_level, risk_score = self._rule_based_assessment(prospect)
        risk_factors, mitigations = self._get_default_factors(risk_level)
        
        return RiskAssessmentOutput(
            risk_level=risk_level,
            risk_score=risk_score,
            risk_factors=risk_factors,
            mitigation_suggestions=mitigations,
            confidence=0.5,  # Lower confidence for fallback
            reasoning=f"Rule-based assessment determined {risk_level} risk level",
            method_used="rule_based"
        )
    
    # =========================================================================
    # ML PREDICTION
    # =========================================================================
    
    def _ml_predict(self, prospect: Dict[str, Any]) -> Tuple[str, float]:
        """
        Make prediction using trained ML model.
        
        Args:
            prospect: Prospect data
            
        Returns:
            Tuple of (risk_level, risk_score)
        """
        # Prepare features
        features = np.array([[
            prospect.get('age', 35),
            prospect.get('income', 100000),
            prospect.get('investment_amount', 50000),
            prospect.get('investment_horizon', 10),
            self._encode_risk_tolerance(prospect.get('risk_tolerance', 'medium'))
        ]])
        
        # Get prediction
        prediction = self.model.predict(features)[0]
        
        # Get probability if available
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(features)[0]
            risk_score = probabilities[prediction]
        else:
            risk_score = 0.8  # Default confidence
        
        # Map to risk level
        risk_map = {0: 'low', 1: 'medium', 2: 'high'}
        risk_level = risk_map.get(prediction, 'medium')
        
        return risk_level, float(risk_score)
    
    def _encode_risk_tolerance(self, tolerance: str) -> int:
        """Encode risk tolerance string to numeric."""
        encoding = {'low': 0, 'medium': 1, 'high': 2}
        return encoding.get(str(tolerance).lower(), 1)
    
    # =========================================================================
    # RULE-BASED ASSESSMENT
    # =========================================================================
    
    def _rule_based_assessment(self, prospect: Dict[str, Any]) -> Tuple[str, float]:
        """
        Rule-based risk assessment when ML model is unavailable.
        
        Scoring logic:
        - Age: Younger = higher risk capacity
        - Income: Higher = more risk capacity
        - Horizon: Longer = more risk capacity
        - Stated tolerance: Direct input
        
        Args:
            prospect: Prospect data
            
        Returns:
            Tuple of (risk_level, risk_score)
        """
        score = 0
        
        age = prospect.get('age', 35)
        income = prospect.get('income', 100000)
        investment_horizon = prospect.get('investment_horizon', 10)
        risk_tolerance = prospect.get('risk_tolerance', 'medium')
        
        # Age scoring (younger = higher risk capacity)
        if age < 35:
            score += 2
        elif age < 50:
            score += 1
        elif age >= 60:
            score -= 1
        
        # Income scoring (higher = more capacity for risk)
        if income > 200000:
            score += 2
        elif income > 100000:
            score += 1
        elif income < 50000:
            score -= 1
        
        # Horizon scoring (longer = can take more risk)
        if investment_horizon > 15:
            score += 2
        elif investment_horizon > 7:
            score += 1
        elif investment_horizon < 3:
            score -= 1
        
        # Risk tolerance direct input
        tolerance_scores = {'low': 0, 'medium': 1, 'high': 2}
        score += tolerance_scores.get(str(risk_tolerance).lower(), 1)
        
        # Determine risk level from total score
        if score <= 2:
            return 'low', 0.25 + (score / 10)
        elif score <= 5:
            return 'medium', 0.45 + (score / 20)
        else:
            return 'high', 0.75 + (min(score, 8) / 40)
    
    # =========================================================================
    # RISK ANALYSIS
    # =========================================================================
    
    def _analyze_risk_factors(
        self, 
        prospect: Dict[str, Any], 
        risk_level: str
    ) -> Tuple[List[str], List[str]]:
        """
        Analyze and generate risk factors and mitigations.
        
        Args:
            prospect: Prospect data
            risk_level: Determined risk level
            
        Returns:
            Tuple of (risk_factors, mitigations)
        """
        risk_factors = []
        mitigations = []
        
        age = prospect.get('age', 35)
        income = prospect.get('income', 100000)
        investment_amount = prospect.get('investment_amount', 50000)
        investment_horizon = prospect.get('investment_horizon', 10)
        
        # Age-based factors
        if age < 30:
            risk_factors.append("Young age provides time for recovery from market downturns")
            mitigations.append("Consider growth-oriented investments to maximize long-term returns")
        elif age > 55:
            risk_factors.append("Approaching retirement may limit recovery time from losses")
            mitigations.append("Gradually shift towards more conservative investments")
        
        # Income-based factors
        investment_ratio = investment_amount / income if income > 0 else 0
        if investment_ratio > 0.5:
            risk_factors.append(f"High investment ratio ({investment_ratio:.0%} of annual income)")
            mitigations.append("Ensure adequate emergency fund before investing")
        elif investment_ratio < 0.1:
            risk_factors.append("Conservative investment amount relative to income")
            mitigations.append("Consider increasing investment allocation for better growth")
        
        # Horizon-based factors
        if investment_horizon < 5:
            risk_factors.append("Short investment horizon limits recovery potential")
            mitigations.append("Focus on lower-volatility investments")
        elif investment_horizon > 15:
            risk_factors.append("Long horizon allows for aggressive growth strategies")
            mitigations.append("Take advantage of compound growth with equity exposure")
        
        # Ensure we have at least some factors
        if not risk_factors:
            risk_factors.append("Standard risk profile with balanced factors")
        if not mitigations:
            mitigations.append("Regular portfolio review recommended")
        
        return risk_factors, mitigations
    
    def _get_default_factors(self, risk_level: str) -> Tuple[List[str], List[str]]:
        """Get default factors when analysis fails."""
        default_factors = {
            'low': (
                ["Conservative risk profile", "Priority on capital preservation"],
                ["Focus on fixed-income investments", "Maintain liquidity"]
            ),
            'medium': (
                ["Balanced risk/reward profile", "Moderate volatility tolerance"],
                ["Diversify across asset classes", "Regular rebalancing"]
            ),
            'high': (
                ["Growth-oriented profile", "High volatility tolerance"],
                ["Monitor positions actively", "Set stop-loss limits"]
            )
        }
        return default_factors.get(risk_level, default_factors['medium'])
    
    def _generate_reasoning(
        self, 
        prospect: Dict[str, Any], 
        risk_level: str,
        risk_factors: List[str]
    ) -> str:
        """
        Generate human-readable reasoning for the risk classification.
        
        Args:
            prospect: Prospect data
            risk_level: Determined risk level
            risk_factors: Identified risk factors
            
        Returns:
            Reasoning string
        """
        age = prospect.get('age', 35)
        income = prospect.get('income', 100000)
        horizon = prospect.get('investment_horizon', 10)
        tolerance = prospect.get('risk_tolerance', 'medium')
        
        reasoning = f"Based on comprehensive analysis: "
        reasoning += f"Age ({age}) "
        
        if age < 35:
            reasoning += "supports higher risk capacity. "
        elif age > 55:
            reasoning += "suggests more conservative approach. "
        else:
            reasoning += "allows balanced risk-taking. "
        
        reasoning += f"With ${income:,.0f} annual income and {horizon}-year investment horizon, "
        reasoning += f"combined with stated {tolerance} risk tolerance, "
        reasoning += f"the overall assessment indicates a {risk_level.upper()} risk profile. "
        
        if risk_factors:
            reasoning += f"Key factor: {risk_factors[0]}."
        
        return reasoning
    
    def _calculate_confidence(self, risk_score: float, method: str) -> float:
        """
        Calculate overall confidence based on method and score.
        
        Args:
            risk_score: Raw risk score
            method: Method used (ml/llm/rule_based)
            
        Returns:
            Adjusted confidence score
        """
        # Base confidence from risk score
        base_confidence = risk_score
        
        # Method-based adjustment
        method_multipliers = {
            'ml': 1.0,        # Full confidence in ML
            'llm': 0.95,      # Slightly less for LLM
            'rule_based': 0.8  # Lower for rule-based
        }
        
        multiplier = method_multipliers.get(method, 0.7)
        
        return min(1.0, base_confidence * multiplier)


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    import asyncio
    
    # Create agent
    agent = RiskAssessmentAgent()
    
    # Sample prospect
    prospect = {
        "client_id": "C001",
        "name": "John Doe",
        "age": 35,
        "income": 150000,
        "investment_amount": 50000,
        "investment_horizon": 10,
        "risk_tolerance": "medium"
    }
    
    # Run assessment
    async def main():
        result = await agent.execute(prospect=prospect)
        
        print("\n" + "="*50)
        print("RISK ASSESSMENT RESULT")
        print("="*50)
        
        if result.success:
            output = result.result
            print(f"\nRisk Level: {output.risk_level.upper()}")
            print(f"Risk Score: {output.risk_score:.2f}")
            print(f"Confidence: {output.confidence:.0%}")
            print(f"Method Used: {output.method_used}")
            
            print("\nRisk Factors:")
            for factor in output.risk_factors:
                print(f"  • {factor}")
            
            print("\nMitigation Suggestions:")
            for mitigation in output.mitigation_suggestions:
                print(f"  • {mitigation}")
            
            print(f"\nReasoning: {output.reasoning}")
        else:
            print(f"\nExecution failed: {result.error_message}")
        
        print(f"\nExecution time: {result.duration_ms:.2f}ms")
        print(f"Fallback used: {result.fallback_used}")
    
    asyncio.run(main())
