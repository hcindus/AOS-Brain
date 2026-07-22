#!/usr/bin/env python3
"""
AOS Brain Visual Knowledge Graph v1.0
Generates Obsidian-compatible markdown with Mermaid diagrams
"""

import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
WIKI_DIR = WORKSPACE / "wiki"
MEMORY_DIR = WORKSPACE / "memory"
GRAPH_DIR = WORKSPACE / "visual-graph"

class KnowledgeGraph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.categories = defaultdict(list)
        
    def scan_memory(self):
        """Extract entities and relationships from memory files"""
        print("📁 Scanning memory files...")
        
        for mem_file in MEMORY_DIR.glob("*.md"):
            content = mem_file.read_text()
            date = mem_file.stem
            
            # Extract entities (bold text, links, system names)
            systems = re.findall(r'\*\*([^*]+)\*\*|\[([^\]]+)\]|(?:🧠|🫀|🫁|💾)\s*(\w+)', content)
            topics = re.findall(r'#\s*(\w+)', content)
            
            # Create memory node
            self.nodes.append({
                "id": f"mem_{date}",
                "label": f"Memory {date}",
                "type": "memory",
                "date": date,
                "file": str(mem_file.relative_to(WORKSPACE))
            })
            
            # Link to systems mentioned
            system_names = ['Brain', 'BHSI', 'Mission Control', 'Thyroid', 'Liver', 'Kidneys', 'Lungs']
            for sys_name in system_names:
                if sys_name.lower() in content.lower():
                    self.edges.append({
                        "source": f"mem_{date}",
                        "target": f"sys_{sys_name.lower().replace(' ', '_')}",
                        "type": "mentions"
                    })
    
    def scan_skills(self):
        """Extract skills as nodes"""
        print("🔧 Scanning skills...")
        
        skills_dir = WORKSPACE / "skills"
        for skill_file in skills_dir.rglob("SKILL.md"):
            skill_name = skill_file.parent.name
            
            self.nodes.append({
                "id": f"skill_{skill_name}",
                "label": skill_name.replace('-', ' ').title(),
                "type": "skill",
                "file": str(skill_file.relative_to(WORKSPACE))
            })
            
            self.categories["skills"].append(skill_name)
    
    def scan_agents(self):
        """Extract Society Agents as nodes"""
        print("🤖 Scanning Society Agents...")
        
        agents = ["patricia-factory", "forge-factory", "chelios-security", 
                  "jordan-office", "aurora-tasks"]
        
        for agent in agents:
            self.nodes.append({
                "id": f"agent_{agent}",
                "label": agent.replace('-', ' ').title(),
                "type": "agent"
            })
            
            # Link agents to skills they might use
            self.edges.append({
                "source": f"agent_{agent}",
                "target": "sys_mission_control",
                "type": "uses"
            })
    
    def scan_systems(self):
        """Define system nodes"""
        print("🧠 Defining system nodes...")
        
        systems = [
            ("sys_brain_v45", "Brain v4.5", "core"),
            ("sys_bhsi_v4", "BHSI v4", "core"),
            ("sys_mission_control", "Mission Control", "interface"),
            ("sys_thyroid", "Thyroid v1.2", "organ"),
            ("sys_liver", "Liver v1.0", "organ"),
            ("sys_kidneys", "Kidneys v1.0", "organ"),
            ("sys_lungs", "Lungs v1.0", "organ"),
        ]
        
        for sys_id, label, cat in systems:
            self.nodes.append({
                "id": sys_id,
                "label": label,
                "type": cat
            })
            self.categories[cat].append(label)
        
        # Define system relationships
        self.edges.extend([
            {"source": "sys_bhsi_v4", "target": "sys_brain_v45", "type": "feeds"},
            {"source": "sys_liver", "target": "sys_brain_v45", "type": "filters"},
            {"source": "sys_brain_v45", "target": "sys_kidneys", "type": "drains"},
            {"source": "sys_lungs", "target": "sys_brain_v45", "type": "oxygenates"},
            {"source": "sys_thyroid", "target": "sys_brain_v45", "type": "regulates"},
        ])
    
    def scan_integrations(self):
        """Extract external integrations"""
        print("🔌 Scanning integrations...")
        
        integrations = [
            ("int_ollama", "Ollama/Mortimer", "ai"),
            ("int_sendgrid", "SendGrid", "communication"),
            ("int_hostinger", "Hostinger", "hosting"),
        ]
        
        for int_id, label, cat in integrations:
            self.nodes.append({
                "id": int_id,
                "label": label,
                "type": "integration"
            })
            
            self.edges.append({
                "source": "sys_brain_v45",
                "target": int_id,
                "type": "connects"
            })
    
    def generate_mermaid(self):
        """Generate Mermaid flowchart"""
        print("📊 Generating Mermaid diagram...")
        
        mermaid = ["```mermaid"]
        mermaid.append("graph TB")
        mermaid.append("")
        
        # Define subgraphs by category
        subgraphs = {
            "core": "Core Systems",
            "organ": "Biological Pipeline",
            "agent": "Society Agents",
            "skill": "Skills",
            "integration": "External APIs"
        }
        
        for node_type, title in subgraphs.items():
            nodes_of_type = [n for n in self.nodes if n.get("type") == node_type]
            if nodes_of_type:
                mermaid.append(f"    subgraph {title}")
                for node in nodes_of_type:
                    safe_id = re.sub(r'[^a-zA-Z0-9_]', '_', node['id'])
                    mermaid.append(f"        {safe_id}[{node['label']}]")
                mermaid.append("    end")
                mermaid.append("")
        
        # Add edges
        for edge in self.edges:
            src = re.sub(r'[^a-zA-Z0-9_]', '_', edge['source'])
            tgt = re.sub(r'[^a-zA-Z0-9_]', '_', edge['target'])
            mermaid.append(f"    {src} -->|{edge['type']}| {tgt}")
        
        mermaid.append("```")
        
        return "\n".join(mermaid)
    
    def generate_obsidian_vault(self):
        """Generate Obsidian-compatible vault structure"""
        print("📦 Generating Obsidian vault...")
        
        vault_dir = GRAPH_DIR / "obsidian-vault"
        vault_dir.mkdir(parents=True, exist_ok=True)
        
        # Create vault root
        readme = vault_dir / "README.md"
        readme.write_text(f"""# AOS Brain Knowledge Graph

**Generated:** {datetime.now().isoformat()}

## Navigation

- [[graph-view]] - Visual relationship diagram
- [[systems-index]] - All core systems
- [[agents-index]] - Society Agents
- [[skills-index]] - Available skills
- [[timeline]] - Chronological memory view

## Quick Stats

- **Total Nodes:** {len(self.nodes)}
- **Total Relationships:** {len(self.edges)}
- **Categories:** {', '.join(self.categories.keys())}
""")
        
        # Graph view with Mermaid
        graph_view = vault_dir / "graph-view.md"
        graph_view.write_text(f"""# Knowledge Graph Visualization

{self.generate_mermaid()}

## Statistics

| Metric | Count |
|--------|-------|
| Nodes | {len(self.nodes)} |
| Edges | {len(self.edges)} |
| Systems | {len(self.categories.get('core', []))} |
| Agents | {len(self.categories.get('agent', []))} |
| Skills | {len(self.categories.get('skills', []))} |
""")
        
        # Systems index
        systems_idx = vault_dir / "systems-index.md"
        systems_content = ["# Systems Index\n"]
        for sys_name in self.categories.get('core', []):
            systems_content.append(f"- [[{sys_name.lower().replace(' ', '_')}|{sys_name}]]")
        systems_idx.write_text("\n".join(systems_content))
        
        # Agents index
        agents_idx = vault_dir / "agents-index.md"
        agents_content = ["# Society Agents Index\n"]
        for agent_name in self.categories.get('agent', []):
            agents_content.append(f"- [[{agent_name}|{agent_name.replace('-', ' ').title()}]]")
        agents_idx.write_text("\n".join(agents_content))
        
        # Skills index
        skills_idx = vault_dir / "skills-index.md"
        skills_content = ["# Skills Index\n"]
        for skill_name in self.categories.get('skills', []):
            skills_content.append(f"- [[{skill_name}|{skill_name.replace('-', ' ').title()}]]")
        skills_idx.write_text("\n".join(skills_content))
        
        # Timeline
        timeline = vault_dir / "timeline.md"
        memories = [n for n in self.nodes if n.get("type") == "memory"]
        memories.sort(key=lambda x: x.get("date", ""), reverse=True)
        
        timeline_content = ["# Memory Timeline\n"]
        for mem in memories[:30]:  # Last 30 days
            timeline_content.append(f"- **{mem['date']}**: [[{mem['file']}|View Memory]]")
        timeline.write_text("\n".join(timeline_content))
        
        # JSON export for programmatic use
        graph_json = vault_dir / "graph.json"
        graph_data = {
            "nodes": self.nodes,
            "edges": self.edges,
            "generated": datetime.now().isoformat(),
            "stats": {
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "categories": {k: len(v) for k, v in self.categories.items()}
            }
        }
        graph_json.write_text(json.dumps(graph_data, indent=2))
        
        return vault_dir
    
    def generate_html_visualization(self):
        """Generate interactive HTML visualization using D3.js"""
        print("🌐 Generating HTML visualization...")
        
        html_file = GRAPH_DIR / "knowledge-graph.html"
        
        graph_data = {
            "nodes": self.nodes,
            "links": self.edges
        }
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>AOS Brain Knowledge Graph</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {{
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #eee;
        }}
        #graph {{
            width: 100vw;
            height: 100vh;
        }}
        .node {{
            cursor: pointer;
        }}
        .node circle {{
            stroke: #fff;
            stroke-width: 2px;
        }}
        .node text {{
            font-size: 12px;
            fill: #eee;
            text-anchor: middle;
            pointer-events: none;
        }}
        .link {{
            stroke: #444;
            stroke-opacity: 0.6;
        }}
        .link-label {{
            font-size: 10px;
            fill: #888;
        }}
        #sidebar {{
            position: fixed;
            right: 0;
            top: 0;
            width: 300px;
            height: 100vh;
            background: #16213e;
            padding: 20px;
            overflow-y: auto;
            border-left: 1px solid #444;
        }}
        h1 {{
            font-size: 18px;
            margin-bottom: 20px;
            color: #e94560;
        }}
        .stats {{
            margin-bottom: 20px;
        }}
        .stat {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #444;
        }}
        .legend {{
            margin-top: 20px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            margin: 8px 0;
        }}
        .legend-color {{
            width: 16px;
            height: 16px;
            border-radius: 50%;
            margin-right: 10px;
        }}
    </style>
