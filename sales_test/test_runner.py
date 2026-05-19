"""
SALES TEST ORCHESTRATOR
Main system to run complete sales testing with all agents
Generates ~21 emails, creates PDF brochures, and runs customer simulations
"""

import sys
import json
import random
from datetime import datetime
from pathlib import Path

# Import agent emails
sys.path.insert(0, '/root/.openclaw/workspace/sales_test')
from agents.miles_emails import MILES_EMAILS
from agents.clippy_emails import CLIPPY_EMAILS
from agents.pulp_emails import PULP_EMAILS
from agents.jane_emails import JANE_EMAILS
from agents.marketing_emails import MARKETING_EMAILS
from customer_sim.customer_responder import CustomerResponder, TestCustomerGenerator, run_test_simulation

def get_all_emails():
    """Collect all emails from all agents"""
    all_emails = []
    
    # Sales Team Emails
    all_emails.extend([{**e, "category": "sales", "team": "Sales"} for e in MILES_EMAILS])
    all_emails.extend([{**e, "category": "sales", "team": "Sales"} for e in CLIPPY_EMAILS])
    all_emails.extend([{**e, "category": "sales", "team": "Sales"} for e in PULP_EMAILS])
    all_emails.extend([{**e, "category": "sales", "team": "Sales"} for e in JANE_EMAILS])
    
    # Marketing Emails
    all_emails.extend([{**e, "category": "marketing", "team": "Marketing"} for e in MARKETING_EMAILS])
    
    return all_emails

def count_emails():
    """Count emails by agent"""
    counts = {
        "Miles": len(MILES_EMAILS),
        "Clippy-42": len(CLIPPY_EMAILS),
        "Pulp": len(PULP_EMAILS),
        "Jane": len(JANE_EMAILS),
        "Marketing": len(MARKETING_EMAILS)
    }
    counts["Total"] = sum(counts.values())
    return counts

def print_email_inventory():
    """Print inventory of all available emails"""
    print("\n" + "=" * 80)
    print("EMAIL INVENTORY")
    print("=" * 80 + "\n")
    
    counts = count_emails()
    
    print(f"{'Agent':<15} {'Count':<8} {'Emails'}")
    print("-" * 80)
    
    for agent, count in counts.items():
        if agent != "Total":
            print(f"{agent:<15} {count:<8}", end="")
            
            # List email names
            if agent == "Miles":
                emails = [e["name"] for e in MILES_EMAILS]
            elif agent == "Clippy-42":
                emails = [e["name"] for e in CLIPPY_EMAILS]
            elif agent == "Pulp":
                emails = [e["name"] for e in PULP_EMAILS]
            elif agent == "Jane":
                emails = [e["name"] for e in JANE_EMAILS]
            else:
                emails = [e["name"] for e in MARKETING_EMAILS]
            
            print(f"  {', '.join(emails)}")
    
    print("-" * 80)
    print(f"{'TOTAL':<15} {counts['Total']:<8}")
    print("=" * 80)
    
    return counts

def generate_test_campaign_sequence(customer_profile="The Eager Buyer"):
    """
    Generate a complete 7-email sales sequence for testing
    Follows typical sales flow: Cold > Qualify > Discovery > Close > Onboard > Retain
    """
    sequence = []
    
    # Email 1: Miles - Cold Outreach
    sequence.append(MILES_EMAILS[0])  # Cold Outreach
    
    # Email 2: Clippy-42 - Research-Based Intro
    sequence.append(CLIPPY_EMAILS[0])  # Research-Based Intro
    
    # Email 3: Miles - Value Add (Free Sample)
    sequence.append(MILES_EMAILS[1])  # Value Add
    
    # Email 4: Clippy-42 - Warm Handoff
    sequence.append(CLIPPY_EMAILS[1])  # Handoff
    
    # Email 5: Pulp - Discovery Call Follow-up
    sequence.append(PULP_EMAILS[0])  # Discovery
    
    # Email 6: Pulp - Price Objection Handler
    sequence.append(PULP_EMAILS[1])  # Price handling
    
    # Email 7: Pulp - Welcome (Closed Won)
    sequence.append(PULP_EMAILS[3])  # Welcome/Onboarding
    
    return sequence

