"""
AI Legal Advisor Agent
Specialized AI agent for legal document analysis, compliance monitoring, and risk assessment
Provides intelligent legal insights and recommendations
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field

from core.enhanced_base_agent import EnhancedBaseAgent
from core.llm_integration import LLMManager, LLMMessage

logger = logging.getLogger(__name__)

@dataclass
class LegalAnalysis:
    """Legal document analysis result"""
    document_id: str
    analysis_type: str  # contract_review, compliance_check, risk_assessment
    
    # Analysis results
    risk_score: float  # 0-10
    compliance_score: float  # 0-10
    key_terms: List[str]
    potential_issues: List[str]
    recommendations: List[str]
    
    # Legal insights
    contract_type: Optional[str] = None
    governing_law: Optional[str] = None
    key_obligations: List[str] = field(default_factory=list)
    termination_clauses: List[str] = field(default_factory=list)
    liability_provisions: List[str] = field(default_factory=list)
    
    # Compliance assessment
    regulatory_requirements: List[str] = field(default_factory=list)
    compliance_gaps: List[str] = field(default_factory=list)
    required_actions: List[str] = field(default_factory=list)
    
    # Risk factors
    high_risk_clauses: List[str] = field(default_factory=list)
    missing_protections: List[str] = field(default_factory=list)
    negotiation_points: List[str] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class ComplianceAlert:
    """Compliance monitoring alert"""
    alert_id: str
    alert_type: str  # deadline_approaching, violation_detected, requirement_updated
    severity: str  # low, medium, high, critical
    
    title: str
    description: str
    regulation: str
    
    # Timeline
    deadline: Optional[str] = None
    days_remaining: Optional[int] = None
    
    # Actions
    required_actions: List[str] = field(default_factory=list)
    responsible_party: Optional[str] = None
    
    # Status
    status: str = "active"  # active, acknowledged, resolved
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class AILegalAdvisorAgent(EnhancedBaseAgent):
    """
    AI Legal Advisor Agent that provides:
    - Contract analysis and review
    - Compliance monitoring and alerts
    - Legal risk assessment
    - Regulatory requirement tracking
    - Document template generation
    - Legal research assistance
    """
    
    def __init__(self):
        super().__init__(
            agent_id="ai_legal_advisor",
            name="AI Legal Advisor",
            description="Intelligent legal document analysis and compliance monitoring",
            capabilities=[
                "contract_analysis",
                "compliance_monitoring", 
                "risk_assessment",
                "legal_research",
                "document_generation",
                "regulatory_tracking"
            ]
        )
        
        # Legal knowledge base
        self.legal_frameworks = {
            "gdpr": {
                "name": "General Data Protection Regulation",
                "jurisdiction": "EU",
                "key_requirements": [
                    "Data subject consent",
                    "Right to erasure",
                    "Data portability",
                    "Privacy by design",
                    "Data protection officer"
                ]
            },
            "ccpa": {
                "name": "California Consumer Privacy Act",
                "jurisdiction": "California, US",
                "key_requirements": [
                    "Consumer right to know",
                    "Right to delete",
                    "Right to opt-out",
                    "Non-discrimination"
                ]
            },
            "sox": {
                "name": "Sarbanes-Oxley Act",
                "jurisdiction": "US",
                "key_requirements": [
                    "Financial reporting controls",
                    "Audit committee independence",
                    "CEO/CFO certification",
                    "Internal control assessment"
                ]
            },
            "hipaa": {
                "name": "Health Insurance Portability and Accountability Act",
                "jurisdiction": "US",
                "key_requirements": [
                    "Protected health information security",
                    "Patient access rights",
                    "Business associate agreements",
                    "Breach notification"
                ]
            }
        }
        
        # Contract templates and clauses
        self.contract_templates = {
            "nda": {
                "name": "Non-Disclosure Agreement",
                "key_clauses": [
                    "Definition of confidential information",
                    "Permitted uses",
                    "Return of information",
                    "Term and termination"
                ]
            },
            "service_agreement": {
                "name": "Service Agreement",
                "key_clauses": [
                    "Scope of services",
                    "Payment terms",
                    "Service level agreements",
                    "Limitation of liability",
                    "Termination rights"
                ]
            },
            "employment": {
                "name": "Employment Agreement",
                "key_clauses": [
                    "Job responsibilities",
                    "Compensation and benefits",
                    "Confidentiality obligations",
                    "Non-compete provisions",
                    "Termination procedures"
                ]
            }
        }
        
        # Risk assessment criteria
        self.risk_factors = {
            "high_risk_terms": [
                "unlimited liability",
                "automatic renewal",
                "broad indemnification",
                "exclusive dealing",
                "non-compete",
                "liquidated damages"
            ],
            "missing_protections": [
                "limitation of liability",
                "force majeure",
                "intellectual property ownership",
                "data protection",
                "termination rights"
            ]
        }
        
        # Active compliance monitoring
        self.compliance_alerts: Dict[str, ComplianceAlert] = {}
        self.analysis_history: Dict[str, LegalAnalysis] = {}
    
    async def analyze_contract(self, document_content: str, contract_type: str = None) -> LegalAnalysis:
        """Analyze a contract for legal risks and compliance issues"""
        
        try:
            logger.info(f"Analyzing contract of type: {contract_type}")
            
            # Generate unique analysis ID
            analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Perform contract analysis
            analysis = LegalAnalysis(
                document_id=analysis_id,
                analysis_type="contract_review"
            )
            
            # Analyze contract content
            await self._analyze_contract_content(document_content, analysis)
            
            # Assess legal risks
            await self._assess_legal_risks(document_content, analysis)
            
            # Check compliance requirements
            await self._check_compliance_requirements(document_content, analysis)
            
            # Generate recommendations
            await self._generate_legal_recommendations(analysis)
            
            # Store analysis
            self.analysis_history[analysis_id] = analysis
            
            logger.info(f"Contract analysis completed: {analysis_id}")
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze contract: {e}")
            raise
    
    async def _analyze_contract_content(self, content: str, analysis: LegalAnalysis):
        """Analyze contract content for key terms and structure"""
        
        content_lower = content.lower()
        
        # Identify contract type
        if "service" in content_lower and "agreement" in content_lower:
            analysis.contract_type = "Service Agreement"
        elif "employment" in content_lower:
            analysis.contract_type = "Employment Agreement"
        elif "non-disclosure" in content_lower or "nda" in content_lower:
            analysis.contract_type = "Non-Disclosure Agreement"
        elif "license" in content_lower:
            analysis.contract_type = "License Agreement"
        else:
            analysis.contract_type = "General Contract"
        
        # Extract key terms
        key_terms = []
        
        # Payment terms
        if "payment" in content_lower:
            key_terms.append("Payment Terms")
        if "invoice" in content_lower:
            key_terms.append("Invoicing")
        
        # Liability and risk
        if "liability" in content_lower:
            key_terms.append("Liability Provisions")
        if "indemnif" in content_lower:
            key_terms.append("Indemnification")
        if "insurance" in content_lower:
            key_terms.append("Insurance Requirements")
        
        # Intellectual property
        if "intellectual property" in content_lower or "ip" in content_lower:
            key_terms.append("Intellectual Property")
        if "copyright" in content_lower:
            key_terms.append("Copyright")
        if "patent" in content_lower:
            key_terms.append("Patent Rights")
        
        # Termination
        if "termination" in content_lower:
            key_terms.append("Termination Clause")
        if "breach" in content_lower:
            key_terms.append("Breach Provisions")
        
        # Confidentiality
        if "confidential" in content_lower:
            key_terms.append("Confidentiality")
        if "non-disclosure" in content_lower:
            key_terms.append("Non-Disclosure")
        
        analysis.key_terms = key_terms
        
        # Identify governing law
        if "governed by" in content_lower:
            if "california" in content_lower:
                analysis.governing_law = "California Law"
            elif "new york" in content_lower:
                analysis.governing_law = "New York Law"
            elif "delaware" in content_lower:
                analysis.governing_law = "Delaware Law"
            else:
                analysis.governing_law = "Specified in Contract"
        
        # Extract key obligations
        obligations = []
        if "shall" in content_lower:
            obligations.append("Mandatory obligations present")
        if "must" in content_lower:
            obligations.append("Required actions specified")
        if "responsible for" in content_lower:
            obligations.append("Responsibility allocation defined")
        
        analysis.key_obligations = obligations
    
    async def _assess_legal_risks(self, content: str, analysis: LegalAnalysis):
        """Assess legal risks in the contract"""
        
        content_lower = content.lower()
        risk_score = 5.0  # Base risk score
        high_risk_clauses = []
        missing_protections = []
        
        # Check for high-risk terms
        for risk_term in self.risk_factors["high_risk_terms"]:
            if risk_term in content_lower:
                risk_score += 1.0
                high_risk_clauses.append(f"Contains {risk_term} clause")
        
        # Check for missing protections
        for protection in self.risk_factors["missing_protections"]:
            if protection.replace(" ", "") not in content_lower.replace(" ", ""):
                risk_score += 0.5
                missing_protections.append(f"Missing {protection} clause")
        
        # Specific risk assessments
        if "unlimited" in content_lower and "liability" in content_lower:
            risk_score += 2.0
            high_risk_clauses.append("Unlimited liability exposure")
        
        if "automatic renewal" in content_lower:
            risk_score += 1.0
            high_risk_clauses.append("Automatic renewal clause")
        
        if "exclusive" in content_lower:
            risk_score += 1.0
            high_risk_clauses.append("Exclusivity provisions")
        
        # Cap risk score at 10
        analysis.risk_score = min(risk_score, 10.0)
        analysis.high_risk_clauses = high_risk_clauses
        analysis.missing_protections = missing_protections
    
    async def _check_compliance_requirements(self, content: str, analysis: LegalAnalysis):
        """Check compliance with regulatory requirements"""
        
        content_lower = content.lower()
        compliance_score = 8.0  # Base compliance score
        regulatory_requirements = []
        compliance_gaps = []
        
        # Data protection compliance
        if "personal data" in content_lower or "customer data" in content_lower:
            regulatory_requirements.append("Data Protection (GDPR/CCPA)")
            
            if "data subject rights" not in content_lower:
                compliance_gaps.append("Missing data subject rights provisions")
                compliance_score -= 1.0
            
            if "data breach" not in content_lower:
                compliance_gaps.append("Missing data breach notification procedures")
                compliance_score -= 0.5
        
        # Employment law compliance
        if analysis.contract_type == "Employment Agreement":
            regulatory_requirements.append("Employment Law Compliance")
            
            if "equal opportunity" not in content_lower:
                compliance_gaps.append("Missing equal opportunity statement")
                compliance_score -= 0.5
            
            if "at-will" not in content_lower and "termination" in content_lower:
                compliance_gaps.append("Unclear employment termination terms")
                compliance_score -= 0.5
        
        # Financial regulations
        if "payment" in content_lower and "financial" in content_lower:
            regulatory_requirements.append("Financial Regulations")
            
            if "anti-money laundering" not in content_lower:
                compliance_gaps.append("Missing AML compliance provisions")
                compliance_score -= 0.5
        
        # Intellectual property compliance
        if "intellectual property" in content_lower:
            regulatory_requirements.append("IP Law Compliance")
            
            if "infringement" not in content_lower:
                compliance_gaps.append("Missing IP infringement protections")
                compliance_score -= 0.5
        
        analysis.compliance_score = max(compliance_score, 0.0)
        analysis.regulatory_requirements = regulatory_requirements
        analysis.compliance_gaps = compliance_gaps
    
    async def _generate_legal_recommendations(self, analysis: LegalAnalysis):
        """Generate legal recommendations based on analysis"""
        
        recommendations = []
        negotiation_points = []
        required_actions = []
        
        # Risk-based recommendations
        if analysis.risk_score > 7.0:
            recommendations.append("High-risk contract - recommend comprehensive legal review")
            required_actions.append("Schedule legal counsel review before signing")
        
        if analysis.risk_score > 5.0:
            recommendations.append("Consider negotiating risk mitigation clauses")
        
        # Missing protection recommendations
        for protection in analysis.missing_protections:
            if "limitation of liability" in protection:
                recommendations.append("Add limitation of liability clause to cap financial exposure")
                negotiation_points.append("Negotiate liability cap amount")
            
            if "force majeure" in protection:
                recommendations.append("Include force majeure clause for unforeseen circumstances")
            
            if "termination rights" in protection:
                recommendations.append("Define clear termination procedures and notice periods")
                negotiation_points.append("Negotiate termination notice period")
        
        # Compliance recommendations
        for gap in analysis.compliance_gaps:
            if "data subject rights" in gap:
                recommendations.append("Add GDPR-compliant data subject rights provisions")
                required_actions.append("Update data processing clauses for GDPR compliance")
            
            if "equal opportunity" in gap:
                recommendations.append("Include equal opportunity and non-discrimination clauses")
        
        # High-risk clause recommendations
        for clause in analysis.high_risk_clauses:
            if "unlimited liability" in clause:
                recommendations.append("CRITICAL: Negotiate liability limitation to reduce financial exposure")
                negotiation_points.append("Cap liability at contract value or annual fees")
            
            if "automatic renewal" in clause:
                recommendations.append("Add opt-out provisions for automatic renewal")
                negotiation_points.append("Negotiate renewal notice period")
        
        # General recommendations
        if not analysis.governing_law:
            recommendations.append("Specify governing law and jurisdiction for dispute resolution")
        
        if len(analysis.key_obligations) < 2:
            recommendations.append("Clarify mutual obligations and responsibilities")
        
        analysis.recommendations = recommendations
        analysis.negotiation_points = negotiation_points
        analysis.required_actions = required_actions
    
    async def monitor_compliance_deadlines(self) -> List[ComplianceAlert]:
        """Monitor compliance deadlines and generate alerts"""
        
        try:
            current_time = datetime.now(timezone.utc)
            alerts = []
            
            # Sample compliance requirements with deadlines
            compliance_requirements = [
                {
                    "regulation": "GDPR",
                    "requirement": "Annual Data Protection Impact Assessment",
                    "deadline": "2025-12-31",
                    "description": "Complete annual DPIA for all high-risk data processing activities"
                },
                {
                    "regulation": "SOC 2",
                    "requirement": "Type II Audit Preparation",
                    "deadline": "2025-11-15",
                    "description": "Prepare for annual SOC 2 Type II security audit"
                },
                {
                    "regulation": "Employment Law",
                    "requirement": "Handbook Update Review",
                    "deadline": "2025-10-31",
                    "description": "Quarterly review of employee handbook for compliance"
                }
            ]
            
            for req in compliance_requirements:
                deadline = datetime.fromisoformat(req["deadline"].replace('Z', '+00:00'))
                days_remaining = (deadline - current_time).days
                
                # Generate alerts based on time remaining
                if days_remaining <= 0:
                    severity = "critical"
                    alert_type = "deadline_overdue"
                elif days_remaining <= 7:
                    severity = "critical"
                    alert_type = "deadline_approaching"
                elif days_remaining <= 30:
                    severity = "high"
                    alert_type = "deadline_approaching"
                elif days_remaining <= 90:
                    severity = "medium"
                    alert_type = "deadline_upcoming"
                else:
                    continue  # No alert needed
                
                alert_id = f"alert_{req['regulation'].lower()}_{datetime.now().strftime('%Y%m%d')}"
                
                alert = ComplianceAlert(
                    alert_id=alert_id,
                    alert_type=alert_type,
                    severity=severity,
                    title=f"{req['regulation']} Compliance Deadline",
                    description=req["description"],
                    regulation=req["regulation"],
                    deadline=req["deadline"],
                    days_remaining=days_remaining,
                    required_actions=[
                        "Review current compliance status",
                        "Prepare required documentation",
                        "Schedule compliance review meeting"
                    ],
                    responsible_party="Legal Team"
                )
                
                alerts.append(alert)
                self.compliance_alerts[alert_id] = alert
            
            logger.info(f"Generated {len(alerts)} compliance alerts")
            return alerts
            
        except Exception as e:
            logger.error(f"Failed to monitor compliance deadlines: {e}")
            raise
    
    async def generate_contract_template(self, contract_type: str, parameters: Dict[str, Any]) -> str:
        """Generate a contract template based on type and parameters"""
        
        try:
            logger.info(f"Generating contract template: {contract_type}")
            
            if contract_type not in self.contract_templates:
                raise ValueError(f"Unknown contract type: {contract_type}")
            
            template_info = self.contract_templates[contract_type]
            
            # Generate basic template structure
            template = f"""
{template_info['name'].upper()}

