"""
Legal Agent with Sub-Agents
Handles legal compliance, contracts, IP, and regulatory requirements across multiple jurisdictions
"""

import asyncio
import logging
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

from core.base_agent import BaseAgent, AgentCapability, TaskResult
from core.simple_message_bus import event_bus

logger = logging.getLogger(__name__)

class LegalSubAgent(ABC):
    """Base class for legal sub-agents"""
    
    def __init__(self, jurisdiction: str, specialization: str):
        self.jurisdiction = jurisdiction
        self.specialization = specialization
        
    @abstractmethod
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle jurisdiction-specific legal task"""
        pass
        
    @abstractmethod
    def get_compliance_requirements(self, business_type: str) -> List[Dict[str, Any]]:
        """Get compliance requirements for business type"""
        pass

class USALegalAgent(LegalSubAgent):
    def __init__(self):
        super().__init__("USA", "US Federal and State Law")
        
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get("type")
        
        if task_type == "incorporation":
            return await self._handle_incorporation(task)
        elif task_type == "compliance_check":
            return await self._check_compliance(task)
        elif task_type == "contract_review":
            return await self._review_contract(task)
        elif task_type == "ip_protection":
            return await self._handle_ip_protection(task)
        elif task_type == "employment_law":
            return await self._handle_employment_law(task)
        else:
            return {"error": f"Unknown task type: {task_type}"}
            
    async def _handle_incorporation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        business_type = task.get("business_type", "LLC")
        state = task.get("state", "Delaware")
        
        incorporation_guide = {
            "recommended_structure": "Delaware C-Corp" if task.get("seeking_investment") else "LLC",
            "required_documents": [
                "Certificate of Incorporation",
                "Corporate Bylaws", 
                "Initial Board Resolutions",
                "Stock Purchase Agreements",
                "Shareholder Agreements"
            ],
            "filing_requirements": {
                "state_filing_fee": "$89" if state == "Delaware" else "$100-500",
                "registered_agent": "Required in state of incorporation",
                "ein_number": "Required from IRS",
                "state_tax_id": "Required if hiring employees"
            },
            "ongoing_compliance": [
                "Annual franchise tax filing",
                "Annual report filing", 
                "Board meeting minutes",
                "Stock ledger maintenance"
            ],
            "estimated_timeline": "1-2 weeks",
            "estimated_cost": "$500-2000 including legal fees"
        }
        
        return {
            "jurisdiction": "USA",
            "incorporation_guide": incorporation_guide,
            "next_steps": [
                "Choose state of incorporation",
                "Reserve company name",
                "Prepare incorporation documents",
                "File with Secretary of State"
            ]
        }
        
    async def _check_compliance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        business_type = task.get("business_type", "SaaS")
        
        compliance_requirements = {
            "federal_requirements": [
                "EIN (Employer Identification Number)",
                "Business license (if applicable)",
                "Industry-specific licenses"
            ],
            "data_privacy": [
                "CCPA compliance (California residents)",
                "COPPA compliance (if serving children)",
                "HIPAA compliance (if handling health data)",
                "SOX compliance (if public company)"
            ],
            "employment_law": [
                "I-9 employment eligibility verification",
                "Workers' compensation insurance",
                "Unemployment insurance",
                "Equal opportunity compliance"
            ],
            "tax_obligations": [
                "Federal income tax",
                "State income tax",
                "Sales tax (if applicable)",
                "Payroll taxes"
            ]
        }
        
        if business_type.lower() in ["fintech", "financial", "banking"]:
            compliance_requirements["financial_regulations"] = [
                "Money transmitter licenses",
                "Bank Secrecy Act compliance",
                "Anti-Money Laundering (AML)",
                "Know Your Customer (KYC)"
            ]
            
        return {
            "jurisdiction": "USA",
            "compliance_requirements": compliance_requirements,
            "risk_level": "medium" if business_type == "SaaS" else "high"
        }
        
    async def _review_contract(self, task: Dict[str, Any]) -> Dict[str, Any]:
        contract_type = task.get("contract_type", "service_agreement")
        
        contract_templates = {
            "service_agreement": {
                "key_clauses": [
                    "Scope of services",
                    "Payment terms",
                    "Intellectual property ownership",
                    "Limitation of liability",
                    "Termination provisions"
                ],
                "risk_areas": [
                    "Unlimited liability exposure",
                    "Broad indemnification clauses",
                    "Automatic renewal terms"
                ]
            },
            "employment_agreement": {
                "key_clauses": [
                    "At-will employment",
                    "Confidentiality provisions",
                    "Non-compete agreements",
                    "Intellectual property assignment",
                    "Compensation and benefits"
                ],
                "compliance_notes": [
                    "Non-compete enforceability varies by state",
                    "California prohibits most non-competes",
                    "Must comply with wage and hour laws"
                ]
            }
        }
        
        return {
            "jurisdiction": "USA",
            "contract_analysis": contract_templates.get(contract_type, {}),
            "recommendations": [
                "Include governing law clause",
                "Add dispute resolution mechanism",
                "Ensure compliance with state laws"
            ]
        }
        
    async def _handle_ip_protection(self, task: Dict[str, Any]) -> Dict[str, Any]:
        ip_type = task.get("ip_type", "trademark")
        
        ip_guide = {
            "trademark": {
                "filing_authority": "USPTO",
                "cost": "$250-400 per class",
                "timeline": "8-12 months",
                "requirements": ["Distinctive mark", "Use in commerce"]
            },
            "patent": {
                "filing_authority": "USPTO", 
                "cost": "$1,600-8,000",
                "timeline": "18-36 months",
                "requirements": ["Novel invention", "Non-obvious", "Useful"]
            },
            "copyright": {
                "filing_authority": "US Copyright Office",
                "cost": "$45-65",
                "timeline": "3-6 months",
                "requirements": ["Original work of authorship"]
            }
        }
        
        return {
            "jurisdiction": "USA",
            "ip_protection_guide": ip_guide.get(ip_type, {}),
            "recommendations": [
                "Conduct trademark search before filing",
                "Consider international protection",
                "Maintain proper documentation"
            ]
        }
        
    async def _handle_employment_law(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "jurisdiction": "USA",
            "employment_law_guide": {
                "hiring_requirements": [
                    "I-9 employment eligibility verification",
                    "Equal opportunity compliance",
                    "Background check compliance"
                ],
                "wage_and_hour": [
                    "Federal minimum wage: $7.25/hour",
                    "Overtime pay for non-exempt employees",
                    "State wage laws may be higher"
                ],
                "workplace_policies": [
                    "Anti-harassment policy required",
                    "Safety training and compliance",
                    "Family and medical leave compliance"
                ]
            }
        }
        
    def get_compliance_requirements(self, business_type: str) -> List[Dict[str, Any]]:
        base_requirements = [
            {"requirement": "Business Registration", "urgency": "high", "cost": "$100-500"},
            {"requirement": "EIN Number", "urgency": "high", "cost": "$0"},
            {"requirement": "Business License", "urgency": "medium", "cost": "$50-500"},
            {"requirement": "Privacy Policy", "urgency": "high", "cost": "$500-2000"}
        ]
        
        if business_type.lower() in ["fintech", "financial"]:
            base_requirements.extend([
                {"requirement": "Money Transmitter License", "urgency": "high", "cost": "$5000-50000"},
                {"requirement": "AML Compliance Program", "urgency": "high", "cost": "$2000-10000"}
            ])
            
        return base_requirements

class IndiaLegalAgent(LegalSubAgent):
    def __init__(self):
        super().__init__("India", "Indian Corporate and Commercial Law")
        
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get("type")
        
        if task_type == "incorporation":
            return await self._handle_incorporation(task)
        elif task_type == "compliance_check":
            return await self._check_compliance(task)
        elif task_type == "gst_compliance":
            return await self._handle_gst_compliance(task)
        elif task_type == "labor_law":
            return await self._handle_labor_law(task)
        else:
            return {"error": f"Unknown task type: {task_type}"}
            
    async def _handle_incorporation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        business_type = task.get("business_type", "Private Limited")
        
        return {
            "jurisdiction": "India",
            "incorporation_guide": {
                "recommended_structure": "Private Limited Company",
                "required_documents": [
                    "Memorandum of Association (MOA)",
                    "Articles of Association (AOA)",
                    "Form INC-32 (SPICe+)",
                    "Director Identification Numbers (DIN)",
                    "Digital Signature Certificates (DSC)"
                ],
                "regulatory_approvals": [
                    "Ministry of Corporate Affairs (MCA)",
                    "Registrar of Companies (ROC)",
                    "PAN and TAN registration",
                    "GST registration"
                ],
                "minimum_requirements": {
                    "directors": "Minimum 2 directors",
                    "shareholders": "Minimum 2 shareholders", 
                    "capital": "No minimum paid-up capital",
                    "registered_office": "Required in India"
                },
                "estimated_timeline": "15-20 days",
                "estimated_cost": "₹10,000-25,000"
            }
        }
        
    async def _check_compliance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        business_type = task.get("business_type", "IT Services")
        
        compliance_requirements = {
            "corporate_compliance": [
                "Annual filing of financial statements",
                "Board meeting requirements (minimum 4 per year)",
                "Annual General Meeting (AGM)",
                "Statutory auditor appointment"
            ],
            "tax_compliance": [
                "Income Tax Return filing",
                "GST return filing (monthly/quarterly)",
                "TDS compliance",
                "Professional Tax (state-specific)"
            ],
            "labor_compliance": [
                "Provident Fund (PF) registration",
                "Employee State Insurance (ESI)",
                "Shops and Establishment Act registration",
                "Contract Labor Act compliance"
            ],
            "data_protection": [
                "Personal Data Protection Bill compliance",
                "IT Act 2000 compliance",
                "Reasonable security practices"
            ]
        }
        
        if business_type.lower() in ["fintech", "nbfc"]:
            compliance_requirements["financial_regulations"] = [
                "RBI licensing (if applicable)",
                "NBFC registration",
                "KYC and AML compliance",
                "Foreign Exchange Management Act (FEMA)"
            ]
            
        return {
            "jurisdiction": "India",
            "compliance_requirements": compliance_requirements
        }
        
    async def _handle_gst_compliance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        annual_turnover = task.get("annual_turnover", 0)
        
        gst_guide = {
            "registration_threshold": "₹20 lakhs (₹10 lakhs for special category states)",
            "gst_rates": {
                "services": "18% (most IT services)",
                "goods": "5%, 12%, 18%, 28% based on classification"
            },
            "filing_requirements": {
                "monthly": "GSTR-1, GSTR-3B" if annual_turnover > 5000000 else "Quarterly",
                "annual": "GSTR-9 (Annual Return)"
            },
            "compliance_calendar": [
                "GSTR-1: 11th of next month",
                "GSTR-3B: 20th of next month", 
                "GSTR-9: 31st December"
            ]
        }
        
        return {
            "jurisdiction": "India",
            "gst_compliance_guide": gst_guide
        }
        
    async def _handle_labor_law(self, task: Dict[str, Any]) -> Dict[str, Any]:
        employee_count = task.get("employee_count", 0)
        
        labor_law_guide = {
            "applicable_acts": [
                "Employees' Provident Funds Act (if 20+ employees)",
                "Employees' State Insurance Act (if 10+ employees)",
                "Payment of Gratuity Act (if 10+ employees)",
                "Contract Labour Act (if using contractors)"
            ],
            "registration_requirements": {
                "pf_registration": "Required if 20+ employees",
                "esi_registration": "Required if 10+ employees",
                "shops_establishment": "Required for all establishments"
            },
            "compliance_obligations": [
                "Monthly PF and ESI contributions",
                "Annual labor law returns",
                "Maintenance of statutory registers",
                "Display of statutory notices"
            ]
        }
        
        return {
            "jurisdiction": "India",
            "labor_law_guide": labor_law_guide
        }
        
    def get_compliance_requirements(self, business_type: str) -> List[Dict[str, Any]]:
        return [
            {"requirement": "Company Incorporation", "urgency": "high", "cost": "₹15,000-25,000"},
            {"requirement": "GST Registration", "urgency": "high", "cost": "₹0"},
            {"requirement": "PAN Registration", "urgency": "high", "cost": "₹110"},
            {"requirement": "Bank Account Opening", "urgency": "high", "cost": "₹500-2,000"},
            {"requirement": "Digital Signature", "urgency": "medium", "cost": "₹1,500-3,000"}
        ]

class ChinaLegalAgent(LegalSubAgent):
    def __init__(self):
        super().__init__("China", "Chinese Corporate and Commercial Law")
        
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get("type")
        
        if task_type == "incorporation":
            return await self._handle_incorporation(task)
        elif task_type == "compliance_check":
            return await self._check_compliance(task)
        else:
            return {"error": f"Unknown task type: {task_type}"}
            
    async def _handle_incorporation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "jurisdiction": "China",
            "incorporation_guide": {
                "recommended_structure": "Wholly Foreign-Owned Enterprise (WFOE)",
                "required_documents": [
                    "Articles of Association",
                    "Feasibility Study Report",
                    "Application for Enterprise Name Pre-approval",
                    "Capital Verification Report"
                ],
                "regulatory_approvals": [
                    "Ministry of Commerce (MOFCOM)",
                    "State Administration for Market Regulation (SAMR)",
                    "Tax registration",
                    "Foreign exchange registration"
                ],
                "minimum_requirements": {
                    "registered_capital": "No minimum for most industries",
                    "legal_representative": "Required",
                    "registered_address": "Required in China"
                },
                "estimated_timeline": "2-3 months",
                "estimated_cost": "¥50,000-150,000"
            }
        }
        
    async def _check_compliance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "jurisdiction": "China",
            "compliance_requirements": {
                "corporate_compliance": [
                    "Annual inspection and filing",
                    "Board resolutions and minutes",
                    "Statutory audits",
                    "Foreign investment reporting"
                ],
                "tax_compliance": [
                    "Corporate Income Tax (25%)",
                    "Value Added Tax (VAT)",
                    "Individual Income Tax withholding",
                    "Monthly/quarterly tax filings"
                ],
                "data_protection": [
                    "Cybersecurity Law compliance",
                    "Personal Information Protection Law (PIPL)",
                    "Data localization requirements",
                    "Cross-border data transfer approvals"
                ]
            }
        }
        
    def get_compliance_requirements(self, business_type: str) -> List[Dict[str, Any]]:
        return [
            {"requirement": "WFOE Registration", "urgency": "high", "cost": "¥80,000-120,000"},
            {"requirement": "Tax Registration", "urgency": "high", "cost": "¥0"},
            {"requirement": "Bank Account Opening", "urgency": "high", "cost": "¥1,000-5,000"},
            {"requirement": "PIPL Compliance", "urgency": "high", "cost": "¥20,000-50,000"}
        ]

class UKLegalAgent(LegalSubAgent):
    def __init__(self):
        super().__init__("UK", "UK Corporate and Commercial Law")
        
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get("type")
        
        if task_type == "incorporation":
            return await self._handle_incorporation(task)
        elif task_type == "compliance_check":
            return await self._check_compliance(task)
        else:
            return {"error": f"Unknown task type: {task_type}"}
            
    async def _handle_incorporation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "jurisdiction": "UK",
            "incorporation_guide": {
                "recommended_structure": "Private Limited Company",
                "required_documents": [
                    "Memorandum of Association",
                    "Articles of Association",
                    "Form IN01 (Application to register a company)",
                    "Statement of capital and initial shareholdings"
                ],
                "regulatory_approvals": [
                    "Companies House registration",
                    "HMRC registration for Corporation Tax",
                    "VAT registration (if applicable)",
                    "PAYE registration (if hiring employees)"
                ],
                "minimum_requirements": {
                    "directors": "Minimum 1 director",
                    "shareholders": "Minimum 1 shareholder",
                    "share_capital": "£100 minimum",
                    "registered_office": "Required in UK"
                },
                "estimated_timeline": "1-3 days (online)",
                "estimated_cost": "£12-50"
            }
        }
        
    async def _check_compliance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "jurisdiction": "UK",
            "compliance_requirements": {
                "corporate_compliance": [
                    "Annual confirmation statement",
                    "Annual accounts filing",
                    "Corporation Tax return",
                    "Directors' duties compliance"
                ],
                "employment_law": [
                    "Auto-enrolment pension scheme",
                    "Employment contracts",
                    "Workplace pension contributions",
                    "Health and safety compliance"
                ],
                "data_protection": [
                    "UK GDPR compliance",
                    "Data Protection Act 2018",
                    "Privacy notices and policies",
                    "Data breach notification procedures"
                ]
            }
        }
        
    def get_compliance_requirements(self, business_type: str) -> List[Dict[str, Any]]:
        return [
            {"requirement": "Company Registration", "urgency": "high", "cost": "£12-50"},
            {"requirement": "Corporation Tax Registration", "urgency": "high", "cost": "£0"},
            {"requirement": "Business Bank Account", "urgency": "high", "cost": "£0-300"},
            {"requirement": "GDPR Compliance", "urgency": "high", "cost": "£500-2000"}
        ]

class BrazilLegalAgent(LegalSubAgent):
    def __init__(self):
        super().__init__("Brazil", "Brazilian Corporate and Commercial Law")
        
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get("type")
        
        if task_type == "incorporation":
            return await self._handle_incorporation(task)
        elif task_type == "compliance_check":
            return await self._check_compliance(task)
        else:
            return {"error": f"Unknown task type: {task_type}"}
            
    async def _handle_incorporation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "jurisdiction": "Brazil",
            "incorporation_guide": {
                "recommended_structure": "Sociedade Limitada (LTDA)",
                "required_documents": [
                    "Articles of Incorporation (Contrato Social)",
                    "CNPJ registration",
                    "State registration (Inscrição Estadual)",
                    "Municipal registration (Inscrição Municipal)"
                ],
                "regulatory_approvals": [
                    "Commercial Registry (Junta Comercial)",
                    "Federal Revenue Service (Receita Federal)",
                    "State tax authority",
                    "Municipal tax authority"
                ],
                "minimum_requirements": {
                    "partners": "Minimum 2 partners",
                    "capital": "No minimum capital requirement",
                    "registered_address": "Required in Brazil"
                },
                "estimated_timeline": "15-30 days",
                "estimated_cost": "R$1,000-3,000"
            }
        }
        
    async def _check_compliance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "jurisdiction": "Brazil",
            "compliance_requirements": {
                "tax_compliance": [
                    "Corporate Income Tax (IRPJ)",
                    "Social Contribution on Net Profit (CSLL)",
                    "PIS/COFINS contributions",
                    "ICMS (state VAT) if applicable"
                ],
                "employment_law": [
                    "CLT (Labor Code) compliance",
                    "FGTS (Employment Guarantee Fund)",
                    "Social security contributions",
                    "Annual labor information (RAIS)"
                ],
                "data_protection": [
                    "LGPD (Lei Geral de Proteção de Dados)",
                    "Privacy policy requirements",
                    "Data processing consent",
                    "Data breach notification"
                ]
            }
        }
        
    def get_compliance_requirements(self, business_type: str) -> List[Dict[str, Any]]:
        return [
            {"requirement": "CNPJ Registration", "urgency": "high", "cost": "R$0"},
            {"requirement": "State Registration", "urgency": "high", "cost": "R$50-200"},
            {"requirement": "Municipal License", "urgency": "high", "cost": "R$100-500"},
            {"requirement": "LGPD Compliance", "urgency": "high", "cost": "R$2,000-10,000"}
        ]

class NigeriaLegalAgent(LegalSubAgent):
    def __init__(self):
        super().__init__("Nigeria", "Nigerian Corporate and Commercial Law")
        
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get("type")
        
        if task_type == "incorporation":
            return await self._handle_incorporation(task)
        elif task_type == "compliance_check":
            return await self._check_compliance(task)
        else:
            return {"error": f"Unknown task type: {task_type}"}
            
    async def _handle_incorporation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "jurisdiction": "Nigeria",
            "incorporation_guide": {
                "recommended_structure": "Private Limited Company",
                "required_documents": [
                    "Memorandum and Articles of Association",
                    "Form CAC 1.1 (Application for registration)",
                    "Statement of share capital",
                    "Particulars of directors and secretary"
                ],
                "regulatory_approvals": [
                    "Corporate Affairs Commission (CAC)",
                    "Federal Inland Revenue Service (FIRS)",
                    "State Internal Revenue Service",
                    "Pension Fund Administrator (PFA)"
                ],
                "minimum_requirements": {
                    "directors": "Minimum 2 directors",
                    "shareholders": "Minimum 2 shareholders",
                    "share_capital": "₦100,000 minimum authorized capital",
                    "registered_office": "Required in Nigeria"
                },
                "estimated_timeline": "2-4 weeks",
                "estimated_cost": "₦50,000-150,000"
            }
        }
        
    async def _check_compliance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "jurisdiction": "Nigeria",
            "compliance_requirements": {
                "corporate_compliance": [
                    "Annual returns filing with CAC",
                    "Board meetings and resolutions",
                    "Statutory audit requirements",
                    "Share transfer documentation"
                ],
                "tax_compliance": [
                    "Companies Income Tax (30%)",
                    "Value Added Tax (7.5%)",
                    "Pay As You Earn (PAYE)",
                    "Withholding Tax obligations"
                ],
                "employment_law": [
                    "Pension Reform Act compliance",
                    "National Housing Fund contributions",
                    "Industrial Training Fund levy",
                    "Nigeria Social Insurance Trust Fund"
                ],
                "data_protection": [
                    "Nigeria Data Protection Regulation (NDPR)",
                    "Data protection impact assessments",
                    "Consent management",
                    "Data breach notifications"
                ]
            }
        }
        
    def get_compliance_requirements(self, business_type: str) -> List[Dict[str, Any]]:
        return [
            {"requirement": "CAC Registration", "urgency": "high", "cost": "₦10,000-50,000"},
            {"requirement": "Tax Identification Number", "urgency": "high", "cost": "₦0"},
            {"requirement": "Business Permit", "urgency": "medium", "cost": "₦25,000-100,000"},
            {"requirement": "NDPR Compliance", "urgency": "high", "cost": "₦200,000-500,000"}
        ]

class LegalAgent(BaseAgent):
    def __init__(self):
        capabilities = [
            AgentCapability(
                name="multi_jurisdiction_compliance",
                description="Handle legal compliance across multiple jurisdictions",
                cost_estimate=25.0,
                confidence_level=0.9,
                requirements=["jurisdiction", "business_type", "legal_task"]
            ),
            AgentCapability(
                name="contract_generation",
                description="Generate legal contracts and agreements",
                cost_estimate=15.0,
                confidence_level=0.85,
                requirements=["contract_type", "jurisdiction", "parties"]
            ),
            AgentCapability(
                name="ip_protection",
                description="Handle intellectual property protection",
                cost_estimate=20.0,
                confidence_level=0.8,
                requirements=["ip_type", "jurisdiction", "asset_details"]
            ),
            AgentCapability(
                name="regulatory_analysis",
                description="Analyze regulatory requirements for business operations",
                cost_estimate=30.0,
                confidence_level=0.85,
                requirements=["industry", "jurisdiction", "business_model"]
            ),
            AgentCapability(
                name="legal_document_review",
                description="Review and analyze legal documents",
                cost_estimate=10.0,
                confidence_level=0.8,
                requirements=["document_type", "jurisdiction"]
            )
        ]
        
        super().__init__("legal_agent", capabilities)
        
        # Initialize sub-agents for different jurisdictions
        self.sub_agents = {
            "USA": USALegalAgent(),
            "India": IndiaLegalAgent(),
            "China": ChinaLegalAgent(),
            "UK": UKLegalAgent(),
            "Brazil": BrazilLegalAgent(),
            "Nigeria": NigeriaLegalAgent()
        }
        
        # Additional jurisdictions for major economies (50M+ population)
        self.supported_jurisdictions = [
            "USA", "India", "China", "Indonesia", "Pakistan", "Brazil", 
            "Nigeria", "Bangladesh", "Russia", "Mexico", "Japan", "Philippines",
            "Ethiopia", "Vietnam", "Egypt", "Turkey", "Iran", "Germany",
            "Thailand", "UK", "France", "Italy", "Tanzania", "South Africa",
            "Myanmar", "Kenya", "South Korea", "Colombia", "Spain", "Uganda",
            "Argentina", "Algeria", "Sudan", "Ukraine", "Iraq", "Afghanistan",
            "Poland", "Canada", "Morocco", "Saudi Arabia", "Uzbekistan",
            "Peru", "Angola", "Malaysia", "Mozambique", "Ghana", "Yemen",
            "Nepal", "Venezuela", "Madagascar", "Cameroon"
        ]
        
    async def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        """Execute legal tasks using appropriate sub-agents"""
        task_type = task.get("type")
        jurisdiction = task.get("jurisdiction", "USA")
        
        try:
            if task_type == "multi_jurisdiction_compliance":
                return await self._handle_multi_jurisdiction_compliance(task)
            elif task_type == "contract_generation":
                return await self._generate_contract(task)
            elif task_type == "ip_protection":
                return await self._handle_ip_protection(task)
            elif task_type == "regulatory_analysis":
                return await self._analyze_regulatory_requirements(task)
            elif task_type == "legal_document_review":
                return await self._review_legal_document(task)
            else:
                # Delegate to appropriate sub-agent
                return await self._delegate_to_sub_agent(task)
                
        except Exception as e:
            logger.error(f"Legal task failed: {e}")
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=[],
                error_message=str(e)
            )
            
    async def _delegate_to_sub_agent(self, task: Dict[str, Any]) -> TaskResult:
        """Delegate task to appropriate jurisdiction sub-agent"""
        jurisdiction = task.get("jurisdiction", "USA")
        
        if jurisdiction not in self.sub_agents:
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=[f"Add support for {jurisdiction} jurisdiction"],
                error_message=f"Jurisdiction {jurisdiction} not supported yet"
            )
            
        # Check approval for legal consultation cost
        estimated_cost = 25.0
        action = {
            "type": "legal_consultation",
            "jurisdiction": jurisdiction,
            "task_type": task.get("type")
        }
        
        if not await self.request_approval(action, estimated_cost):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Wait for founder approval"],
                error_message="Legal consultation not approved"
            )
            
        # Execute task with sub-agent
        sub_agent = self.sub_agents[jurisdiction]
        result = await sub_agent.handle_task(task)
        
        # Save legal analysis
        os.makedirs("legal_data", exist_ok=True)
        analysis_file = f"legal_data/{jurisdiction.lower()}_{task.get('type')}_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        legal_analysis = {
            "jurisdiction": jurisdiction,
            "task_type": task.get("type"),
            "analysis": result,
            "created_at": datetime.utcnow().isoformat(),
            "sub_agent": sub_agent.__class__.__name__
        }
        
        with open(analysis_file, "w") as f:
            json.dump(legal_analysis, f, indent=2)
            
        return TaskResult(
            success=True,
            output=result,
            cost_incurred=estimated_cost,
            evidence=[analysis_file],
            next_steps=[
                "Review legal recommendations",
                "Implement compliance measures",
                "Consult with local legal counsel if needed"
            ]
        )
        
    async def _handle_multi_jurisdiction_compliance(self, task: Dict[str, Any]) -> TaskResult:
        """Handle compliance requirements across multiple jurisdictions"""
        jurisdictions = task.get("jurisdictions", ["USA"])
        business_type = task.get("business_type", "SaaS")
        
        # Check approval for multi-jurisdiction analysis
        estimated_cost = len(jurisdictions) * 15.0
        action = {
            "type": "multi_jurisdiction_analysis",
            "jurisdiction_count": len(jurisdictions),
            "business_type": business_type
        }
        
        if not await self.request_approval(action, estimated_cost):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Wait for founder approval"],
                error_message="Multi-jurisdiction analysis not approved"
            )
            
        compliance_matrix = {}
        
        for jurisdiction in jurisdictions:
            if jurisdiction in self.sub_agents:
                sub_agent = self.sub_agents[jurisdiction]
                requirements = sub_agent.get_compliance_requirements(business_type)
                compliance_matrix[jurisdiction] = requirements
            else:
                compliance_matrix[jurisdiction] = [
                    {"requirement": f"{jurisdiction} legal review needed", "urgency": "high", "cost": "TBD"}
                ]
                
        # Create compliance roadmap
        roadmap = await self._create_compliance_roadmap(compliance_matrix, business_type)
        
        # Save compliance analysis
        os.makedirs("legal_data", exist_ok=True)
        compliance_file = f"legal_data/multi_jurisdiction_compliance_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        compliance_analysis = {
            "business_type": business_type,
            "jurisdictions": jurisdictions,
            "compliance_matrix": compliance_matrix,
            "roadmap": roadmap,
            "created_at": datetime.utcnow().isoformat()
        }
        
        with open(compliance_file, "w") as f:
            json.dump(compliance_analysis, f, indent=2)
            
        return TaskResult(
            success=True,
            output={
                "compliance_matrix": compliance_matrix,
                "roadmap": roadmap,
                "total_jurisdictions": len(jurisdictions),
                "supported_jurisdictions": len([j for j in jurisdictions if j in self.sub_agents])
            },
            cost_incurred=estimated_cost,
            evidence=[compliance_file],
            next_steps=[
                "Prioritize high-urgency requirements",
                "Engage local legal counsel",
                "Implement compliance measures",
                "Set up ongoing monitoring"
            ]
        )
        
    async def _create_compliance_roadmap(self, compliance_matrix: Dict, business_type: str) -> Dict[str, Any]:
        """Create prioritized compliance roadmap"""
        high_priority = []
        medium_priority = []
        low_priority = []
        
        for jurisdiction, requirements in compliance_matrix.items():
            for req in requirements:
                urgency = req.get("urgency", "medium")
                req_with_jurisdiction = {**req, "jurisdiction": jurisdiction}
                
                if urgency == "high":
                    high_priority.append(req_with_jurisdiction)
                elif urgency == "medium":
                    medium_priority.append(req_with_jurisdiction)
                else:
                    low_priority.append(req_with_jurisdiction)
                    
        return {
            "phase_1_immediate": {
                "timeline": "0-30 days",
                "requirements": high_priority,
                "focus": "Critical compliance and business registration"
            },
            "phase_2_short_term": {
                "timeline": "30-90 days", 
                "requirements": medium_priority,
                "focus": "Operational compliance and risk mitigation"
            },
            "phase_3_ongoing": {
                "timeline": "90+ days",
                "requirements": low_priority,
                "focus": "Optimization and advanced compliance"
            }
        }
        
    async def _generate_contract(self, task: Dict[str, Any]) -> TaskResult:
        """Generate legal contracts and agreements"""
        contract_type = task.get("contract_type", "service_agreement")
        jurisdiction = task.get("jurisdiction", "USA")
        parties = task.get("parties", {})
        
        # Check approval for contract generation
        estimated_cost = 15.0
        action = {
            "type": "contract_generation",
            "contract_type": contract_type,
            "jurisdiction": jurisdiction
        }
        
        if not await self.request_approval(action, estimated_cost):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Wait for founder approval"],
                error_message="Contract generation not approved"
            )
            
        # Contract templates by type and jurisdiction
        contract_templates = {
            "service_agreement": {
                "USA": {
                    "template": """
