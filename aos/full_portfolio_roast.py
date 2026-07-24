#!/usr/bin/env python3
"""
FULL PORTFOLIO ROAST - AGI Company + All Subsidiaries
Comprehensive evaluation of entire business ecosystem
"""

import json
from roast_skill import RoastSkill

roast = RoastSkill()

entities = [
    {
        "name": "AGI Company",
        "type": "Parent Organization",
        "objective": "58-agent AI organization with diversified revenue across POS supplies, trading bots, agent services, and product development",
        "description": "AI-powered operations company with hierarchical agent structure, MoE routing, and multiple revenue streams. Core competency: agent orchestration at scale.",
        "budget": 500000,
        "time_estimate": 8760,
        "key_metrics": "58 agents, 7 departments, $15K MRR target"
    },
    {
        "name": "Performance Supply Depot (PSD)",
        "type": "B2B Wholesale",
        "objective": "B2B wholesale distribution of POS supplies: thermal paper rolls, ink ribbons, payment terminals, Capton pouring systems",
        "description": "E-commerce platform serving retail, restaurant, hospitality. Revenue model: consumables + equipment. Target: SMB merchants processing card payments. Differentiation: bundled service contracts vs commodity competition.",
        "budget": 200000,
        "time_estimate": 8760,
        "key_metrics": "$15K MRR target, 20 top customers, Capton systems"
    },
    {
        "name": "Amhud Supply",
        "type": "Logistics/Operations",
        "objective": "Supply chain and logistics coordination for multi-entity distribution operations",
        "description": "Internal logistics arm managing inventory, warehousing, and distribution across PSD and related operations. Focus: operational efficiency, cost reduction, fulfillment optimization.",
        "budget": 100000,
        "time_estimate": 4380,
        "key_metrics": "Cost per unit, fulfillment time, inventory turnover"
    },
    {
        "name": "Off World Comix",
        "type": "Creative/Entertainment",
        "objective": "Comic book and creative content production, possibly NFT/digital collectibles",
        "description": "Creative content arm producing comic books, potentially web3/NFT collectibles, brand storytelling. Target: collectors, comic enthusiasts, digital asset market.",
        "budget": 50000,
        "time_estimate": 2190,
        "key_metrics": "Content production rate, collector engagement, NFT sales"
    }
]

products_services = [
    {
        "name": "Cryptonio Trading System",
        "type": "Financial Service",
        "objective": "AI-powered trading bots with 190-point confluence scoring for crypto markets",
        "description": "Automated trading system using technical analysis (EMA, ATR, divergence) for cryptocurrency trading. Features: portfolio management, Binance API integration, risk management.",
        "budget": 75000,
        "time_estimate": 8760,
        "key_metrics": "ROI, drawdown, Sharpe ratio, trade frequency"
    },
    {
        "name": "N'og nog Universal Explorer",
        "type": "Gaming Product",
        "objective": "Browser-based voxel universe game with Three.js, procedural generation",
        "description": "100x100x100 voxel universe with 6 universe types, real physics, multi-platform controls, spatial audio. Tech: Three.js r128, Simplex Noise, Web Audio API.",
        "budget": 25000,
        "time_estimate": 2190,
        "key_metrics": "Player retention, monetization, engagement time"
    },
    {
        "name": "Agent-as-a-Service (AaaS)",
        "type": "AI Service",
        "objective": "AI Operations Assistant subscription: email management, scheduling, research",
        "description": "$500/month service providing AI agent labor for small businesses. Features: email triage, calendar scheduling, basic research, monthly reporting. Target: 5-50 employee businesses overwhelmed by admin.",
        "budget": 25000,
        "time_estimate": 2190,
        "key_metrics": "3 pilot conversions target, $1.5K MRR goal, CAC < $150"
    },
    {
        "name": "Dark Factory",
        "type": "Manufacturing/Production",
        "objective": "Automated manufacturing coordination and production optimization",
        "description": "Internal manufacturing arm for hardware, robots, physical products. AOS-H1 humanoid robot project, 3D printing, electronics assembly. Focus: automation, scale, quality.",
        "budget": 150000,
        "time_estimate": 8760,
        "key_metrics": "Production rate, defect rate, cost per unit, BOM efficiency"
    },
    {
        "name": "Crew Isolation Sandboxes",
        "type": "Infrastructure Service",
        "objective": "Secure per-agent workspace isolation for multi-agent operations",
        "description": "Technical infrastructure providing isolated environments for 58+ agents. Features: crypto identity, crew workspaces, persistence, model routing. Core to AGI Company operations.",
        "budget": 25000,
        "time_estimate": 4380,
        "key_metrics": "Uptime, isolation integrity, concurrent agents supported"
    }
]