This {template_info['name']} ("Agreement") is entered into on [DATE] between:

Party A: {parameters.get('party_a', '[PARTY A NAME]')}
Address: {parameters.get('party_a_address', '[PARTY A ADDRESS]')}

Party B: {parameters.get('party_b', '[PARTY B NAME]')}
Address: {parameters.get('party_b_address', '[PARTY B ADDRESS]')}

RECITALS
WHEREAS, the parties desire to enter into this Agreement to [PURPOSE];

NOW, THEREFORE, in consideration of the mutual covenants contained herein, the parties agree as follows:

"""
            
            # Add contract-specific clauses
            if contract_type == "nda":
                template += self._generate_nda_clauses(parameters)
            elif contract_type == "service_agreement":
                template += self._generate_service_agreement_clauses(parameters)
            elif contract_type == "employment":
                template += self._generate_employment_clauses(parameters)
            
            # Add standard closing clauses
            template += """

GENERAL PROVISIONS

Governing Law: This Agreement shall be governed by the laws of [JURISDICTION].

Entire Agreement: This Agreement constitutes the entire agreement between the parties.

Amendment: This Agreement may only be amended in writing signed by both parties.

Severability: If any provision is deemed invalid, the remainder shall remain in effect.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.

[PARTY A SIGNATURE]                    [PARTY B SIGNATURE]
Name: ________________________        Name: ________________________
Title: _______________________        Title: _______________________
Date: ________________________        Date: ________________________
"""
            
            logger.info(f"Contract template generated successfully")
            return template
            
        except Exception as e:
            logger.error(f"Failed to generate contract template: {e}")
            raise
    
    def _generate_nda_clauses(self, parameters: Dict[str, Any]) -> str:
        """Generate NDA-specific clauses"""
        
        return """