SERVICE AGREEMENT

This Service Agreement ("Agreement") is entered into on [DATE] between:

Client: {client_name}
Address: {client_address}

Service Provider: {provider_name}  
Address: {provider_address}

1. SERVICES
The Service Provider agrees to provide the following services:
{service_description}

2. PAYMENT TERMS
- Total Fee: {total_fee}
- Payment Schedule: {payment_schedule}
- Late Payment: 1.5% per month on overdue amounts

3. INTELLECTUAL PROPERTY
All work product created shall be owned by {ip_owner}.

4. LIMITATION OF LIABILITY
Service Provider's liability shall not exceed the total fees paid under this Agreement.

5. TERMINATION
Either party may terminate with {termination_notice} days written notice.

6. GOVERNING LAW
This Agreement shall be governed by the laws of {governing_state}.

IN WITNESS WHEREOF, the parties have executed this Agreement.

Client: ___________________ Date: ___________
Service Provider: ___________________ Date: ___________
                    """,
                    "required_fields": ["client_name", "client_address", "provider_name", "provider_address", 
                                      "service_description", "total_fee", "payment_schedule", "ip_owner", 
                                      "termination_notice", "governing_state"]
                },
                "UK": {
                    "template": """
SERVICE AGREEMENT

This Agreement is made on [DATE] between:

