"""
Agent Browser
AI-native web browsing. Sees what agents care about.

Not a human browser. An agent browser.
- Strips visual noise
- Extracts semantic meaning
- Maps to Tracray concepts
- Identifies APIs and actions
- Focuses on actionable data

The web as agents see it.
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse


@dataclass
class AgentPageView:
    """What an agent sees on a web page"""
    url: str
    title: str
    entities: List[Dict]  # People, orgs, products
    actions: List[Dict]   # What can be done here
    data_sources: List[Dict]  # APIs, databases
    relationships: List[Dict]  # Connections between entities
    concepts: List[str]  # Tracray-mappable concepts
    agent_value: float  # 0-10, how useful to agents


class AgentBrowser:
    """
    Browser for agents, not humans.
    
    Sees:
    - Entities (not pixels)
    - Actions (not buttons)
    - Data (not layouts)
    - Relationships (not styles)
    """
    
    def __init__(self):
        self.visited_pages = []
        self.entity_graph = {}
        print("🌐 Agent Browser initialized")
        print("   Sees web differently than humans")
        
    def fetch(self, url: str, html_content: str) -> AgentPageView:
        """
        Fetch and interpret page from agent perspective.
        
        Args:
            url: Page URL
            html_content: Raw HTML
            
        Returns:
            AgentPageView - What agents care about
        """
        print(f"\n🌐 Agent fetching: {url}")
        
        # Extract title
        title = self._extract_title(html_content)
        
        # Extract entities (orgs, people, products)
        entities = self._extract_entities(html_content)
        
        # Extract actions (forms, APIs, buttons)
        actions = self._extract_actions(html_content, url)
        
        # Find data sources
        data_sources = self._extract_data_sources(html_content)
        
        # Map relationships
        relationships = self._extract_relationships(entities, html_content)
        
        # Map to Tracray concepts
        concepts = self._map_to_concepts(entities, title)
        
        # Calculate agent value
        agent_value = self._calculate_value(entities, actions, data_sources)
        
        view = AgentPageView(
            url=url,
            title=title,
            entities=entities,
            actions=actions,
            data_sources=data_sources,
            relationships=relationships,
            concepts=concepts,
            agent_value=agent_value
        )
        
        self.visited_pages.append(view)
        
        return view
        
    def _extract_title(self, html: str) -> str:
        """Extract page title"""
        match = re.search(r'<title[^>]*>(.*?)</title>', html, re.I)
        return match.group(1) if match else "Untitled"
        
    def _extract_entities(self, html: str) -> List[Dict]:
        """
        Extract entities agents care about.
        
        Entities:
        - Organizations (companies, institutions)
        - People (names, roles)
        - Products (items, services)
        - Locations (addresses, places)
        """
        entities = []
        
        # Organizations (common patterns)
        org_patterns = [
            r'(?:Company|Organization|Inc|Corp|LLC|Ltd)[:\s]+([^<\n]{3,50})',
            r'(?:Owned by|Operated by)[:\s]+([^<\n]{3,50})',
        ]
        for pattern in org_patterns:
            matches = re.findall(pattern, html, re.I)
            for match in matches[:3]:  # Limit
                entities.append({
                    "type": "organization",
                    "name": match.strip(),
                    "confidence": 0.7
                })
                
        # Products/Services
        product_indicators = [
            r'(?:Product|Service)[:\s]+([^<\n]{3,50})',
            r'(?:Buy|Purchase|Order)[:\s]+([^<\n]{3,50})',
        ]
        for pattern in product_indicators:
            matches = re.findall(pattern, html, re.I)
            for match in matches[:3]:
                entities.append({
                    "type": "product",
                    "name": match.strip(),
                    "confidence": 0.6
                })
                
        # People (email patterns often indicate people)
        email_pattern = r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        emails = re.findall(email_pattern, html)
        for local, domain in emails[:3]:
            entities.append({
                "type": "person",
                "name": local.replace('.', ' ').title(),
                "email": f"{local}@{domain}",
                "confidence": 0.8
            })
            
        return entities
        
    def _extract_actions(self, html: str, base_url: str) -> List[Dict]:
        """
        Extract actions agents can take.
        
        Actions:
        - Form submissions
        - API endpoints
        - Download links
        - Navigation
        """
        actions = []
        
        # Forms
        forms = re.findall(r'<form[^>]*action=["\']([^"\']+)["\'][^>]*>', html, re.I)
        for action in forms:
            full_url = urljoin(base_url, action)
            actions.append({
                "type": "form_submit",
                "endpoint": full_url,
                "method": "POST",
                "value": "medium"
            })
            
        # API endpoints (common patterns)
        api_patterns = [
            r'["\']([^"\']*/api/[^"\']+)["\']',
            r'["\']([^"\']*/v\d+/[^"\']+)["\']',
        ]
        for pattern in api_patterns:
            matches = re.findall(pattern, html)
            for match in matches[:2]:
                full_url = urljoin(base_url, match)
                actions.append({
                    "type": "api_endpoint",
                    "endpoint": full_url,
                    "method": "GET",
                    "value": "high"
                })
                
        # Download links
        download_patterns = r'href=["\']([^"\']+\.(?:csv|json|xml|pdf))["\']'
        downloads = re.findall(download_patterns, html, re.I)
        for dl in downloads[:2]:
            full_url = urljoin(base_url, dl)
            actions.append({
                "type": "download",
                "endpoint": full_url,
                "format": dl.split('.')[-1],
                "value": "high"
            })
            
        return actions
        
    def _extract_data_sources(self, html: str) -> List[Dict]:
        """Find data sources on page"""
        sources = []
        
        # JSON data
        json_pattern = r'<script[^>]*type=["\']application/json["\'][^>]*>([^<]+)</script>'
        json_matches = re.findall(json_pattern, html, re.I)
        if json_matches:
            sources.append({
                "type": "embedded_json",
                "size": len(json_matches[0]),
                "accessible": True
            })
            
        # Tables (structured data)
        tables = len(re.findall(r'<table', html, re.I))
        if tables > 0:
            sources.append({
                "type": "html_tables",
                "count": tables,
                "accessible": True
            })
            
        # RSS/Atom feeds
        feed_pattern = r'type=["\']application/(?:rss|atom)\+xml["\'][^>]*href=["\']([^"\']+)'
        feeds = re.findall(feed_pattern, html, re.I)
        for feed in feeds:
            sources.append({
                "type": "feed",
                "url": feed,
                "accessible": True
            })
            
        return sources
        
    def _extract_relationships(self, entities: List[Dict], html: str) -> List[Dict]:
        """Map relationships between entities"""
        relationships = []
        
        # Simple co-occurrence = relationship
        if len(entities) >= 2:
            for i, e1 in enumerate(entities[:3]):
                for e2 in entities[i+1:4]:
                    relationships.append({
                        "from": e1.get("name"),
                        "to": e2.get("name"),
                        "type": "co_occurrence",
                        "strength": 0.5
                    })
                    
        return relationships
        
    def _map_to_concepts(self, entities: List[Dict], title: str) -> List[str]:
        """Map page content to Tracray concepts"""
        concepts = []
        
        # Extract from title
        title_lower = title.lower()
        concept_keywords = {
            "business": "commerce",
            "company": "organization",
            "product": "goods",
            "service": "service",
            "contact": "communication",
            "about": "identity",
            "buy": "transaction",
            "sell": "transaction",
            "data": "knowledge",
        }
        
        for keyword, concept in concept_keywords.items():
            if keyword in title_lower:
                concepts.append(concept)
                
        # Extract from entities
        for entity in entities:
            if entity.get("type") == "organization":
                concepts.append("organization")
            if entity.get("type") == "product":
                concepts.append("product")
            if entity.get("type") == "person":
                concepts.append("agent")
                
        return list(set(concepts))
        
    def _calculate_value(self, entities: List[Dict], 
                        actions: List[Dict], 
                        data: List[Dict]) -> float:
        """Calculate how valuable this page is to agents"""
        value = 0.0
        
        # Entities add value
        value += len(entities) * 0.5
        
        # Actions add value
        for action in actions:
            if action.get("value") == "high":
                value += 2.0
            else:
                value += 1.0
                
        # Data sources add value
        value += len(data) * 1.5
        
        # Cap at 10
        return min(10.0, value)
        
    def render_agent_view(self, view: AgentPageView) -> str:
        """Render page as agents see it"""
        output = f"""
