"""
Feature 5: Intelligent Bottleneck Explorer
LLM-powered bottleneck identification based on administrative context.
"""
from typing import List, Dict
import os
from dotenv import load_dotenv, find_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv(find_dotenv())

class BottleneckExplorer:
    def __init__(self):
        self.llm = self._init_llm()
    
    def _init_llm(self):
        """Initialize LLM with fallback handling"""
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        
        if not api_key:
            print("WARNING: HUGGINGFACE_API_KEY not found. Using fallback mode.")
            return None
        
        try:
            llm = HuggingFaceEndpoint(
                repo_id="mistralai/Mistral-7B-Instruct-v0.2",
                huggingfacehub_api_token=api_key,
                temperature=0.7,
                max_new_tokens=800,
                top_p=0.95
            )
            return llm
        except Exception as e:
            print(f"LLM initialization failed: {e}")
            return None
    
    def analyze_bottlenecks(self, context: Dict) -> Dict:
        """
        Main analysis function that identifies critical bottlenecks.
        
        Args:
            context: Dictionary containing:
                - target_year: int
                - evm_deficit: int (from F2)
                - ready_states: int
                - total_states: int
                - timeline_status: str (from F7)
                - months_remaining: int
                - months_needed: int
        
        Returns:
            Dictionary with bottlenecks list and metadata
        """
        # Try LLM analysis first
        if self.llm:
            try:
                bottlenecks = self._llm_analyze(context)
                if bottlenecks:
                    return {
                        "bottlenecks": bottlenecks,
                        "analysis_mode": "LLM",
                        "risk_contribution": self._calculate_overall_risk(bottlenecks),
                        "status": self._determine_status(bottlenecks)
                    }
            except Exception as e:
                print(f"LLM analysis failed: {e}")
        
        # Fallback to rule-based analysis
        bottlenecks = self._fallback_analyze(context)
        return {
            "bottlenecks": bottlenecks,
            "analysis_mode": "Fallback",
            "risk_contribution": self._calculate_overall_risk(bottlenecks),
            "status": self._determine_status(bottlenecks)
        }
    
    def _llm_analyze(self, context: Dict) -> List[Dict]:
        """Use LLM to intelligently identify bottlenecks"""
        prompt = ChatPromptTemplate.from_template("""
You are an expert election logistics analyst for India's One Nation One Election (ONOE) implementation.

Analyze the following administrative data and identify the top 5-7 CRITICAL BOTTLENECKS that could derail ONOE by {target_year}.

Current Status:
- Target Year: {target_year}
- EVM Deficit: {evm_deficit:,} units
- States Ready: {ready_states}/{total_states} ({ready_pct}%)
- Timeline: {timeline_status} ({months_remaining} months available, {months_needed} months needed)

For each bottleneck, provide EXACTLY this format (one per line):
NAME||SEVERITY||DESCRIPTION||IMPACT

Where:
- NAME: 3-5 word concise name
- SEVERITY: CRITICAL or HIGH or MEDIUM
- DESCRIPTION: One sentence explaining the issue
- IMPACT: One sentence on consequences if unresolved

Example:
EVM Production Shortage||CRITICAL||Manufacturing capacity insufficient to produce 2.5M units by deadline||Elections may need to be postponed or conducted in phases

Provide 5-7 bottlenecks, most critical first.
""")
        
        ready_pct = round((context.get('ready_states', 0) / context.get('total_states', 28)) * 100)
        
        chain = prompt | self.llm
        response = chain.invoke({
            "target_year": context.get('target_year', 2029),
            "evm_deficit": abs(context.get('evm_deficit', 0)),
            "ready_states": context.get('ready_states', 0),
            "total_states": context.get('total_states', 28),
            "ready_pct": ready_pct,
            "timeline_status": context.get('timeline_status', 'Unknown'),
            "months_remaining": context.get('months_remaining', 0),
            "months_needed": context.get('months_needed', 0)
        })
        
        # Parse LLM response
        return self._parse_llm_response(response)
    
    def _parse_llm_response(self, response: str) -> List[Dict]:
        """Parse LLM response into structured bottleneck list"""
        bottlenecks = []
        lines = response.strip().split('\n')
        
        for line in lines:
            if '||' in line:
                parts = [p.strip() for p in line.split('||')]
                if len(parts) >= 4:
                    bottlenecks.append({
                        "name": parts[0],
                        "severity": parts[1].upper(),
                        "description": parts[2],
                        "impact": parts[3],
                        "category": self._categorize_bottleneck(parts[0])
                    })
        
        return bottlenecks[:7]  # Limit to 7
    
    def _fallback_analyze(self, context: Dict) -> List[Dict]:
        """Rule-based bottleneck detection when LLM fails"""
        bottlenecks = []
        
        # EVM Deficit Check
        evm_deficit = context.get('evm_deficit', 0)
        if evm_deficit > 500000:
            bottlenecks.append({
                "name": "EVM Production Shortage",
                "severity": "CRITICAL",
                "description": f"Massive deficit of {evm_deficit:,} EVM units against 2.5M target poses existential risk.",
                "impact": "Elections may need postponement or phased approach, defeating ONOE purpose.",
                "category": "manufacturing"
            })
        elif evm_deficit > 100000:
            bottlenecks.append({
                "name": "EVM Supply Gap",
                "severity": "HIGH",
                "description": f"Shortfall of {evm_deficit:,} units requires accelerated production.",
                "impact": "Last-minute procurement risks quality issues and delivery delays.",
                "category": "manufacturing"
            })
        
        # State Readiness Check
        ready_pct = (context.get('ready_states', 0) / context.get('total_states', 28)) * 100
        if ready_pct < 50:
            bottlenecks.append({
                "name": "State Coordination Failure",
                "severity": "CRITICAL",
                "description": f"Only {ready_pct:.0f}% states ready indicates severe federal-state misalignment.",
                "impact": "Without consensus, constitutional amendment itself becomes impossible.",
                "category": "coordination"
            })
        elif ready_pct < 75:
            bottlenecks.append({
                "name": "State Readiness Gap",
                "severity": "HIGH",
                "description": f"{ready_pct:.0f}% state readiness insufficient for synchronized implementation.",
                "impact": "Opposition states may challenge implementation or demand exemptions.",
                "category": "coordination"
            })
        
        # Timeline Check
        months_remaining = context.get('months_remaining', 0)
        months_needed = context.get('months_needed', 0)
        timeline_buffer = months_remaining - months_needed
        
        if timeline_buffer < 0:
            bottlenecks.append({
                "name": "Timeline Physically Impossible",
                "severity": "CRITICAL",
                "description": f"Need {months_needed} months but only {months_remaining} available - deficit of {abs(timeline_buffer)} months.",
                "impact": "Target year must be pushed back or scope reduced drastically.",
                "category": "timeline"
            })
        elif timeline_buffer < 6:
            bottlenecks.append({
                "name": "Timeline Risk",
                "severity": "HIGH",
                "description": f"Only {timeline_buffer} month buffer leaves no room for delays.",
                "impact": "Any supply chain disruption will cascade into deadline breach.",
                "category": "timeline"
            })
        
        # Additional standard bottlenecks
        bottlenecks.extend([
            {
                "name": "Security Force Deployment",
                "severity": "HIGH",
                "description": "1.5 Crore personnel mobilization simultaneously strains CAPF reserves.",
                "impact": "Border areas and LWE zones may face security vacuums.",
                "category": "security"
            },
            {
                "name": "Semiconductor Dependency",
                "severity": "MEDIUM",
                "description": "24-month chip procurement lead time creates vulnerability to global supply shocks.",
                "impact": "Any Taiwan strait tension or trade war could halt EVM production.",
                "category": "supply_chain"
            },
            {
                "name": "Constitutional Amendment Passage",
                "severity": "HIGH",
                "description": "Requires 2/3 majority in both houses plus 50% state ratification.",
                "impact": "Political opposition can block the entire initiative at Parliament stage.",
                "category": "legal"
            }
        ])
        
        # Sort by severity and return top 7
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2}
        bottlenecks.sort(key=lambda x: severity_order.get(x['severity'], 3))
        
        return bottlenecks[:7]
    
    def _categorize_bottleneck(self, name: str) -> str:
        """Categorize bottleneck based on name"""
        name_lower = name.lower()
        if any(word in name_lower for word in ['evm', 'vvpat', 'production', 'manufacturing']):
            return 'manufacturing'
        elif any(word in name_lower for word in ['state', 'coordination', 'consensus', 'federal']):
            return 'coordination'
        elif any(word in name_lower for word in ['timeline', 'deadline', 'schedule']):
            return 'timeline'
        elif any(word in name_lower for word in ['security', 'capf', 'force']):
            return 'security'
        elif any(word in name_lower for word in ['amendment', 'constitutional', 'legal', 'parliament']):
            return 'legal'
        elif any(word in name_lower for word in ['supply', 'logistics', 'semiconductor']):
            return 'supply_chain'
        else:
            return 'other'
    
    def _calculate_overall_risk(self, bottlenecks: List[Dict]) -> float:
        """Calculate aggregate risk from bottleneck list"""
        if not bottlenecks:
            return 0.0
        
        severity_weights = {
            "CRITICAL": 20,
            "HIGH": 12,
            "MEDIUM": 6
        }
        
        total_risk = sum(severity_weights.get(b['severity'], 0) for b in bottlenecks)
        return min(100.0, total_risk)
    
    def _determine_status(self, bottlenecks: List[Dict]) -> str:
        """Determine overall status based on bottleneck severity"""
        if not bottlenecks:
            return "OPTIMAL"
        
        critical_count = sum(1 for b in bottlenecks if b['severity'] == 'CRITICAL')
        high_count = sum(1 for b in bottlenecks if b['severity'] == 'HIGH')
        
        if critical_count >= 2:
            return "CRITICAL - Multiple Blockers"
        elif critical_count == 1:
            return "HIGH RISK - Critical Bottleneck Identified"
        elif high_count >= 3:
            return "ELEVATED - Multiple High Risks"
        else:
            return "MANAGEABLE - Standard Challenges"

bottleneck_explorer = BottleneckExplorer()