def generate_full_campaign_test(customer_profile="The Eager Buyer"):
    """
    Generate a full 21-email campaign for comprehensive testing
    Tests all agents and all email types
    """
    sequence = []
    
    # WAVE 1: Prospecting (5 emails)
    sequence.append(MILES_EMAILS[0])      # Cold outreach
    sequence.append(CLIPPY_EMAILS[0])     # Research intro
    sequence.append(MILES_EMAILS[1])      # Free sample
    sequence.append(CLIPPY_EMAILS[2])     # Resource follow-up
    sequence.append(MILES_EMAILS[2])      # Breakup
    
    # WAVE 2: Qualification (5 emails)
    sequence.append(CLIPPY_EMAILS[1])     # Warm handoff
    sequence.append(MILES_EMAILS[3])      # Thermal paper product
    sequence.append(PULP_EMAILS[0])       # Discovery/proposal
    sequence.append(PULP_EMAILS[1])       # Price objection handler
    sequence.append(PULP_EMAILS[2])       # Urgency close
    
    # WAVE 3: Post-Sale (5 emails)
    sequence.append(PULP_EMAILS[3])       # Welcome/onboarding
    sequence.append(JANE_EMAILS[0])       # 30-day check-in
    sequence.append(JANE_EMAILS[1])       # Upsell to enterprise
    sequence.append(JANE_EMAILS[2])       # Reorder reminder
    sequence.append(JANE_EMAILS[3])       # Anniversary
    
    # WAVE 4: Marketing/Retention (6 emails)
    sequence.append(MARKETING_EMAILS[0])  # Product launch
    sequence.append(MARKETING_EMAILS[1])  # Newsletter
    sequence.append(MILES_EMAILS[4])      # Referral request
    sequence.append(MARKETING_EMAILS[3])  # Case study
    sequence.append(MARKETING_EMAILS[2])  # Webinar
    sequence.append(MARKETING_EMAILS[4])  # Survey
    
    return sequence

def print_campaign_details(sequence):
    """Print details of a campaign sequence"""
    print("\n" + "=" * 80)
    print(f"CAMPAIGN SEQUENCE ({len(sequence)} EMAILS)")
    print("=" * 80 + "\n")
    
    current_wave = None
    wave_sizes = [5, 5, 5, 6]
    wave_names = ["WAVE 1: Prospecting", "WAVE 2: Qualification", "WAVE 3: Post-Sale", "WAVE 4: Marketing"]
    
    email_idx = 0
    for wave_num, (wave_name, wave_size) in enumerate(zip(wave_names, wave_sizes), 1):
        print(f"\n{wave_name}")
        print("-" * 80)
        
        for i in range(wave_size):
            if email_idx >= len(sequence):
                break
            
            email = sequence[email_idx]
            print(f"  {email_idx + 1:2d}. [{email.get('agent', 'Unknown'):<12}] {email.get('name', 'Unknown')[:40]}")
            email_idx += 1
    
    print("\n" + "=" * 80)

def run_full_simulation(num_customers=7, save_results=True):
    """
    Run complete simulation with PDF generation and customer responses
    
    Args:
        num_customers: Number of customer personas to test (default 7 for all profiles)
        save_results: Whether to save results to file
    """
    print("\n" + "=" * 80)
    print("AGI COMPANY SALES TEAM EMAIL TESTING SYSTEM")
    print("=" * 80)
    
    # Show email inventory
    counts = print_email_inventory()
    
    # Generate full campaign
    print("\n[+] Generating full 21-email campaign sequence...")
    campaign = generate_full_campaign_test()
    print_campaign_details(campaign)
    
    # Try to generate PDF brochures
    print("\n[+] Generating PDF brochures...")
    try:
        from brochures.pdf_generator import BrochureGenerator
        gen = BrochureGenerator()
        
        brochure_paths = {
            "datadepot": gen.generate_datadepot_brochure(
                customer_name="Test Customer",
                territory="Los Angeles County"
            ),
            "pos_supplies": gen.generate_pos_supplies_brochure(
                customer_name="Test Customer"
            ),
            "combined": gen.generate_combined_brochure(
                customer_name="Test Customer",
                territory="Los Angeles County"
            )
        }
        print("\n  ✅ PDF brochures generated successfully")
        for name, path in brochure_paths.items():
            print(f"     - {name}: {path}")
    except ImportError as e:
        print(f"\n  ⚠️  PDF generation requires reportlab: pip install reportlab")
        print(f"     Error: {e}")
        brochure_paths = {}
    
    # Run customer simulations
    print("\n[+] Running customer simulations...")
    print("\n" + "=" * 80)
    print("CUSTOMER PERSONA PROFILES")
    print("=" * 80)
    
    from customer_sim.customer_responder import CustomerProfile
    
    for i, profile in enumerate(CustomerProfile.PROFILES, 1):
        print(f"\n{i}. {profile['name']}")
        print(f"   Description: {profile['description']}")
        print(f"   Openness: {profile['openness']*100:.0f}% | Price Sensitivity: {profile['price_sensitivity']*100:.0f}% | Decision Speed: {profile['decision_speed']*100:.0f}%")
    
    # Run simulation
    results = run_test_simulation(campaign, num_customers=num_customers)
    
    # Save results
    if save_results:
        results_file = Path("/root/.openclaw/workspace/sales_test/results")
        results_file.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save simulation results
        with open(results_file / f"simulation_results_{timestamp}.json", 'w') as f:
            json.dump({
                "timestamp": timestamp,
                "total_emails": len(campaign),
                "customer_count": num_customers,
                "results": results
            }, f, indent=2)
        
        # Save campaign sequence
        with open(results_file / f"campaign_sequence_{timestamp}.json", 'w') as f:
            json.dump({
                "timestamp": timestamp,
                "campaign": [
                    {
                        "id": e.get("id"),
                        "name": e.get("name"),
                        "agent": e.get("agent"),
                        "stage": e.get("stage"),
                        "subject": e.get("subject"),
                        "variables": e.get("variables")
                    } for e in campaign
                ]
            }, f, indent=2)
        
        print(f"\n\n💾 Results saved to:")
        print(f"   - {results_file}/simulation_results_{timestamp}.json")
        print(f"   - {results_file}/campaign_sequence_{timestamp}.json")
    
    # Final summary
    print("\n" + "=" * 80)
    print("TESTING COMPLETE")
    print("=" * 80)
    print(f"\n📧 Total Emails: {len(campaign)}")
    print(f"👥 Customer Personas Tested: {num_customers}")
    print(f"📄 PDF Brochures Generated: {len(brochure_paths) if brochure_paths else 'N/A (reportlab not installed)'}")
    print(f"\nEmail Breakdown:")
    print(f"  - Miles (Primary Sales): 5 emails")
    print(f"  - Clippy-42 (Assistant): 4 emails")
    print(f"  - Pulp (Closer): 4 emails")
    print(f"  - Jane (Nurturer): 4 emails")
    print(f"  - Marketing Team: 5 emails")
    print(f"  - TOTAL: 21+ emails")
    
    return results