1. CONFIDENTIAL INFORMATION
"Confidential Information" means any and all non-public information disclosed by either party.

2. OBLIGATIONS
The receiving party agrees to:
a) Hold all Confidential Information in strict confidence
b) Not disclose Confidential Information to third parties
c) Use Confidential Information solely for the permitted purpose

3. EXCEPTIONS
Confidential Information does not include information that:
a) Is publicly available through no breach of this Agreement
b) Was known prior to disclosure
c) Is independently developed

4. TERM
This Agreement shall remain in effect for [TERM] years from the date of execution.

5. RETURN OF INFORMATION
Upon termination, all Confidential Information shall be returned or destroyed.
"""
    
    def _generate_service_agreement_clauses(self, parameters: Dict[str, Any]) -> str:
        """Generate Service Agreement-specific clauses"""
        
        return f"""
1. SERVICES
Provider shall provide the following services: {parameters.get('services', '[DESCRIBE SERVICES]')}

2. PAYMENT TERMS
a) Fees: {parameters.get('fees', '[SPECIFY FEES]')}
b) Payment Schedule: {parameters.get('payment_schedule', '[PAYMENT TERMS]')}
c) Late Fees: {parameters.get('late_fees', '1.5% per month')}

3. SERVICE LEVEL AGREEMENT
Provider shall maintain service availability of {parameters.get('sla_uptime', '99.9%')}.