The Client: {client_name}
Address: {client_address}

The Service Provider: {provider_name}
Address: {provider_address}

1. SERVICES
The Service Provider shall provide: {service_description}

2. FEES AND PAYMENT
- Fee: £{total_fee}
- Payment Terms: {payment_schedule}
- VAT: Added where applicable

3. INTELLECTUAL PROPERTY RIGHTS
All intellectual property created shall vest in {ip_owner}.

4. LIABILITY
Liability is limited to the total fees payable under this Agreement.

5. TERMINATION
{termination_notice} days' notice required for termination.

6. GOVERNING LAW
This Agreement is governed by English law.

Signed:
Client: ___________________ Date: ___________
Service Provider: ___________________ Date: ___________
                    """,
                    "required_fields": ["client_name", "client_address", "provider_name", "provider_address",
                                      "service_description", "total_fee", "payment_schedule", "ip_owner",
                                      "termination_notice"]
                }
            },
            "employment_agreement": {
                "USA": {
                    "template": """
EMPLOYMENT AGREEMENT

This Employment Agreement is between:

Employer: {company_name}
Address: {company_address}

Employee: {employee_name}
Address: {employee_address}

1. POSITION AND DUTIES
Position: {job_title}
Duties: {job_description}

2. COMPENSATION
- Base Salary: ${annual_salary} per year
- Benefits: {benefits_description}