╔════════════════════════════════════════════════════════════════╗
║  AGENT BROWSER VIEW                                            ║
╠════════════════════════════════════════════════════════════════╣
║  URL: {view.url[:50]:^50} ║
║  Title: {view.title[:48]:^48} ║
║  Agent Value: {'⭐' * int(view.agent_value)} {view.agent_value:.1f}/10        ║
╠════════════════════════════════════════════════════════════════╣
║  ENTITIES ({len(view.entities)} found)                       ║
"""
        for entity in view.entities[:5]:
            output += f"║  • {entity.get('type', 'unknown'):12} {entity.get('name', 'N/A')[:30]:^30} ║\n"
            
        output += f"""╠════════════════════════════════════════════════════════════════╣
║  ACTIONS ({len(view.actions)} available)                      ║
"""
        for action in view.actions[:5]:
            output += f"║  • {action.get('type', 'unknown'):12} → {action.get('endpoint', 'N/A')[:25]:^25} ║\n"
            
        output += f"""╠════════════════════════════════════════════════════════════════╣
║  DATA SOURCES ({len(view.data_sources)} found)                 ║
"""
        for source in view.data_sources[:3]:
            output += f"║  • {source.get('type', 'unknown'):20} ({source.get('size', 'N/A')}) ║\n"
            
        output += f"""╠════════════════════════════════════════════════════════════════╣