4. LIMITATION OF LIABILITY
Provider's liability shall not exceed the fees paid in the preceding 12 months.

5. TERMINATION
Either party may terminate with {parameters.get('termination_notice', '30')} days written notice.

6. INTELLECTUAL PROPERTY
All work product shall be owned by {parameters.get('ip_owner', 'Client')}.
"""
    
    def _generate_employment_clauses(self, parameters: Dict[str, Any]) -> str:
        """Generate Employment Agreement-specific clauses"""
        
        return f"""
1. POSITION AND DUTIES
Employee shall serve as {parameters.get('position', '[JOB TITLE]')} and perform duties as assigned.

2. COMPENSATION
a) Base Salary: {parameters.get('salary', '[ANNUAL SALARY]')} per year
b) Benefits: {parameters.get('benefits', 'As per company policy')}
c) Vacation: {parameters.get('vacation_days', '20')} days per year

3. CONFIDENTIALITY
Employee agrees to maintain confidentiality of all proprietary information.

4. NON-COMPETE
Employee agrees not to compete with Company for {parameters.get('non_compete_period', '12')} months after termination.

5. TERMINATION
Employment may be terminated by either party with {parameters.get('notice_period', '2')} weeks notice.

6. INTELLECTUAL PROPERTY
All work product created during employment shall be owned by Company.
"""
    
    async def research_legal_precedent(self, legal_issue: str, jurisdiction: str = "US") -> Dict[str, Any]:
        """Research legal precedents and case law for a specific issue"""
        
        try:
            logger.info(f"Researching legal precedent: {legal_issue}")
            
            # Simulate legal research (in real implementation, would query legal databases)
            research_results = {
                "issue": legal_issue,
                "jurisdiction": jurisdiction,
                "key_cases": [],
                "legal_principles": [],
                "recommendations": [],
                "confidence_level": "medium"
            }
            
            # Sample research based on common legal issues
            if "data breach" in legal_issue.lower():
                research_results.update({
                    "key_cases": [
                        "Equifax Inc. Customer Data Security Breach Litigation (2017)",
                        "Target Corp. Customer Data Security Breach Litigation (2013)"
                    ],
                    "legal_principles": [
                        "Companies have duty to protect customer data",
                        "Notification requirements vary by state",
                        "Class action liability for inadequate security"
                    ],
                    "recommendations": [
                        "Implement comprehensive data security program",
                        "Maintain cyber insurance coverage",
                        "Develop incident response procedures"
                    ],
                    "confidence_level": "high"
                })
            
            elif "employment termination" in legal_issue.lower():
                research_results.update({
                    "key_cases": [
                        "At-will employment doctrine",
                        "Wrongful termination exceptions"
                    ],
                    "legal_principles": [
                        "At-will employment allows termination without cause",
                        "Exceptions for discrimination and retaliation",
                        "Documentation requirements for performance issues"
                    ],
                    "recommendations": [
                        "Maintain detailed performance documentation",
                        "Follow progressive discipline procedures",
                        "Ensure compliance with anti-discrimination laws"
                    ],
                    "confidence_level": "high"
                })
            
            elif "intellectual property" in legal_issue.lower():
                research_results.update({
                    "key_cases": [
                        "Patent eligibility under Alice Corp. v. CLS Bank",
                        "Trade secret protection under DTSA"
                    ],
                    "legal_principles": [
                        "Software patents require technical innovation",
                        "Trade secrets need reasonable protection measures",
                        "Employee invention assignment agreements"
                    ],
                    "recommendations": [
                        "File patent applications for technical innovations",
                        "Implement trade secret protection procedures",
                        "Use comprehensive IP assignment agreements"
                    ],
                    "confidence_level": "medium"
                })
            
            logger.info(f"Legal research completed for: {legal_issue}")
            return research_results
            
        except Exception as e:
            logger.error(f"Failed to research legal precedent: {e}")
            raise
    
    async def get_legal_insights(self) -> Dict[str, Any]:
        """Get comprehensive legal insights and recommendations"""
        
        try:
            current_time = datetime.now(timezone.utc)
            
            # Analyze recent legal activities
            recent_analyses = [
                analysis for analysis in self.analysis_history.values()
                if (current_time - datetime.fromisoformat(analysis.created_at.replace('Z', '+00:00'))).days <= 30
            ]
            
            # Calculate metrics
            avg_risk_score = sum(a.risk_score for a in recent_analyses) / max(len(recent_analyses), 1)
            avg_compliance_score = sum(a.compliance_score for a in recent_analyses) / max(len(recent_analyses), 1)
            
            # Active alerts
            active_alerts = [alert for alert in self.compliance_alerts.values() if alert.status == "active"]
            critical_alerts = [alert for alert in active_alerts if alert.severity == "critical"]
            
            # Generate insights
            insights = {
                "legal_health_score": round((avg_compliance_score + (10 - avg_risk_score)) / 2, 1),
                "risk_assessment": {
                    "average_risk_score": round(avg_risk_score, 1),
                    "high_risk_contracts": len([a for a in recent_analyses if a.risk_score > 7.0]),
                    "total_analyses": len(recent_analyses)
                },
                "compliance_status": {
                    "average_compliance_score": round(avg_compliance_score, 1),
                    "active_alerts": len(active_alerts),
                    "critical_alerts": len(critical_alerts)
                },
                "recommendations": [],
                "priority_actions": [],
                "trends": {
                    "risk_trend": "stable",  # Would calculate from historical data
                    "compliance_trend": "improving"
                }
            }
            
            # Generate recommendations
            if avg_risk_score > 7.0:
                insights["recommendations"].append("High average risk score - review contract negotiation strategies")
                insights["priority_actions"].append("Conduct comprehensive contract risk assessment")
            
            if avg_compliance_score < 7.0:
                insights["recommendations"].append("Compliance scores below target - strengthen compliance procedures")
                insights["priority_actions"].append("Implement automated compliance monitoring")
            
            if len(critical_alerts) > 0:
                insights["recommendations"].append(f"{len(critical_alerts)} critical compliance alerts require immediate attention")
                insights["priority_actions"].append("Address critical compliance deadlines")
            
            # Default recommendations
            if not insights["recommendations"]:
                insights["recommendations"] = [
                    "Legal operations are performing well",
                    "Continue regular contract reviews",
                    "Maintain proactive compliance monitoring"
                ]
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to get legal insights: {e}")
            raise

# Global AI legal advisor agent
ai_legal_advisor = AILegalAdvisorAgent()AI Legal Advisor Agent
Specialized AI agent for legal document analysis, compliance monitoring, and risk assessment
Provides intelligent legal insights and recommendations
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field

from core.enhanced_base_agent import EnhancedBaseAgent
from core.llm_integration import LLMManager, LLMMessage

logger = logging.getLogger(__name__)

@dataclass
class LegalAnalysis:
    """Legal document analysis result"""
    document_id: str
    analysis_type: str  # contract_review, compliance_check, risk_assessment
    
    # Analysis results
    risk_score: float  # 0-10
    compliance_score: float  # 0-10
    key_terms: List[str]
    potential_issues: List[str]
    recommendations: List[str]
    
    # Legal insights
    contract_type: Optional[str] = None
    governing_law: Optional[str] = None
    key_obligations: List[str] = field(default_factory=list)
    termination_clauses: List[str] = field(default_factory=list)
    liability_provisions: List[str] = field(default_factory=list)
    
    # Compliance assessment
    regulatory_requirements: List[str] = field(default_factory=list)
    compliance_gaps: List[str] = field(default_factory=list)
    required_actions: List[str] = field(default_factory=list)
    
    # Risk factors
    high_risk_clauses: List[str] = field(default_factory=list)
    missing_protections: List[str] = field(default_factory=list)
    negotiation_points: List[str] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class ComplianceAlert:
    """Compliance monitoring alert"""
    alert_id: str
    alert_type: str  # deadline_approaching, violation_detected, requirement_updated
    severity: str  # low, medium, high, critical
    
    title: str
    description: str
    regulation: str
    
    # Timeline
    deadline: Optional[str] = None
    days_remaining: Optional[int] = None
    
    # Actions
    required_actions: List[str] = field(default_factory=list)
    responsible_party: Optional[str] = None
    
    # Status
    status: str = "active"  # active, acknowledged, resolved
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class AILegalAdvisorAgent(EnhancedBaseAgent):
    """
    AI Legal Advisor Agent that provides:
    - Contract analysis and review
    - Compliance monitoring and alerts
    - Legal risk assessment
    - Regulatory requirement tracking
    - Document template generation
    - Legal research assistance
    """
    
    def __init__(self):
        super().__init__(
            agent_id="ai_legal_advisor",
            name="AI Legal Advisor",
            description="Intelligent legal document analysis and compliance monitoring",
            capabilities=[
                "contract_analysis",
                "compliance_monitoring", 
                "risk_assessment",
                "legal_research",
                "document_generation",
                "regulatory_tracking"
            ]
        )
        
        # Legal knowledge base
        self.legal_frameworks = {
            "gdpr": {
                "name": "General Data Protection Regulation",
                "jurisdiction": "EU",
                "key_requirements": [
                    "Data subject consent",
                    "Right to erasure",
                    "Data portability",
                    "Privacy by design",
                    "Data protection officer"
                ]
            },
            "ccpa": {
                "name": "California Consumer Privacy Act",
                "jurisdiction": "California, US",
                "key_requirements": [
                    "Consumer right to know",
                    "Right to delete",
                    "Right to opt-out",
                    "Non-discrimination"
                ]
            },
            "sox": {
                "name": "Sarbanes-Oxley Act",
                "jurisdiction": "US",
                "key_requirements": [
                    "Financial reporting controls",
                    "Audit committee independence",
                    "CEO/CFO certification",
                    "Internal control assessment"
                ]
            },
            "hipaa": {
                "name": "Health Insurance Portability and Accountability Act",
                "jurisdiction": "US",
                "key_requirements": [
                    "Protected health information security",
                    "Patient access rights",
                    "Business associate agreements",
                    "Breach notification"
                ]
            }
        }
        
        # Contract templates and clauses
        self.contract_templates = {
            "nda": {
                "name": "Non-Disclosure Agreement",
                "key_clauses": [
                    "Definition of confidential information",
                    "Permitted uses",
                    "Return of information",
                    "Term and termination"
                ]
            },
            "service_agreement": {
                "name": "Service Agreement",
                "key_clauses": [
                    "Scope of services",
                    "Payment terms",
                    "Service level agreements",
                    "Limitation of liability",
                    "Termination rights"
                ]
            },
            "employment": {
                "name": "Employment Agreement",
                "key_clauses": [
                    "Job responsibilities",
                    "Compensation and benefits",
                    "Confidentiality obligations",
                    "Non-compete provisions",
                    "Termination procedures"
                ]
            }
        }
        
        # Risk assessment criteria
        self.risk_factors = {
            "high_risk_terms": [
                "unlimited liability",
                "automatic renewal",
                "broad indemnification",
                "exclusive dealing",
                "non-compete",
                "liquidated damages"
            ],
            "missing_protections": [
                "limitation of liability",
                "force majeure",
                "intellectual property ownership",
                "data protection",
                "termination rights"
            ]
        }
        
        # Active compliance monitoring
        self.compliance_alerts: Dict[str, ComplianceAlert] = {}
        self.analysis_history: Dict[str, LegalAnalysis] = {}
    
    async def analyze_contract(self, document_content: str, contract_type: str = None) -> LegalAnalysis:
        """Analyze a contract for legal risks and compliance issues"""
        
        try:
            logger.info(f"Analyzing contract of type: {contract_type}")
            
            # Generate unique analysis ID
            analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Perform contract analysis
            analysis = LegalAnalysis(
                document_id=analysis_id,
                analysis_type="contract_review"
            )
            
            # Analyze contract content
            await self._analyze_contract_content(document_content, analysis)
            
            # Assess legal risks
            await self._assess_legal_risks(document_content, analysis)
            
            # Check compliance requirements
            await self._check_compliance_requirements(document_content, analysis)
            
            # Generate recommendations
            await self._generate_legal_recommendations(analysis)
            
            # Store analysis
            self.analysis_history[analysis_id] = analysis
            
            logger.info(f"Contract analysis completed: {analysis_id}")
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze contract: {e}")
            raise
    
    async def _analyze_contract_content(self, content: str, analysis: LegalAnalysis):
        """Analyze contract content for key terms and structure"""
        
        content_lower = content.lower()
        
        # Identify contract type
        if "service" in content_lower and "agreement" in content_lower:
            analysis.contract_type = "Service Agreement"
        elif "employment" in content_lower:
            analysis.contract_type = "Employment Agreement"
        elif "non-disclosure" in content_lower or "nda" in content_lower:
            analysis.contract_type = "Non-Disclosure Agreement"
        elif "license" in content_lower:
            analysis.contract_type = "License Agreement"
        else:
            analysis.contract_type = "General Contract"
        
        # Extract key terms
        key_terms = []
        
        # Payment terms
        if "payment" in content_lower:
            key_terms.append("Payment Terms")
        if "invoice" in content_lower:
            key_terms.append("Invoicing")
        
        # Liability and risk
        if "liability" in content_lower:
            key_terms.append("Liability Provisions")
        if "indemnif" in content_lower:
            key_terms.append("Indemnification")
        if "insurance" in content_lower:
            key_terms.append("Insurance Requirements")
        
        # Intellectual property
        if "intellectual property" in content_lower or "ip" in content_lower:
            key_terms.append("Intellectual Property")
        if "copyright" in content_lower:
            key_terms.append("Copyright")
        if "patent" in content_lower:
            key_terms.append("Patent Rights")
        
        # Termination
        if "termination" in content_lower:
            key_terms.append("Termination Clause")
        if "breach" in content_lower:
            key_terms.append("Breach Provisions")
        
        # Confidentiality
        if "confidential" in content_lower:
            key_terms.append("Confidentiality")
        if "non-disclosure" in content_lower:
            key_terms.append("Non-Disclosure")
        
        analysis.key_terms = key_terms
        
        # Identify governing law
        if "governed by" in content_lower:
            if "california" in content_lower:
                analysis.governing_law = "California Law"
            elif "new york" in content_lower:
                analysis.governing_law = "New York Law"
            elif "delaware" in content_lower:
                analysis.governing_law = "Delaware Law"
            else:
                analysis.governing_law = "Specified in Contract"
        
        # Extract key obligations
        obligations = []
        if "shall" in content_lower:
            obligations.append("Mandatory obligations present")
        if "must" in content_lower:
            obligations.append("Required actions specified")
        if "responsible for" in content_lower:
            obligations.append("Responsibility allocation defined")
        
        analysis.key_obligations = obligations
    
    async def _assess_legal_risks(self, content: str, analysis: LegalAnalysis):
        """Assess legal risks in the contract"""
        
        content_lower = content.lower()
        risk_score = 5.0  # Base risk score
        high_risk_clauses = []
        missing_protections = []
        
        # Check for high-risk terms
        for risk_term in self.risk_factors["high_risk_terms"]:
            if risk_term in content_lower:
                risk_score += 1.0
                high_risk_clauses.append(f"Contains {risk_term} clause")
        
        # Check for missing protections
        for protection in self.risk_factors["missing_protections"]:
            if protection.replace(" ", "") not in content_lower.replace(" ", ""):
                risk_score += 0.5
                missing_protections.append(f"Missing {protection} clause")
        
        # Specific risk assessments
        if "unlimited" in content_lower and "liability" in content_lower:
            risk_score += 2.0
            high_risk_clauses.append("Unlimited liability exposure")
        
        if "automatic renewal" in content_lower:
            risk_score += 1.0
            high_risk_clauses.append("Automatic renewal clause")
        
        if "exclusive" in content_lower:
            risk_score += 1.0
            high_risk_clauses.append("Exclusivity provisions")
        
        # Cap risk score at 10
        analysis.risk_score = min(risk_score, 10.0)
        analysis.high_risk_clauses = high_risk_clauses
        analysis.missing_protections = missing_protections
    
    async def _check_compliance_requirements(self, content: str, analysis: LegalAnalysis):
        """Check compliance with regulatory requirements"""
        
        content_lower = content.lower()
        compliance_score = 8.0  # Base compliance score
        regulatory_requirements = []
        compliance_gaps = []
        
        # Data protection compliance
        if "personal data" in content_lower or "customer data" in content_lower:
            regulatory_requirements.append("Data Protection (GDPR/CCPA)")
            
            if "data subject rights" not in content_lower:
                compliance_gaps.append("Missing data subject rights provisions")
                compliance_score -= 1.0
            
            if "data breach" not in content_lower:
                compliance_gaps.append("Missing data breach notification procedures")
                compliance_score -= 0.5
        
        # Employment law compliance
        if analysis.contract_type == "Employment Agreement":
            regulatory_requirements.append("Employment Law Compliance")
            
            if "equal opportunity" not in content_lower:
                compliance_gaps.append("Missing equal opportunity statement")
                compliance_score -= 0.5
            
            if "at-will" not in content_lower and "termination" in content_lower:
                compliance_gaps.append("Unclear employment termination terms")
                compliance_score -= 0.5
        
        # Financial regulations
        if "payment" in content_lower and "financial" in content_lower:
            regulatory_requirements.append("Financial Regulations")
            
            if "anti-money laundering" not in content_lower:
                compliance_gaps.append("Missing AML compliance provisions")
                compliance_score -= 0.5
        
        # Intellectual property compliance
        if "intellectual property" in content_lower:
            regulatory_requirements.append("IP Law Compliance")
            
            if "infringement" not in content_lower:
                compliance_gaps.append("Missing IP infringement protections")
                compliance_score -= 0.5
        
        analysis.compliance_score = max(compliance_score, 0.0)
        analysis.regulatory_requirements = regulatory_requirements
        analysis.compliance_gaps = compliance_gaps
    
    async def _generate_legal_recommendations(self, analysis: LegalAnalysis):
        """Generate legal recommendations based on analysis"""
        
        recommendations = []
        negotiation_points = []
        required_actions = []
        
        # Risk-based recommendations
        if analysis.risk_score > 7.0:
            recommendations.append("High-risk contract - recommend comprehensive legal review")
            required_actions.append("Schedule legal counsel review before signing")
        
        if analysis.risk_score > 5.0:
            recommendations.append("Consider negotiating risk mitigation clauses")
        
        # Missing protection recommendations
        for protection in analysis.missing_protections:
            if "limitation of liability" in protection:
                recommendations.append("Add limitation of liability clause to cap financial exposure")
                negotiation_points.append("Negotiate liability cap amount")
            
            if "force majeure" in protection:
                recommendations.append("Include force majeure clause for unforeseen circumstances")
            
            if "termination rights" in protection:
                recommendations.append("Define clear termination procedures and notice periods")
                negotiation_points.append("Negotiate termination notice period")
        
        # Compliance recommendations
        for gap in analysis.compliance_gaps:
            if "data subject rights" in gap:
                recommendations.append("Add GDPR-compliant data subject rights provisions")
                required_actions.append("Update data processing clauses for GDPR compliance")
            
            if "equal opportunity" in gap:
                recommendations.append("Include equal opportunity and non-discrimination clauses")
        
        # High-risk clause recommendations
        for clause in analysis.high_risk_clauses:
            if "unlimited liability" in clause:
                recommendations.append("CRITICAL: Negotiate liability limitation to reduce financial exposure")
                negotiation_points.append("Cap liability at contract value or annual fees")
            
            if "automatic renewal" in clause:
                recommendations.append("Add opt-out provisions for automatic renewal")
                negotiation_points.append("Negotiate renewal notice period")
        
        # General recommendations
        if not analysis.governing_law:
            recommendations.append("Specify governing law and jurisdiction for dispute resolution")
        
        if len(analysis.key_obligations) < 2:
            recommendations.append("Clarify mutual obligations and responsibilities")
        
        analysis.recommendations = recommendations
        analysis.negotiation_points = negotiation_points
        analysis.required_actions = required_actions
    
    async def monitor_compliance_deadlines(self) -> List[ComplianceAlert]:
        """Monitor compliance deadlines and generate alerts"""
        
        try:
            current_time = datetime.now(timezone.utc)
            alerts = []
            
            # Sample compliance requirements with deadlines
            compliance_requirements = [
                {
                    "regulation": "GDPR",
                    "requirement": "Annual Data Protection Impact Assessment",
                    "deadline": "2025-12-31",
                    "description": "Complete annual DPIA for all high-risk data processing activities"
                },
                {
                    "regulation": "SOC 2",
                    "requirement": "Type II Audit Preparation",
                    "deadline": "2025-11-15",
                    "description": "Prepare for annual SOC 2 Type II security audit"
                },
                {
                    "regulation": "Employment Law",
                    "requirement": "Handbook Update Review",
                    "deadline": "2025-10-31",
                    "description": "Quarterly review of employee handbook for compliance"
                }
            ]
            
            for req in compliance_requirements:
                deadline = datetime.fromisoformat(req["deadline"].replace('Z', '+00:00'))
                days_remaining = (deadline - current_time).days
                
                # Generate alerts based on time remaining
                if days_remaining <= 0:
                    severity = "critical"
                    alert_type = "deadline_overdue"
                elif days_remaining <= 7:
                    severity = "critical"
                    alert_type = "deadline_approaching"
                elif days_remaining <= 30:
                    severity = "high"
                    alert_type = "deadline_approaching"
                elif days_remaining <= 90:
                    severity = "medium"
                    alert_type = "deadline_upcoming"
                else:
                    continue  # No alert needed
                
                alert_id = f"alert_{req['regulation'].lower()}_{datetime.now().strftime('%Y%m%d')}"
                
                alert = ComplianceAlert(
                    alert_id=alert_id,
                    alert_type=alert_type,
                    severity=severity,
                    title=f"{req['regulation']} Compliance Deadline",
                    description=req["description"],
                    regulation=req["regulation"],
                    deadline=req["deadline"],
                    days_remaining=days_remaining,
                    required_actions=[
                        "Review current compliance status",
                        "Prepare required documentation",
                        "Schedule compliance review meeting"
                    ],
                    responsible_party="Legal Team"
                )
                
                alerts.append(alert)
                self.compliance_alerts[alert_id] = alert
            
            logger.info(f"Generated {len(alerts)} compliance alerts")
            return alerts
            
        except Exception as e:
            logger.error(f"Failed to monitor compliance deadlines: {e}")
            raise
    
    async def generate_contract_template(self, contract_type: str, parameters: Dict[str, Any]) -> str:
        """Generate a contract template based on type and parameters"""
        
        try:
            logger.info(f"Generating contract template: {contract_type}")
            
            if contract_type not in self.contract_templates:
                raise ValueError(f"Unknown contract type: {contract_type}")
            
            template_info = self.contract_templates[contract_type]
            
            # Generate basic template structure
            template = f"""
{template_info['name'].upper()}

