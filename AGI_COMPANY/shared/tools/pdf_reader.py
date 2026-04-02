#!/usr/bin/env python3
"""
📄 PDF READER UTILITY
Extracts text and metadata from PDF files for team review
"""

import sys
import os
from pathlib import Path

def read_pdf(filepath):
    """Extract text from PDF using available libraries"""
    filepath = Path(filepath)
    
    if not filepath.exists():
        print(f"❌ File not found: {filepath}")
        return None
    
    # Try PyMuPDF first (best quality)
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return {
            'text': text,
            'pages': len(doc),
            'method': 'PyMuPDF'
        }
    except ImportError:
        pass
    
    # Try pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(filepath) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return {
            'text': text,
            'pages': len(pdf.pages),
            'method': 'pdfplumber'
        }
    except ImportError:
        pass
    
    # Try pdftotext (command line)
    import subprocess
    try:
        result = subprocess.run(
            ['pdftotext', str(filepath), '-'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return {
                'text': result.stdout,
                'pages': 'unknown',
                'method': 'pdftotext'
            }
    except FileNotFoundError:
        pass
    
    print("❌ No PDF reader available. Install with:")
    print("   pip install pymupdf")
    return None

def summarize_pdf(filepath, max_chars=3000):
    """Read PDF and return formatted summary"""
    result = read_pdf(filepath)
    
    if not result:
        return None
    
    text = result['text']
    preview = text[:max_chars]
    
    if len(text) > max_chars:
        preview += "\n\n... [truncated]"
    
    summary = f"""
📄 PDF SUMMARY: {Path(filepath).name}
═══════════════════════════════════════
Method: {result['method']}
Pages: {result['pages']}
Extracted: {len(text):,} characters

📝 CONTENT PREVIEW:
────────────────────────────────────────
{preview}
"""
    return summary

def batch_read_pdf_directory(directory):
    """Process all PDFs in a directory"""
    directory = Path(directory)
    pdfs = list(directory.glob('*.pdf'))
    
    if not pdfs:
        print(f"📂 No PDF files found in {directory}")
        return []
    
    print(f"📂 Found {len(pdfs)} PDF file(s) in {directory}\n")
    
    results = []
    for pdf in pdfs:
        summary = summarize_pdf(pdf)
        if summary:
            print(summary)
            results.append({
                'file': str(pdf),
                'summary': summary
            })
    
    return results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        # Check for attachments directory
        attach_dir = Path('/root/.openclaw/workspace/data/email_attachments')
        if attach_dir.exists():
            pdfs = list(attach_dir.glob('*.pdf'))
            if pdfs:
                print("📎 Found PDF attachments:\n")
                for pdf in pdfs:
                    print(f"File: {pdf.name}")
                    print("-" * 40)
                    result = read_pdf(pdf)
                    if result:
                        preview = result['text'][:1500]
                        print(f"Pages: {result['pages']} | Method: {result['method']}")
                        print(f"\nPreview:\n{preview}...")
                    print("\n" + "=" * 60 + "\n")
            else:
                print("📂 No PDF files found in attachments directory")
                print(f"   {attach_dir}")
        else:
            print("Usage: python3 pdf_reader.py <pdf_file>")
            print("       python3 pdf_reader.py  # auto-scan attachments")
    else:
        filepath = sys.argv[1]
        summary = summarize_pdf(filepath)
        if summary:
            print(summary)