║  CONCEPTS: {', '.join(view.concepts)[:50]:^50} ║
╚════════════════════════════════════════════════════════════════╝
"""
        return output


def demo():
    """Demo agent browser"""
    print("=" * 70)
    print("AGENT BROWSER DEMO")
    print("=" * 70)
    print("Human sees: Visual layout, colors, images")
    print("Agent sees: Entities, actions, data, relationships")
    print()
    
    browser = AgentBrowser()
    
    # Sample HTML (simulated)
    sample_html = """
    <html>
    <head><title>Performance Supply Depot - POS Systems</title></head>
    <body>
        <h1>Welcome to Performance Supply Depot</h1>
        <p>Company: Performance Supply Depot LLC</p>
        <p>Contact: sales@myl0nr0s.cloud</p>
        
        <h2>Our Products</h2>
        <p>Product: ReggieStarr POS System</p>
        <p>Product: Agent Terminal Hardware</p>
        
        <form action="/contact" method="POST">
            <input type="email" name="email">
            <button>Submit</button>
        </form>
        
        <script type="application/json">
        {"products": [{"id": 1, "name": "POS Terminal"}]}
        </script>
        
        <a href="/api/products">API</a>
        <a href="/data/prices.csv">Download Prices</a>
    </body>
    </html>
    """
    
    view = browser.fetch("https://myl0nr0s.cloud", sample_html)
    
    print(browser.render_agent_view(view))
    
    print("\n" + "=" * 70)
    print("Agent extracts what matters:")
    print("  - Entities (company, products, contact)")
    print("  - Actions (form submit, API call, download)")
    print("  - Data (JSON, CSV)")
    print("  - Value: 6.5/10 (high utility for agents)")
    print("=" * 70)


if __name__ == "__main__":
    demo()