This {template_info['name']} ("Agreement") is entered into on [DATE] between:

Party A: {parameters.get('party_a', '[PARTY A NAME]')}
Address: {parameters.get('party_a_address', '[PARTY A ADDRESS]')}

Party B: {parameters.get('party_b', '[PARTY B NAME]')}
Address: {parameters.get('party_b_address', '[PARTY B ADDRESS]')}

RECITALS
WHEREAS, the parties desire to enter into this Agreement to [PURPOSE];

NOW, THEREFORE, in consideration of the mutual covenants contained herein, the parties agree as follows:

"""
            
            # Add contract-specific clauses
            if contract_type == "nda":
                template += self._generate_nda_clauses(parameters)
            elif contract_type == "service_agreement":
                template += self._generate_service_agreement_clauses(parameters)
            elif contract_type == "employment":
                template += self._generate_employment_clauses(parameters)
            
            # Add standard closing clauses
            template += """

GENERAL PROVISIONS

Governing Law: This Agreement shall be governed by the laws of [JURISDICTION].

Entire Agreement: This Agreement constitutes the entire agreement between the parties.

Amendment: This Agreement may only be amended in writing signed by both parties.

Severability: If any provision is deemed invalid, the remainder shall remain in effect.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.

[PARTY A SIGNATURE]                    [PARTY B SIGNATURE]
Name: ________________________        Name: ________________________
Title: _______________________        Title: _______________________
Date: ________________________        Date: ________________________
"""
            
            logger.info(f"Contract template generated successfully")
            return template
            
        except Exception as e:
            logger.error(f"Failed to generate contract template: {e}")
            raise
    
    def _generate_nda_clauses(self, parameters: Dict[str, Any]) -> str:
        """Generate NDA-specific clauses"""
        
        return """