3. AT-WILL EMPLOYMENT
This is at-will employment. Either party may terminate at any time.

4. CONFIDENTIALITY
Employee agrees to maintain confidentiality of proprietary information.

5. INTELLECTUAL PROPERTY
All work product belongs to the Company.

6. GOVERNING LAW
Governed by the laws of {governing_state}.

Employee: ___________________ Date: ___________
Employer: ___________________ Date: ___________
                    """,
                    "required_fields": ["company_name", "company_address", "employee_name", "employee_address",
                                      "job_title", "job_description", "annual_salary", "benefits_description",
                                      "governing_state"]
                }
            },
            "nda": {
                "USA": {
                    "template": """
NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement ("NDA") is between:

Disclosing Party: {disclosing_party}
Receiving Party: {receiving_party}

1. CONFIDENTIAL INFORMATION
Confidential Information includes: {confidential_info_definition}

2. OBLIGATIONS
Receiving Party agrees to:
- Keep information confidential
- Use only for {permitted_purpose}
- Not disclose to third parties

3. TERM
This Agreement remains in effect for {term_years} years.

4. RETURN OF INFORMATION
All materials must be returned upon request.

5. GOVERNING LAW
Governed by {governing_state} law.

Disclosing Party: ___________________ Date: ___________
Receiving Party: ___________________ Date: ___________
                    """,
                    "required_fields": ["disclosing_party", "receiving_party", "confidential_info_definition",
                                      "permitted_purpose", "term_years", "governing_state"]
                }
            }
        }
        
        # Get appropriate template
        template_data = contract_templates.get(contract_type, {}).get(jurisdiction)
        if not template_data:
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=[f"Add {contract_type} template for {jurisdiction}"],
                error_message=f"No template available for {contract_type} in {jurisdiction}"
            )
            
        # Generate contract with provided data
        contract_content = template_data["template"]
        missing_fields = []
        
        for field in template_data["required_fields"]:
            if field in parties:
                contract_content = contract_content.replace(f"{{{field}}}", str(parties[field]))
            else:
                missing_fields.append(field)
                
        # Save generated contract
        os.makedirs("legal_data/contracts", exist_ok=True)
        contract_file = f"legal_data/contracts/{contract_type}_{jurisdiction.lower()}_{datetime.utcnow().strftime('%Y_%m_%d_%H_%M')}.txt"
        
        with open(contract_file, "w") as f:
            f.write(str(contract_content))
            
        contract_analysis = {
            "contract_type": contract_type,
            "jurisdiction": jurisdiction,
            "template_used": f"{contract_type}_{jurisdiction}",
            "missing_fields": missing_fields,
            "generated_at": datetime.utcnow().isoformat(),
            "file_path": contract_file
        }
        
        return TaskResult(
            success=True,
            output={
                "contract_file": contract_file,
                "contract_analysis": contract_analysis,
                "missing_fields": missing_fields,
                "next_steps": ["Review contract", "Fill missing fields", "Get legal review", "Execute contract"]
            },
            cost_incurred=estimated_cost,
            evidence=[contract_file],
            next_steps=[
                "Review generated contract",
                "Complete missing field information" if missing_fields else "Contract ready for review",
                "Consult legal counsel before execution",
                "Execute contract with proper signatures"
            ]
        )
        
    async def _handle_ip_protection(self, task: Dict[str, Any]) -> TaskResult:
        """Handle intellectual property protection tasks"""
        ip_type = task.get("ip_type", "trademark")
        jurisdiction = task.get("jurisdiction", "USA")
        asset_details = task.get("asset_details", {})
        
        # Check approval for IP protection analysis
        estimated_cost = 20.0
        action = {
            "type": "ip_protection_analysis",
            "ip_type": ip_type,
            "jurisdiction": jurisdiction
        }
        
        if not await self.request_approval(action, estimated_cost):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Wait for founder approval"],
                error_message="IP protection analysis not approved"
            )
            
        # Delegate to appropriate sub-agent if available
        if jurisdiction in self.sub_agents:
            sub_agent = self.sub_agents[jurisdiction]
            # Use the sub-agent's handle_task method which supports ip_protection
            try:
                result = await sub_agent.handle_task(task)
            except Exception:
                result = await self._generic_ip_analysis(task)
        else:
            result = await self._generic_ip_analysis(task)
            
        # Save IP analysis
        os.makedirs("legal_data/ip_protection", exist_ok=True)
        ip_file = f"legal_data/ip_protection/{ip_type}_{jurisdiction.lower()}_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        ip_analysis = {
            "ip_type": ip_type,
            "jurisdiction": jurisdiction,
            "asset_details": asset_details,
            "analysis": result,
            "created_at": datetime.utcnow().isoformat()
        }
        
        with open(ip_file, "w") as f:
            json.dump(ip_analysis, f, indent=2)
            
        return TaskResult(
            success=True,
            output=result,
            cost_incurred=estimated_cost,
            evidence=[ip_file],
            next_steps=[
                "Conduct IP search",
                "Prepare filing documents",
                "Submit application",
                "Monitor application status"
            ]
        )
        
    async def _generic_ip_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Generic IP protection analysis for unsupported jurisdictions"""
        ip_type = task.get("ip_type", "trademark")
        jurisdiction = task.get("jurisdiction", "Unknown")
        
        generic_guidance = {
            "trademark": {
                "description": "Protection for brand names, logos, and slogans",
                "typical_cost": "$500-2000",
                "typical_timeline": "6-18 months",
                "requirements": ["Distinctive mark", "Use in commerce", "Proper classification"],
                "next_steps": ["Trademark search", "Application preparation", "Filing", "Examination"]
            },
            "patent": {
                "description": "Protection for inventions and processes",
                "typical_cost": "$5000-15000",
                "typical_timeline": "18-36 months",
                "requirements": ["Novel invention", "Non-obvious", "Useful", "Detailed specification"],
                "next_steps": ["Prior art search", "Patent drafting", "Filing", "Examination"]
            },
            "copyright": {
                "description": "Protection for original creative works",
                "typical_cost": "$50-500",
                "typical_timeline": "3-6 months",
                "requirements": ["Original work", "Fixed in tangible medium"],
                "next_steps": ["Prepare application", "Submit work samples", "Filing", "Registration"]
            },
            "trade_secret": {
                "description": "Protection through confidentiality measures",
                "typical_cost": "$1000-5000 (for policies)",
                "typical_timeline": "Immediate",
                "requirements": ["Economic value", "Secrecy measures", "Reasonable efforts"],
                "next_steps": ["Identify secrets", "Implement policies", "Train employees", "Monitor compliance"]
            }
        }
        
        guidance = generic_guidance.get(ip_type, generic_guidance["trademark"])
        
        return {
            "jurisdiction": jurisdiction,
            "ip_type": ip_type,
            "guidance": guidance,
            "recommendation": f"Consult local IP attorney in {jurisdiction} for specific requirements",
            "international_options": [
                "Madrid Protocol (trademarks)",
                "PCT (patents)",
                "Berne Convention (copyright)"
            ]
        }
        
    async def _analyze_regulatory_requirements(self, task: Dict[str, Any]) -> TaskResult:
        """Analyze regulatory requirements for business operations"""
        industry = task.get("industry", "Technology")
        jurisdiction = task.get("jurisdiction", "USA")
        business_model = task.get("business_model", "SaaS")
        
        # Check approval for regulatory analysis
        estimated_cost = 30.0
        action = {
            "type": "regulatory_analysis",
            "industry": industry,
            "jurisdiction": jurisdiction
        }
        
        if not await self.request_approval(action, estimated_cost):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Wait for founder approval"],
                error_message="Regulatory analysis not approved"
            )
            
        # Industry-specific regulatory frameworks
        regulatory_frameworks = {
            "fintech": {
                "USA": {
                    "primary_regulators": ["SEC", "CFTC", "FinCEN", "State Banking Regulators"],
                    "key_regulations": [
                        "Bank Secrecy Act (BSA)",
                        "Anti-Money Laundering (AML)",
                        "Know Your Customer (KYC)",
                        "Payment Card Industry (PCI DSS)",
                        "State Money Transmitter Laws"
                    ],
                    "licensing_requirements": [
                        "Money Service Business (MSB) registration",
                        "State money transmitter licenses",
                        "NMLS registration"
                    ],
                    "compliance_costs": "$50,000-500,000 annually"
                },
                "UK": {
                    "primary_regulators": ["FCA", "Bank of England", "HM Treasury"],
                    "key_regulations": [
                        "Payment Services Regulations 2017",
                        "Electronic Money Regulations 2011",
                        "Money Laundering Regulations 2017"
                    ],
                    "licensing_requirements": [
                        "FCA authorization",
                        "Payment Institution license",
                        "E-money Institution license"
                    ],
                    "compliance_costs": "£25,000-200,000 annually"
                }
            },
            "healthcare": {
                "USA": {
                    "primary_regulators": ["FDA", "CMS", "HHS"],
                    "key_regulations": [
                        "HIPAA Privacy Rule",
                        "HIPAA Security Rule",
                        "FDA regulations (if medical devices)",
                        "HITECH Act"
                    ],
                    "licensing_requirements": [
                        "State healthcare licenses",
                        "FDA clearance (devices)",
                        "DEA registration (controlled substances)"
                    ],
                    "compliance_costs": "$25,000-250,000 annually"
                }
            },
            "technology": {
                "USA": {
                    "primary_regulators": ["FTC", "State AGs"],
                    "key_regulations": [
                        "CCPA (California)",
                        "COPPA (children's privacy)",
                        "CAN-SPAM Act",
                        "Section 230 (content moderation)"
                    ],
                    "licensing_requirements": [
                        "Business license",
                        "Professional licenses (if applicable)"
                    ],
                    "compliance_costs": "$5,000-50,000 annually"
                },
                "EU": {
                    "primary_regulators": ["Data Protection Authorities", "European Commission"],
                    "key_regulations": [
                        "GDPR",
                        "Digital Services Act",
                        "Digital Markets Act",
                        "ePrivacy Directive"
                    ],
                    "licensing_requirements": [
                        "GDPR compliance certification",
                        "CE marking (if applicable)"
                    ],
                    "compliance_costs": "€10,000-100,000 annually"
                }
            }
        }
        
        # Get regulatory framework
        framework = regulatory_frameworks.get(industry.lower(), {}).get(jurisdiction, {})
        
        if not framework:
            framework = {
                "primary_regulators": ["Local regulatory authorities"],
                "key_regulations": ["Industry-specific regulations", "General business regulations"],
                "licensing_requirements": ["Business registration", "Professional licenses"],
                "compliance_costs": "Varies by jurisdiction and industry",
                "recommendation": f"Consult local regulatory expert for {industry} in {jurisdiction}"
            }
            
        # Create regulatory compliance plan
        compliance_plan = await self._create_regulatory_compliance_plan(framework, business_model)
        
        # Save regulatory analysis
        os.makedirs("legal_data/regulatory", exist_ok=True)
        regulatory_file = f"legal_data/regulatory/{industry.lower()}_{jurisdiction.lower()}_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        regulatory_analysis = {
            "industry": industry,
            "jurisdiction": jurisdiction,
            "business_model": business_model,
            "regulatory_framework": framework,
            "compliance_plan": compliance_plan,
            "created_at": datetime.utcnow().isoformat()
        }
        
        with open(regulatory_file, "w") as f:
            json.dump(regulatory_analysis, f, indent=2)
            
        return TaskResult(
            success=True,
            output={
                "regulatory_framework": framework,
                "compliance_plan": compliance_plan,
                "risk_assessment": "Medium" if framework else "High - Unknown requirements"
            },
            cost_incurred=estimated_cost,
            evidence=[regulatory_file],
            next_steps=[
                "Engage regulatory counsel",
                "Begin compliance implementation",
                "Set up monitoring systems",
                "Schedule regular compliance reviews"
            ]
        )
        
    async def _create_regulatory_compliance_plan(self, framework: Dict[str, Any], business_model: str) -> Dict[str, Any]:
        """Create a regulatory compliance implementation plan"""
        return {
            "phase_1_foundation": {
                "timeline": "0-60 days",
                "tasks": [
                    "Engage regulatory counsel",
                    "Conduct compliance gap analysis",
                    "Develop compliance policies",
                    "Begin licensing applications"
                ],
                "estimated_cost": framework.get("compliance_costs", "TBD")
            },
            "phase_2_implementation": {
                "timeline": "60-180 days",
                "tasks": [
                    "Implement compliance systems",
                    "Train staff on regulations",
                    "Establish monitoring procedures",
                    "Complete licensing process"
                ]
            },
            "phase_3_ongoing": {
                "timeline": "Ongoing",
                "tasks": [
                    "Regular compliance audits",
                    "Regulatory update monitoring",
                    "Staff training updates",
                    "Renewal of licenses"
                ]
            }
        }
        
    async def _review_legal_document(self, task: Dict[str, Any]) -> TaskResult:
        """Review and analyze legal documents"""
        document_type = task.get("document_type", "contract")
        jurisdiction = task.get("jurisdiction", "USA")
        document_content = task.get("document_content", "")
        
        # Check approval for document review
        estimated_cost = 10.0
        action = {
            "type": "document_review",
            "document_type": document_type,
            "jurisdiction": jurisdiction
        }
        
        if not await self.request_approval(action, estimated_cost):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Wait for founder approval"],
                error_message="Document review not approved"
            )
            
        # Document review checklist by type
        review_checklists = {
            "contract": {
                "key_clauses": [
                    "Parties identification",
                    "Scope of work/services",
                    "Payment terms",
                    "Intellectual property rights",
                    "Limitation of liability",
                    "Termination provisions",
                    "Governing law",
                    "Dispute resolution"
                ],
                "red_flags": [
                    "Unlimited liability",
                    "Automatic renewal without notice",
                    "Broad indemnification",
                    "Exclusive dealing requirements",
                    "Unreasonable termination penalties"
                ]
            },
            "privacy_policy": {
                "key_sections": [
                    "Data collection practices",
                    "Use of personal information",
                    "Data sharing/disclosure",
                    "User rights and choices",
                    "Security measures",
                    "Contact information"
                ],
                "compliance_requirements": [
                    "GDPR compliance (if EU users)",
                    "CCPA compliance (if CA users)",
                    "COPPA compliance (if children)",
                    "Clear and conspicuous notice"
                ]
            },
            "terms_of_service": {
                "key_sections": [
                    "Acceptable use policy",
                    "User responsibilities",
                    "Service availability",
                    "Intellectual property rights",
                    "Limitation of liability",
                    "Termination rights"
                ],
                "legal_requirements": [
                    "Clear terms presentation",
                    "Reasonable limitation of liability",
                    "Fair termination provisions",
                    "Compliance with consumer protection laws"
                ]
            }
        }
        
        checklist = review_checklists.get(document_type, review_checklists["contract"])
        
        # Perform basic document analysis
        analysis_results = {
            "document_type": document_type,
            "jurisdiction": jurisdiction,
            "review_checklist": checklist,
            "document_length": len(document_content.split()) if document_content else 0,
            "recommendations": [
                "Ensure all key clauses are present",
                "Review for jurisdiction-specific requirements",
                "Consider legal counsel review",
                "Update based on current regulations"
            ],
            "risk_level": "Medium - Requires legal review"
        }
        
        # Save document review
        os.makedirs("legal_data/document_reviews", exist_ok=True)
        review_file = f"legal_data/document_reviews/{document_type}_{jurisdiction.lower()}_{datetime.utcnow().strftime('%Y_%m_%d_%H_%M')}.json"
        
        document_review = {
            "document_type": document_type,
            "jurisdiction": jurisdiction,
            "analysis": analysis_results,
            "reviewed_at": datetime.utcnow().isoformat()
        }
        
        with open(review_file, "w") as f:
            json.dump(document_review, f, indent=2)
            
        return TaskResult(
            success=True,
            output=analysis_results,
            cost_incurred=estimated_cost,
            evidence=[review_file],
            next_steps=[
                "Address identified issues",
                "Consult legal counsel",
                "Update document as needed",
                "Implement reviewed document"
            ]
        )
        
    async def get_daily_goals(self) -> List[Dict[str, Any]]:
        """Get daily legal compliance goals"""
        return [
            {
                "goal": "Review pending compliance requirements",
                "priority": "high",
                "estimated_time": "30 minutes"
            },
            {
                "goal": "Monitor regulatory updates in key jurisdictions",
                "priority": "medium",
                "estimated_time": "45 minutes"
            },
            {
                "goal": "Update legal document templates",
                "priority": "low",
                "estimated_time": "1 hour"
            },
            {
                "goal": "Prepare legal risk assessment",
                "priority": "medium",
                "estimated_time": "1 hour"
            }
        ]

# Example usage
async def main():
    """Example usage of LegalAgent"""
    agent = LegalAgent()
    await agent.start()
    
    # Test multi-jurisdiction compliance
    task = {
        "type": "multi_jurisdiction_compliance",
        "jurisdictions": ["USA", "India", "UK", "Nigeria"],
        "business_type": "SaaS"
    }
    
    result = await agent.execute_task(task)
    print("Legal compliance result:", json.dumps(result.__dict__, indent=2, default=str))
    
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())