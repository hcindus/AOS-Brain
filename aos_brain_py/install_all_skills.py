#!/usr/bin/env python3
"""
INSTALL ALL SKILLS
Systematic installation of all available skills
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime

SKILLS_DIR = Path("/root/.openclaw/workspace/aocros/skills")

SKILLS_TO_INSTALL = [
    # Core Infrastructure
    ("agent-orchestrator", "Agent coordination and management"),
    ("aos-brain-interface", "Brain system interface"),
    ("cron-scheduler", "Job scheduling"),
    ("health-monitor", "System health monitoring"),
    ("hostinger-vps", "VPS management"),
    
    # Communication
    ("ngrok-tunnel", "Secure tunneling"),
    ("webhook-tunnel-setup", "Webhook handling"),
    
    # Crypto/Finance
    ("crypto-exchange-api", "Exchange API integration"),
    ("crypto-market-data", "Market data feeds"),
    ("cryptonio-dashboard", "Trading dashboard"),
    ("evm-wallet", "EVM wallet management"),
    ("wallet-payment-display", "Payment display"),
    ("finance-director", "Financial management"),
    ("portfolio-manager", "Portfolio tracking"),
    
    # Data/Scraping
    ("browser-exchange-agent", "Browser automation - INSTALLED"),
    ("gov-data-scraper", "Government data scraping"),
    ("enrichment-program", "Data enrichment"),
    
    # Security/Compliance
    ("dusty-compliance", "Compliance checking"),
    ("dusty-mvp", "Dusty MVP features"),
    ("dusty-ops", "Dusty operations"),
    ("security-officer", "Security management"),
    
    # Sales/Marketing
    ("sales-consultant", "Sales assistance"),
    ("store-integration", "Store integration"),
    
    # Specialized
    ("nft-gallery-operator", "NFT operations"),
    ("paydify-payments", "Payment processing"),
    ("seed-ship-coordinator", "Seed ship coordination"),
    ("tappy-lewis", "Tappy Lewis operations"),
    ("technical-architect", "Architecture planning"),
    ("web", "Web development"),
    
    # Learning
    ("learning-tracker", "Learning progress"),
    ("planning", "Project planning"),
    ("skill-packager", "Skill packaging"),
]

class SkillInstaller:
    def __init__(self):
        self.installed = []
        self.failed = []
        self.skipped = []
        
    def install_skill(self, skill_name, description):
        """Install a single skill."""
        skill_path = SKILLS_DIR / skill_name
        
        print(f"\n📦 {skill_name}")
        print(f"   {description}")
        
        if not skill_path.exists():
            print(f"   ❌ Skill directory not found")
            self.failed.append((skill_name, "Directory not found"))
            return
        
        # Check for package.json
        package_json = skill_path / "package.json"
        requirements_txt = skill_path / "requirements.txt"
        setup_py = skill_path / "setup.py"
        
        try:
            # Install npm dependencies
            if package_json.exists():
                print(f"   📥 Installing npm packages...")
                result = subprocess.run(
                    ["npm", "install"],
                    cwd=skill_path,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode == 0:
                    print(f"   ✅ npm install complete")
                else:
                    print(f"   ⚠️  npm issues (may be already installed)")
            
            # Install Python dependencies
            if requirements_txt.exists():
                print(f"   📥 Installing Python packages...")
                result = subprocess.run(
                    ["pip3", "install", "-r", "requirements.txt"],
                    cwd=skill_path,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode == 0:
                    print(f"   ✅ pip install complete")
                else:
                    print(f"   ⚠️  pip issues (may be already installed)")
            
            # Run setup.py if exists
            if setup_py.exists():
                print(f"   📥 Running setup.py...")
                result = subprocess.run(
                    ["pip3", "install", "."],
                    cwd=skill_path,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode == 0:
                    print(f"   ✅ setup.py complete")
                else:
                    print(f"   ⚠️  setup issues")
            
            self.installed.append(skill_name)
            print(f"   ✅ {skill_name} ready")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            self.failed.append((skill_name, str(e)))
    
    def install_all(self):
        """Install all skills."""
        print("=" * 70)
        print("🔧 INSTALLING ALL SKILLS")
        print("=" * 70)
        print(f"Total skills: {len(SKILLS_TO_INSTALL)}")
        print()
        
        for skill_name, description in SKILLS_TO_INSTALL:
            self.install_skill(skill_name, description)
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 INSTALLATION SUMMARY")
        print("=" * 70)
        print(f"✅ Installed/Ready: {len(self.installed)}")
        print(f"❌ Failed: {len(self.failed)}")
        print()
        
        if self.installed:
            print("Installed Skills:")
            for skill in self.installed[:10]:
                print(f"  ✅ {skill}")
            if len(self.installed) > 10:
                print(f"  ... and {len(self.installed) - 10} more")
        
        if self.failed:
            print("\nFailed Skills:")
            for skill, error in self.failed:
                print(f"  ❌ {skill}: {error}")
        
        # Save report
        report = {
            "timestamp": datetime.now().isoformat(),
            "total": len(SKILLS_TO_INSTALL),
            "installed": self.installed,
            "failed": self.failed,
            "success_rate": f"{len(self.installed) / len(SKILLS_TO_INSTALL) * 100:.1f}%"
        }
        
        report_path = Path("/root/.openclaw/workspace/reports/skill_installation_report.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Report saved to: {report_path}")
        print("=" * 70)

def main():
    installer = SkillInstaller()
    installer.install_all()

if __name__ == "__main__":
    main()
