"""
Feature 1: AI Debate Agent (LangGraph Enhanced)
Multi-node constitutional debate workflow using LangGraph and DeepSeek
"""
from langgraph.graph import StateGraph, END
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models import VulnerabilityScoreAssessment, RiskMitigationResponse, MitigationStrategy

from typing import TypedDict, List, Dict
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# STATE DEFINITION
# ============================================================================

class DebateState(TypedDict):
    """State for constitutional debate"""
    article: int
    amendment_text: str
    context: str
    government_argument: str
    court_argument: str
    debate_transcript: List[Dict[str, str]]
    vulnerability_score: float
    court_challenge_probability: str
    mitigations: List[Dict[str, str]]
    step: int

# ============================================================================
# INITIALIZE LLM (DeepSeek via Hugging Face)
# ============================================================================

def get_llm():
    """Initialize DeepSeek LLM via Hugging Face"""
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    
    if not api_key:
        print("WARNING: HUGGINGFACE_API_KEY not found. Using mock responses.")
        return None
    
    try:
        llm = HuggingFaceEndpoint(
            repo_id="HuggingFaceH4/zephyr-7b-beta",
            huggingfacehub_api_token=api_key,
            temperature=0.7,
            max_new_tokens=512,
            top_p=0.95
        )
        model = ChatHuggingFace(llm=llm)
        return model
    except Exception as e:
        print(f"Error initializing Zephyr: {e}")
        return None
    
def vulnerability_llm():
    """Initialize DeepSeek LLM via Hugging Face"""
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    
    if not api_key:
        print("WARNING: HUGGINGFACE_API_KEY not found. Using mock responses.")
        return None
    
    try:
        llm = HuggingFaceEndpoint(
            repo_id="HuggingFaceH4/zephyr-7b-beta",
            huggingfacehub_api_token=api_key,
            temperature=0.7,
            max_new_tokens=512,
            top_p=0.95
        )
        model = ChatHuggingFace(llm=llm)
        return model
    except Exception as e:
        print(f"Error initializing Zephyr: {e}")
        return None

# ============================================================================
# NODE 1: GOVERNMENT POSITION
# ============================================================================

def government_position_node(state: DebateState) -> DebateState:
    """Government argues for ONOE feasibility"""
    
    llm = get_llm()
    
    # Predefined arguments for each article (fallback if LLM unavailable)
    fallback_arguments = {
        83: "ONOE ensures unified elections, reduces costs, and improves governance efficiency. Co-terminus provision is necessary for electoral synchronization and is within Parliament's legislative competence under Article 368.",
        172: "States can voluntarily consent to synchronization. This is a procedural reform, not a substantive change to federalism. Precedent exists in coordinated elections.",
        356: "Administrator can represent the state during ONOE elections. Precedent exists from 1977 elections held during President's Rule in multiple states. This is an administrative arrangement, not a constitutional violation."
    }
    
    if llm is None:
        # Use fallback
        government_arg = fallback_arguments.get(
            state["article"],
            "The proposed amendment is constitutionally sound and necessary for ONOE implementation."
        )
    else:
        prompt_template = ChatPromptTemplate.from_template(
            """You are a constitutional expert representing the Government of India.
 
 Article: {article}
 Amendment: {amendment_text}
 Context: {context}
 
 Task: Present the Government's position on why this constitutional amendment is feasible and legally sound.
 
 Guidelines:
 - Focus on: legislative competence, precedent, and practical benefits.
 - Respond in 2-3 clear sentences. 
 - DO NOT generate a dialogue or script. 
 - DO NOT include "GOVERNMENT:" or "Judge:" labels.
 - Provide ONLY the argument text."""
        )
        
        try:
            chain = prompt_template | llm
            response = chain.invoke({
                "article": state["article"],
                "amendment_text": state["amendment_text"],
                "context": state["context"]
            })
            government_arg = response.content.strip()
        except Exception as e:
            print(f"LLM error in government node: {e}")
            government_arg = fallback_arguments.get(state["article"], "Amendment is feasible.")
    
    state["government_argument"] = government_arg
    state["debate_transcript"].append({
        "speaker": "GOVERNMENT",
        "argument": government_arg,
        "type": "position"
    })
    state["step"] = 1
    
    return state

# ============================================================================
# NODE 2: SUPREME COURT POSITION
# ============================================================================