1. CONFIDENTIAL INFORMATION
"Confidential Information" means any and all non-public information disclosed by either party.

2. OBLIGATIONS
The receiving party agrees to:
a) Hold all Confidential Information in strict confidence
b) Not disclose Confidential Information to third parties
c) Use Confidential Information solely for the permitted purpose

3. EXCEPTIONS
Confidential Information does not include information that:
a) Is publicly available through no breach of this Agreement
b) Was known prior to disclosure
c) Is independently developed

4. TERM
This Agreement shall remain in effect for [TERM] years from the date of execution.

5. RETURN OF INFORMATION
Upon termination, all Confidential Information shall be returned or destroyed.
"""
    
    def _generate_service_agreement_clauses(self, parameters: Dict[str, Any]) -> str:
        """Generate Service Agreement-specific clauses"""
        
        return f"""
1. SERVICES
Provider shall provide the following services: {parameters.get('services', '[DESCRIBE SERVICES]')}

2. PAYMENT TERMS
a) Fees: {parameters.get('fees', '[SPECIFY FEES]')}
b) Payment Schedule: {parameters.get('payment_schedule', '[PAYMENT TERMS]')}
c) Late Fees: {parameters.get('late_fees', '1.5% per month')}

3. SERVICE LEVEL AGREEMENT
Provider shall maintain service availability of {parameters.get('sla_uptime', '99.9%')}.

