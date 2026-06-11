#!/usr/bin/env python3
"""
AnnualCreditReport.gov Connector
Stage: 04_FINANCIAL_CREDIT
Purpose: Ingest credit reports and extract identity markers
"""

import os
import re
import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

import aiohttp
import psycopg2
from psycopg2.extras import execute_values
import pdfplumber
from playwright.async_api import async_playwright

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CreditReportMarker:
    """Single data point extracted from credit report"""
    marker_key: str
    marker_value: str
    pii_classification: str  # 'HIGH', 'MEDIUM', 'LOW'
    source_section: str  # Which credit report section

@dataclass
class ConnectorResult:
    """Result of connector run"""
    success: bool
    identity_id: Optional[str]
    event_id: Optional[str]
    markers_inserted: int
    error_message: Optional[str] = None

class AnnualCreditReportConnector:
    """
    Connector for AnnualCreditReport.gov
    
    Flow:
    1. User provides SSN/DOB/Address (via secure form)
    2. Navigate to annualcreditreport.com
    3. Request reports from all 3 bureaus
    4. Download PDFs
    5. Parse and extract markers
    6. Insert into database
    """
    
    BUREAUS = ['experian', 'transunion', 'equifax']
    
    def __init__(self, db_config: Dict[str, str]):
        self.db_config = db_config
        self.stage_code = '04_FINANCIAL_CREDIT'
        self.source_system = 'AnnualCreditReport.gov'
        self.confidence_score = 0.95  # Official government source
        
    async def run(self, 
                  identity_id: str,
                  ssn: str,
                  dob: str,
                  address: Dict[str, str]) -> ConnectorResult:
        """
        Main connector execution
        
        Args:
            identity_id: UUID from identity table
            ssn: Social Security Number (full)
            dob: Date of birth (YYYY-MM-DD)
            address: Dict with street, city, state, zip
        """
        try:
            # Create stage_event record
            event_id = await self._create_event(identity_id)
            
            # Download credit reports (requires browser automation)
            report_paths = await self._download_reports(
                ssn, dob, address
            )
            
            if not report_paths:
                return ConnectorResult(
                    success=False,
                    identity_id=identity_id,
                    event_id=event_id,
                    markers_inserted=0,
                    error_message="Failed to download credit reports"
                )
            
            # Parse PDFs and extract markers
            all_markers = []
            for bureau, pdf_path in report_paths.items():
                markers = await self._parse_credit_report(pdf_path, bureau)
                all_markers.extend(markers)
            
            # Insert markers into database
            inserted_count = await self._insert_markers(event_id, all_markers)
            
            # Update event status
            await self._update_event_status(event_id, 'completed')
            
            return ConnectorResult(
                success=True,
                identity_id=identity_id,
                event_id=event_id,
                markers_inserted=inserted_count
            )
            
        except Exception as e:
            logger.error(f"Connector failed: {str(e)}")
            return ConnectorResult(
                success=False,
                identity_id=identity_id,
                event_id=None,
                markers_inserted=0,
                error_message=str(e)
            )
    
    async def _create_event(self, identity_id: str) -> str:
        """Create stage_event record"""
        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO stage_event (
                identity_id, stage_code, event_date, 
                source_system, confidence_score, is_active
            ) VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING event_id
        """, (
            identity_id, 
            self.stage_code,
            datetime.now(),
            self.source_system,
            self.confidence_score,
            True
        ))
        
        event_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        return str(event_id)
    
    async def _download_reports(self, 
                               ssn: str, 
                               dob: str, 
                               address: Dict[str, str]) -> Dict[str, Path]:
        """
        Download credit report PDFs using Playwright
        
        WARNING: This requires browser automation and may break
        if AnnualCreditReport.gov changes their UI
        """
        report_paths = {}
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                # Navigate to AnnualCreditReport.com
                await page.goto('https://www.annualcreditreport.com/')
                await page.wait_for_load_state('networkidle')
                
                # Click "Request your free credit reports"
                await page.click('text=Request your free credit reports')
                await page.wait_for_load_state('networkidle')
                
                # Fill in personal information
                await page.fill('input[name="ssn"]', ssn)
                await page.fill('input[name="dob"]', dob)
                await page.fill('input[name="address"]', address['street'])
                await page.fill('input[name="city"]', address['city'])
                await page.select_option('select[name="state"]', address['state'])
                await page.fill('input[name="zip"]', address['zip'])
                
                # Select all three bureaus
                for bureau in self.BUREAUS:
                    await page.check(f'input[value="{bureau}"]')
                
                # Submit request
                await page.click('button[type="submit"]')
                await page.wait_for_load_state('networkidle')
                
                # Handle identity verification questions (if prompted)
                # This is the tricky part - knowledge-based authentication
                await self._handle_kba_questions(page)
                
                # Download each bureau's report
                for bureau in self.BUREAUS:
                    pdf_path = await self._download_bureau_report(page, bureau)
                    if pdf_path:
                        report_paths[bureau] = pdf_path
                
            except Exception as e:
                logger.error(f"Browser automation failed: {e}")
                
            finally:
                await browser.close()
        
        return report_paths
    
    async def _handle_kba_questions(self, page):
        """
        Handle knowledge-based authentication questions
        These are multiple choice questions based on credit history
        """
        # Wait for KBA screen
        kba_selector = 'text=Identity Verification'
        try:
            await page.wait_for_selector(kba_selector, timeout=10000)
            
            # This requires user input - cannot be automated safely
            # In production, pause here and notify user to answer questions
            logger.warning("KBA questions detected - user intervention required")
            
            # Placeholder: Wait for manual intervention
            # In real implementation, send notification and wait for response
            await asyncio.sleep(30)  # Placeholder
            
        except:
            # No KBA required
            pass
    
    async def _download_bureau_report(self, page, bureau: str) -> Optional[Path]:
        """Download single bureau report PDF"""
        try:
            # Find download link for this bureau
            download_link = await page.query_selector(
                f'a[href*="{bureau}"][download]'
            )
            
            if download_link:
                async with page.expect_download() as download_info:
                    await download_link.click()
                download = await download_info.value
                
                # Save to temp directory
                pdf_path = Path(f'/tmp/credit_report_{bureau}_{datetime.now().strftime("%Y%m%d")}.pdf')
                await download.save_as(str(pdf_path))
                
                return pdf_path
                
        except Exception as e:
            logger.error(f"Failed to download {bureau} report: {e}")
            
        return None
    
    async def _parse_credit_report(self, 
                                  pdf_path: Path, 
                                  bureau: str) -> List[CreditReportMarker]:
        """
        Parse credit report PDF and extract identity markers
        
        Sections to parse:
        - Personal Information (name variations, addresses, employers)
        - Accounts (creditors, account numbers, balances)
        - Inquiries (who checked credit, when)
        - Public Records (bankruptcies, liens, judgments)
        """
        markers = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                for page in pdf.pages:
                    full_text += page.extract_text() + "\n"
                
                # Extract personal information section
                personal_markers = self._extract_personal_info(full_text, bureau)
                markers.extend(personal_markers)
                
                # Extract addresses
                address_markers = self._extract_addresses(full_text, bureau)
                markers.extend(address_markers)
                
                # extract employer
                employer_markers = self._extract_employers(full_text, bureau)
                markers.extend(employer_markers)
                
                # Extract accounts (creditors)
                account_markers = self._extract_accounts(full_text, bureau)
                markers.extend(account_markers)
                
                # Extract inquiries
                inquiry_markers = self._extract_inquiries(full_text, bureau)
                markers.extend(inquiry_markers)
                
        except Exception as e:
            logger.error(f"PDF parsing failed for {bureau}: {e}")
        
        return markers
    
    def _extract_personal_info(self, text: str, bureau: str) -> List[CreditReportMarker]:
        """Extract name variations and personal identifiers"""
        markers = []
        
        # Look for name variations
        name_patterns = [
            r'Name:\s*([A-Z\s,]+)',
            r'Also Known As:\s*([A-Z\s,]+)',
            r'Former Name:\s*([A-Z\s,]+)'
        ]
        
        for pattern in name_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                markers.append(CreditReportMarker(
                    marker_key=f'{bureau}_name_variation',
                    marker_value=match.strip(),
                    pii_classification='HIGH',
                    source_section='Personal Information'
                ))
        
        return markers
    
    def _extract_addresses(self, text: str, bureau: str) -> List[CreditReportMarker]:
        """Extract address history"""
        markers = []
        
        # Pattern for addresses (simplified)
        address_pattern = r'(\d+\s+[A-Za-z0-9\s,]+(?:Apt|Suite|#)?\s*[\d]*,\s*[A-Za-z]+,\s*[A-Z]{2}\s*\d{5})'
        
        matches = re.findall(address_pattern, text)
        for i, match in enumerate(matches):
            markers.append(CreditReportMarker(
                marker_key=f'{bureau}_address_history_{i}',
                marker_value=match.strip(),
                pii_classification='HIGH',
                source_section='Address History'
            ))
        
        return markers
    
    def _extract_employers(self, text: str, bureau: str) -> List[CreditReportMarker]:
        """Extract employer information"""
        markers = []
        
        employer_pattern = r'Employer:\s*([A-Za-z0-9\s&,]+)'
        matches = re.findall(employer_pattern, text, re.IGNORECASE)
        
        for i, match in enumerate(matches):
            markers.append(CreditReportMarker(
                marker_key=f'{bureau}_employer_{i}',
                marker_value=match.strip(),
                pii_classification='MEDIUM',
                source_section='Employment'
            ))
        
        return markers
    
    def _extract_accounts(self, text: str, bureau: str) -> List[CreditReportMarker]:
        """Extract creditor accounts"""
        markers = []
        
        # Look for creditor names and account types
        account_pattern = r'Creditor:\s*([A-Za-z0-9\s&,]+)'
        matches = re.findall(account_pattern, text, re.IGNORECASE)
        
        for i, match in enumerate(matches):
            markers.append(CreditReportMarker(
                marker_key=f'{bureau}_creditor_{i}',
                marker_value=match.strip(),
                pii_classification='MEDIUM',
                source_section='Accounts'
            ))
        
        return markers
    
    def _extract_inquiries(self, text: str, bureau: str) -> List[CreditReportMarker]:
        """Extract credit inquiries"""
        markers = []
        
        inquiry_pattern = r'Inquiry:\s*([A-Za-z0-9\s&,]+)\s+on\s+(\d{2}/\d{2}/\d{4})'
        matches = re.findall(inquiry_pattern, text, re.IGNORECASE)
        
        for i, (company, date) in enumerate(matches):
            markers.append(CreditReportMarker(
                marker_key=f'{bureau}_inquiry_{i}',
                marker_value=f'{company.strip()}|{date}',
                pii_classification='LOW',
                source_section='Inquiries'
            ))
        
        return markers
    
    async def _insert_markers(self, 
                              event_id: str, 
                              markers: List[CreditReportMarker]) -> int:
        """Insert markers into data_markers table"""
        if not markers:
            return 0
        
        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()
        
        # Prepare values for bulk insert
        values = []
        for marker in markers:
            # Encrypt the marker value
            cur.execute("""
                SELECT pgp_sym_encrypt(%s, %s)
            """, (marker.marker_value, os.getenv('DB_ENCRYPTION_KEY', 'default_key')))
            
            encrypted_value = cur.fetchone()[0]
            
            values.append((
                event_id,
                marker.marker_key,
                encrypted_value,
                marker.pii_classification
            ))
        
        # Bulk insert
        execute_values(cur, """
            INSERT INTO data_markers (
                event_id, marker_key, marker_value_encrypted, 
                pii_classification
            ) VALUES %s
        """, values)
        
        conn.commit()
        inserted_count = len(values)
        cur.close()
        conn.close()
        
        return inserted_count
    
    async def _update_event_status(self, event_id: str, status: str):
        """Update stage_event status"""
        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE stage_event 
            SET is_active = %s, updated_at = NOW()
            WHERE event_id = %s
        """, (status == 'completed', event_id))
        
        conn.commit()
        cur.close()
        conn.close()


# CLI entry point
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='AnnualCreditReport Connector')
    parser.add_argument('--identity-id', required=True, help='UUID from identity table')
    parser.add_argument('--ssn', required=True, help='Social Security Number')
    parser.add_argument('--dob', required=True, help='Date of birth (YYYY-MM-DD)')
    parser.add_argument('--address', required=True, help='JSON string with address')
    
    args = parser.parse_args()
    
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'identity_db'),
        'user': os.getenv('DB_USER', 'identity_user'),
        'password': os.getenv('DB_PASSWORD', '')
    }
    
    connector = AnnualCreditReportConnector(db_config)
    
    result = asyncio.run(connector.run(
        identity_id=args.identity_id,
        ssn=args.ssn,
        dob=args.dob,
        address=json.loads(args.address)
    ))
    
    print(json.dumps({
        'success': result.success,
        'event_id': result.event_id,
        'markers_inserted': result.markers_inserted,
        'error': result.error_message
    }, indent=2))