def preview_email(email_data, variables=None):
    """
    Preview a single email with variable substitution
    
    Args:
        email_data: Email template dict
        variables: Dict of variable values
    """
    if variables is None:
        variables = {
            "First_Name": "Alex",
            "Company": "Tech Solutions Inc",
            "POS_Focus": "restaurant POS systems",
            "County": "Orange",
            "State": "CA",
            "Cuisine_Type": "Italian",
            "City": "Irvine",
            "Competitor_System": "Aloha",
            "Top_Competitor": "POSPro",
            "Reference_Company": "RestaurantTech",
            "Customer_ID": "CUST001",
            "Close_Rate": "15",
            "Average_Deal_Value": "$5,000",
            "Projected_Deals": "75",
            "Projected_Revenue": "$375,000",
            "ROI_Percentage": "126000"
        }
    
    subject = email_data.get("subject", "")
    body = email_data.get("body_html", "")
    
    # Substitute variables
    for var, val in variables.items():
        subject = subject.replace(f"{{{{{var}}}}}", str(val))
        body = body.replace(f"{{{{{var}}}}}", str(val))
    
    print("\n" + "=" * 80)
    print(f"EMAIL PREVIEW: {email_data.get('name', 'Unknown')}")
    print(f"Agent: {email_data.get('agent', 'Unknown')} | Stage: {email_data.get('stage', 'Unknown')}")
    print("=" * 80)
    print(f"\nSubject: {subject}")
    print(f"\n{body[:500]}..." if len(body) > 500 else f"\n{body}")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AGI Company Sales Team Email Testing")
    parser.add_argument("--inventory", action="store_true", help="Show email inventory only")
    parser.add_argument("--preview", type=str, help="Preview specific email by ID (e.g., miles_01_cold)")
    parser.add_argument("--customers", type=int, default=7, help="Number of customer personas to test")
    parser.add_argument("--no-pdf", action="store_true", help="Skip PDF generation")
    parser.add_argument("--quick", action="store_true", help="Quick test with 7-email sequence")
    
    args = parser.parse_args()
    
    if args.inventory:
        print_email_inventory()
    elif args.preview:
        all_emails = get_all_emails()
        email = next((e for e in all_emails if e.get("id") == args.preview), None)
        if email:
            preview_email(email)
        else:
            print(f"Email '{args.preview}' not found.")
            print(f"Available IDs: {[e.get('id') for e in all_emails]}")
    elif args.quick:
        print("Running quick test with 7-email sequence...")
        campaign = generate_test_campaign_sequence()
        run_test_simulation(campaign, num_customers=3)
    else:
        run_full_simulation(num_customers=args.customers)