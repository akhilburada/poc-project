"""
LangGraph Workflow Definition

This module defines the multi-agent workflow using LangGraph.
It orchestrates the sequence of agents and manages state flow.
"""

from langgraph.graph import StateGraph, END
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio

from state import (
    GraphState, WorkflowState, ProspectData,
    RiskAssessmentResult, PersonaResult, GoalPredictionResult,
    ProductRecommendation, ComplianceCheck, ExecutionMetrics,
    RiskLevel, PersonaType, ComplianceStatus
)


# =============================================================================
# NODE FUNCTIONS
# =============================================================================

async def data_validation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 1: Data Validation
    
    Validates input data completeness and quality.
    Generates a data quality score and identifies issues.
    """
    start_time = datetime.now()
    
    try:
        prospect_data = state.get("prospect", {})
        
        # Validate required fields
        required_fields = ['client_id', 'name', 'age', 'income', 
                          'investment_amount', 'investment_horizon', 'risk_tolerance']
        
        issues = []
        for field in required_fields:
            if field not in prospect_data or prospect_data[field] is None:
                issues.append(f"Missing required field: {field}")
        
        # Calculate quality score
        filled_fields = sum(1 for f in required_fields if prospect_data.get(f) is not None)
        quality_score = filled_fields / len(required_fields)
        
        # Validate data ranges
        if prospect_data.get('age', 0) < 18 or prospect_data.get('age', 0) > 100:
            issues.append("Age must be between 18 and 100")
            quality_score -= 0.1
        
        if prospect_data.get('income', 0) <= 0:
            issues.append("Income must be positive")
            quality_score -= 0.1
        
        if prospect_data.get('investment_amount', 0) <= 0:
            issues.append("Investment amount must be positive")
            quality_score -= 0.1
        
        quality_score = max(0, min(1, quality_score))  # Clamp to 0-1
        
        duration = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            "data_quality_score": quality_score,
            "execution_log": [f"DataValidation: SUCCESS in {duration:.2f}ms (Quality: {quality_score:.2f})"]
        }
        
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds() * 1000
        return {
            "data_quality_score": 0.5,
            "execution_log": [f"DataValidation: FALLBACK in {duration:.2f}ms - {str(e)}"]
        }


async def risk_assessment_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 2: Risk Assessment
    
    Assesses investor risk profile using ML model and LLM analysis.
    Falls back to rule-based assessment if ML/LLM unavailable.
    """
    start_time = datetime.now()
    
    try:
        prospect = state.get("prospect", {})
        
        # Extract features
        age = prospect.get('age', 35)
        income = prospect.get('income', 100000)
        investment_amount = prospect.get('investment_amount', 50000)
        investment_horizon = prospect.get('investment_horizon', 10)
        risk_tolerance = prospect.get('risk_tolerance', 'medium').lower()
        
        # Rule-based risk assessment (simplified for template)
        score = 0
        
        # Age factor
        if age < 35:
            score += 2
        elif age < 50:
            score += 1
        
        # Income factor
        if income > 200000:
            score += 2
        elif income > 100000:
            score += 1
        
        # Horizon factor
        if investment_horizon > 15:
            score += 2
        elif investment_horizon > 7:
            score += 1
        
        # Risk tolerance
        tolerance_scores = {'low': 0, 'medium': 1, 'high': 2}
        score += tolerance_scores.get(risk_tolerance, 1)
        
        # Determine risk level
        if score <= 2:
            risk_level = "low"
            risk_score = 0.25
        elif score <= 5:
            risk_level = "medium"
            risk_score = 0.55
        else:
            risk_level = "high"
            risk_score = 0.85
        
        # Generate risk factors
        risk_factors = []
        if age < 35:
            risk_factors.append("Young age allows for higher risk tolerance")
        if investment_horizon > 10:
            risk_factors.append("Long investment horizon provides recovery time")
        if investment_amount / income > 0.3:
            risk_factors.append("Significant portion of income being invested")
        
        # Generate mitigations
        mitigations = [
            "Maintain emergency fund of 6 months expenses",
            "Diversify across asset classes",
            "Review portfolio allocation annually"
        ]
        
        result = {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "risk_factors": risk_factors,
            "mitigation_suggestions": mitigations,
            "confidence": 0.85,
            "reasoning": f"Based on age ({age}), income (${income:,}), and {investment_horizon}-year horizon",
            "method_used": "rule_based"
        }
        
        duration = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            "risk_assessment": result,
            "execution_log": [f"RiskAssessment: SUCCESS in {duration:.2f}ms (Level: {risk_level})"]
        }
        
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds() * 1000
        return {
            "risk_assessment": {
                "risk_level": "medium",
                "risk_score": 0.5,
                "confidence": 0.5,
                "method_used": "fallback"
            },
            "execution_log": [f"RiskAssessment: FALLBACK in {duration:.2f}ms - {str(e)}"]
        }