</head>
<body>
    <div id="graph"></div>
    <div id="sidebar">
        <h1>🧠 AOS Brain Knowledge Graph</h1>
        <div class="stats">
            <div class="stat"><span>Total Nodes:</span><span>{len(self.nodes)}</span></div>
            <div class="stat"><span>Relationships:</span><span>{len(self.edges)}</span></div>
            <div class="stat"><span>Systems:</span><span>{len(self.categories.get('core', []))}</span></div>
            <div class="stat"><span>Agents:</span><span>{len(self.categories.get('agent', []))}</span></div>
            <div class="stat"><span>Skills:</span><span>{len(self.categories.get('skills', []))}</span></div>
        </div>
        <div class="legend">
            <h3>Legend</h3>
            <div class="legend-item"><div class="legend-color" style="background:#e94560"></div>Core Systems</div>
            <div class="legend-item"><div class="legend-color" style="background:#0f3460"></div>Organs</div>
            <div class="legend-item"><div class="legend-color" style="background:#16c79a"></div>Agents</div>
            <div class="legend-item"><div class="legend-color" style="background:#f9a825"></div>Skills</div>
            <div class="legend-item"><div class="legend-color" style="background:#7c4dff"></div>Integrations</div>
            <div class="legend-item"><div class="legend-color" style="background:#78909c"></div>Memory</div>
        </div>
        <p style="margin-top:30px;font-size:12px;color:#888;">
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </p>
    </div>

    <script>
        const data = {json.dumps(graph_data, indent=2)};
        
        const width = window.innerWidth - 300;
        const height = window.innerHeight;
        
        const colorScale = {{
            'core': '#e94560',
            'organ': '#0f3460', 
            'agent': '#16c79a',
            'skill': '#f9a825',
            'integration': '#7c4dff',
            'memory': '#78909c',
            'interface': '#ff7043'
        }};
        
        const svg = d3.select("#graph")
            .append("svg")
            .attr("width", width)
            .attr("height", height);
        
        const simulation = d3.forceSimulation(data.nodes)
            .force("link", d3.forceLink(data.links).id(d => d.id).distance(100))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide().radius(50));
        
        // Links
        const link = svg.append("g")
            .selectAll("line")
            .data(data.links)
            .enter()
            .append("line")
            .attr("class", "link")
            .attr("stroke-width", 2);
        
        // Link labels
        const linkLabel = svg.append("g")
            .selectAll("text")
            .data(data.links)
            .enter()
            .append("text")
            .attr("class", "link-label")
            .text(d => d.type)
            .attr("text-anchor", "middle");
        
        // Nodes
        const node = svg.append("g")
            .selectAll("g")
            .data(data.nodes)
            .enter()
            .append("g")
            .attr("class", "node")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));
        
        node.append("circle")
            .attr("r", d => d.type === 'core' ? 25 : 15)
            .attr("fill", d => colorScale[d.type] || '#999');
        
        node.append("text")
            .attr("dy", d => d.type === 'core' ? 35 : 25)
            .text(d => d.label.length > 15 ? d.label.substring(0, 12) + '...' : d.label);
        
        simulation.on("tick", () => {{
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
            
            linkLabel
                .attr("x", d => (d.source.x + d.target.x) / 2)
                .attr("y", d => (d.source.y + d.target.y) / 2);
            
            node.attr("transform", d => `translate(${{d.x}},${{d.y}})`);
        }});
        
        function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }}
        
        function dragged(event, d) {{
            d.fx = event.x;
            d.fy = event.y;
        }}
        
        function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }}
        
        // Zoom
        const zoom = d3.zoom()
            .scaleExtent([0.1, 4])
            .on("zoom", (event) => {{
                svg.selectAll("g").attr("transform", event.transform);
            }});
        
        svg.call(zoom);
    </script>
</body>
</html>
"""
        
        html_file.write_text(html_content)
        return html_file
    
    def build(self):
        """Build complete knowledge graph"""
        print("🔨 Building AOS Brain Knowledge Graph...\n")
        
        self.scan_systems()
        self.scan_agents()
        self.scan_integrations()
        self.scan_skills()
        self.scan_memory()
        
        print(f"\n📊 Discovered:")
        print(f"   {len(self.nodes)} nodes")
        print(f"   {len(self.edges)} relationships")
        print(f"   {len(self.categories)} categories")
        
        vault_dir = self.generate_obsidian_vault()
        html_file = self.generate_html_visualization()
        
        print(f"\n✅ Knowledge Graph generated!")
        print(f"   Obsidian vault: {vault_dir}")
        print(f"   Interactive HTML: {html_file}")
        print(f"   JSON data: {vault_dir}/graph.json")
        
        return vault_dir, html_file

if __name__ == "__main__":
    graph = KnowledgeGraph()
    graph.build()