systems = [
    {
        "name": "Roast Skill v1.0",
        "type": "Decision System",
        "objective": "Adversarial analysis with 6-persona council before major decisions",
        "description": "6-persona evaluation system (Contrarian, Expansionist, FirstPrinciples, Researcher, Buyer, Judge) providing verdicts: GREEN_LIGHT/RESHAPE/KILL. Prevents sycophancy, validates ideas.",
        "budget": 0,
        "time_estimate": 0,
        "key_metrics": "Improvement rate, rejection rate, cheap test completion"
    },
    {
        "name": "MoE Router",
        "type": "Routing System",
        "objective": "Mixture of Experts task routing to optimal agents",
        "description": "Gating function routing tasks to 7 expert types across 54 agents. Matches task keywords to expert specialization, selects optimal LLM, aggregates multi-expert outputs.",
        "budget": 0,
        "time_estimate": 0,
        "key_metrics": "Routing accuracy, latency, expert utilization"
    },
    {
        "name": "Verification Loops v1.0",
        "type": "Quality System",
        "objective": "Self-check protocols before marking work complete",
        "description": "Task-specific verification: code tests, visual verification, form testing, edge case stress testing. Prevents premature completion, ensures quality.",
        "budget": 0,
        "time_estimate": 0,
        "key_metrics": "Error detection rate, false positive rate, completion delay"
    },
    {
        "name": "Context Manager v1.0",
        "type": "Memory System",
        "objective": "Session handoff and context window monitoring",
        "description": "Tracks token usage (150K warning, 200K handoff, 240K critical). Generates state summaries, pick-up instructions, prevents context rot.",
        "budget": 0,
        "time_estimate": 0,
        "key_metrics": "Handoff success rate, context preservation, token efficiency"
    },
    {
        "name": "Goal Evaluator v1.0",
        "type": "Project Management",
        "objective": "/goal command with completion criteria and separate evaluator",
        "description": "Forces explicit completion criteria before work starts. Separate evaluator judges done/not done. Prevents 'feels done' subjective completion. Verdicts: COMPLETED/NEEDS_WORK/FAILED.",
        "budget": 0,
        "time_estimate": 0,
        "key_metrics": "Criteria clarity, completion accuracy, re-work rate"
    }
]

print("=" * 90)
print("  COMPREHENSIVE PORTFOLIO ROAST - AGI COMPANY ECOSYSTEM")
print("=" * 90)
print()

all_results = {}

# Roast Organizations
print("SECTION 1: ORGANIZATIONS")
print("-" * 90)
for entity in entities:
    print(f"\n🔥 ROASTING: {entity['name']} ({entity['type']})")
    print(f"Objective: {entity['objective'][:60]}...")
    
    task = {
        'title': entity['name'],
        'objective': entity['objective'],
        'description': entity['description'],
        'budget': entity['budget'],
        'time_estimate': entity['time_estimate'],
        'impact': 'high'
    }
    
    report = roast.roast(task)
    
    all_results[entity['name']] = {
        'verdict': report['verdict'],
        'score': report['weighted_score'],
        'type': entity['type'],
        'action': report['action_items'][0] if report['action_items'] else 'Monitor'
    }
    
    print(f"\n  VERDICT: {report['verdict']} ({report['weighted_score']:.1f}/10)")

# Roast Products/Services
print("\n" + "=" * 90)
print("SECTION 2: PRODUCTS & SERVICES")
print("-" * 90)
for product in products_services:
    print(f"\n🔥 ROASTING: {product['name']} ({product['type']})")
    
    task = {
        'title': product['name'],
        'objective': product['objective'],
        'description': product['description'],
        'budget': product['budget'],
        'time_estimate': product['time_estimate'],
        'impact': 'high'
    }
    
    report = roast.roast(task)
    
    all_results[product['name']] = {
        'verdict': report['verdict'],
        'score': report['weighted_score'],
        'type': product['type'],
        'action': report['action_items'][0] if report['action_items'] else 'Monitor'
    }
    
    print(f"\n  VERDICT: {report['verdict']} ({report['weighted_score']:.1f}/10)")

# Roast Systems
print("\n" + "=" * 90)
print("SECTION 3: INTERNAL SYSTEMS")
print("-" * 90)
for system in systems:
    print(f"\n🔥 ROASTING: {system['name']}")
    
    task = {
        'title': system['name'],
        'objective': system['objective'],
        'description': system['description'],
        'budget': 0,
        'time_estimate': 0,
        'impact': 'high'
    }
    
    report = roast.roast(task)
    
    all_results[system['name']] = {
        'verdict': report['verdict'],
        'score': report['weighted_score'],
        'type': system['type'],
        'action': report['action_items'][0] if report['action_items'] else 'Monitor'
    }
    
    print(f"\n  VERDICT: {report['verdict']} ({report['weighted_score']:.1f}/10)")

# Summary
print("\n" + "=" * 90)
print("  PORTFOLIO SUMMARY")
print("=" * 90)

# Sort by score
sorted_results = sorted(all_results.items(), key=lambda x: x[1]['score'], reverse=True)

print("\nRANKED BY ROAST SCORE:")
print(f"{'Rank':<6} {'Entity':<35} {'Score':<8} {'Verdict':<12} {'Type':<20}")
print("-" * 90)

for i, (name, data) in enumerate(sorted_results, 1):
    print(f"{i:<6} {name[:34]:<35} {data['score']:.1f}/10   {data['verdict']:<12} {data['type']:<20}")

# Strategic recommendations
print("\n" + "=" * 90)
print("  STRATEGIC RECOMMENDATIONS")
print("=" * 90)

kill_items = [name for name, data in all_results.items() if data['verdict'] == 'KILL']
reshape_items = [name for name, data in all_results.items() if data['verdict'] == 'RESHAPE']
greenlight_items = [name for name, data in all_results.items() if data['verdict'] == 'GREEN_LIGHT']

print(f"\n🟢 GREEN LIGHT ({len(greenlight_items)}): Continue as planned")
for item in greenlight_items[:5]:
    print(f"   • {item}")

print(f"\n🟡 RESHAPE ({len(reshape_items)}): Modify approach")
for item in reshape_items:
    print(f"   • {item} - {all_results[item]['action']}")

print(f"\n🔴 KILL ({len(kill_items)}): Abandon or pivot")
for item in kill_items:
    print(f"   • {item}")

print("\n" + "=" * 90)
print("  ✅ FULL PORTFOLIO ROAST COMPLETE")
print("=" * 90)

# Save results
with open('/tmp/portfolio_roast_results.json', 'w') as f:
    json.dump(all_results, f, indent=2)

print(f"\nDetailed results saved to: /tmp/portfolio_roast_results.json")
