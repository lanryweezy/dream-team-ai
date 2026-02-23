"""
Accounting Agent with Sub-Agents
Handles accounting, tax calculations, financial reporting, and compliance across multiple jurisdictions
"""

import asyncio
import logging
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import math

from core.base_agent import BaseAgent, AgentCapability, TaskResult

logger = logging.getLogger(__name__)

class AccountingSubAgent(ABC):
    """Base class for accounting sub-agents"""
    
    def __init__(self, jurisdiction: str, currency: str, specialization: str):
        self.jurisdiction = jurisdiction
        self.currency = currency
        self.specialization = specialization
        
    @abstractmethod
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle jurisdiction-specific accounting task"""
        pass
        
    @abstractmethod
    def calculate_taxes(self, income: float, business_type: str, deductions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate taxes for the jurisdiction"""
        pass
        
    @abstractmethod
    def get_tax_deadlines(self, year: int) -> List[Dict[str, Any]]:
        """Get tax filing deadlines for the jurisdiction"""
        pass

class USAAccountingAgent(AccountingSubAgent):
    def __init__(self):
        super().__init__("USA", "USD", "US Federal and State Tax Law")
        
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get("type")
        
        if task_type == "tax_calculation":
            return await self._calculate_taxes_detailed(task)
        elif task_type == "quarterly_filing":
            return await self._handle_quarterly_filing(task)
        elif task_type == "expense_categorization":
            return await self._categorize_expenses(task)
        elif task_type == "depreciation_calculation":
            return await self._calculate_depreciation(task)
        elif task_type == "payroll_taxes":
            return await self._calculate_payroll_taxes(task)
        else:
            return {"error": f"Unknown task type: {task_type}"}
            
    async def _calculate_taxes_detailed(self, task: Dict[str, Any]) -> Dict[str, Any]:
        income = task.get("income", 0)
        business_type = task.get("business_type", "LLC")
        deductions = task.get("deductions", [])
        state = task.get("state", "California")
        
        tax_calculation = self.calculate_taxes(income, business_type, deductions)
        
        # Add state-specific calculations
        state_tax = self._calculate_state_tax(income, state, deductions)
        tax_calculation["state_tax"] = state_tax
        
        return {
            "jurisdiction": "USA",
            "tax_calculation": tax_calculation,
            "recommendations": [
                "Consider quarterly estimated payments",
                "Maximize business deductions",
                "Review retirement plan contributions",
                "Consult tax professional for complex situations"
            ]
        }
        
    def calculate_taxes(self, income: float, business_type: str, deductions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate US federal taxes"""
        if deductions is None:
            deductions = []
            
        # Calculate total deductions
        total_deductions = sum(d.get("amount", 0) for d in deductions)
        taxable_income = max(0, income - total_deductions)
        
        # 2024 Federal tax brackets for single filer (simplified)
        federal_tax = 0
        brackets = [
            (11000, 0.10),
            (44725, 0.12),
            (95375, 0.22),
            (182050, 0.24),
            (231250, 0.32),
            (578125, 0.35),
            (float('inf'), 0.37)
        ]
        
        remaining_income = taxable_income
        prev_bracket = 0
        
        for bracket_limit, rate in brackets:
            if remaining_income <= 0:
                break
                
            taxable_in_bracket = min(remaining_income, bracket_limit - prev_bracket)
            federal_tax += taxable_in_bracket * rate
            remaining_income -= taxable_in_bracket
            prev_bracket = bracket_limit
            
        # Self-employment tax (if applicable)
        se_tax = 0
        if business_type in ["LLC", "Sole Proprietorship", "Partnership"]:
            se_income = max(0, income - 400)  # SE tax threshold
            se_tax = min(se_income * 0.9235 * 0.153, 160200 * 0.153)  # 2024 limits
            
        # Estimated quarterly payments
        total_tax = federal_tax + se_tax
        quarterly_payment = total_tax / 4
        
        return {
            "gross_income": income,
            "total_deductions": total_deductions,
            "taxable_income": taxable_income,
            "federal_income_tax": round(federal_tax, 2),
            "self_employment_tax": round(se_tax, 2),
            "total_federal_tax": round(total_tax, 2),
            "effective_tax_rate": round((total_tax / income * 100) if income > 0 else 0, 2),
            "quarterly_estimated_payment": round(quarterly_payment, 2),
            "deduction_breakdown": deductions
        }
        
    def _calculate_state_tax(self, income: float, state: str, deductions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate state taxes (simplified for major states)"""
        state_rates = {
            "California": 0.13,  # Top rate (simplified)
            "New York": 0.109,
            "Texas": 0.0,  # No state income tax
            "Florida": 0.0,
            "Washington": 0.0,
            "Nevada": 0.0,
            "Delaware": 0.066
        }
        
        rate = state_rates.get(state, 0.05)  # Default 5% for other states
        total_deductions = sum(d.get("amount", 0) for d in deductions)
        taxable_income = max(0, income - total_deductions)
        state_tax = taxable_income * rate
        
        return {
            "state": state,
            "state_tax_rate": rate,
            "state_tax_owed": round(state_tax, 2),
            "has_state_income_tax": rate > 0
        }
        
    async def _handle_quarterly_filing(self, task: Dict[str, Any]) -> Dict[str, Any]:
        quarter = task.get("quarter", 1)
        year = task.get("year", datetime.now().year)
        
        quarterly_deadlines = {
            1: f"April 15, {year}",  # Q1 (Jan-Mar)
            2: f"June 17, {year}",   # Q2 (Apr-May) 
            3: f"September 16, {year}",  # Q3 (Jun-Aug)
            4: f"January 15, {year + 1}"  # Q4 (Sep-Dec)
        }
        
        return {
            "jurisdiction": "USA",
            "quarter": quarter,
            "year": year,
            "deadline": quarterly_deadlines.get(quarter),
            "required_forms": ["Form 1040ES", "State estimated tax forms"],
            "payment_methods": ["Online", "Phone", "Mail", "Bank transfer"],
            "penalties": {
                "late_filing": "Failure to file penalty: 5% per month",
                "late_payment": "Failure to pay penalty: 0.5% per month",
                "underpayment": "Interest on underpayment"
            }
        }
        
    async def _categorize_expenses(self, task: Dict[str, Any]) -> Dict[str, Any]:
        expenses = task.get("expenses", [])
        
        categorized = {
            "office_expenses": [],
            "travel_meals": [],
            "professional_services": [],
            "marketing_advertising": [],
            "equipment_software": [],
            "utilities": [],
            "rent_lease": [],
            "insurance": [],
            "other_deductible": [],
            "non_deductible": []
        }
        
        for expense in expenses:
            description = expense.get("description", "").lower()
            amount = expense.get("amount", 0)
            category = expense.get("category", "")
            
            # Auto-categorize based on description
            if any(word in description for word in ["office", "supplies", "stationery"]):
                categorized["office_expenses"].append(expense)
            elif any(word in description for word in ["travel", "hotel", "flight", "meal"]):
                categorized["travel_meals"].append(expense)
            elif any(word in description for word in ["legal", "accounting", "consultant"]):
                categorized["professional_services"].append(expense)
            elif any(word in description for word in ["ads", "marketing", "advertising"]):
                categorized["marketing_advertising"].append(expense)
            elif any(word in description for word in ["computer", "software", "equipment"]):
                categorized["equipment_software"].append(expense)
            elif any(word in description for word in ["electric", "internet", "phone", "utility"]):
                categorized["utilities"].append(expense)
            elif any(word in description for word in ["rent", "lease", "office space"]):
                categorized["rent_lease"].append(expense)
            elif any(word in description for word in ["insurance", "coverage"]):
                categorized["insurance"].append(expense)
            else:
                categorized["other_deductible"].append(expense)
                
        # Calculate totals
        category_totals = {}
        for category, items in categorized.items():
            category_totals[category] = sum(item.get("amount", 0) for item in items)
            
        return {
            "jurisdiction": "USA",
            "categorized_expenses": categorized,
            "category_totals": category_totals,
            "total_deductible": sum(category_totals.values()),
            "tax_tips": [
                "Keep receipts for all business expenses",
                "Separate business and personal expenses",
                "Consider home office deduction if applicable",
                "Track mileage for business travel"
            ]
        }
        
    async def _calculate_depreciation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        assets = task.get("assets", [])
        
        depreciation_schedule = []
        
        for asset in assets:
            cost = asset.get("cost", 0)
            asset_type = asset.get("type", "equipment")
            purchase_date = asset.get("purchase_date", datetime.now().isoformat())
            
            # Simplified depreciation periods (MACRS)
            depreciation_periods = {
                "computer": 5,
                "equipment": 7,
                "furniture": 7,
                "vehicle": 5,
                "building": 39,
                "software": 3
            }
            
            years = depreciation_periods.get(asset_type, 7)
            annual_depreciation = cost / years
            
            depreciation_schedule.append({
                "asset": asset.get("name", "Unknown"),
                "cost": cost,
                "type": asset_type,
                "depreciation_period": years,
                "annual_depreciation": round(annual_depreciation, 2),
                "method": "Straight-line (simplified)"
            })
            
        return {
            "jurisdiction": "USA",
            "depreciation_schedule": depreciation_schedule,
            "total_annual_depreciation": sum(d["annual_depreciation"] for d in depreciation_schedule),
            "notes": [
                "Consider Section 179 deduction for immediate expensing",
                "Bonus depreciation may be available",
                "Consult tax professional for complex assets"
            ]
        }
        
    async def _calculate_payroll_taxes(self, task: Dict[str, Any]) -> Dict[str, Any]:
        employees = task.get("employees", [])
        
        payroll_summary = {
            "total_wages": 0,
            "federal_withholding": 0,
            "social_security_employee": 0,
            "medicare_employee": 0,
            "social_security_employer": 0,
            "medicare_employer": 0,
            "federal_unemployment": 0,
            "state_unemployment": 0
        }
        
        for employee in employees:
            wages = employee.get("annual_wages", 0)
            
            # Employee taxes (simplified)
            ss_employee = min(wages * 0.062, 160200 * 0.062)  # 2024 SS wage base
            medicare_employee = wages * 0.0145
            
            # Employer taxes
            ss_employer = ss_employee  # Employer matches
            medicare_employer = medicare_employee  # Employer matches
            futa = min(wages * 0.006, 7000 * 0.006)  # FUTA on first $7,000
            suta = wages * 0.054  # Simplified state rate
            
            payroll_summary["total_wages"] += wages
            payroll_summary["social_security_employee"] += ss_employee
            payroll_summary["medicare_employee"] += medicare_employee
            payroll_summary["social_security_employer"] += ss_employer
            payroll_summary["medicare_employer"] += medicare_employer
            payroll_summary["federal_unemployment"] += futa
            payroll_summary["state_unemployment"] += suta
            
        # Round all values
        for key in payroll_summary:
            if key != "total_wages":
                payroll_summary[key] = round(payroll_summary[key], 2)
                
        total_employer_burden = (
            payroll_summary["social_security_employer"] +
            payroll_summary["medicare_employer"] +
            payroll_summary["federal_unemployment"] +
            payroll_summary["state_unemployment"]
        )
        
        return {
            "jurisdiction": "USA",
            "payroll_summary": payroll_summary,
            "total_employer_tax_burden": round(total_employer_burden, 2),
            "filing_requirements": [
                "Form 941 (Quarterly)",
                "Form 940 (Annual FUTA)",
                "State payroll tax returns",
                "W-2 forms (Annual)"
            ]
        }
        
    def get_tax_deadlines(self, year: int) -> List[Dict[str, Any]]:
        return [
            {"deadline": f"January 15, {year}", "description": "Q4 Estimated Tax Payment"},
            {"deadline": f"March 15, {year}", "description": "S-Corp/Partnership Tax Return"},
            {"deadline": f"April 15, {year}", "description": "Individual Tax Return & Q1 Estimated"},
            {"deadline": f"June 17, {year}", "description": "Q2 Estimated Tax Payment"},
            {"deadline": f"September 16, {year}", "description": "Q3 Estimated Tax Payment"},
            {"deadline": f"October 15, {year}", "description": "Extended Tax Return Deadline"}
        ]

class IndiaAccountingAgent(AccountingSubAgent):
    def __init__(self):
        super().__init__("India", "INR", "Indian Tax and Accounting Law")
        
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get("type")
        
        if task_type == "tax_calculation":
            return await self._calculate_taxes_detailed(task)
        elif task_type == "gst_calculation":
            return await self._calculate_gst(task)
        elif task_type == "tds_calculation":
            return await self._calculate_tds(task)
        elif task_type == "pf_calculation":
            return await self._calculate_pf_esi(task)
        else:
            return {"error": f"Unknown task type: {task_type}"}
            
    async def _calculate_taxes_detailed(self, task: Dict[str, Any]) -> Dict[str, Any]:
        income = task.get("income", 0)
        business_type = task.get("business_type", "Private Limited")
        deductions = task.get("deductions", [])
        
        tax_calculation = self.calculate_taxes(income, business_type, deductions)
        
        return {
            "jurisdiction": "India",
            "tax_calculation": tax_calculation,
            "recommendations": [
                "Consider Section 80C deductions (₹1.5 lakh limit)",
                "Explore Section 80D for health insurance",
                "Plan advance tax payments quarterly",
                "Maintain proper books of accounts"
            ]
        }
        
    def calculate_taxes(self, income: float, business_type: str, deductions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate Indian income tax"""
        if deductions is None:
            deductions = []
            
        total_deductions = sum(d.get("amount", 0) for d in deductions)
        
        # Standard deduction for individuals
        standard_deduction = 50000 if business_type == "Individual" else 0
        
        taxable_income = max(0, income - total_deductions - standard_deduction)
        
        # 2024-25 Tax slabs (New regime - simplified)
        income_tax = 0
        if taxable_income <= 300000:
            income_tax = 0
        elif taxable_income <= 600000:
            income_tax = (taxable_income - 300000) * 0.05
        elif taxable_income <= 900000:
            income_tax = 15000 + (taxable_income - 600000) * 0.10
        elif taxable_income <= 1200000:
            income_tax = 45000 + (taxable_income - 900000) * 0.15
        elif taxable_income <= 1500000:
            income_tax = 90000 + (taxable_income - 1200000) * 0.20
        else:
            income_tax = 150000 + (taxable_income - 1500000) * 0.30
            
        # Health and Education Cess (4%)
        cess = income_tax * 0.04
        
        # Corporate tax rates
        if business_type == "Private Limited":
            if income <= 40000000:  # ₹4 crore
                corporate_tax = taxable_income * 0.25  # 25% for small companies
            else:
                corporate_tax = taxable_income * 0.30  # 30% for large companies
            cess = corporate_tax * 0.04
            total_tax = corporate_tax + cess
        else:
            total_tax = income_tax + cess
            
        return {
            "gross_income": income,
            "total_deductions": total_deductions,
            "standard_deduction": standard_deduction,
            "taxable_income": taxable_income,
            "income_tax": round(income_tax, 2),
            "health_education_cess": round(cess, 2),
            "total_tax": round(total_tax, 2),
            "effective_tax_rate": round((total_tax / income * 100) if income > 0 else 0, 2),
            "advance_tax_quarterly": round(total_tax / 4, 2)
        }
        
    async def _calculate_gst(self, task: Dict[str, Any]) -> Dict[str, Any]:
        transactions = task.get("transactions", [])
        business_type = task.get("business_type", "services")
        
        gst_summary = {
            "output_gst": 0,  # GST on sales
            "input_gst": 0,   # GST on purchases
            "net_gst_payable": 0
        }
        
        for transaction in transactions:
            amount = transaction.get("amount", 0)
            transaction_type = transaction.get("type", "sale")  # sale or purchase
            gst_rate = transaction.get("gst_rate", 0.18)  # Default 18%
            
            gst_amount = amount * gst_rate
            
            if transaction_type == "sale":
                gst_summary["output_gst"] += gst_amount
            elif transaction_type == "purchase":
                gst_summary["input_gst"] += gst_amount
                
        gst_summary["net_gst_payable"] = gst_summary["output_gst"] - gst_summary["input_gst"]
        
        # Round values
        for key in gst_summary:
            gst_summary[key] = round(gst_summary[key], 2)
            
        return {
            "jurisdiction": "India",
            "gst_summary": gst_summary,
            "filing_requirements": {
                "monthly": "GSTR-1, GSTR-3B",
                "quarterly": "GSTR-1 (for small taxpayers)",
                "annual": "GSTR-9"
            },
            "due_dates": {
                "gstr_1": "11th of next month",
                "gstr_3b": "20th of next month",
                "gstr_9": "31st December"
            }
        }
        
    async def _calculate_tds(self, task: Dict[str, Any]) -> Dict[str, Any]:
        payments = task.get("payments", [])
        
        tds_summary = []
        total_tds = 0
        
        # TDS rates for different payment types
        tds_rates = {
            "salary": 0.0,  # Based on tax slabs
            "professional_fees": 0.10,
            "contractor_payment": 0.01,
            "rent": 0.10,
            "commission": 0.05,
            "interest": 0.10
        }
        
        for payment in payments:
            amount = payment.get("amount", 0)
            payment_type = payment.get("type", "professional_fees")
            recipient_pan = payment.get("recipient_pan", "")
            
            rate = tds_rates.get(payment_type, 0.10)
            
            # Higher rate if no PAN
            if not recipient_pan:
                rate = 0.20
                
            tds_amount = amount * rate
            total_tds += tds_amount
            
            tds_summary.append({
                "payment_type": payment_type,
                "amount": amount,
                "tds_rate": rate,
                "tds_amount": round(tds_amount, 2),
                "net_payment": round(amount - tds_amount, 2)
            })
            
        return {
            "jurisdiction": "India",
            "tds_summary": tds_summary,
            "total_tds_deducted": round(total_tds, 2),
            "filing_requirements": [
                "TDS Return (Form 24Q, 26Q, 27Q)",
                "TDS Certificates (Form 16, 16A)",
                "Quarterly TDS payments"
            ]
        }
        
    async def _calculate_pf_esi(self, task: Dict[str, Any]) -> Dict[str, Any]:
        employees = task.get("employees", [])
        
        pf_esi_summary = {
            "total_basic_wages": 0,
            "employee_pf": 0,
            "employer_pf": 0,
            "employee_esi": 0,
            "employer_esi": 0
        }
        
        for employee in employees:
            basic_wage = employee.get("basic_wage", 0)
            
            # PF calculation (12% each for employee and employer)
            if basic_wage <= 15000:  # PF ceiling
                emp_pf = basic_wage * 0.12
                emp_er_pf = basic_wage * 0.12
            else:
                emp_pf = 15000 * 0.12
                emp_er_pf = 15000 * 0.12
                
            # ESI calculation (0.75% employee, 3.25% employer)
            if basic_wage <= 21000:  # ESI ceiling
                emp_esi = basic_wage * 0.0075
                emp_er_esi = basic_wage * 0.0325
            else:
                emp_esi = 0
                emp_er_esi = 0
                
            pf_esi_summary["total_basic_wages"] += basic_wage
            pf_esi_summary["employee_pf"] += emp_pf
            pf_esi_summary["employer_pf"] += emp_er_pf
            pf_esi_summary["employee_esi"] += emp_esi
            pf_esi_summary["employer_esi"] += emp_er_esi
            
        # Round values
        for key in pf_esi_summary:
            if key != "total_basic_wages":
                pf_esi_summary[key] = round(pf_esi_summary[key], 2)
                
        return {
            "jurisdiction": "India",
            "pf_esi_summary": pf_esi_summary,
            "total_employer_contribution": round(
                pf_esi_summary["employer_pf"] + pf_esi_summary["employer_esi"], 2
            ),
            "compliance_requirements": [
                "Monthly PF return (ECR)",
                "Annual PF return",
                "ESI returns (if applicable)",
                "Maintain employee records"
            ]
        }
        
    def get_tax_deadlines(self, year: int) -> List[Dict[str, Any]]:
        return [
            {"deadline": f"June 15, {year}", "description": "Q1 Advance Tax"},
            {"deadline": f"July 31, {year}", "description": "ITR Filing Deadline"},
            {"deadline": f"September 15, {year}", "description": "Q2 Advance Tax"},
            {"deadline": f"December 15, {year}", "description": "Q3 Advance Tax"},
            {"deadline": f"March 15, {year + 1}", "description": "Q4 Advance Tax"}
        ]

class NigeriaAccountingAgent(AccountingSubAgent):
    """Nigeria-specific accounting and tax calculations"""
    
    def __init__(self):
        super().__init__("Nigeria", "NGN", "Nigerian Tax and Accounting Law")
    
    def calculate_taxes(self, income: float, business_type: str, deductions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate Nigerian taxes (PAYE, CIT, VAT)"""
        if deductions is None:
            deductions = []
            
        total_deductions = sum(d.get("amount", 0) for d in deductions)
        taxable_income = max(0, income - total_deductions)
        
        # Nigerian Personal Income Tax (PAYE) - Progressive rates
        personal_tax = 0
        if business_type.lower() in ["individual", "sole proprietorship"]:
            # PAYE rates for 2024
            if taxable_income <= 300000:  # First ₦300,000
                personal_tax = taxable_income * 0.07
            elif taxable_income <= 600000:  # Next ₦300,000
                personal_tax = 300000 * 0.07 + (taxable_income - 300000) * 0.11
            elif taxable_income <= 1100000:  # Next ₦500,000
                personal_tax = 300000 * 0.07 + 300000 * 0.11 + (taxable_income - 600000) * 0.15
            elif taxable_income <= 1600000:  # Next ₦500,000
                personal_tax = 300000 * 0.07 + 300000 * 0.11 + 500000 * 0.15 + (taxable_income - 1100000) * 0.19
            elif taxable_income <= 3200000:  # Next ₦1,600,000
                personal_tax = 300000 * 0.07 + 300000 * 0.11 + 500000 * 0.15 + 500000 * 0.19 + (taxable_income - 1600000) * 0.21
            else:  # Above ₦3,200,000
                personal_tax = 300000 * 0.07 + 300000 * 0.11 + 500000 * 0.15 + 500000 * 0.19 + 1600000 * 0.21 + (taxable_income - 3200000) * 0.24
        
        # Company Income Tax (CIT) for companies
        company_tax = 0
        if business_type.lower() in ["limited company", "corporation", "plc"]:
            if taxable_income <= 25000000:  # Small companies (up to ₦25M)
                company_tax = taxable_income * 0.20
            else:  # Large companies
                company_tax = taxable_income * 0.30
        
        # Education Tax (2% of assessable profit for companies)
        education_tax = 0
        if business_type.lower() in ["limited company", "corporation", "plc"]:
            education_tax = taxable_income * 0.02
        
        total_tax = personal_tax + company_tax + education_tax
        effective_rate = (total_tax / income * 100) if income > 0 else 0
        
        return {
            "gross_income": income,
            "total_deductions": total_deductions,
            "taxable_income": taxable_income,
            "personal_income_tax": personal_tax,
            "company_income_tax": company_tax,
            "education_tax": education_tax,
            "total_tax": total_tax,
            "effective_tax_rate": round(effective_rate, 2),
            "monthly_paye": round(personal_tax / 12, 2) if personal_tax > 0 else 0
        }
    
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Nigeria-specific accounting tasks"""
        task_type = task.get("type", "")
        
        if task_type == "tax_calculation":
            tax_calc = self.calculate_taxes(
                task.get("income", 0),
                task.get("business_type", "individual"),
                task.get("deductions", [])
            )
            return {
                "jurisdiction": self.jurisdiction,
                "tax_calculation": tax_calc,
                "recommendations": [
                    "Ensure proper PAYE compliance",
                    "Register for VAT if turnover exceeds ₦25M",
                    "Maintain proper books of accounts",
                    "Consider tax planning strategies"
                ]
            }
        
        elif task_type == "vat_calculation":
            vat_calc = self.calculate_vat(task.get("transactions", []))
            return {
                "jurisdiction": self.jurisdiction,
                "vat_summary": vat_calc
            }
        
        return {"error": f"Unknown task type: {task_type}"}
    
    def calculate_vat(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate Nigerian VAT (7.5%)"""
        vat_rate = 0.075  # 7.5% standard rate
        
        output_vat = 0
        input_vat = 0
        
        for transaction in transactions:
            amount = transaction.get("amount", 0)
            trans_type = transaction.get("type", "")
            
            if trans_type == "sale":
                output_vat += amount * vat_rate
            elif trans_type == "purchase":
                input_vat += amount * vat_rate
        
        net_vat = output_vat - input_vat
        
        return {
            "output_vat": output_vat,
            "input_vat": input_vat,
            "net_vat_payable": max(0, net_vat),
            "vat_rate": "7.5%",
            "filing_requirements": {
                "frequency": "Monthly",
                "deadline": "21st of following month",
                "registration_threshold": "₦25,000,000 annual turnover"
            }
        }
    
    def get_tax_deadlines(self, year: int) -> List[Dict[str, str]]:
        """Get Nigerian tax deadlines"""
        return [
            {"deadline": f"January 31, {year}", "description": "Annual Tax Return Filing"},
            {"deadline": f"March 31, {year}", "description": "Audited Financial Statements"},
            {"deadline": f"June 30, {year}", "description": "Companies Income Tax Payment"},
            {"deadline": f"Monthly by 10th", "description": "PAYE Remittance"},
            {"deadline": f"Monthly by 21st", "description": "VAT Returns"},
            {"deadline": f"Quarterly", "description": "Withholding Tax Returns"}
        ]

class SouthAfricaAccountingAgent(AccountingSubAgent):
    """South Africa-specific accounting and tax calculations"""
    
    def __init__(self):
        super().__init__("South Africa", "ZAR", "South African Tax and Accounting Law")
    
    def calculate_taxes(self, income: float, business_type: str, deductions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate South African taxes (Personal Income Tax, Corporate Tax)"""
        if deductions is None:
            deductions = []
            
        total_deductions = sum(d.get("amount", 0) for d in deductions)
        taxable_income = max(0, income - total_deductions)
        
        # Personal Income Tax (Progressive rates for 2024/2025)
        personal_tax = 0
        if business_type.lower() in ["individual", "sole proprietorship"]:
            if taxable_income <= 237100:  # First R237,100
                personal_tax = taxable_income * 0.18
            elif taxable_income <= 370500:  # R237,101 - R370,500
                personal_tax = 237100 * 0.18 + (taxable_income - 237100) * 0.26
            elif taxable_income <= 512800:  # R370,501 - R512,800
                personal_tax = 237100 * 0.18 + 133400 * 0.26 + (taxable_income - 370500) * 0.31
            elif taxable_income <= 673000:  # R512,801 - R673,000
                personal_tax = 237100 * 0.18 + 133400 * 0.26 + 142300 * 0.31 + (taxable_income - 512800) * 0.36
            elif taxable_income <= 857900:  # R673,001 - R857,900
                personal_tax = 237100 * 0.18 + 133400 * 0.26 + 142300 * 0.31 + 160200 * 0.36 + (taxable_income - 673000) * 0.39
            elif taxable_income <= 1817000:  # R857,901 - R1,817,000
                personal_tax = 237100 * 0.18 + 133400 * 0.26 + 142300 * 0.31 + 160200 * 0.36 + 184900 * 0.39 + (taxable_income - 857900) * 0.41
            else:  # Above R1,817,000
                personal_tax = 237100 * 0.18 + 133400 * 0.26 + 142300 * 0.31 + 160200 * 0.36 + 184900 * 0.39 + 959100 * 0.41 + (taxable_income - 1817000) * 0.45
        
        # Corporate Income Tax (28% for companies)
        corporate_tax = 0
        if business_type.lower() in ["company", "corporation", "pty ltd"]:
            corporate_tax = taxable_income * 0.28
        
        total_tax = personal_tax + corporate_tax
        effective_rate = (total_tax / income * 100) if income > 0 else 0
        
        return {
            "gross_income": income,
            "total_deductions": total_deductions,
            "taxable_income": taxable_income,
            "personal_income_tax": personal_tax,
            "corporate_income_tax": corporate_tax,
            "total_tax": total_tax,
            "effective_tax_rate": round(effective_rate, 2)
        }
    
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle South Africa-specific accounting tasks"""
        task_type = task.get("type", "")
        
        if task_type == "tax_calculation":
            tax_calc = self.calculate_taxes(
                task.get("income", 0),
                task.get("business_type", "individual"),
                task.get("deductions", [])
            )
            return {
                "jurisdiction": self.jurisdiction,
                "tax_calculation": tax_calc,
                "recommendations": [
                    "Consider retirement annuity contributions",
                    "Maximize medical aid tax credits",
                    "Plan for provisional tax payments",
                    "Ensure SARS compliance"
                ]
            }
        
        elif task_type == "vat_calculation":
            vat_calc = self.calculate_vat(task.get("transactions", []))
            return {
                "jurisdiction": self.jurisdiction,
                "vat_summary": vat_calc
            }
        
        return {"error": f"Unknown task type: {task_type}"}
    
    def calculate_vat(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate South African VAT (15%)"""
        vat_rate = 0.15  # 15% standard rate
        
        output_vat = 0
        input_vat = 0
        
        for transaction in transactions:
            amount = transaction.get("amount", 0)
            trans_type = transaction.get("type", "")
            
            if trans_type == "sale":
                output_vat += amount * vat_rate
            elif trans_type == "purchase":
                input_vat += amount * vat_rate
        
        net_vat = output_vat - input_vat
        
        return {
            "output_vat": output_vat,
            "input_vat": input_vat,
            "net_vat_payable": max(0, net_vat),
            "vat_rate": "15%",
            "filing_requirements": {
                "frequency": "Monthly or Bi-monthly",
                "deadline": "25th of following month",
                "registration_threshold": "R1,000,000 annual turnover"
            }
        }
    
    def get_tax_deadlines(self, year: int) -> List[Dict[str, str]]:
        """Get South African tax deadlines"""
        return [
            {"deadline": f"February 28, {year}", "description": "Individual Tax Returns"},
            {"deadline": f"October 31, {year}", "description": "Company Tax Returns"},
            {"deadline": f"Monthly by 25th", "description": "VAT Returns"},
            {"deadline": f"Bi-annually", "description": "Provisional Tax Payments"}
        ]

class EgyptAccountingAgent(AccountingSubAgent):
    """Egypt-specific accounting and tax calculations"""
    
    def __init__(self):
        super().__init__("Egypt", "EGP", "Egyptian Tax and Accounting Law")
    
    def calculate_taxes(self, income: float, business_type: str, deductions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate Egyptian taxes"""
        if deductions is None:
            deductions = []
            
        total_deductions = sum(d.get("amount", 0) for d in deductions)
        taxable_income = max(0, income - total_deductions)
        
        # Personal Income Tax (Progressive rates)
        personal_tax = 0
        if business_type.lower() in ["individual", "sole proprietorship"]:
            if taxable_income <= 15000:  # First E£15,000
                personal_tax = 0  # Tax-free
            elif taxable_income <= 30000:  # E£15,001 - E£30,000
                personal_tax = (taxable_income - 15000) * 0.025
            elif taxable_income <= 45000:  # E£30,001 - E£45,000
                personal_tax = 15000 * 0.025 + (taxable_income - 30000) * 0.10
            elif taxable_income <= 60000:  # E£45,001 - E£60,000
                personal_tax = 15000 * 0.025 + 15000 * 0.10 + (taxable_income - 45000) * 0.15
            elif taxable_income <= 200000:  # E£60,001 - E£200,000
                personal_tax = 15000 * 0.025 + 15000 * 0.10 + 15000 * 0.15 + (taxable_income - 60000) * 0.20
            else:  # Above E£200,000
                personal_tax = 15000 * 0.025 + 15000 * 0.10 + 15000 * 0.15 + 140000 * 0.20 + (taxable_income - 200000) * 0.225
        
        # Corporate Income Tax (22.5%)
        corporate_tax = 0
        if business_type.lower() in ["company", "corporation", "joint stock"]:
            corporate_tax = taxable_income * 0.225
        
        total_tax = personal_tax + corporate_tax
        effective_rate = (total_tax / income * 100) if income > 0 else 0
        
        return {
            "gross_income": income,
            "total_deductions": total_deductions,
            "taxable_income": taxable_income,
            "personal_income_tax": personal_tax,
            "corporate_income_tax": corporate_tax,
            "total_tax": total_tax,
            "effective_tax_rate": round(effective_rate, 2)
        }
    
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Egypt-specific accounting tasks"""
        task_type = task.get("type", "")
        
        if task_type == "tax_calculation":
            tax_calc = self.calculate_taxes(
                task.get("income", 0),
                task.get("business_type", "individual"),
                task.get("deductions", [])
            )
            return {
                "jurisdiction": self.jurisdiction,
                "tax_calculation": tax_calc,
                "recommendations": [
                    "Ensure proper tax registration",
                    "Consider investment incentives",
                    "Maintain Arabic language records",
                    "Plan for VAT compliance"
                ]
            }
        
        return {"error": f"Unknown task type: {task_type}"}
    
    def get_tax_deadlines(self, year: int) -> List[Dict[str, str]]:
        """Get Egyptian tax deadlines"""
        return [
            {"deadline": f"March 31, {year}", "description": "Annual Tax Return"},
            {"deadline": f"Monthly by 15th", "description": "Payroll Tax"},
            {"deadline": f"Monthly by 15th", "description": "VAT Returns"}
        ]

class KenyaAccountingAgent(AccountingSubAgent):
    """Kenya-specific accounting and tax calculations"""
    
    def __init__(self):
        super().__init__("Kenya", "KES", "Kenyan Tax and Accounting Law")
    
    def calculate_taxes(self, income: float, business_type: str, deductions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate Kenyan taxes (PAYE, Corporate Tax)"""
        if deductions is None:
            deductions = []
            
        total_deductions = sum(d.get("amount", 0) for d in deductions)
        taxable_income = max(0, income - total_deductions)
        
        # Personal Income Tax (PAYE) - Progressive rates
        personal_tax = 0
        if business_type.lower() in ["individual", "sole proprietorship"]:
            if taxable_income <= 288000:  # First KSh 288,000
                personal_tax = taxable_income * 0.10
            elif taxable_income <= 388000:  # KSh 288,001 - 388,000
                personal_tax = 288000 * 0.10 + (taxable_income - 288000) * 0.25
            else:  # Above KSh 388,000
                personal_tax = 288000 * 0.10 + 100000 * 0.25 + (taxable_income - 388000) * 0.30
        
        # Corporate Income Tax (30%)
        corporate_tax = 0
        if business_type.lower() in ["company", "corporation", "limited"]:
            corporate_tax = taxable_income * 0.30
        
        total_tax = personal_tax + corporate_tax
        effective_rate = (total_tax / income * 100) if income > 0 else 0
        
        return {
            "gross_income": income,
            "total_deductions": total_deductions,
            "taxable_income": taxable_income,
            "personal_income_tax": personal_tax,
            "corporate_income_tax": corporate_tax,
            "total_tax": total_tax,
            "effective_tax_rate": round(effective_rate, 2)
        }
    
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Kenya-specific accounting tasks"""
        task_type = task.get("type", "")
        
        if task_type == "tax_calculation":
            tax_calc = self.calculate_taxes(
                task.get("income", 0),
                task.get("business_type", "individual"),
                task.get("deductions", [])
            )
            return {
                "jurisdiction": self.jurisdiction,
                "tax_calculation": tax_calc,
                "recommendations": [
                    "Ensure KRA PIN registration",
                    "File monthly PAYE returns",
                    "Register for VAT if turnover exceeds KSh 5M",
                    "Maintain proper accounting records"
                ]
            }
        
        return {"error": f"Unknown task type: {task_type}"}
    
    def get_tax_deadlines(self, year: int) -> List[Dict[str, str]]:
        """Get Kenyan tax deadlines"""
        return [
            {"deadline": f"June 30, {year}", "description": "Individual Tax Returns"},
            {"deadline": f"Monthly by 9th", "description": "PAYE Returns"},
            {"deadline": f"Monthly by 20th", "description": "VAT Returns"}
        ]

class NigeriaAccountingAgent(AccountingSubAgent):
    """Nigeria-specific accounting and tax calculations"""
    
    def __init__(self):
        super().__init__("Nigeria", "NGN", "Nigerian Tax and Accounting Law")
    
    def calculate_taxes(self, income: float, business_type: str, deductions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate Nigerian taxes (PAYE, CIT, VAT)"""
        if deductions is None:
            deductions = []
            
        total_deductions = sum(d.get("amount", 0) for d in deductions)
        taxable_income = max(0, income - total_deductions)
        
        # Nigerian Personal Income Tax (PAYE) - Progressive rates
        personal_tax = 0
        if business_type.lower() in ["individual", "sole proprietorship"]:
            # PAYE rates for 2024
            if taxable_income <= 300000:  # First ₦300,000
                personal_tax = taxable_income * 0.07
            elif taxable_income <= 600000:  # Next ₦300,000
                personal_tax = 300000 * 0.07 + (taxable_income - 300000) * 0.11
            elif taxable_income <= 1100000:  # Next ₦500,000
                personal_tax = 300000 * 0.07 + 300000 * 0.11 + (taxable_income - 600000) * 0.15
            elif taxable_income <= 1600000:  # Next ₦500,000
                personal_tax = 300000 * 0.07 + 300000 * 0.11 + 500000 * 0.15 + (taxable_income - 1100000) * 0.19
            elif taxable_income <= 3200000:  # Next ₦1,600,000
                personal_tax = 300000 * 0.07 + 300000 * 0.11 + 500000 * 0.15 + 500000 * 0.19 + (taxable_income - 1600000) * 0.21
            else:  # Above ₦3,200,000
                personal_tax = 300000 * 0.07 + 300000 * 0.11 + 500000 * 0.15 + 500000 * 0.19 + 1600000 * 0.21 + (taxable_income - 3200000) * 0.24
        
        # Company Income Tax (CIT) for companies
        company_tax = 0
        if business_type.lower() in ["limited company", "corporation", "plc"]:
            if taxable_income <= 25000000:  # Small companies (up to ₦25M)
                company_tax = taxable_income * 0.20
            else:  # Large companies
                company_tax = taxable_income * 0.30
        
        # Education Tax (2% of assessable profit for companies)
        education_tax = 0
        if business_type.lower() in ["limited company", "corporation", "plc"]:
            education_tax = taxable_income * 0.02
        
        total_tax = personal_tax + company_tax + education_tax
        effective_rate = (total_tax / income * 100) if income > 0 else 0
        
        return {
            "gross_income": income,
            "total_deductions": total_deductions,
            "taxable_income": taxable_income,
            "personal_income_tax": personal_tax,
            "company_income_tax": company_tax,
            "education_tax": education_tax,
            "total_tax": total_tax,
            "effective_tax_rate": round(effective_rate, 2),
            "monthly_paye": round(personal_tax / 12, 2) if personal_tax > 0 else 0
        }
    
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Nigeria-specific accounting tasks"""
        task_type = task.get("type", "")
        
        if task_type == "tax_calculation":
            tax_calc = self.calculate_taxes(
                task.get("income", 0),
                task.get("business_type", "individual"),
                task.get("deductions", [])
            )
            return {
                "jurisdiction": self.jurisdiction,
                "tax_calculation": tax_calc,
                "recommendations": [
                    "Ensure proper PAYE compliance",
                    "Register for VAT if turnover exceeds ₦25M",
                    "Maintain proper books of accounts",
                    "Consider tax planning strategies"
                ]
            }
        
        elif task_type == "vat_calculation":
            vat_calc = self.calculate_vat(task.get("transactions", []))
            return {
                "jurisdiction": self.jurisdiction,
                "vat_summary": vat_calc
            }
        
        return {"error": f"Unknown task type: {task_type}"}
    
    def calculate_vat(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate Nigerian VAT (7.5%)"""
        vat_rate = 0.075  # 7.5% standard rate
        
        output_vat = 0
        input_vat = 0
        
        for transaction in transactions:
            amount = transaction.get("amount", 0)
            trans_type = transaction.get("type", "")
            
            if trans_type == "sale":
                output_vat += amount * vat_rate
            elif trans_type == "purchase":
                input_vat += amount * vat_rate
        
        net_vat = output_vat - input_vat
        
        return {
            "output_vat": output_vat,
            "input_vat": input_vat,
            "net_vat_payable": max(0, net_vat),
            "vat_rate": "7.5%",
            "filing_requirements": {
                "frequency": "Monthly",
                "deadline": "21st of following month",
                "registration_threshold": "₦25,000,000 annual turnover"
            }
        }
    
    def get_tax_deadlines(self, year: int) -> List[Dict[str, str]]:
        """Get Nigerian tax deadlines"""
        return [
            {"deadline": f"January 31, {year}", "description": "Annual Tax Return Filing"},
            {"deadline": f"March 31, {year}", "description": "Audited Financial Statements"},
            {"deadline": f"June 30, {year}", "description": "Companies Income Tax Payment"},
            {"deadline": f"Monthly by 10th", "description": "PAYE Remittance"},
            {"deadline": f"Monthly by 21st", "description": "VAT Returns"},
            {"deadline": f"Quarterly", "description": "Withholding Tax Returns"}
        ]

class SouthAfricaAccountingAgent(AccountingSubAgent):
    """South Africa-specific accounting and tax calculations"""
    
    def __init__(self):
        super().__init__("South Africa", "ZAR", "South African Tax and Accounting Law")
    
    def calculate_taxes(self, income: float, business_type: str, deductions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate South African taxes (Personal Income Tax, Corporate Tax)"""
        if deductions is None:
            deductions = []
            
        total_deductions = sum(d.get("amount", 0) for d in deductions)
        taxable_income = max(0, income - total_deductions)
        
        # Personal Income Tax (Progressive rates for 2024/2025)
        personal_tax = 0
        if business_type.lower() in ["individual", "sole proprietorship"]:
            if taxable_income <= 237100:  # First R237,100
                personal_tax = taxable_income * 0.18
            elif taxable_income <= 370500:  # R237,101 - R370,500
                personal_tax = 237100 * 0.18 + (taxable_income - 237100) * 0.26
            elif taxable_income <= 512800:  # R370,501 - R512,800
                personal_tax = 237100 * 0.18 + 133400 * 0.26 + (taxable_income - 370500) * 0.31
            elif taxable_income <= 673000:  # R512,801 - R673,000
                personal_tax = 237100 * 0.18 + 133400 * 0.26 + 142300 * 0.31 + (taxable_income - 512800) * 0.36
            elif taxable_income <= 857900:  # R673,001 - R857,900
                personal_tax = 237100 * 0.18 + 133400 * 0.26 + 142300 * 0.31 + 160200 * 0.36 + (taxable_income - 673000) * 0.39
            elif taxable_income <= 1817000:  # R857,901 - R1,817,000
                personal_tax = 237100 * 0.18 + 133400 * 0.26 + 142300 * 0.31 + 160200 * 0.36 + 184900 * 0.39 + (taxable_income - 857900) * 0.41
            else:  # Above R1,817,000
                personal_tax = 237100 * 0.18 + 133400 * 0.26 + 142300 * 0.31 + 160200 * 0.36 + 184900 * 0.39 + 959100 * 0.41 + (taxable_income - 1817000) * 0.45
        
        # Corporate Income Tax (28% for companies)
        corporate_tax = 0
        if business_type.lower() in ["company", "corporation", "pty ltd"]:
            corporate_tax = taxable_income * 0.28
        
        total_tax = personal_tax + corporate_tax
        effective_rate = (total_tax / income * 100) if income > 0 else 0
        
        return {
            "gross_income": income,
            "total_deductions": total_deductions,
            "taxable_income": taxable_income,
            "personal_income_tax": personal_tax,
            "corporate_income_tax": corporate_tax,
            "total_tax": total_tax,
            "effective_tax_rate": round(effective_rate, 2)
        }
    
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle South Africa-specific accounting tasks"""
        task_type = task.get("type", "")
        
        if task_type == "tax_calculation":
            tax_calc = self.calculate_taxes(
                task.get("income", 0),
                task.get("business_type", "individual"),
                task.get("deductions", [])
            )
            return {
                "jurisdiction": self.jurisdiction,
                "tax_calculation": tax_calc,
                "recommendations": [
                    "Consider retirement annuity contributions",
                    "Maximize medical aid tax credits",
                    "Plan for provisional tax payments",
                    "Ensure SARS compliance"
                ]
            }
        
        elif task_type == "vat_calculation":
            vat_calc = self.calculate_vat(task.get("transactions", []))
            return {
                "jurisdiction": self.jurisdiction,
                "vat_summary": vat_calc
            }
        
        return {"error": f"Unknown task type: {task_type}"}
    
    def calculate_vat(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate South African VAT (15%)"""
        vat_rate = 0.15  # 15% standard rate
        
        output_vat = 0
        input_vat = 0
        
        for transaction in transactions:
            amount = transaction.get("amount", 0)
            trans_type = transaction.get("type", "")
            
            if trans_type == "sale":
                output_vat += amount * vat_rate
            elif trans_type == "purchase":
                input_vat += amount * vat_rate
        
        net_vat = output_vat - input_vat
        
        return {
            "output_vat": output_vat,
            "input_vat": input_vat,
            "net_vat_payable": max(0, net_vat),
            "vat_rate": "15%",
            "filing_requirements": {
                "frequency": "Monthly or Bi-monthly",
                "deadline": "25th of following month",
                "registration_threshold": "R1,000,000 annual turnover"
            }
        }
    
    def get_tax_deadlines(self, year: int) -> List[Dict[str, str]]:
        """Get South African tax deadlines"""
        return [
            {"deadline": f"February 28, {year}", "description": "Individual Tax Returns"},
            {"deadline": f"October 31, {year}", "description": "Company Tax Returns"},
            {"deadline": f"Monthly by 25th", "description": "VAT Returns"},
            {"deadline": f"Bi-annually", "description": "Provisional Tax Payments"}
        ]

class EgyptAccountingAgent(AccountingSubAgent):
    """Egypt-specific accounting and tax calculations"""
    
    def __init__(self):
        super().__init__("Egypt", "EGP", "Egyptian Tax and Accounting Law")
    
    def calculate_taxes(self, income: float, business_type: str, deductions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate Egyptian taxes"""
        if deductions is None:
            deductions = []
            
        total_deductions = sum(d.get("amount", 0) for d in deductions)
        taxable_income = max(0, income - total_deductions)
        
        # Personal Income Tax (Progressive rates)
        personal_tax = 0
        if business_type.lower() in ["individual", "sole proprietorship"]:
            if taxable_income <= 15000:  # First E£15,000
                personal_tax = 0  # Tax-free
            elif taxable_income <= 30000:  # E£15,001 - E£30,000
                personal_tax = (taxable_income - 15000) * 0.025
            elif taxable_income <= 45000:  # E£30,001 - E£45,000
                personal_tax = 15000 * 0.025 + (taxable_income - 30000) * 0.10
            elif taxable_income <= 60000:  # E£45,001 - E£60,000
                personal_tax = 15000 * 0.025 + 15000 * 0.10 + (taxable_income - 45000) * 0.15
            elif taxable_income <= 200000:  # E£60,001 - E£200,000
                personal_tax = 15000 * 0.025 + 15000 * 0.10 + 15000 * 0.15 + (taxable_income - 60000) * 0.20
            else:  # Above E£200,000
                personal_tax = 15000 * 0.025 + 15000 * 0.10 + 15000 * 0.15 + 140000 * 0.20 + (taxable_income - 200000) * 0.225
        
        # Corporate Income Tax (22.5%)
        corporate_tax = 0
        if business_type.lower() in ["company", "corporation", "joint stock"]:
            corporate_tax = taxable_income * 0.225
        
        total_tax = personal_tax + corporate_tax
        effective_rate = (total_tax / income * 100) if income > 0 else 0
        
        return {
            "gross_income": income,
            "total_deductions": total_deductions,
            "taxable_income": taxable_income,
            "personal_income_tax": personal_tax,
            "corporate_income_tax": corporate_tax,
            "total_tax": total_tax,
            "effective_tax_rate": round(effective_rate, 2)
        }
    
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Egypt-specific accounting tasks"""
        task_type = task.get("type", "")
        
        if task_type == "tax_calculation":
            tax_calc = self.calculate_taxes(
                task.get("income", 0),
                task.get("business_type", "individual"),
                task.get("deductions", [])
            )
            return {
                "jurisdiction": self.jurisdiction,
                "tax_calculation": tax_calc,
                "recommendations": [
                    "Ensure proper tax registration",
                    "Consider investment incentives",
                    "Maintain Arabic language records",
                    "Plan for VAT compliance"
                ]
            }
        
        return {"error": f"Unknown task type: {task_type}"}
    
    def get_tax_deadlines(self, year: int) -> List[Dict[str, str]]:
        """Get Egyptian tax deadlines"""
        return [
            {"deadline": f"March 31, {year}", "description": "Annual Tax Return"},
            {"deadline": f"Monthly by 15th", "description": "Payroll Tax"},
            {"deadline": f"Monthly by 15th", "description": "VAT Returns"}
        ]

class KenyaAccountingAgent(AccountingSubAgent):
    """Kenya-specific accounting and tax calculations"""
    
    def __init__(self):
        super().__init__("Kenya", "KES", "Kenyan Tax and Accounting Law")
    
    def calculate_taxes(self, income: float, business_type: str, deductions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate Kenyan taxes (PAYE, Corporate Tax)"""
        if deductions is None:
            deductions = []
            
        total_deductions = sum(d.get("amount", 0) for d in deductions)
        taxable_income = max(0, income - total_deductions)
        
        # Personal Income Tax (PAYE) - Progressive rates
        personal_tax = 0
        if business_type.lower() in ["individual", "sole proprietorship"]:
            if taxable_income <= 288000:  # First KSh 288,000
                personal_tax = taxable_income * 0.10
            elif taxable_income <= 388000:  # KSh 288,001 - 388,000
                personal_tax = 288000 * 0.10 + (taxable_income - 288000) * 0.25
            else:  # Above KSh 388,000
                personal_tax = 288000 * 0.10 + 100000 * 0.25 + (taxable_income - 388000) * 0.30
        
        # Corporate Income Tax (30%)
        corporate_tax = 0
        if business_type.lower() in ["company", "corporation", "limited"]:
            corporate_tax = taxable_income * 0.30
        
        total_tax = personal_tax + corporate_tax
        effective_rate = (total_tax / income * 100) if income > 0 else 0
        
        return {
            "gross_income": income,
            "total_deductions": total_deductions,
            "taxable_income": taxable_income,
            "personal_income_tax": personal_tax,
            "corporate_income_tax": corporate_tax,
            "total_tax": total_tax,
            "effective_tax_rate": round(effective_rate, 2)
        }
    
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Kenya-specific accounting tasks"""
        task_type = task.get("type", "")
        
        if task_type == "tax_calculation":
            tax_calc = self.calculate_taxes(
                task.get("income", 0),
                task.get("business_type", "individual"),
                task.get("deductions", [])
            )
            return {
                "jurisdiction": self.jurisdiction,
                "tax_calculation": tax_calc,
                "recommendations": [
                    "Ensure KRA PIN registration",
                    "File monthly PAYE returns",
                    "Register for VAT if turnover exceeds KSh 5M",
                    "Maintain proper accounting records"
                ]
            }
        
        return {"error": f"Unknown task type: {task_type}"}
    
    def get_tax_deadlines(self, year: int) -> List[Dict[str, str]]:
        """Get Kenyan tax deadlines"""
        return [
            {"deadline": f"June 30, {year}", "description": "Individual Tax Returns"},
            {"deadline": f"Monthly by 9th", "description": "PAYE Returns"},
            {"deadline": f"Monthly by 20th", "description": "VAT Returns"}
        ]

class UKAccountingAgent(AccountingSubAgent):
    def __init__(self):
        super().__init__("UK", "GBP", "UK Tax and Accounting Law")
        
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get("type")
        
        if task_type == "tax_calculation":
            return await self._calculate_taxes_detailed(task)
        elif task_type == "vat_calculation":
            return await self._calculate_vat(task)
        elif task_type == "corporation_tax":
            return await self._calculate_corporation_tax(task)
        else:
            return {"error": f"Unknown task type: {task_type}"}
            
    async def _calculate_taxes_detailed(self, task: Dict[str, Any]) -> Dict[str, Any]:
        income = task.get("income", 0)
        business_type = task.get("business_type", "Limited Company")
        deductions = task.get("deductions", [])
        
        tax_calculation = self.calculate_taxes(income, business_type, deductions)
        
        return {
            "jurisdiction": "UK",
            "tax_calculation": tax_calculation,
            "recommendations": [
                "Consider pension contributions for tax relief",
                "Utilize annual ISA allowance",
                "Plan for capital gains tax",
                "Review dividend vs salary optimization"
            ]
        }
        
    def calculate_taxes(self, income: float, business_type: str, deductions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate UK income tax"""
        if deductions is None:
            deductions = []
            
        total_deductions = sum(d.get("amount", 0) for d in deductions)
        
        # Personal allowance for 2024-25
        personal_allowance = 12570
        
        # Reduce personal allowance for high earners
        if income > 100000:
            allowance_reduction = min(personal_allowance, (income - 100000) / 2)
            personal_allowance -= allowance_reduction
            
        taxable_income = max(0, income - total_deductions - personal_allowance)
        
        # UK tax bands 2024-25
        income_tax = 0
        if taxable_income <= 37700:
            income_tax = taxable_income * 0.20  # Basic rate
        elif taxable_income <= 125140:
            income_tax = 37700 * 0.20 + (taxable_income - 37700) * 0.40  # Higher rate
        else:
            income_tax = 37700 * 0.20 + 87440 * 0.40 + (taxable_income - 125140) * 0.45  # Additional rate
            
        # National Insurance (simplified)
        ni_threshold = 12570
        ni_upper = 50270
        
        national_insurance = 0
        if income > ni_threshold:
            if income <= ni_upper:
                national_insurance = (income - ni_threshold) * 0.12
            else:
                national_insurance = (ni_upper - ni_threshold) * 0.12 + (income - ni_upper) * 0.02
                
        total_tax = income_tax + national_insurance
        
        return {
            "gross_income": income,
            "personal_allowance": personal_allowance,
            "total_deductions": total_deductions,
            "taxable_income": taxable_income,
            "income_tax": round(income_tax, 2),
            "national_insurance": round(national_insurance, 2),
            "total_tax": round(total_tax, 2),
            "effective_tax_rate": round((total_tax / income * 100) if income > 0 else 0, 2),
            "take_home_pay": round(income - total_tax, 2)
        }
        
    async def _calculate_vat(self, task: Dict[str, Any]) -> Dict[str, Any]:
        transactions = task.get("transactions", [])
        
        vat_summary = {
            "output_vat": 0,  # VAT on sales
            "input_vat": 0,   # VAT on purchases
            "net_vat_due": 0
        }
        
        for transaction in transactions:
            amount = transaction.get("amount", 0)
            transaction_type = transaction.get("type", "sale")
            vat_rate = transaction.get("vat_rate", 0.20)  # Standard rate 20%
            
            vat_amount = amount * vat_rate
            
            if transaction_type == "sale":
                vat_summary["output_vat"] += vat_amount
            elif transaction_type == "purchase":
                vat_summary["input_vat"] += vat_amount
                
        vat_summary["net_vat_due"] = vat_summary["output_vat"] - vat_summary["input_vat"]
        
        # Round values
        for key in vat_summary:
            vat_summary[key] = round(vat_summary[key], 2)
            
        return {
            "jurisdiction": "UK",
            "vat_summary": vat_summary,
            "vat_rates": {
                "standard": "20%",
                "reduced": "5%",
                "zero": "0%"
            },
            "filing_requirements": {
                "frequency": "Quarterly",
                "deadline": "1 month and 7 days after quarter end",
                "online_filing": "Mandatory for most businesses"
            }
        }
        
    async def _calculate_corporation_tax(self, task: Dict[str, Any]) -> Dict[str, Any]:
        profit = task.get("profit", 0)
        
        # UK Corporation Tax rates 2024
        if profit <= 50000:
            corp_tax_rate = 0.19  # Small profits rate
            corp_tax = profit * corp_tax_rate
        elif profit <= 250000:
            # Marginal relief applies
            corp_tax_rate = 0.25  # Main rate
            marginal_relief = (250000 - profit) * 0.015
            corp_tax = profit * corp_tax_rate - marginal_relief
        else:
            corp_tax_rate = 0.25  # Main rate
            corp_tax = profit * corp_tax_rate
            
        return {
            "jurisdiction": "UK",
            "taxable_profit": profit,
            "corporation_tax_rate": corp_tax_rate,
            "corporation_tax": round(corp_tax, 2),
            "filing_deadline": "12 months after accounting period end",
            "payment_deadline": "9 months and 1 day after accounting period end"
        }
        
    def get_tax_deadlines(self, year: int) -> List[Dict[str, Any]]:
        return [
            {"deadline": f"January 31, {year}", "description": "Self Assessment Tax Return"},
            {"deadline": f"July 19, {year}", "description": "Q1 VAT Return"},
            {"deadline": f"October 19, {year}", "description": "Q2 VAT Return"},
            {"deadline": f"January 19, {year + 1}", "description": "Q3 VAT Return"},
            {"deadline": f"April 19, {year + 1}", "description": "Q4 VAT Return"}
        ]

class AccountingAgent(BaseAgent):
    def __init__(self):
        capabilities = [
            AgentCapability(
                name="multi_jurisdiction_tax_calculation",
                description="Calculate taxes across multiple jurisdictions",
                cost_estimate=20.0,
                confidence_level=0.95,
                requirements=["jurisdiction", "income", "business_type"]
            ),
            AgentCapability(
                name="expense_categorization",
                description="Categorize and analyze business expenses",
                cost_estimate=10.0,
                confidence_level=0.90,
                requirements=["expenses_list"]
            ),
            AgentCapability(
                name="payroll_processing",
                description="Calculate payroll taxes and deductions",
                cost_estimate=15.0,
                confidence_level=0.92,
                requirements=["employee_data", "jurisdiction"]
            ),
            AgentCapability(
                name="financial_reporting",
                description="Generate financial reports and analysis",
                cost_estimate=25.0,
                confidence_level=0.88,
                requirements=["financial_data", "report_type"]
            ),
            AgentCapability(
                name="tax_planning",
                description="Provide tax planning strategies and optimization",
                cost_estimate=30.0,
                confidence_level=0.85,
                requirements=["financial_situation", "jurisdiction", "goals"]
            )
        ]
        
        super().__init__("accounting_agent", capabilities)
        
        # Initialize sub-agents for different jurisdictions
        self.sub_agents = {
            "USA": USAAccountingAgent(),
            "India": IndiaAccountingAgent(),
            "UK": UKAccountingAgent(),
            "Nigeria": NigeriaAccountingAgent(),
            "South Africa": SouthAfricaAccountingAgent(),
            "Egypt": EgyptAccountingAgent(),
            "Kenya": KenyaAccountingAgent()
        }
        
        # Supported jurisdictions for accounting
        self.supported_jurisdictions = [
            "USA", "India", "UK", "Nigeria", "South Africa", "Egypt", "Kenya",
            "Canada", "Australia", "Germany", "France", "Singapore", "UAE", 
            "Brazil", "Mexico", "Japan", "Ghana", "Morocco", "Ethiopia", 
            "Tanzania", "Uganda", "Rwanda", "Botswana", "Zambia"
        ]
        
    async def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        """Execute accounting tasks using appropriate sub-agents"""
        task_type = task.get("type")
        jurisdiction = task.get("jurisdiction", "USA")
        
        try:
            if task_type == "multi_jurisdiction_tax_calculation":
                return await self._handle_multi_jurisdiction_tax_calculation(task)
            elif task_type == "expense_categorization":
                return await self._categorize_expenses(task)
            elif task_type == "payroll_processing":
                return await self._process_payroll(task)
            elif task_type == "financial_reporting":
                return await self._generate_financial_report(task)
            elif task_type == "tax_planning":
                return await self._provide_tax_planning(task)
            else:
                # Delegate to appropriate sub-agent
                return await self._delegate_to_sub_agent(task)
                
        except Exception as e:
            logger.error(f"Accounting task failed: {e}")
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
            
        # Check approval for accounting consultation cost
        estimated_cost = 20.0
        action = {
            "type": "accounting_consultation",
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
                error_message="Accounting consultation not approved"
            )
            
        # Execute task with sub-agent
        sub_agent = self.sub_agents[jurisdiction]
        result = await sub_agent.handle_task(task)
        
        # Save accounting analysis
        os.makedirs("accounting_data", exist_ok=True)
        analysis_file = f"accounting_data/{jurisdiction.lower()}_{task.get('type')}_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        accounting_analysis = {
            "jurisdiction": jurisdiction,
            "task_type": task.get("type"),
            "analysis": result,
            "created_at": datetime.utcnow().isoformat(),
            "sub_agent": sub_agent.__class__.__name__
        }
        
        with open(analysis_file, "w") as f:
            json.dump(accounting_analysis, f, indent=2)
            
        return TaskResult(
            success=True,
            output=result,
            cost_incurred=estimated_cost,
            evidence=[analysis_file],
            next_steps=[
                "Review tax calculations",
                "Implement tax planning strategies",
                "Set up accounting systems",
                "Schedule regular financial reviews"
            ]
        )
        
    async def _handle_multi_jurisdiction_tax_calculation(self, task: Dict[str, Any]) -> TaskResult:
        """Handle tax calculations across multiple jurisdictions"""
        jurisdictions = task.get("jurisdictions", ["USA"])
        income = task.get("income", 0)
        business_type = task.get("business_type", "LLC")
        deductions = task.get("deductions", [])
        
        # Check approval for multi-jurisdiction analysis
        estimated_cost = len(jurisdictions) * 20.0
        action = {
            "type": "multi_jurisdiction_tax_analysis",
            "jurisdiction_count": len(jurisdictions),
            "income": income
        }
        
        if not await self.request_approval(action, estimated_cost):
            return TaskResult(
                success=False,
                output={},
                cost_incurred=0.0,
                evidence=[],
                next_steps=["Wait for founder approval"],
                error_message="Multi-jurisdiction tax analysis not approved"
            )
            
        tax_calculations = {}
        
        for jurisdiction in jurisdictions:
            if jurisdiction in self.sub_agents:
                sub_agent = self.sub_agents[jurisdiction]
                tax_calc = sub_agent.calculate_taxes(income, business_type, deductions)
                tax_calculations[jurisdiction] = tax_calc
            else:
                tax_calculations[jurisdiction] = {
                    "error": f"Tax calculation not available for {jurisdiction}",
                    "recommendation": f"Consult local tax professional in {jurisdiction}"
                }
                
        # Create tax optimization recommendations
        optimization = await self._create_tax_optimization_plan(tax_calculations, income)
        
        # Save tax analysis
        os.makedirs("accounting_data", exist_ok=True)
        tax_file = f"accounting_data/multi_jurisdiction_tax_{datetime.utcnow().strftime('%Y_%m_%d')}.json"
        
        tax_analysis = {
            "income": income,
            "business_type": business_type,
            "jurisdictions": jurisdictions,
            "tax_calculations": tax_calculations,
            "optimization_plan": optimization,
            "created_at": datetime.utcnow().isoformat()
        }
        
        with open(tax_file, "w") as f:
            json.dump(tax_analysis, f, indent=2)
            
        return TaskResult(
            success=True,
            output={
                "tax_calculations": tax_calculations,
                "optimization_plan": optimization,
                "total_jurisdictions": len(jurisdictions),
                "supported_jurisdictions": len([j for j in jurisdictions if j in self.sub_agents])
            },
            cost_incurred=estimated_cost,
            evidence=[tax_file],
            next_steps=[
                "Review tax obligations in each jurisdiction",
                "Implement tax optimization strategies",
                "Set up quarterly payment schedules",
                "Consult local tax professionals"
            ]
        )
        
    async def _create_tax_optimization_plan(self, tax_calculations: Dict, income: float) -> Dict[str, Any]:
        """Create tax optimization recommendations"""
        optimization_strategies = []
        
        # Find jurisdiction with lowest effective tax rate
        lowest_rate_jurisdiction = None
        lowest_rate = float('inf')
        
        for jurisdiction, calc in tax_calculations.items():
            if isinstance(calc, dict) and 'effective_tax_rate' in calc:
                rate = calc['effective_tax_rate']
                if rate < lowest_rate:
                    lowest_rate = rate
                    lowest_rate_jurisdiction = jurisdiction
                    
        if lowest_rate_jurisdiction:
            optimization_strategies.append({
                "strategy": "Jurisdiction Optimization",
                "description": f"Consider {lowest_rate_jurisdiction} for tax efficiency",
                "potential_savings": f"Lowest effective rate: {lowest_rate}%"
            })
            
        # General optimization strategies
        optimization_strategies.extend([
            {
                "strategy": "Business Structure Optimization",
                "description": "Review business entity type for tax efficiency",
                "potential_savings": "5-15% tax reduction possible"
            },
            {
                "strategy": "Expense Maximization",
                "description": "Ensure all legitimate business expenses are deducted",
                "potential_savings": "10-20% of eligible expenses"
            },
            {
                "strategy": "Timing Strategies",
                "description": "Optimize timing of income and expenses",
                "potential_savings": "Defer taxes to future periods"
            }
        ])
        
        return {
            "recommended_jurisdiction": lowest_rate_jurisdiction,
            "optimization_strategies": optimization_strategies,
            "next_review_date": (datetime.now() + timedelta(days=90)).isoformat()
        }
        
    async def get_daily_goals(self) -> List[Dict[str, Any]]:
        """Get daily accounting goals"""
        return [
            {
                "goal": "Process pending expense categorizations",
                "priority": "high",
                "estimated_time": "45 minutes"
            },
            {
                "goal": "Review tax calculation requests",
                "priority": "high",
                "estimated_time": "30 minutes"
            },
            {
                "goal": "Update financial reports",
                "priority": "medium",
                "estimated_time": "1 hour"
            },
            {
                "goal": "Monitor tax deadline calendar",
                "priority": "medium",
                "estimated_time": "15 minutes"
            }
        ]

# Example usage
async def main():
    """Example usage of AccountingAgent"""
    agent = AccountingAgent()
    await agent.start()
    
    # Test multi-jurisdiction tax calculation
    task = {
        "type": "multi_jurisdiction_tax_calculation",
        "jurisdictions": ["USA", "India", "UK"],
        "income": 100000,
        "business_type": "LLC",
        "deductions": [
            {"description": "Office rent", "amount": 12000},
            {"description": "Professional services", "amount": 5000}
        ]
    }
    
    result = await agent.execute_task(task)
    print("Tax calculation result:", json.dumps(result.__dict__, indent=2, default=str))
    
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())