async def persona_classification_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 3: Persona Classification
    
    Classifies investor into behavioral persona based on
    profile and risk assessment.
    """
    start_time = datetime.now()
    
    try:
        prospect = state.get("prospect", {})
        risk_assessment = state.get("risk_assessment", {})
        
        risk_level = risk_assessment.get("risk_level", "medium")
        risk_tolerance = prospect.get("risk_tolerance", "medium").lower()
        age = prospect.get("age", 35)
        
        # Determine persona based on profile
        if risk_level == "high" and risk_tolerance == "high":
            persona_type = "aggressive_growth"
            behavioral_insights = [
                "Comfortable with market volatility",
                "Focused on long-term capital appreciation",
                "May consider concentrated positions"
            ]
            investment_preferences = {
                "preferred_asset_types": ["equity", "growth_stocks"],
                "time_horizon_preference": "long",
                "volatility_tolerance": "high"
            }
            communication_style = "Direct, data-driven discussions about growth opportunities"
            
        elif risk_level == "low" or risk_tolerance == "low":
            persona_type = "cautious_planner"
            behavioral_insights = [
                "Prioritizes capital preservation",
                "Prefers stable, predictable returns",
                "May need reassurance during market downturns"
            ]
            investment_preferences = {
                "preferred_asset_types": ["fixed_income", "bonds", "money_market"],
                "time_horizon_preference": "short_to_medium",
                "volatility_tolerance": "low"
            }
            communication_style = "Gentle, reassuring approach emphasizing safety and stability"
            
        else:
            persona_type = "steady_saver"
            behavioral_insights = [
                "Balanced approach to risk and reward",
                "Values consistent contributions",
                "Appreciates diversification"
            ]
            investment_preferences = {
                "preferred_asset_types": ["balanced_funds", "index_funds"],
                "time_horizon_preference": "medium_to_long",
                "volatility_tolerance": "medium"
            }
            communication_style = "Balanced discussions covering both risks and opportunities"
        
        result = {
            "persona_type": persona_type,
            "confidence": 0.82,
            "behavioral_insights": behavioral_insights,
            "investment_preferences": investment_preferences,
            "communication_style": communication_style
        }
        
        duration = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            "persona": result,
            "execution_log": [f"PersonaClassification: SUCCESS in {duration:.2f}ms (Type: {persona_type})"]
        }
        
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds() * 1000
        return {
            "persona": {
                "persona_type": "steady_saver",
                "confidence": 0.5,
                "behavioral_insights": [],
                "investment_preferences": {},
                "communication_style": "Standard professional approach"
            },
            "execution_log": [f"PersonaClassification: FALLBACK in {duration:.2f}ms - {str(e)}"]
        }


async def product_recommendation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 4: Product Recommendation
    
    Generates personalized product recommendations based on
    persona and risk profile.
    """
    start_time = datetime.now()
    
    try:
        persona = state.get("persona", {})
        risk_assessment = state.get("risk_assessment", {})
        prospect = state.get("prospect", {})
        
        persona_type = persona.get("persona_type", "steady_saver")
        risk_level = risk_assessment.get("risk_level", "medium")
        
        # Product catalog (simplified)
        products = [
            {"id": "P001", "name": "Conservative Bond Fund", "type": "fixed_income", 
             "risk": "low", "return": 0.04},
            {"id": "P002", "name": "Balanced Growth Fund", "type": "balanced", 
             "risk": "medium", "return": 0.07},
            {"id": "P003", "name": "Aggressive Equity Fund", "type": "equity", 
             "risk": "high", "return": 0.12},
            {"id": "P004", "name": "Blue Chip Dividend Fund", "type": "equity", 
             "risk": "medium", "return": 0.08},
            {"id": "P005", "name": "Government Securities Fund", "type": "fixed_income", 
             "risk": "low", "return": 0.035},
            {"id": "P006", "name": "International Growth Fund", "type": "equity", 
             "risk": "high", "return": 0.10},
        ]
        
        # Filter by risk level
        risk_compatibility = {
            "low": ["low"],
            "medium": ["low", "medium"],
            "high": ["low", "medium", "high"]
        }
        allowed_risks = risk_compatibility.get(risk_level, ["low", "medium"])
        filtered_products = [p for p in products if p["risk"] in allowed_risks]
        
        # Score products based on persona
        persona_preferences = {
            "aggressive_growth": {"equity": 1.0, "balanced": 0.7, "fixed_income": 0.3},
            "steady_saver": {"balanced": 1.0, "fixed_income": 0.8, "equity": 0.5},
            "cautious_planner": {"fixed_income": 1.0, "balanced": 0.6, "equity": 0.2}
        }
        preferences = persona_preferences.get(persona_type, persona_preferences["steady_saver"])
        
        # Calculate suitability scores
        recommendations = []
        for product in filtered_products:
            persona_score = preferences.get(product["type"], 0.5)
            risk_score = 1.0 if product["risk"] == risk_level else 0.7
            return_score = min(1.0, product["return"] / 0.10)
            
            suitability = (persona_score * 0.4 + risk_score * 0.3 + return_score * 0.2 + 0.1)
            
            recommendations.append({
                "product_id": product["id"],
                "product_name": product["name"],
                "product_type": product["type"],
                "risk_rating": product["risk"],
                "expected_return": product["return"],
                "suitability_score": min(1.0, suitability),
                "allocation_percentage": 0,  # Set below
                "justification": f"Matches {persona_type.replace('_', ' ')} profile with {suitability:.0%} suitability",
                "warnings": []
            })
        
        # Sort by suitability and take top 5
        recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)
        top_recommendations = recommendations[:5]
        
        # Calculate allocations
        total_score = sum(r["suitability_score"] for r in top_recommendations)
        for rec in top_recommendations:
            rec["allocation_percentage"] = (rec["suitability_score"] / total_score) * 100
        
        duration = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            "recommendations": top_recommendations,
            "execution_log": [f"ProductRecommendation: SUCCESS in {duration:.2f}ms ({len(top_recommendations)} products)"]
        }
        
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds() * 1000
        return {
            "recommendations": [{
                "product_id": "DEFAULT",
                "product_name": "Diversified Index Fund",
                "product_type": "balanced",
                "risk_rating": "medium",
                "expected_return": 0.07,
                "suitability_score": 0.7,
                "allocation_percentage": 100,
                "justification": "Default balanced recommendation",
                "warnings": ["Based on fallback logic"]
            }],
            "execution_log": [f"ProductRecommendation: FALLBACK in {duration:.2f}ms - {str(e)}"]
        }