def court_position_node(state: DebateState) -> DebateState:
    """Supreme Court presents counter-argument"""
    
    llm = get_llm()
    
    # Predefined counter-arguments (fallback)
    fallback_arguments = {
        83: "Violates Article 246 state autonomy and federalism, which is a basic structure under Kesavananda Bharati (1973). Forcing state assemblies to align with Lok Sabha terms undermines state legislative independence. Basic structure cannot be amended.",
        172: "Article 246 explicitly grants states autonomy over their legislative terms. Mandatory synchronization violates the federal structure. Even with consent, the constitutional amendment may be challenged as it affects the basic structure of federalism established in Kesavananda Bharati.",
        356: "Violates Article 356 spirit and S.R. Bommai principles. A suspended state government cannot participate in synchronized elections as an equal partner. The Constitution is completely silent on this scenario. No amendment can legitimize elections in a state where constitutional machinery has failed - this contradicts the very purpose of Article 356."
    }
    
    if llm is None:
        court_arg = fallback_arguments.get(
            state["article"],
            "This amendment violates basic structure doctrine and federalism principles."
        )
    else:
        prompt_template = ChatPromptTemplate.from_template(
            """You are a Supreme Court constitutional expert.
 
 Article: {article}
 Amendment: {amendment_text}
 Context: {context}
 
 Government argues: "{government_argument}"
 
 Task: Present constitutional challenges to this amendment.
 
 Guidelines:
 - Focus on: Federalism (Article 246), State autonomy, and Basic structure limitations.
 - Respond in 2-3 clear sentences.
 - DO NOT generate a dialogue or script.
 - DO NOT include "SUPREME COURT:" or "Opposition:" labels.
 - Provide ONLY the counter-argument text."""
        )
        
        try:
            chain = prompt_template | llm
            response = chain.invoke({
                "article": state["article"],
                "amendment_text": state["amendment_text"],
                "context": state["context"],
                "government_argument": state["government_argument"]
            })
            court_arg = response.content.strip()
        except Exception as e:
            print(f"LLM error in court node: {e}")
            court_arg = fallback_arguments.get(state["article"], "Amendment violates basic structure.")
    
    state["court_argument"] = court_arg
    state["debate_transcript"].append({
        "speaker": "SUPREME COURT",
        "argument": court_arg,
        "type": "counter"
    })
    state["step"] = 2
    
    return state

# ============================================================================
# NODE 3: VULNERABILITY ASSESSMENT
# ============================================================================

def vulnerability_assessment_node(state: DebateState) -> DebateState:
    """AI evaluates court challenge probability"""
    
    llm = vulnerability_llm()
    
    # Predefined vulnerability scores
    vulnerability_scores = {
        83: 0.68,
        172: 0.72,
        356: 0.85
    }
    
    if llm is None:
        vulnerability = vulnerability_scores.get(state["article"], 0.65)
    else:
        # Use PydanticOutputParser
        parser = PydanticOutputParser(pydantic_object=VulnerabilityScoreAssessment)
        
        prompt_template = ChatPromptTemplate.from_template(
            """Analyze litigation risk for this constitutional amendment.
 
 Article: {article}
 Government: {government_argument}
 Court: {court_argument}
 
 Based on federalism concerns, precedent strength, and court history, provide a vulnerability score (0.0 to 1.0) and explanation.
 
 {format_instructions}"""
        )
        
        try:
            chain = prompt_template | llm | parser
            response: VulnerabilityScoreAssessment = chain.invoke({
                "article": state["article"],
                "government_argument": state["government_argument"],
                "court_argument": state["court_argument"],
                "format_instructions": parser.get_format_instructions()
            })
            
            # The structured output returns a Pydantic object directly
            vulnerability = response.vulnerability_score1
            print(f"LLM Assessment: {vulnerability} - {response.explanation}")
            
        except Exception as e:
            print(f"LLM error in assessment node: {e}")
            import traceback
            traceback.print_exc()
            vulnerability = vulnerability_scores.get(state["article"], 0.68)
    
    vulnerability = max(0, min(1, vulnerability))
    
    state["vulnerability_score"] = round(vulnerability, 2)
    state["court_challenge_probability"] = f"{int(vulnerability * 100)}%"
    state["step"] = 3
    
    state["debate_transcript"].append({
        "speaker": "ASSESSMENT",
        "argument": f"Vulnerability Score: {state['vulnerability_score']} ({state['court_challenge_probability']} court challenge probability)",
        "type": "assessment"
    })
    
    return state

# ============================================================================
# NODE 4: RISK MITIGATION
# ============================================================================

