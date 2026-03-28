#!/usr/bin/env python3
"""
Coding Curriculum for Mylonen + R2.

Teaches website design, vibe coding, and programming through stomach-brain pipeline.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.stomach_auto_feeder_full import StomachAutoFeederFull


class CodingCurriculum:
    """Comprehensive coding education for agents."""
    
    def __init__(self):
        self.feeder = StomachAutoFeederFull()
        self.lessons = []
        
    def get_web_design_lessons(self):
        """Website design principles."""
        lessons = [
            # HTML Fundamentals
            ("HTML: HyperText Markup Language - structure of web pages", "web_html"),
            ("HTML tags: <html>, <head>, <body>, <div>, <span>, <p>, <h1>-<h6>", "web_html"),
            ("HTML semantic elements: <header>, <nav>, <main>, <article>, <section>, <footer>", "web_html"),
            ("HTML forms: <form>, <input>, <textarea>, <button>, <select>, <label>", "web_html"),
            ("HTML attributes: id, class, style, src, href, alt, title", "web_html"),
            
            # CSS Fundamentals
            ("CSS: Cascading Style Sheets - presentation and styling", "web_css"),
            ("CSS selectors: element, .class, #id, [attribute], :hover, :focus", "web_css"),
            ("CSS box model: content, padding, border, margin", "web_css"),
            ("CSS Flexbox: display:flex, justify-content, align-items, flex-direction", "web_css"),
            ("CSS Grid: display:grid, grid-template-columns, grid-template-rows, gap", "web_css"),
            ("CSS responsive: media queries @media, mobile-first design", "web_css"),
            ("CSS animations: @keyframes, transition, transform, animation", "web_css"),
            ("CSS variables: --primary-color, var(), custom properties", "web_css"),
            
            # Design Principles
            ("Design principle: Visual hierarchy - size, color, contrast, spacing", "web_design"),
            ("Design principle: Typography - font-family, font-size, line-height, readability", "web_design"),
            ("Design principle: Color theory - primary, secondary, complementary, contrast", "web_design"),
            ("Design principle: Whitespace - negative space, breathing room, minimalism", "web_design"),
            ("Design principle: Consistency - repeated patterns, design systems", "web_design"),
            ("Design principle: Accessibility - a11y, screen readers, alt text, contrast", "web_design"),
            ("Design principle: User Experience - UX, intuitive navigation, feedback", "web_design"),
            
            # JavaScript Fundamentals
            ("JavaScript: Programming language of the web", "web_js"),
            ("JS variables: let, const, var - scope and mutability", "web_js"),
            ("JS data types: string, number, boolean, null, undefined, object, array", "web_js"),
            ("JS functions: function declaration, arrow functions, callbacks", "web_js"),
            ("JS DOM manipulation: document.querySelector, addEventListener, innerHTML", "web_js"),
            ("JS async: Promises, async/await, fetch API, callbacks", "web_js"),
            ("JS events: click, submit, keydown, load, DOMContentLoaded", "web_js"),
            ("JS modules: import, export, ES6 modules", "web_js"),
        ]
        return lessons
    
    def get_vibe_coding_lessons(self):
        """Vibe coding - AI-assisted development."""
        lessons = [
            ("Vibe coding: AI-assisted programming - describe intent, AI generates code", "vibe_coding"),
            ("Vibe coding principle: Iterate with AI - generate, review, refine, repeat", "vibe_coding"),
            ("Vibe coding prompt engineering: Be specific, provide context, examples", "vibe_coding"),
            ("Vibe coding: Prompt patterns - 'Create a function that...', 'Refactor this to...'", "vibe_coding"),
            ("Vibe coding: Context management - provide files, structure, requirements", "vibe_coding"),
            ("Vibe coding: Code review with AI - 'Explain this code', 'Find bugs in...'", "vibe_coding"),
            ("Vibe coding: Documentation - 'Generate docs for...', 'Add comments to...'", "vibe_coding"),
            ("Vibe coding: Testing - 'Write unit tests for...', 'Generate test cases'", "vibe_coding"),
            ("Vibe coding: Architecture - 'Design a system for...', 'Suggest improvements'", "vibe_coding"),
            ("Vibe coding: StackOverflow style - paste error, get explanation and fix", "vibe_coding"),
            ("Vibe coding: Pair programming - AI as navigator, human as driver", "vibe_coding"),
            ("Vibe coding: Refactoring - 'Make this more efficient', 'Simplify this code'", "vibe_coding"),
            ("Vibe coding: Language translation - 'Convert Python to JavaScript'", "vibe_coding"),
            ("Vibe coding: Regex generation - 'Create regex for email validation'", "vibe_coding"),
            ("Vibe coding: SQL generation - 'Write query to join these tables'", "vibe_coding"),
        ]
        return lessons
    
    def get_programming_fundamentals(self):
        """General programming concepts."""
        lessons = [
            # Programming Basics
            ("Programming: Writing instructions for computers to execute", "programming"),
            ("Algorithm: Step-by-step procedure to solve a problem", "programming"),
            ("Variable: Named storage for data values", "programming"),
            ("Function: Reusable block of code that performs a specific task", "programming"),
            ("Conditionals: if/else/elif - decision making in code", "programming"),
            ("Loops: for, while - repeating code execution", "programming"),
            ("Array/List: Ordered collection of items", "programming"),
            ("Object/Dict: Key-value pairs, structured data", "programming"),
            
            # Programming Paradigms
            ("Paradigm: Object-Oriented Programming - classes, objects, inheritance", "programming"),
            ("Paradigm: Functional Programming - pure functions, immutability, higher-order", "programming"),
            ("Paradigm: Procedural Programming - sequential steps, procedures", "programming"),
            ("Paradigm: Event-Driven Programming - callbacks, event handlers", "programming"),
            
            # Data Structures
            ("Data structure: Stack - LIFO (Last In, First Out)", "programming"),
            ("Data structure: Queue - FIFO (First In, First Out)", "programming"),
            ("Data structure: Linked List - nodes with pointers", "programming"),
            ("Data structure: Tree - hierarchical, parent-child relationships", "programming"),
            ("Data structure: Graph - nodes and edges, networks", "programming"),
            ("Data structure: Hash Map - key-value with O(1) lookup", "programming"),
            
            # Algorithms
            ("Algorithm: Sorting - bubble, merge, quick, heap sort", "programming"),
            ("Algorithm: Searching - linear, binary search", "programming"),
            ("Algorithm: Recursion - function calling itself, base case", "programming"),
            ("Algorithm: Dynamic Programming - memoization, optimal substructure", "programming"),
            ("Algorithm: Big O Notation - time/space complexity O(1), O(n), O(n²), O(log n)", "programming"),
            
            # Software Engineering
            ("Engineering: DRY principle - Don't Repeat Yourself", "programming"),
            ("Engineering: KISS principle - Keep It Simple, Stupid", "programming"),
            ("Engineering: SOLID principles - Single responsibility, Open/closed, etc.", "programming"),
            ("Engineering: Design Patterns - singleton, factory, observer, MVC", "programming"),
            ("Engineering: Testing - unit tests, integration tests, TDD", "programming"),
            ("Engineering: Debugging - breakpoints, logging, stack traces", "programming"),
            ("Engineering: Version Control - git, commits, branches, merge", "programming"),
            ("Engineering: CI/CD - Continuous Integration, Continuous Deployment", "programming"),
            ("Engineering: API design - REST, GraphQL, endpoints, status codes", "programming"),
            ("Engineering: Database - SQL, NoSQL, normalization, indexing", "programming"),
            
            # Python Specific
            ("Python: Interpreted, high-level, general-purpose language", "python"),
            ("Python: Indentation matters - 4 spaces standard", "python"),
            ("Python: List comprehensions - [x for x in items if condition]", "python"),
            ("Python: Decorators - @property, @staticmethod, custom decorators", "python"),
            ("Python: Context managers - with statement, __enter__, __exit__", "python"),
            ("Python: Virtual environments - venv, pip, requirements.txt", "python"),
            ("Python: PEP 8 - style guide, naming conventions", "python"),
            ("Python: Common libraries - requests, pandas, numpy, flask, django", "python"),
            
            # Web Development
            ("Web: Client-Server architecture - browser requests, server responds", "web_dev"),
            ("Web: HTTP methods - GET, POST, PUT, DELETE, PATCH", "web_dev"),
            ("Web: Status codes - 200 OK, 404 Not Found, 500 Server Error", "web_dev"),
            ("Web: Cookies and Sessions - state management", "web_dev"),
            ("Web: Security - XSS, CSRF, SQL injection, HTTPS/TLS", "web_dev"),
            ("Web: Performance - caching, CDN, lazy loading, minification", "web_dev"),
            ("Web: SEO - meta tags, semantic HTML, sitemaps, robots.txt", "web_dev"),
            
            # Modern Frameworks
            ("Framework: React - components, JSX, hooks, state management", "frameworks"),
            ("Framework: Vue - directives, components, Vuex", "frameworks"),
            ("Framework: Next.js - SSR, SSG, API routes, React-based", "frameworks"),
            ("Framework: Flask - Python micro web framework", "frameworks"),
            ("Framework: Django - Python full-stack framework, ORM", "frameworks"),
            ("Framework: FastAPI - modern, fast Python web framework", "frameworks"),
            ("Framework: Tailwind CSS - utility-first CSS framework", "frameworks"),
            ("Framework: Bootstrap - component-based CSS framework", "frameworks"),
            
            # Tools & Workflow
            ("Tools: IDE/Editor - VS Code, PyCharm, vim, cursor", "tools"),
            ("Tools: Terminal - bash, zsh, command line navigation", "tools"),
            ("Tools: Package managers - npm, pip, yarn, poetry", "tools"),
            ("Tools: Build tools - webpack, vite, parcel, rollup", "tools"),
            ("Tools: Linters - ESLint, Pylint, Prettier, Black", "tools"),
            ("Tools: Docker - containers, images, Dockerfile, docker-compose", "tools"),
            ("Tools: Cloud - AWS, GCP, Azure, deployment, serverless", "tools"),
        ]
        return lessons
    
    def get_code_examples(self):
        """Practical code examples."""
        examples = [
            # HTML Examples
            ("HTML example: <!DOCTYPE html><html><head><title>Page</title></head><body><h1>Hello</h1></body></html>", "code_html"),
            
            # CSS Examples
            ("CSS example: .container { display: flex; justify-content: center; align-items: center; }", "code_css"),
            ("CSS example: @media (max-width: 768px) { .responsive { width: 100%; } }", "code_css"),
            
            # JavaScript Examples
            ("JS example: const greet = (name) => { return `Hello, ${name}!`; };", "code_js"),
            ("JS example: fetch('/api/data').then(r => r.json()).then(data => console.log(data));", "code_js"),
            ("JS example: document.getElementById('btn').addEventListener('click', handleClick);", "code_js"),
            
            # Python Examples
            ("Python example: def factorial(n): return 1 if n <= 1 else n * factorial(n-1)", "code_python"),
            ("Python example: with open('file.txt', 'r') as f: content = f.read()", "code_python"),
            ("Python example: [x**2 for x in range(10) if x % 2 == 0]  # squares of evens", "code_python"),
            ("Python example: class Person: def __init__(self, name): self.name = name", "code_python"),
            ("Python example: import requests; r = requests.get('https://api.example.com')", "code_python"),
            
            # Git Examples
            ("Git example: git add . && git commit -m 'message' && git push origin main", "code_git"),
            ("Git example: git checkout -b feature-branch && git merge main", "code_git"),
            
            # SQL Examples
            ("SQL example: SELECT users.name, orders.total FROM users JOIN orders ON users.id = orders.user_id", "code_sql"),
            ("SQL example: INSERT INTO users (name, email) VALUES ('John', 'john@example.com')", "code_sql"),
            
            # React Examples
            ("React example: const App = () => { const [count, setCount] = useState(0); return <button onClick={() => setCount(c => c+1)}>{count}</button>; }", "code_react"),
        ]
        return examples
    
    def teach_curriculum(self):
        """Run complete coding curriculum."""
        print("=" * 70)
        print("📚 CODING CURRICULUM FOR MYLONEN + R2")
        print("=" * 70)
        print()
        
        # Collect all lessons
        all_lessons = []
        
        print("📖 Loading Web Design curriculum...")
        web_lessons = self.get_web_design_lessons()
        all_lessons.extend([(content, "", "", category) for content, category in web_lessons])
        print(f"   ✓ {len(web_lessons)} lessons")
        
        print("📖 Loading Vibe Coding curriculum...")
        vibe_lessons = self.get_vibe_coding_lessons()
        all_lessons.extend([(content, "", "", category) for content, category in vibe_lessons])
        print(f"   ✓ {len(vibe_lessons)} lessons")
        
        print("📖 Loading Programming Fundamentals...")
        prog_lessons = self.get_programming_fundamentals()
        all_lessons.extend([(content, "", "", category) for content, category in prog_lessons])
        print(f"   ✓ {len(prog_lessons)} lessons")
        
        print("📖 Loading Code Examples...")
        code_examples = self.get_code_examples()
        all_lessons.extend([(content, "", "", category) for content, category in code_examples])
        print(f"   ✓ {len(code_examples)} examples")
        
        total_lessons = len(all_lessons)
        print(f"\n🎓 Total curriculum: {total_lessons} items")
        print()
        
        # Feed through stomach-brain pipeline
        print("🍽️ Teaching through stomach-brain pipeline...")
        print("=" * 70)
        result = self.feeder.run_until_empty(all_lessons)
        
        # Final report
        print("\n" + "=" * 70)
        print("🎓 CURRICULUM COMPLETE")
        print("=" * 70)
        print()
        print(f"📊 Teaching Stats:")
        print(f"   Lessons taught: {result['fed']}")
        print(f"   Digested to brain: {result['digested']}")
        print(f"   Efficiency: {result['efficiency']:.1f}%")
        print()
        print(f"🧠 Brain Knowledge:")
        print(f"   Total ticks: {result['brain_ticks']}")
        print(f"   Total clusters: {result['brain_clusters']}")
        print(f"   New knowledge: {result['digested']} coding concepts")
        print()
        
        if result['efficiency'] == 100.0:
            print("✅ PERFECT TEACHING: All lessons learned!")
        
        categories = {}
        for _, _, _, cat in all_lessons:
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\n📚 Knowledge by Category:")
        for cat, count in sorted(categories.items()):
            print(f"   - {cat}: {count} concepts")
        
        return result


if __name__ == "__main__":
    curriculum = CodingCurriculum()
    curriculum.teach_curriculum()
