"""
Legal & Compliance Tracker Engine
Comprehensive legal document management, compliance monitoring, and risk assessment
Provides AI-powered legal insights and regulatory compliance tracking
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
import statistics
import uuid

from core.company_blueprint_dataclass import CompanyBlueprint
from core.llm_integration import LLMManager, LLMMessage

logger = logging.getLogger(__name__)

class DocumentType(Enum):
    CONTRACT = "contract"
    AGREEMENT = "agreement"
    POLICY = "policy"
    COMPLIANCE_REPORT = "compliance_report"
    LEGAL_MEMO = "legal_memo"
    REGULATORY_FILING = "regulatory_filing"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    EMPLOYMENT_DOCUMENT = "employment_document"
    PRIVACY_POLICY = "privacy_policy"
    TERMS_OF_SERVICE = "terms_of_service"

class ComplianceStatus(Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PENDING_REVIEW = "pending_review"
    REQUIRES_ACTION = "requires_action"
    EXPIRED = "expired"
    UPCOMING_DEADLINE = "upcoming_deadline"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RegulationType(Enum):
    GDPR = "gdpr"
    CCPA = "ccpa"
    SOX = "sox"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    ISO_27001 = "iso_27001"
    SOC2 = "soc2"
    EMPLOYMENT_LAW = "employment_law"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    SECURITIES = "securities"
    TAX = "tax"
    ENVIRONMENTAL = "environmental"

@dataclass
class LegalDocument:
    """Legal document with compliance tracking"""
    document_id: str
    title: str
    document_type: DocumentType
    description: str
    
    # Document details
    file_path: Optional[str] = None
    version: str = "1.0"
    status: str = "active"  # active, draft, archived, expired
    
    # Parties and ownership
    parties: List[str] = field(default_factory=list)
    owner_department: str = "Legal"
    responsible_person: Optional[str] = None
    
    # Timeline
    effective_date: Optional[str] = None
    expiration_date: Optional[str] = None
    review_date: Optional[str] = None
    last_reviewed: Optional[str] = None
    
    # Compliance and risk
    compliance_requirements: List[str] = field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.MEDIUM
    
    # AI insights
    ai_risk_score: float = 0.0  # 0-10
    ai_compliance_score: float = 0.0  # 0-10
    ai_key_terms: List[str] = field(default_factory=list)
    ai_recommendations: List[str] = field(default_factory=list)
    ai_summary: Optional[str] = None
    
    # Tracking
    access_log: List[Dict[str, Any]] = field(default_factory=list)
    modification_history: List[Dict[str, Any]] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class ComplianceRequirement:
    """Regulatory compliance requirement"""
    requirement_id: str
    title: str
    regulation_type: RegulationType
    description: str
    
    # Compliance details
    mandatory: bool = True
    deadline: Optional[str] = None
    frequency: Optional[str] = None  # annual, quarterly, monthly, ongoing
    
    # Status and tracking
    status: ComplianceStatus = ComplianceStatus.PENDING_REVIEW
    completion_percentage: float = 0.0
    last_assessment: Optional[str] = None
    next_assessment: Optional[str] = None
    
    # Responsibility
    responsible_department: str = "Legal"
    assigned_to: Optional[str] = None
    
    # Documentation
    evidence_documents: List[str] = field(default_factory=list)  # document_ids
    audit_trail: List[Dict[str, Any]] = field(default_factory=list)
    
    # AI insights
    ai_risk_assessment: RiskLevel = RiskLevel.MEDIUM
    ai_compliance_confidence: float = 0.0  # 0-10
    ai_recommendations: List[str] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class LegalRisk:
    """Identified legal risk with mitigation strategies"""
    risk_id: str
    title: str
    description: str
    category: str  # contract, compliance, litigation, ip, employment, etc.
    
    # Risk assessment
    risk_level: RiskLevel = RiskLevel.MEDIUM
    probability: float = 0.5  # 0-1
    impact_score: float = 5.0  # 0-10
    
    # Timeline
    identified_date: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    target_resolution: Optional[str] = None
    
    # Mitigation
    mitigation_strategies: List[str] = field(default_factory=list)
    action_items: List[Dict[str, Any]] = field(default_factory=list)
    responsible_person: Optional[str] = None
    
    # Status tracking
    status: str = "open"  # open, in_progress, mitigated, closed
    resolution_notes: Optional[str] = None
    
    # Related items
    related_documents: List[str] = field(default_factory=list)
    related_requirements: List[str] = field(default_factory=list)
    
    # AI insights
    ai_severity_score: float = 0.0  # 0-10
    ai_mitigation_suggestions: List[str] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class ComplianceAudit:
    """Compliance audit record"""
    audit_id: str
    title: str
    audit_type: str  # internal, external, regulatory
    scope: str
    
    # Timeline
    start_date: str
    end_date: str
    report_date: Optional[str] = None
    
    # Participants
    auditor: str
    auditees: List[str] = field(default_factory=list)
    
    # Results
    findings: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    action_items: List[Dict[str, Any]] = field(default_factory=list)
    
    # Scoring
    overall_score: Optional[float] = None  # 0-10
    compliance_percentage: Optional[float] = None
    
    # Status
    status: str = "planned"  # planned, in_progress, completed, reported
    
    # AI insights
    ai_risk_areas: List[str] = field(default_factory=list)
    ai_priority_actions: List[str] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass
class IntellectualProperty:
    """Intellectual property asset tracking"""
    ip_id: str
    title: str
    ip_type: str  # patent, trademark, copyright, trade_secret
    description: str
    
    # Legal details
    registration_number: Optional[str] = None
    filing_date: Optional[str] = None
    grant_date: Optional[str] = None
    expiration_date: Optional[str] = None
    
    # Ownership
    inventors: List[str] = field(default_factory=list)
    assignee: str = "Company"
    
    # Status and maintenance
    status: str = "active"  # pending, active, expired, abandoned
    maintenance_fees: List[Dict[str, Any]] = field(default_factory=list)
    renewal_dates: List[str] = field(default_factory=list)
    
    # Valuation and strategy
    estimated_value: Optional[float] = None
    strategic_importance: str = "medium"  # low, medium, high, critical
    
    # AI insights
    ai_value_assessment: float = 0.0  # 0-10
    ai_protection_recommendations: List[str] = field(default_factory=list)
    
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class LegalComplianceEngine:
    """
    Comprehensive legal and compliance management system that provides:
    - Legal document management and tracking
    - Regulatory compliance monitoring
    - Risk assessment and mitigation
    - Intellectual property management
    - Audit trail and reporting
    - AI-powered legal insights
    """
    
    def __init__(self):
        self.llm_manager = LLMManager()
        
        # Data storage
        self.legal_documents: Dict[str, LegalDocument] = {}
        self.compliance_requirements: Dict[str, ComplianceRequirement] = {}
        self.legal_risks: Dict[str, LegalRisk] = {}
        self.compliance_audits: Dict[str, ComplianceAudit] = {}
        self.intellectual_property: Dict[str, IntellectualProperty] = {}
        
        # Configuration
        self.compliance_thresholds = {
            "high_risk_score": 7.0,
            "compliance_warning": 30,  # days before deadline
            "review_frequency_days": 90
        }
        
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample legal and compliance data"""
        
        # Sample legal documents
        sample_documents = [
            LegalDocument(
                document_id="doc_001",
                title="Master Service Agreement - CloudTech Solutions",
                document_type=DocumentType.CONTRACT,
                description="Primary service agreement with cloud infrastructure provider",
                parties=["Company", "CloudTech Solutions Inc."],
                effective_date="2025-01-01",
                expiration_date="2026-12-31",
                review_date="2025-07-01",
                compliance_requirements=["SOC2", "ISO 27001", "Data Processing Agreement"],
                risk_level=RiskLevel.HIGH,
                ai_risk_score=7.5,
                ai_compliance_score=8.2,
                ai_key_terms=["Data Processing", "Service Level Agreement", "Liability Limitation", "Termination Clause"],
                ai_recommendations=[
                    "Review data processing terms for GDPR compliance",
                    "Negotiate better SLA terms for critical services",
                    "Add specific security requirements clause"
                ],
                ai_summary="High-value service agreement with comprehensive data processing and security obligations"
            ),
            LegalDocument(
                document_id="doc_002",
                title="Employee Handbook 2025",
                document_type=DocumentType.EMPLOYMENT_DOCUMENT,
                description="Comprehensive employee policies and procedures",
                effective_date="2025-01-01",
                review_date="2025-12-31",
                compliance_requirements=["Employment Law", "Equal Opportunity", "Workplace Safety"],
                risk_level=RiskLevel.MEDIUM,
                ai_risk_score=5.5,
                ai_compliance_score=9.1,
                ai_key_terms=["Equal Opportunity", "Remote Work Policy", "Code of Conduct", "Disciplinary Procedures"],
                ai_recommendations=[
                    "Update remote work policies for hybrid model",
                    "Add AI/ML ethics guidelines",
                    "Review disciplinary procedures for compliance"
                ],
                ai_summary="Current employee handbook with strong compliance foundation, needs minor updates for modern workplace"
            ),
            LegalDocument(
                document_id="doc_003",
                title="Privacy Policy v3.2",
                document_type=DocumentType.PRIVACY_POLICY,
                description="Customer data privacy policy for web platform",
                effective_date="2025-09-01",
                review_date="2026-03-01",
                compliance_requirements=["GDPR", "CCPA", "Privacy Shield"],
                risk_level=RiskLevel.HIGH,
                ai_risk_score=8.0,
                ai_compliance_score=7.8,
                ai_key_terms=["Data Collection", "Cookie Policy", "User Rights", "Data Retention"],
                ai_recommendations=[
                    "Clarify AI/ML data usage policies",
                    "Add specific cookie consent mechanisms",
                    "Update data retention schedules"
                ],
                ai_summary="Privacy policy covering major regulations but requires updates for AI data usage transparency"
            ),
            LegalDocument(
                document_id="doc_004",
                title="Software License Agreement - Analytics Platform",
                document_type=DocumentType.AGREEMENT,
                description="End-user license agreement for analytics software",
                parties=["Company", "End Users"],
                effective_date="2025-06-01",
                compliance_requirements=["Software Licensing", "Export Control"],
                risk_level=RiskLevel.MEDIUM,
                ai_risk_score=6.0,
                ai_compliance_score=8.5,
                ai_key_terms=["Usage Rights", "Restrictions", "Intellectual Property", "Warranty Disclaimer"],
                ai_recommendations=[
                    "Add AI model usage restrictions",
                    "Clarify data ownership rights",
                    "Update export control compliance"
                ],
                ai_summary="Standard software license with good IP protection, needs AI-specific terms"
            )
        ]
        
        for doc in sample_documents:
            self.legal_documents[doc.document_id] = doc
        
        # Sample compliance requirements
        sample_requirements = [
            ComplianceRequirement(
                requirement_id="req_001",
                title="GDPR Data Protection Impact Assessment",
                regulation_type=RegulationType.GDPR,
                description="Annual assessment of data processing activities for privacy impact",
                mandatory=True,
                deadline="2025-12-31",
                frequency="annual",
                status=ComplianceStatus.PENDING_REVIEW,
                completion_percentage=65.0,
                responsible_department="Legal",
                assigned_to="Privacy Officer",
                evidence_documents=["doc_003"],
                ai_risk_assessment=RiskLevel.HIGH,
                ai_compliance_confidence=7.2,
                ai_recommendations=[
                    "Complete data mapping exercise",
                    "Update privacy impact assessments",
                    "Implement automated consent management"
                ]
            ),
            ComplianceRequirement(
                requirement_id="req_002",
                title="SOC 2 Type II Audit Preparation",
                regulation_type=RegulationType.SOC2,
                description="Prepare for annual SOC 2 Type II security audit",
                mandatory=True,
                deadline="2025-11-15",
                frequency="annual",
                status=ComplianceStatus.REQUIRES_ACTION,
                completion_percentage=40.0,
                responsible_department="Security",
                assigned_to="CISO",
                evidence_documents=["doc_001"],
                ai_risk_assessment=RiskLevel.HIGH,
                ai_compliance_confidence=6.8,
                ai_recommendations=[
                    "Implement continuous monitoring controls",
                    "Document security procedures",
                    "Conduct pre-audit assessment"
                ]
            ),
            ComplianceRequirement(
                requirement_id="req_003",
                title="Employment Law Compliance Review",
                regulation_type=RegulationType.EMPLOYMENT_LAW,
                description="Quarterly review of employment practices and policies",
                mandatory=True,
                deadline="2025-10-31",
                frequency="quarterly",
                status=ComplianceStatus.COMPLIANT,
                completion_percentage=95.0,
                responsible_department="HR",
                assigned_to="HR Director",
                evidence_documents=["doc_002"],
                ai_risk_assessment=RiskLevel.LOW,
                ai_compliance_confidence=9.1,
                ai_recommendations=[
                    "Update remote work guidelines",
                    "Review compensation equity analysis",
                    "Enhance diversity reporting"
                ]
            ),
            ComplianceRequirement(
                requirement_id="req_004",
                title="Intellectual Property Audit",
                regulation_type=RegulationType.INTELLECTUAL_PROPERTY,
                description="Semi-annual review of IP portfolio and protection strategies",
                mandatory=False,
                deadline="2025-12-15",
                frequency="semi-annual",
                status=ComplianceStatus.UPCOMING_DEADLINE,
                completion_percentage=20.0,
                responsible_department="Legal",
                assigned_to="IP Counsel",
                ai_risk_assessment=RiskLevel.MEDIUM,
                ai_compliance_confidence=5.5,
                ai_recommendations=[
                    "Conduct patent landscape analysis",
                    "Review trademark registrations",
                    "Assess trade secret protection"
                ]
            )
        ]
        
        for req in sample_requirements:
            self.compliance_requirements[req.requirement_id] = req
        
        # Sample legal risks
        sample_risks = [
            LegalRisk(
                risk_id="risk_001",
                title="Data Breach Liability Exposure",
                description="Potential liability from customer data breach due to insufficient security controls",
                category="data_privacy",
                risk_level=RiskLevel.HIGH,
                probability=0.3,
                impact_score=9.0,
                target_resolution="2025-11-30",
                mitigation_strategies=[
                    "Implement advanced threat detection",
                    "Enhance employee security training",
                    "Review cyber insurance coverage",
                    "Conduct penetration testing"
                ],
                action_items=[
                    {"task": "Deploy SIEM solution", "owner": "Security Team", "due": "2025-10-15"},
                    {"task": "Update incident response plan", "owner": "Legal", "due": "2025-10-30"}
                ],
                responsible_person="CISO",
                status="in_progress",
                related_documents=["doc_003"],
                related_requirements=["req_001", "req_002"],
                ai_severity_score=8.7,
                ai_mitigation_suggestions=[
                    "Implement zero-trust architecture",
                    "Add real-time monitoring alerts",
                    "Create data classification system"
                ]
            ),
            LegalRisk(
                risk_id="risk_002",
                title="Contract Termination Risk - Key Vendor",
                description="Risk of service disruption if key cloud vendor terminates contract",
                category="contract",
                risk_level=RiskLevel.MEDIUM,
                probability=0.2,
                impact_score=7.5,
                target_resolution="2025-12-31",
                mitigation_strategies=[
                    "Negotiate longer-term contract",
                    "Identify alternative vendors",
                    "Implement multi-cloud strategy",
                    "Create contingency plans"
                ],
                action_items=[
                    {"task": "Renegotiate contract terms", "owner": "Procurement", "due": "2025-11-15"},
                    {"task": "Evaluate backup vendors", "owner": "Engineering", "due": "2025-10-31"}
                ],
                responsible_person="COO",
                status="open",
                related_documents=["doc_001"],
                ai_severity_score=6.8,
                ai_mitigation_suggestions=[
                    "Add service level guarantees",
                    "Negotiate termination notice period",
                    "Include data portability clauses"
                ]
            ),
            LegalRisk(
                risk_id="risk_003",
                title="Intellectual Property Infringement Claims",
                description="Potential patent infringement claims related to AI/ML algorithms",
                category="intellectual_property",
                risk_level=RiskLevel.MEDIUM,
                probability=0.4,
                impact_score=6.0,
                target_resolution="2025-11-01",
                mitigation_strategies=[
                    "Conduct freedom-to-operate analysis",
                    "File defensive patents",
                    "Review third-party licenses",
                    "Implement IP monitoring"
                ],
                action_items=[
                    {"task": "Patent landscape analysis", "owner": "IP Counsel", "due": "2025-10-20"},
                    {"task": "Review AI model licenses", "owner": "Engineering", "due": "2025-10-15"}
                ],
                responsible_person="CTO",
                status="open",
                ai_severity_score=5.8,
                ai_mitigation_suggestions=[
                    "Create IP clearance process",
                    "Add indemnification clauses",
                    "Monitor competitor patents"
                ]
            )
        ]
        
        for risk in sample_risks:
            self.legal_risks[risk.risk_id] = risk
        
        # Sample compliance audits
        sample_audits = [
            ComplianceAudit(
                audit_id="audit_001",
                title="Q3 2025 SOC 2 Readiness Assessment",
                audit_type="internal",
                scope="Security controls and data processing procedures",
                start_date="2025-09-01",
                end_date="2025-09-15",
                report_date="2025-09-20",
                auditor="Internal Audit Team",
                auditees=["Security Team", "Engineering Team", "Operations Team"],
                findings=[
                    {"category": "Access Controls", "severity": "medium", "description": "Some admin accounts lack MFA"},
                    {"category": "Data Encryption", "severity": "low", "description": "Minor gaps in encryption at rest"},
                    {"category": "Incident Response", "severity": "high", "description": "Response procedures need updating"}
                ],
                recommendations=[
                    "Implement mandatory MFA for all admin accounts",
                    "Complete encryption implementation for all data stores",
                    "Update and test incident response procedures"
                ],
                action_items=[
                    {"task": "Deploy MFA solution", "owner": "Security", "due": "2025-10-15", "status": "in_progress"},
                    {"task": "Encrypt remaining databases", "owner": "Engineering", "due": "2025-10-30", "status": "planned"}
                ],
                overall_score=7.2,
                compliance_percentage=85.0,
                status="completed",
                ai_risk_areas=["Access Management", "Incident Response", "Data Protection"],
                ai_priority_actions=[
                    "Immediate MFA deployment for critical systems",
                    "Incident response drill within 30 days",
                    "Quarterly access review implementation"
                ]
            ),
            ComplianceAudit(
                audit_id="audit_002",
                title="GDPR Compliance Assessment 2025",
                audit_type="external",
                scope="Data protection and privacy compliance across all systems",
                start_date="2025-10-15",
                end_date="2025-10-25",
                auditor="Privacy Consulting Firm",
                auditees=["Legal Team", "Engineering Team", "Marketing Team"],
                status="planned",
                ai_risk_areas=["Data Mapping", "Consent Management", "Data Subject Rights"],
                ai_priority_actions=[
                    "Complete comprehensive data inventory",
                    "Implement automated consent tracking",
                    "Test data subject request procedures"
                ]
            )
        ]
        
        for audit in sample_audits:
            self.compliance_audits[audit.audit_id] = audit
        
        # Sample intellectual property
        sample_ip = [
            IntellectualProperty(
                ip_id="ip_001",
                title="AI-Powered Analytics Engine",
                ip_type="patent",
                description="Machine learning algorithm for predictive business analytics",
                filing_date="2024-03-15",
                status="pending",
                inventors=["Dr. Sarah Chen", "Alex Rodriguez"],
                estimated_value=500000.0,
                strategic_importance="critical",
                ai_value_assessment=8.5,
                ai_protection_recommendations=[
                    "File continuation applications in key markets",
                    "Consider trade secret protection for implementation details",
                    "Monitor competitor patent filings"
                ]
            ),
            IntellectualProperty(
                ip_id="ip_002",
                title="DreamTeam™ Brand Trademark",
                ip_type="trademark",
                description="Company brand name and logo trademark",
                registration_number="TM2024-001234",
                filing_date="2024-01-10",
                grant_date="2024-08-15",
                expiration_date="2034-08-15",
                status="active",
                renewal_dates=["2029-08-15", "2034-08-15"],
                estimated_value=250000.0,
                strategic_importance="high",
                ai_value_assessment=7.8,
                ai_protection_recommendations=[
                    "Monitor for trademark infringement",
                    "File international trademark applications",
                    "Maintain consistent brand usage"
                ]
            ),
            IntellectualProperty(
                ip_id="ip_003",
                title="Customer Onboarding Process Documentation",
                ip_type="trade_secret",
                description="Proprietary customer onboarding methodology and best practices",
                status="active",
                estimated_value=150000.0,
                strategic_importance="medium",
                ai_value_assessment=6.5,
                ai_protection_recommendations=[
                    "Implement stronger confidentiality agreements",
                    "Limit access to need-to-know basis",
                    "Regular training on trade secret protection"
                ]
            )
        ]
        
        for ip in sample_ip:
            self.intellectual_property[ip.ip_id] = ip
    
    async def add_legal_document(self, document_data: Dict[str, Any]) -> LegalDocument:
        """Add a new legal document to the system"""
        
        try:
            logger.info(f"Adding legal document: {document_data.get('title')}")
            
            document = LegalDocument(
                document_id=f"doc_{uuid.uuid4().hex[:8]}",
                title=document_data["title"],
                document_type=DocumentType(document_data["document_type"]),
                description=document_data["description"],
                file_path=document_data.get("file_path"),
                parties=document_data.get("parties", []),
                effective_date=document_data.get("effective_date"),
                expiration_date=document_data.get("expiration_date"),
                compliance_requirements=document_data.get("compliance_requirements", []),
                risk_level=RiskLevel(document_data.get("risk_level", "medium"))
            )
            
            # Generate AI insights
            await self._generate_document_ai_insights(document)
            
            # Store document
            self.legal_documents[document.document_id] = document
            
            logger.info(f"Legal document added: {document.document_id}")
            return document
            
        except Exception as e:
            logger.error(f"Failed to add legal document: {e}")
            raise
    
    async def _generate_document_ai_insights(self, document: LegalDocument):
        """Generate AI insights for a legal document"""
        
        # Risk scoring based on document type and characteristics
        risk_factors = {
            DocumentType.CONTRACT: 7.0,
            DocumentType.AGREEMENT: 6.5,
            DocumentType.PRIVACY_POLICY: 8.0,
            DocumentType.EMPLOYMENT_DOCUMENT: 5.5,
            DocumentType.REGULATORY_FILING: 7.5,
            DocumentType.INTELLECTUAL_PROPERTY: 6.0
        }
        
        base_risk = risk_factors.get(document.document_type, 5.0)
        
        # Adjust risk based on expiration and review dates
        if document.expiration_date:
            exp_date = datetime.fromisoformat(document.expiration_date.replace('Z', '+00:00'))
            days_to_expiry = (exp_date - datetime.now(timezone.utc)).days
            
            if days_to_expiry < 30:
                base_risk += 2.0
            elif days_to_expiry < 90:
                base_risk += 1.0
        
        document.ai_risk_score = min(base_risk, 10.0)
        
        # Compliance scoring
        compliance_score = 8.0  # Base compliance score
        
        if not document.review_date:
            compliance_score -= 1.0
        
        if not document.compliance_requirements:
            compliance_score -= 1.5
        
        document.ai_compliance_score = max(compliance_score, 0.0)
        
        # Generate key terms based on document type
        key_terms_map = {
            DocumentType.CONTRACT: ["Service Level Agreement", "Payment Terms", "Termination Clause", "Liability"],
            DocumentType.PRIVACY_POLICY: ["Data Collection", "User Rights", "Cookie Policy", "Data Retention"],
            DocumentType.EMPLOYMENT_DOCUMENT: ["Equal Opportunity", "Code of Conduct", "Compensation", "Benefits"],
            DocumentType.INTELLECTUAL_PROPERTY: ["Usage Rights", "Licensing", "Royalties", "Infringement"]
        }
        
        document.ai_key_terms = key_terms_map.get(document.document_type, ["Terms", "Conditions", "Rights", "Obligations"])
        
        # Generate recommendations
        recommendations = []
        
        if document.ai_risk_score > 7.0:
            recommendations.append("High-risk document - schedule immediate legal review")
        
        if not document.review_date:
            recommendations.append("Set regular review schedule for this document")
        
        if document.expiration_date:
            exp_date = datetime.fromisoformat(document.expiration_date.replace('Z', '+00:00'))
            days_to_expiry = (exp_date - datetime.now(timezone.utc)).days
            
            if days_to_expiry < 90:
                recommendations.append(f"Document expires in {days_to_expiry} days - plan renewal")
        
        document.ai_recommendations = recommendations
        
        # Generate summary
        document.ai_summary = f"{document.document_type.value.title()} document with {document.risk_level.value} risk level requiring {len(document.compliance_requirements)} compliance considerations"
    
    async def assess_compliance_status(self, requirement_id: str) -> Dict[str, Any]:
        """Assess current compliance status for a requirement"""
        
        try:
            if requirement_id not in self.compliance_requirements:
                raise ValueError(f"Compliance requirement {requirement_id} not found")
            
            requirement = self.compliance_requirements[requirement_id]
            current_time = datetime.now(timezone.utc)
            
            assessment = {
                "requirement_id": requirement_id,
                "title": requirement.title,
                "current_status": requirement.status.value,
                "completion_percentage": requirement.completion_percentage,
                "risk_level": requirement.ai_risk_assessment.value,
                "compliance_confidence": requirement.ai_compliance_confidence,
                "days_to_deadline": None,
                "is_overdue": False,
                "recommendations": requirement.ai_recommendations,
                "next_actions": []
            }
            
            # Calculate days to deadline
            if requirement.deadline:
                deadline = datetime.fromisoformat(requirement.deadline.replace('Z', '+00:00'))
                days_to_deadline = (deadline - current_time).days
                assessment["days_to_deadline"] = days_to_deadline
                assessment["is_overdue"] = days_to_deadline < 0
                
                # Generate time-based recommendations
                if days_to_deadline < 0:
                    assessment["next_actions"].append("URGENT: Requirement is overdue - immediate action required")
                elif days_to_deadline <= 7:
                    assessment["next_actions"].append("Critical: Less than 1 week to deadline")
                elif days_to_deadline <= 30:
                    assessment["next_actions"].append("Important: Less than 1 month to deadline")
            
            # Status-based recommendations
            if requirement.status == ComplianceStatus.NON_COMPLIANT:
                assessment["next_actions"].append("Develop immediate remediation plan")
            elif requirement.status == ComplianceStatus.REQUIRES_ACTION:
                assessment["next_actions"].append("Complete outstanding action items")
            elif requirement.completion_percentage < 50:
                assessment["next_actions"].append("Accelerate completion activities")
            
            return assessment
            
        except Exception as e:
            logger.error(f"Failed to assess compliance status: {e}")
            raise
    
    async def identify_legal_risks(self, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Identify potential legal risks based on current state"""
        
        try:
            current_time = datetime.now(timezone.utc)
            identified_risks = []
            
            # Check for expiring documents
            for doc in self.legal_documents.values():
                if doc.expiration_date:
                    exp_date = datetime.fromisoformat(doc.expiration_date.replace('Z', '+00:00'))
                    days_to_expiry = (exp_date - current_time).days
                    
                    if days_to_expiry <= 30:
                        identified_risks.append({
                            "type": "document_expiration",
                            "severity": "high" if days_to_expiry <= 7 else "medium",
                            "title": f"Document Expiring: {doc.title}",
                            "description": f"Legal document expires in {days_to_expiry} days",
                            "impact": "Service disruption or compliance violation",
                            "recommendation": "Initiate renewal process immediately",
                            "related_document": doc.document_id
                        })
            
            # Check for overdue compliance requirements
            for req in self.compliance_requirements.values():
                if req.deadline:
                    deadline = datetime.fromisoformat(req.deadline.replace('Z', '+00:00'))
                    if deadline < current_time and req.status != ComplianceStatus.COMPLIANT:
                        identified_risks.append({
                            "type": "compliance_overdue",
                            "severity": "critical",
                            "title": f"Overdue Compliance: {req.title}",
                            "description": f"Compliance requirement is overdue by {(current_time - deadline).days} days",
                            "impact": "Regulatory penalties and legal exposure",
                            "recommendation": "Immediate compliance action required",
                            "related_requirement": req.requirement_id
                        })
            
            # Check for high-risk documents without recent review
            for doc in self.legal_documents.values():
                if doc.ai_risk_score > 7.0:
                    if not doc.last_reviewed:
                        identified_risks.append({
                            "type": "unreviewed_high_risk",
                            "severity": "medium",
                            "title": f"High-Risk Document Needs Review: {doc.title}",
                            "description": "High-risk document has not been recently reviewed",
                            "impact": "Potential legal exposure from outdated terms",
                            "recommendation": "Schedule legal review within 30 days",
                            "related_document": doc.document_id
                        })
            
            # Check for IP maintenance deadlines
            for ip in self.intellectual_property.values():
                if ip.renewal_dates:
                    for renewal_date in ip.renewal_dates:
                        renewal = datetime.fromisoformat(renewal_date.replace('Z', '+00:00'))
                        days_to_renewal = (renewal - current_time).days
                        
                        if 0 <= days_to_renewal <= 90:
                            identified_risks.append({
                                "type": "ip_renewal",
                                "severity": "medium",
                                "title": f"IP Renewal Due: {ip.title}",
                                "description": f"Intellectual property renewal due in {days_to_renewal} days",
                                "impact": "Loss of IP protection rights",
                                "recommendation": "Prepare renewal documentation and fees",
                                "related_ip": ip.ip_id
                            })
            
            # Sort by severity
            severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            identified_risks.sort(key=lambda x: severity_order.get(x["severity"], 3))
            
            return identified_risks
            
        except Exception as e:
            logger.error(f"Failed to identify legal risks: {e}")
            raise
    
    async def generate_compliance_report(self, report_type: str = "comprehensive") -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        
        try:
            current_time = datetime.now(timezone.utc)
            
            # Overall compliance metrics
            total_requirements = len(self.compliance_requirements)
            compliant_count = len([req for req in self.compliance_requirements.values() if req.status == ComplianceStatus.COMPLIANT])
            overdue_count = len([
                req for req in self.compliance_requirements.values()
                if req.deadline and datetime.fromisoformat(req.deadline.replace('Z', '+00:00')) < current_time
                and req.status != ComplianceStatus.COMPLIANT
            ])
            
            compliance_percentage = (compliant_count / max(total_requirements, 1)) * 100
            
            # Risk assessment
            total_risks = len(self.legal_risks)
            high_risks = len([risk for risk in self.legal_risks.values() if risk.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]])
            open_risks = len([risk for risk in self.legal_risks.values() if risk.status == "open"])
            
            # Document status
            total_documents = len(self.legal_documents)
            expiring_documents = len([
                doc for doc in self.legal_documents.values()
                if doc.expiration_date and (
                    datetime.fromisoformat(doc.expiration_date.replace('Z', '+00:00')) - current_time
                ).days <= 90
            ])
            
            # IP portfolio
            total_ip = len(self.intellectual_property)
            active_ip = len([ip for ip in self.intellectual_property.values() if ip.status == "active"])
            
            # Compliance by regulation type
            regulation_compliance = {}
            for reg_type in RegulationType:
                reqs = [req for req in self.compliance_requirements.values() if req.regulation_type == reg_type]
                if reqs:
                    compliant_reqs = [req for req in reqs if req.status == ComplianceStatus.COMPLIANT]
                    regulation_compliance[reg_type.value] = {
                        "total": len(reqs),
                        "compliant": len(compliant_reqs),
                        "percentage": (len(compliant_reqs) / len(reqs)) * 100
                    }
            
            # Recent audit findings
            recent_audits = [
                audit for audit in self.compliance_audits.values()
                if audit.status == "completed" and (
                    current_time - datetime.fromisoformat(audit.end_date.replace('Z', '+00:00'))
                ).days <= 90
            ]
            
            # Upcoming deadlines
            upcoming_deadlines = []
            for req in self.compliance_requirements.values():
                if req.deadline:
                    deadline = datetime.fromisoformat(req.deadline.replace('Z', '+00:00'))
                    days_to_deadline = (deadline - current_time).days
                    
                    if 0 <= days_to_deadline <= 90:
                        upcoming_deadlines.append({
                            "requirement_id": req.requirement_id,
                            "title": req.title,
                            "deadline": req.deadline,
                            "days_remaining": days_to_deadline,
                            "status": req.status.value,
                            "completion": req.completion_percentage
                        })
            
            upcoming_deadlines.sort(key=lambda x: x["days_remaining"])
            
            report = {
                "report_metadata": {
                    "generated_at": current_time.isoformat(),
                    "report_type": report_type,
                    "period": "Current Status"
                },
                "executive_summary": {
                    "overall_compliance_score": round(compliance_percentage, 1),
                    "total_requirements": total_requirements,
                    "compliant_requirements": compliant_count,
                    "overdue_requirements": overdue_count,
                    "high_risk_items": high_risks,
                    "key_concerns": []
                },
                "compliance_metrics": {
                    "by_regulation": regulation_compliance,
                    "by_status": {
                        status.value: len([req for req in self.compliance_requirements.values() if req.status == status])
                        for status in ComplianceStatus
                    },
                    "completion_rates": {
                        "above_90": len([req for req in self.compliance_requirements.values() if req.completion_percentage >= 90]),
                        "50_to_90": len([req for req in self.compliance_requirements.values() if 50 <= req.completion_percentage < 90]),
                        "below_50": len([req for req in self.compliance_requirements.values() if req.completion_percentage < 50])
                    }
                },
                "risk_assessment": {
                    "total_risks": total_risks,
                    "high_priority_risks": high_risks,
                    "open_risks": open_risks,
                    "risk_by_category": {},
                    "mitigation_progress": round(statistics.mean([
                        100 if risk.status in ["mitigated", "closed"] else 50 if risk.status == "in_progress" else 0
                        for risk in self.legal_risks.values()
                    ]), 1) if self.legal_risks else 0
                },
                "document_management": {
                    "total_documents": total_documents,
                    "expiring_soon": expiring_documents,
                    "high_risk_documents": len([doc for doc in self.legal_documents.values() if doc.ai_risk_score > 7.0]),
                    "needs_review": len([doc for doc in self.legal_documents.values() if not doc.last_reviewed])
                },
                "intellectual_property": {
                    "total_assets": total_ip,
                    "active_assets": active_ip,
                    "estimated_value": sum(ip.estimated_value or 0 for ip in self.intellectual_property.values()),
                    "renewal_alerts": len([
                        ip for ip in self.intellectual_property.values()
                        if ip.renewal_dates and any(
                            0 <= (datetime.fromisoformat(date.replace('Z', '+00:00')) - current_time).days <= 90
                            for date in ip.renewal_dates
                        )
                    ])
                },
                "upcoming_deadlines": upcoming_deadlines[:10],
                "recent_audit_summary": [
                    {
                        "audit_id": audit.audit_id,
                        "title": audit.title,
                        "completion_date": audit.end_date,
                        "overall_score": audit.overall_score,
                        "findings_count": len(audit.findings),
                        "high_severity_findings": len([f for f in audit.findings if f.get("severity") == "high"])
                    }
                    for audit in recent_audits
                ],
                "recommendations": await self._generate_compliance_recommendations()
            }
            
            # Add key concerns to executive summary
            if overdue_count > 0:
                report["executive_summary"]["key_concerns"].append(f"{overdue_count} overdue compliance requirements")
            
            if high_risks > 0:
                report["executive_summary"]["key_concerns"].append(f"{high_risks} high-priority legal risks")
            
            if expiring_documents > 0:
                report["executive_summary"]["key_concerns"].append(f"{expiring_documents} documents expiring within 90 days")
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate compliance report: {e}")
            raise
    
    async def _generate_compliance_recommendations(self) -> List[str]:
        """Generate AI-powered compliance recommendations"""
        
        recommendations = []
        current_time = datetime.now(timezone.utc)
        
        # Check overdue items
        overdue_requirements = [
            req for req in self.compliance_requirements.values()
            if req.deadline and datetime.fromisoformat(req.deadline.replace('Z', '+00:00')) < current_time
            and req.status != ComplianceStatus.COMPLIANT
        ]
        
        if overdue_requirements:
            recommendations.append(f"🚨 Address {len(overdue_requirements)} overdue compliance requirements immediately")
        
        # Check high-risk items
        high_risk_count = len([risk for risk in self.legal_risks.values() if risk.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]])
        
        if high_risk_count > 0:
            recommendations.append(f"⚠️ Prioritize mitigation of {high_risk_count} high-risk legal issues")
        
        # Check document reviews
        unreviewed_docs = [doc for doc in self.legal_documents.values() if not doc.last_reviewed and doc.ai_risk_score > 6.0]
        
        if unreviewed_docs:
            recommendations.append(f"📋 Schedule legal review for {len(unreviewed_docs)} high-risk documents")
        
        # Check IP renewals
        upcoming_renewals = []
        for ip in self.intellectual_property.values():
            if ip.renewal_dates:
                for renewal_date in ip.renewal_dates:
                    renewal = datetime.fromisoformat(renewal_date.replace('Z', '+00:00'))
                    if 0 <= (renewal - current_time).days <= 90:
                        upcoming_renewals.append(ip)
                        break
        
        if upcoming_renewals:
            recommendations.append(f"🔄 Prepare for {len(upcoming_renewals)} IP renewals in next 90 days")
        
        # General recommendations
        compliance_rate = len([req for req in self.compliance_requirements.values() if req.status == ComplianceStatus.COMPLIANT]) / max(len(self.compliance_requirements), 1)
        
        if compliance_rate < 0.8:
            recommendations.append("📈 Implement systematic compliance monitoring to improve overall compliance rate")
        
        if not recommendations:
            recommendations = [
                "✅ Compliance status is good - maintain current monitoring practices",
                "🔍 Consider implementing automated compliance tracking",
                "📊 Schedule quarterly compliance review meetings"
            ]
        
        return recommendations
    
    async def get_legal_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive legal and compliance dashboard data"""
        
        try:
            current_time = datetime.now(timezone.utc)
            
            # Calculate key metrics
            total_documents = len(self.legal_documents)
            total_requirements = len(self.compliance_requirements)
            total_risks = len(self.legal_risks)
            total_ip = len(self.intellectual_property)
            
            # Compliance metrics
            compliant_count = len([req for req in self.compliance_requirements.values() if req.status == ComplianceStatus.COMPLIANT])
            compliance_percentage = (compliant_count / max(total_requirements, 1)) * 100
            
            # Risk metrics
            high_risks = len([risk for risk in self.legal_risks.values() if risk.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]])
            open_risks = len([risk for risk in self.legal_risks.values() if risk.status == "open"])
            
            # Document alerts
            expiring_docs = len([
                doc for doc in self.legal_documents.values()
                if doc.expiration_date and (
                    datetime.fromisoformat(doc.expiration_date.replace('Z', '+00:00')) - current_time
                ).days <= 30
            ])
            
            # IP metrics
            active_ip = len([ip for ip in self.intellectual_property.values() if ip.status == "active"])
            ip_value = sum(ip.estimated_value or 0 for ip in self.intellectual_property.values())
            
            # Recent activity
            recent_documents = sorted(
                self.legal_documents.values(),
                key=lambda x: x.updated_at,
                reverse=True
            )[:5]
            
            recent_risks = sorted(
                [risk for risk in self.legal_risks.values() if risk.status in ["open", "in_progress"]],
                key=lambda x: x.ai_severity_score,
                reverse=True
            )[:5]
            
            # Upcoming deadlines
            upcoming_deadlines = []
            for req in self.compliance_requirements.values():
                if req.deadline:
                    deadline = datetime.fromisoformat(req.deadline.replace('Z', '+00:00'))
                    days_to_deadline = (deadline - current_time).days
                    
                    if 0 <= days_to_deadline <= 90:
                        upcoming_deadlines.append({
                            "type": "compliance",
                            "title": req.title,
                            "deadline": req.deadline,
                            "days_remaining": days_to_deadline,
                            "status": req.status.value,
                            "priority": "high" if days_to_deadline <= 7 else "medium" if days_to_deadline <= 30 else "low"
                        })
            
            for doc in self.legal_documents.values():
                if doc.expiration_date:
                    exp_date = datetime.fromisoformat(doc.expiration_date.replace('Z', '+00:00'))
                    days_to_expiry = (exp_date - current_time).days
                    
                    if 0 <= days_to_expiry <= 90:
                        upcoming_deadlines.append({
                            "type": "document",
                            "title": f"Document Expiry: {doc.title}",
                            "deadline": doc.expiration_date,
                            "days_remaining": days_to_expiry,
                            "status": "active",
                            "priority": "high" if days_to_expiry <= 7 else "medium" if days_to_expiry <= 30 else "low"
                        })
            
            upcoming_deadlines.sort(key=lambda x: x["days_remaining"])
            
            dashboard_data = {
                "overview_metrics": {
                    "total_documents": total_documents,
                    "compliance_percentage": round(compliance_percentage, 1),
                    "high_risk_items": high_risks,
                    "ip_portfolio_value": ip_value,
                    "expiring_documents": expiring_docs
                },
                "compliance_status": {
                    "total_requirements": total_requirements,
                    "compliant": compliant_count,
                    "pending": len([req for req in self.compliance_requirements.values() if req.status == ComplianceStatus.PENDING_REVIEW]),
                    "requires_action": len([req for req in self.compliance_requirements.values() if req.status == ComplianceStatus.REQUIRES_ACTION]),
                    "overdue": len([
                        req for req in self.compliance_requirements.values()
                        if req.deadline and datetime.fromisoformat(req.deadline.replace('Z', '+00:00')) < current_time
                        and req.status != ComplianceStatus.COMPLIANT
                    ])
                },
                "risk_summary": {
                    "total_risks": total_risks,
                    "high_priority": high_risks,
                    "open_risks": open_risks,
                    "in_progress": len([risk for risk in self.legal_risks.values() if risk.status == "in_progress"]),
                    "mitigated": len([risk for risk in self.legal_risks.values() if risk.status in ["mitigated", "closed"]])
                },
                "document_status": {
                    "total": total_documents,
                    "active": len([doc for doc in self.legal_documents.values() if doc.status == "active"]),
                    "expiring_soon": expiring_docs,
                    "needs_review": len([doc for doc in self.legal_documents.values() if not doc.last_reviewed]),
                    "high_risk": len([doc for doc in self.legal_documents.values() if doc.ai_risk_score > 7.0])
                },
                "ip_portfolio": {
                    "total_assets": total_ip,
                    "active": active_ip,
                    "patents": len([ip for ip in self.intellectual_property.values() if ip.ip_type == "patent"]),
                    "trademarks": len([ip for ip in self.intellectual_property.values() if ip.ip_type == "trademark"]),
                    "estimated_value": ip_value
                },
                "recent_documents": [
                    {
                        "document_id": doc.document_id,
                        "title": doc.title,
                        "type": doc.document_type.value,
                        "risk_score": doc.ai_risk_score,
                        "compliance_score": doc.ai_compliance_score,
                        "updated_at": doc.updated_at
                    }
                    for doc in recent_documents
                ],
                "priority_risks": [
                    {
                        "risk_id": risk.risk_id,
                        "title": risk.title,
                        "category": risk.category,
                        "risk_level": risk.risk_level.value,
                        "severity_score": risk.ai_severity_score,
                        "status": risk.status,
                        "target_resolution": risk.target_resolution
                    }
                    for risk in recent_risks
                ],
                "upcoming_deadlines": upcoming_deadlines[:10],
                "ai_insights": await self._generate_legal_dashboard_insights()
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Failed to get legal dashboard data: {e}")
            raise
    
    async def _generate_legal_dashboard_insights(self) -> List[str]:
        """Generate AI-powered legal dashboard insights"""
        
        insights = []
        current_time = datetime.now(timezone.utc)
        
        # Check for critical deadlines
        critical_deadlines = []
        for req in self.compliance_requirements.values():
            if req.deadline:
                deadline = datetime.fromisoformat(req.deadline.replace('Z', '+00:00'))
                days_to_deadline = (deadline - current_time).days
                
                if 0 <= days_to_deadline <= 7:
                    critical_deadlines.append(req)
        
        if critical_deadlines:
            insights.append(f"🚨 {len(critical_deadlines)} compliance deadlines within 7 days - immediate action required")
        
        # Check compliance rate
        compliance_rate = len([req for req in self.compliance_requirements.values() if req.status == ComplianceStatus.COMPLIANT]) / max(len(self.compliance_requirements), 1)
        
        if compliance_rate >= 0.9:
            insights.append("✅ Excellent compliance rate - maintain current practices")
        elif compliance_rate < 0.7:
            insights.append("⚠️ Compliance rate below 70% - review and strengthen processes")
        
        # Check high-risk items
        high_risk_count = len([risk for risk in self.legal_risks.values() if risk.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]])
        
        if high_risk_count > 3:
            insights.append(f"🔴 {high_risk_count} high-priority risks identified - prioritize mitigation efforts")
        
        # Check IP portfolio
        ip_renewals = []
        for ip in self.intellectual_property.values():
            if ip.renewal_dates:
                for renewal_date in ip.renewal_dates:
                    renewal = datetime.fromisoformat(renewal_date.replace('Z', '+00:00'))
                    if 0 <= (renewal - current_time).days <= 60:
                        ip_renewals.append(ip)
                        break
        
        if ip_renewals:
            insights.append(f"🔄 {len(ip_renewals)} IP assets require renewal attention within 60 days")
        
        # Default insights
        if not insights:
            insights = [
                "📊 Legal and compliance status is stable",
                "💡 Consider implementing automated compliance monitoring",
                "🎯 Schedule quarterly legal risk assessment"
            ]
        
        return insights

# Global legal compliance engine
legal_compliance_engine = LegalComplianceEngine()