def risk_mitigation_node(state: DebateState) -> DebateState:
    """Suggest constitutional safeguards"""
    
    llm = get_llm()
    
    # Fallback mitigations
    fallback_mitigations = {
        356: [
            {
                "strategy": "Define explicit electoral procedure",
                "legal_basis": "Add Article 356A specifying election protocols during President's Rule"
            },
            {
                "strategy": "State consent mechanism",
                "legal_basis": "Require state ratification before ONOE implementation"
            }
        ]
    }
    
    if llm is None:
        mitigations = fallback_mitigations.get(state["article"], [])
    else:
        # Use PydanticOutputParser
        parser = PydanticOutputParser(pydantic_object=RiskMitigationResponse)
        
        prompt_template = ChatPromptTemplate.from_template(
            """Suggest constitutional safeguards to reduce court challenge risk.

Article: {article}
Vulnerability: {vulnerability_score}
Court Concern: {court_argument}

Provide 2 mitigation strategies with legal basis.

{format_instructions}"""
        )
        
        try:
            chain = prompt_template | llm | parser
            response: RiskMitigationResponse = chain.invoke({
                "article": state["article"],
                "vulnerability_score": state["vulnerability_score"],
                "court_argument": state["court_argument"],
                "format_instructions": parser.get_format_instructions()
            })
            
            # Convert Pydantic models to list of dicts for state
            mitigations = [m.model_dump() for m in response.mitigations]
            
        except Exception as e:
            print(f"LLM error in mitigation node: {e}")
            import traceback
            traceback.print_exc()
            mitigations = fallback_mitigations.get(state["article"], [])
    
    state["mitigations"] = mitigations
    
    for mitigation in mitigations:
        state["debate_transcript"].append({
            "speaker": "MITIGATION",
            "argument": f"{mitigation.get('strategy', '')}: {mitigation.get('legal_basis', '')}",
            "type": "mitigation"
        })
    
    state["step"] = 4
    return state

# ============================================================================
# BUILD LANGGRAPH
# ============================================================================

def build_debate_graph():
    """Build the LangGraph debate workflow"""
    
    workflow = StateGraph(DebateState)
    
    # Add nodes
    workflow.add_node("government", government_position_node)
    workflow.add_node("court", court_position_node)
    workflow.add_node("assess", vulnerability_assessment_node)
    workflow.add_node("mitigate", risk_mitigation_node)
    
    # Add edges (workflow sequence)
    workflow.set_entry_point("government")
    workflow.add_edge("government", "court")
    workflow.add_edge("court", "assess")
    workflow.add_edge("assess", "mitigate")
    workflow.add_edge("mitigate", END)
    
    return workflow.compile()

# ============================================================================
# MAIN DEBATE FUNCTION
# ============================================================================

class EnhancedDebateAgent:
    def __init__(self):
        self.graph = build_debate_graph()
        
        # Article-specific contexts
        self.contexts = {
            83: "Article 83(2) governs Lok Sabha duration. Co-terminus provision needed to sync with state assemblies for ONOE.",
            172: "Article 172(1) governs state assembly duration. 28 states have different expiry dates, requiring synchronization.",
            356: "Article 356 allows President's Rule but lacks electoral procedure clarity when state is under federal administration during ONOE."
        }
        
        self.amendments = {
            83: "Establish co-terminus provision linking Lok Sabha and State Assembly terms",
            172: "Synchronize all state assembly terms through constitutional amendment",
            356: "Define explicit procedure for elections during President's Rule in ONOE context"
        }
    
    def simulate_debate(self, article_number: int, topic: str = None, use_llm: bool = True) -> Dict:
        """Run complete constitutional debate using LangGraph"""
        
        if not use_llm:
            # Return pre-calculated fallback immediately
            return {
                "vulnerability_score": 0.68 if article_number != 356 else 0.85,
                "government_argument": "Amendment is feasible (Fast Mode estimate)",
                "court_argument": "Amendment challenges federal structure (Fast Mode estimate)",
                "risk_contribution": (0.68 if article_number != 356 else 0.85) * (40 if article_number == 356 else 25),
                "debate_transcript": [],
                "mitigations": [],
                "court_challenge_probability": "High"
            }
        
        initial_state = {
            "article": article_number,
            "amendment_text": self.amendments.get(article_number, "Constitutional amendment for ONOE"),
            "context": self.contexts.get(article_number, "ONOE implementation context"),
            "government_argument": "",
            "court_argument": "",
            "debate_transcript": [],
            "vulnerability_score": 0.0,
            "court_challenge_probability": "0%",
            "mitigations": [],
            "step": 0
        }
        
        try:
            final_state = self.graph.invoke(initial_state)
        except Exception as e:
            print(f"Error in debate graph: {e}")
            # Return fallback state
            final_state = initial_state
            final_state["vulnerability_score"] = 0.68
            final_state["government_argument"] = "Amendment is feasible"
            final_state["court_argument"] = "Amendment violates basic structure"
        
        # Calculate risk contribution
        risk_weight = 40 if article_number == 356 else 25
        risk_contribution = final_state["vulnerability_score"] * risk_weight
        
        return {
            "vulnerability_score": final_state["vulnerability_score"],
            "government_argument": final_state["government_argument"],
            "court_argument": final_state["court_argument"],
            "risk_contribution": risk_contribution,
            "debate_transcript": final_state["debate_transcript"],
            "mitigations": final_state.get("mitigations", []),
            "court_challenge_probability": final_state["court_challenge_probability"]
        }

# Singleton instance
debate_agent = EnhancedDebateAgent()