async def finalization_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node 5: Finalization
    
    Performs compliance checks, aggregates results,
    and generates final insights and action items.
    """
    start_time = datetime.now()
    
    try:
        risk_assessment = state.get("risk_assessment", {})
        persona = state.get("persona", {})
        recommendations = state.get("recommendations", [])
        prospect = state.get("prospect", {})
        
        # Compliance checks
        checks_performed = []
        passed_checks = []
        failed_checks = []
        warnings = []
        
        # Check 1: Suitability
        checks_performed.append("suitability_check")
        if recommendations:
            high_risk_products = [r for r in recommendations if r.get("risk_rating") == "high"]
            if high_risk_products and risk_assessment.get("risk_level") == "low":
                warnings.append("High-risk products recommended for low-risk profile - verify suitability")
            else:
                passed_checks.append("suitability_check")
        
        # Check 2: Concentration risk
        checks_performed.append("concentration_check")
        if recommendations:
            max_allocation = max(r.get("allocation_percentage", 0) for r in recommendations)
            if max_allocation > 60:
                warnings.append(f"Single product allocation ({max_allocation:.0f}%) exceeds 60% threshold")
            else:
                passed_checks.append("concentration_check")
        
        # Check 3: KYC completeness
        checks_performed.append("kyc_check")
        if prospect.get("income") and prospect.get("age"):
            passed_checks.append("kyc_check")
        else:
            failed_checks.append("kyc_check")
        
        # Determine compliance status
        if failed_checks:
            compliance_status = "failed"
        elif warnings:
            compliance_status = "warning"
        else:
            compliance_status = "passed"
        
        # Generate disclosures
        disclosures = [
            "Past performance is not indicative of future results",
            "Investments are subject to market risks",
            "Please read all scheme related documents carefully before investing"
        ]
        
        if risk_assessment.get("risk_level") == "high":
            disclosures.append("High-risk investments may result in significant capital loss")
        
        compliance = {
            "status": compliance_status,
            "checks_performed": checks_performed,
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "warnings": warnings,
            "disclosures": disclosures,
            "regulatory_notes": []
        }
        
        # Generate key insights
        key_insights = []
        if risk_assessment:
            key_insights.append(f"Client classified as {risk_assessment.get('risk_level', 'medium').upper()} risk")
        if persona:
            key_insights.append(f"Investor persona: {persona.get('persona_type', 'steady_saver').replace('_', ' ').title()}")
        if recommendations:
            top_rec = recommendations[0]
            key_insights.append(f"Top recommendation: {top_rec.get('product_name')} ({top_rec.get('suitability_score', 0):.0%} suitability)")
        
        # Generate action items
        action_items = [
            "Schedule follow-up call within 5 business days",
            "Review and confirm client risk acknowledgment",
            "Document recommendation rationale in CRM"
        ]
        
        if compliance_status == "warning":
            action_items.insert(0, "Review compliance warnings before proceeding")
        
        # Calculate overall confidence
        confidences = [
            risk_assessment.get("confidence", 0.5),
            persona.get("confidence", 0.5)
        ]
        if recommendations:
            avg_suitability = sum(r.get("suitability_score", 0.5) for r in recommendations) / len(recommendations)
            confidences.append(avg_suitability)
        
        overall_confidence = sum(confidences) / len(confidences)
        
        duration = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            "compliance": compliance,
            "key_insights": key_insights,
            "action_items": action_items,
            "overall_confidence": overall_confidence,
            "execution_log": [f"Finalization: SUCCESS in {duration:.2f}ms (Compliance: {compliance_status})"]
        }
        
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds() * 1000
        return {
            "compliance": {"status": "warning", "warnings": [str(e)]},
            "key_insights": ["Analysis completed with warnings"],
            "action_items": ["Review results manually"],
            "overall_confidence": 0.5,
            "execution_log": [f"Finalization: FALLBACK in {duration:.2f}ms - {str(e)}"]
        }


# =============================================================================
# WORKFLOW CREATION
# =============================================================================

def create_workflow() -> StateGraph:
    """
    Create and compile the LangGraph workflow.
    
    Returns:
        Compiled StateGraph ready for execution
        
    Example:
        workflow = create_workflow()
        result = await workflow.ainvoke({"prospect": prospect_data})
    """
    # Initialize graph with state schema
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("data_validation", data_validation_node)
    workflow.add_node("risk_assessment", risk_assessment_node)
    workflow.add_node("persona_classification", persona_classification_node)
    workflow.add_node("product_recommendation", product_recommendation_node)
    workflow.add_node("finalization", finalization_node)
    
    # Define edges (linear workflow)
    workflow.add_edge("data_validation", "risk_assessment")
    workflow.add_edge("risk_assessment", "persona_classification")
    workflow.add_edge("persona_classification", "product_recommendation")
    workflow.add_edge("product_recommendation", "finalization")
    workflow.add_edge("finalization", END)
    
    # Set entry point
    workflow.set_entry_point("data_validation")
    
    # Compile and return
    return workflow.compile()


def create_workflow_with_conditional_edges() -> StateGraph:
    """
    Create workflow with conditional routing.
    
    This version includes conditional edges for advanced scenarios
    like skipping to compliance for high-risk clients.
    """
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("data_validation", data_validation_node)
    workflow.add_node("risk_assessment", risk_assessment_node)
    workflow.add_node("persona_classification", persona_classification_node)
    workflow.add_node("product_recommendation", product_recommendation_node)
    workflow.add_node("finalization", finalization_node)
    
    # Conditional edge function
    def should_skip_to_compliance(state: Dict[str, Any]) -> str:
        """Route based on risk level"""
        risk_assessment = state.get("risk_assessment", {})
        risk_level = risk_assessment.get("risk_level", "medium")
        
        if risk_level == "high" and state.get("data_quality_score", 1) < 0.7:
            return "finalization"  # Skip to compliance for high-risk with poor data
        return "persona_classification"
    
    # Add edges
    workflow.add_edge("data_validation", "risk_assessment")
    workflow.add_conditional_edges(
        "risk_assessment",
        should_skip_to_compliance,
        {
            "finalization": "finalization",
            "persona_classification": "persona_classification"
        }
    )
    workflow.add_edge("persona_classification", "product_recommendation")
    workflow.add_edge("product_recommendation", "finalization")
    workflow.add_edge("finalization", END)
    
    workflow.set_entry_point("data_validation")
    
    return workflow.compile()


# =============================================================================
# WORKFLOW EXECUTION HELPERS
# =============================================================================

async def run_analysis(prospect_data: dict) -> dict:
    """
    Run complete analysis workflow.
    
    Args:
        prospect_data: Dictionary with prospect information
        
    Returns:
        Complete workflow result
    """
    workflow = create_workflow()
    
    initial_state = {
        "prospect": prospect_data,
        "data_quality_score": None,
        "risk_assessment": None,
        "persona": None,
        "goal_prediction": None,
        "recommendations": [],
        "compliance": None,
        "key_insights": [],
        "action_items": [],
        "overall_confidence": 0.0,
        "execution_log": []
    }
    
    result = await workflow.ainvoke(initial_state)
    return result


def run_analysis_sync(prospect_data: dict) -> dict:
    """
    Run analysis synchronously (blocking).
    
    Args:
        prospect_data: Dictionary with prospect information
        
    Returns:
        Complete workflow result
    """
    return asyncio.run(run_analysis(prospect_data))


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Example usage
    sample_prospect = {
        "client_id": "C001",
        "name": "John Doe",
        "age": 35,
        "income": 150000,
        "investment_amount": 50000,
        "investment_horizon": 10,
        "risk_tolerance": "medium"
    }
    
    result = run_analysis_sync(sample_prospect)
    
    print("\n" + "="*60)
    print("ANALYSIS RESULTS")
    print("="*60)
    print(f"\nClient: {sample_prospect['name']}")
    print(f"Risk Level: {result['risk_assessment']['risk_level']}")
    print(f"Persona: {result['persona']['persona_type']}")
    print(f"Compliance: {result['compliance']['status']}")
    print(f"Overall Confidence: {result['overall_confidence']:.2%}")
    
    print("\nTop Recommendations:")
    for i, rec in enumerate(result['recommendations'][:3], 1):
        print(f"  {i}. {rec['product_name']} ({rec['suitability_score']:.0%} suitability)")
    
    print("\nKey Insights:")
    for insight in result['key_insights']:
        print(f"  • {insight}")
    
    print("\nExecution Log:")
    for log in result['execution_log']:
        print(f"  {log}")