4. LIMITATION OF LIABILITY
Provider's liability shall not exceed the fees paid in the preceding 12 months.

5. TERMINATION
Either party may terminate with {parameters.get('termination_notice', '30')} days written notice.

6. INTELLECTUAL PROPERTY
All work product shall be owned by {parameters.get('ip_owner', 'Client')}.
"""
    
    def _generate_employment_clauses(self, parameters: Dict[str, Any]) -> str:
        """Generate Employment Agreement-specific clauses"""
        
        return f"""
1. POSITION AND DUTIES
Employee shall serve as {parameters.get('position', '[JOB TITLE]')} and perform duties as assigned.

2. COMPENSATION
a) Base Salary: {parameters.get('salary', '[ANNUAL SALARY]')} per year
b) Benefits: {parameters.get('benefits', 'As per company policy')}
c) Vacation: {parameters.get('vacation_days', '20')} days per year

3. CONFIDENTIALITY
Employee agrees to maintain confidentiality of all proprietary information.

4. NON-COMPETE
Employee agrees not to compete with Company for {parameters.get('non_compete_period', '12')} months after termination.

5. TERMINATION
Employment may be terminated by either party with {parameters.get('notice_period', '2')} weeks notice.

6. INTELLECTUAL PROPERTY
All work product created during employment shall be owned by Company.
"""
    
    async def research_legal_precedent(self, legal_issue: str, jurisdiction: str = "US") -> Dict[str, Any]:
        """Research legal precedents and case law for a specific issue"""
        
        try:
            logger.info(f"Researching legal precedent: {legal_issue}")
            
            # Simulate legal research (in real implementation, would query legal databases)
            research_results = {
                "issue": legal_issue,
                "jurisdiction": jurisdiction,
                "key_cases": [],
                "legal_principles": [],
                "recommendations": [],
                "confidence_level": "medium"
            }
            
            # Sample research based on common legal issues
            if "data breach" in legal_issue.lower():
                research_results.update({
                    "key_cases": [
                        "Equifax Inc. Customer Data Security Breach Litigation (2017)",
                        "Target Corp. Customer Data Security Breach Litigation (2013)"
                    ],
                    "legal_principles": [
                        "Companies have duty to protect customer data",
                        "Notification requirements vary by state",
                        "Class action liability for inadequate security"
                    ],
                    "recommendations": [
                        "Implement comprehensive data security program",
                        "Maintain cyber insurance coverage",
                        "Develop incident response procedures"
                    ],
                    "confidence_level": "high"
                })
            
            elif "employment termination" in legal_issue.lower():
                research_results.update({
                    "key_cases": [
                        "At-will employment doctrine",
                        "Wrongful termination exceptions"
                    ],
                    "legal_principles": [
                        "At-will employment allows termination without cause",
                        "Exceptions for discrimination and retaliation",
                        "Documentation requirements for performance issues"
                    ],
                    "recommendations": [
                        "Maintain detailed performance documentation",
                        "Follow progressive discipline procedures",
                        "Ensure compliance with anti-discrimination laws"
                    ],
                    "confidence_level": "high"
                })
            
            elif "intellectual property" in legal_issue.lower():
                research_results.update({
                    "key_cases": [
                        "Patent eligibility under Alice Corp. v. CLS Bank",
                        "Trade secret protection under DTSA"
                    ],
                    "legal_principles": [
                        "Software patents require technical innovation",
                        "Trade secrets need reasonable protection measures",
                        "Employee invention assignment agreements"
                    ],
                    "recommendations": [
                        "File patent applications for technical innovations",
                        "Implement trade secret protection procedures",
                        "Use comprehensive IP assignment agreements"
                    ],
                    "confidence_level": "medium"
                })
            
            logger.info(f"Legal research completed for: {legal_issue}")
            return research_results
            
        except Exception as e:
            logger.error(f"Failed to research legal precedent: {e}")
            raise
    
    async def get_legal_insights(self) -> Dict[str, Any]:
        """Get comprehensive legal insights and recommendations"""
        
        try:
            current_time = datetime.now(timezone.utc)
            
            # Analyze recent legal activities
            recent_analyses = [
                analysis for analysis in self.analysis_history.values()
                if (current_time - datetime.fromisoformat(analysis.created_at.replace('Z', '+00:00'))).days <= 30
            ]
            
            # Calculate metrics
            avg_risk_score = sum(a.risk_score for a in recent_analyses) / max(len(recent_analyses), 1)
            avg_compliance_score = sum(a.compliance_score for a in recent_analyses) / max(len(recent_analyses), 1)
            
            # Active alerts
            active_alerts = [alert for alert in self.compliance_alerts.values() if alert.status == "active"]
            critical_alerts = [alert for alert in active_alerts if alert.severity == "critical"]
            
            # Generate insights
            insights = {
                "legal_health_score": round((avg_compliance_score + (10 - avg_risk_score)) / 2, 1),
                "risk_assessment": {
                    "average_risk_score": round(avg_risk_score, 1),
                    "high_risk_contracts": len([a for a in recent_analyses if a.risk_score > 7.0]),
                    "total_analyses": len(recent_analyses)
                },
                "compliance_status": {
                    "average_compliance_score": round(avg_compliance_score, 1),
                    "active_alerts": len(active_alerts),
                    "critical_alerts": len(critical_alerts)
                },
                "recommendations": [],
                "priority_actions": [],
                "trends": {
                    "risk_trend": "stable",  # Would calculate from historical data
                    "compliance_trend": "improving"
                }
            }
            
            # Generate recommendations
            if avg_risk_score > 7.0:
                insights["recommendations"].append("High average risk score - review contract negotiation strategies")
                insights["priority_actions"].append("Conduct comprehensive contract risk assessment")
            
            if avg_compliance_score < 7.0:
                insights["recommendations"].append("Compliance scores below target - strengthen compliance procedures")
                insights["priority_actions"].append("Implement automated compliance monitoring")
            
            if len(critical_alerts) > 0:
                insights["recommendations"].append(f"{len(critical_alerts)} critical compliance alerts require immediate attention")
                insights["priority_actions"].append("Address critical compliance deadlines")
            
            # Default recommendations
            if not insights["recommendations"]:
                insights["recommendations"] = [
                    "Legal operations are performing well",
                    "Continue regular contract reviews",
                    "Maintain proactive compliance monitoring"
                ]
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to get legal insights: {e}")
            raise

# Global AI legal advisor agent
ai_legal_advisor = AILegalAdvisorAgent()