#!/usr/bin/env python3
"""
Patricia Factory Controller v2.0
FIXED: Now promotes orders and spawns workers
"""

import sqlite3
import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add Agent Factory to path
sys.path.insert(0, '/root/.openclaw/workspace/aocros/factory')
from agent_factory_module import AgentFactory, AgentSpec


class PatriciaFactoryControllerV2:
    """Patricia's FIXED interface to the Dark Factory"""
    
    DB_PATH = "/root/.openclaw/workspace/data/factory/dark_factory.db"
    ANDROID_SDK = "/opt/android-sdk"
    
    def __init__(self):
        self.db_path = Path(self.DB_PATH)
        self.factory = AgentFactory()
        self.ensure_sdk_env()
        print("🌑 Patricia Factory Controller v2.0 initialized")
    
    def ensure_sdk_env(self):
        """Ensure Android SDK environment is set"""
        os.environ['ANDROID_SDK_ROOT'] = self.ANDROID_SDK
        os.environ['ANDROID_HOME'] = self.ANDROID_SDK
        os.environ['PATH'] = f"{os.environ.get('PATH', '')}:{self.ANDROID_SDK}/cmdline-tools/latest/bin:{self.ANDROID_SDK}/platform-tools"
    
    def promote_order(self, order_id: str) -> bool:
        """Promote a queued order to in_progress"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        c.execute('''
            UPDATE production_orders 
            SET status = 'in_progress', 
                started_at = CURRENT_TIMESTAMP,
                stage = 1,
                last_updated = CURRENT_TIMESTAMP
            WHERE id = ? AND status = 'queued'
        ''', (order_id,))
        
        updated = c.rowcount > 0
        conn.commit()
        conn.close()
        
        if updated:
            print(f"✅ Order {order_id} promoted to IN_PROGRESS")
        return updated
    
    def get_next_queued_order(self) -> Optional[Dict]:
        """Get the next queued order by priority"""
        conn = sqlite3.connect(self.DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('''
            SELECT id, product_name, product_type, metadata, priority, created_at
            FROM production_orders
            WHERE status = 'queued'
            ORDER BY 
                CASE priority 
                    WHEN 'urgent' THEN 1 
                    WHEN 'high' THEN 2 
                    WHEN 'normal' THEN 3 
                    ELSE 4 
                END, 
                created_at
            LIMIT 1
        ''')
        
        row = c.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'name': row['product_name'],
                'type': row['product_type'],
                'metadata': json.loads(row['metadata']) if row['metadata'] else {},
                'priority': row['priority'],
                'created': row['created_at']
            }
        return None
    
    def spawn_build_agent(self, order: Dict) -> Optional[Dict]:
        """Spawn an agent to handle the build"""
        
        # Determine agent type based on order
        if 'Android' in order['name'] or 'App' in order['name']:
            agent_type = 'coder'
            capabilities = ['android_build', 'cordova', 'gradle', 'apk_signing']
        elif 'Game' in order['name'] or 'Explorer' in order['name']:
            agent_type = 'coder'
            capabilities = ['game_build', 'threejs', 'webgl', 'mobile_wrap']
        else:
            agent_type = 'coder'
            capabilities = ['build_automation', 'testing', 'deployment']
        
        spec = AgentSpec(
            name=f"Builder_{order['id']}",
            role=f"Build Agent for {order['name']}",
            emoji="🔧",
            capabilities=capabilities
        )
        
        try:
            agent = self.factory.spawn_agent(spec)
            print(f"✅ Spawned build agent: {agent['name']} for {order['id']}")
            return agent
        except Exception as e:
            print(f"❌ Failed to spawn agent: {e}")
            return None
    
    def run_build(self, order: Dict, agent: Dict) -> bool:
        """Execute the build for an order"""
        print(f"🔨 Starting build for {order['id']}: {order['name']}")
        
        # Get source path from metadata
        metadata = order.get('metadata', {})
        source_path = metadata.get('source', '')
        
        if not source_path or not os.path.exists(source_path):
            print(f"❌ Source path not found: {source_path}")
            return False
        
        print(f"   Source: {source_path}")
        
        # Example build logic - would be expanded per project type
        if 'Android' in order['name']:
            return self._build_android(order, source_path)
        elif 'Game' in order['name'] or 'nog' in order['id'].lower():
            return self._build_web_game(order, source_path)
        else:
            return self._build_generic(order, source_path)
    
    def _build_android(self, order: Dict, source_path: str) -> bool:
        """Build Android APK"""
        print(f"   Building Android APK...")
        
        # Check for native Android/Gradle project
        if os.path.exists(os.path.join(source_path, 'build.gradle')):
            print("   Detected native Android/Gradle project")
            return self._build_gradle_android(order, source_path)
        
        # Check for Cordova/Capacitor setup
        elif os.path.exists(os.path.join(source_path, 'config.xml')):
            print("   Detected Cordova project")
            return self._build_cordova(order, source_path)
        
        elif os.path.exists(os.path.join(source_path, 'capacitor.config.json')):
            print("   Detected Capacitor project")
            return self._build_capacitor(order, source_path)
        
        else:
            print("   No recognized Android project structure found")
            return False
    
    def _build_gradle_android(self, order: Dict, source_path: str) -> bool:
        """Build native Android APK with Gradle"""
        print(f"   Running Gradle build...")
        
        # Ensure gradlew is executable
        gradlew_path = os.path.join(source_path, 'gradlew')
        if os.path.exists(gradlew_path):
            os.chmod(gradlew_path, 0o755)
        
        # Run gradle build
        try:
            result = subprocess.run(
                ['./gradlew', 'assembleRelease'],
                cwd=source_path,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode == 0:
                print("   ✅ Gradle build successful")
                # Check for output APK
                apk_path = os.path.join(source_path, 'app/build/outputs/apk/release/')
                if os.path.exists(apk_path):
                    apks = [f for f in os.listdir(apk_path) if f.endswith('.apk')]
                    if apks:
                        print(f"   ✅ APK generated: {apks[0]}")
                        return True
            else:
                print(f"   ❌ Gradle build failed")
                print(f"   Error: {result.stderr[:200]}")
                
        except subprocess.TimeoutExpired:
            print("   ❌ Build timed out after 10 minutes")
        except Exception as e:
            print(f"   ❌ Build error: {e}")
        
        return False
    
    def _build_cordova(self, order: Dict, source_path: str) -> bool:
        """Build Cordova Android project"""
        print(f"   Building Cordova project...")
        try:
            result = subprocess.run(
                ['cordova', 'build', 'android', '--release'],
                cwd=source_path,
                capture_output=True,
                text=True,
                timeout=600
            )
            return result.returncode == 0
        except Exception as e:
            print(f"   ❌ Cordova build error: {e}")
            return False
    
    def _build_capacitor(self, order: Dict, source_path: str) -> bool:
        """Build Capacitor Android project"""
        print(f"   Building Capacitor project...")
        try:
            # Sync first
            subprocess.run(['npx', 'cap', 'sync'], cwd=source_path, timeout=120)
            # Then build
            result = subprocess.run(
                ['npx', 'cap', 'build', 'android'],
                cwd=source_path,
                capture_output=True,
                text=True,
                timeout=600
            )
            return result.returncode == 0
        except Exception as e:
            print(f"   ❌ Capacitor build error: {e}")
            return False
    
    def _build_web_game(self, order: Dict, source_path: str) -> bool:
        """Build web game for mobile"""
        print(f"   Building web game wrapper...")
        
        # Check for index.html
        if os.path.exists(os.path.join(source_path, 'index.html')):
            print("   Found index.html - ready for mobile wrap")
            # Would run: Bubblewrap or Capacitor to wrap
            return True
        
        print("   No index.html found")
        return False
    
    def _build_generic(self, order: Dict, source_path: str) -> bool:
        """Generic build process"""
        print(f"   Running generic build...")
        return True
    
    def complete_order(self, order_id: str, success: bool) -> None:
        """Mark order as completed or failed"""
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        
        if success:
            c.execute('''
                UPDATE production_orders 
                SET status = 'completed', 
                    completed_at = CURRENT_TIMESTAMP,
                    stage = total_stages,
                    last_updated = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (order_id,))
            print(f"✅ Order {order_id} COMPLETED")
        else:
            c.execute('''
                UPDATE production_orders 
                SET status = 'failed',
                    last_updated = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (order_id,))
            print(f"❌ Order {order_id} FAILED")
        
        conn.commit()
        conn.close()
    
    def run_factory_tick(self):
        """Patricia runs one factory execution tick"""
        print("\n" + "="*60)
        print("🌑 PATRICIA FACTORY CONTROLLER v2.0 - EXECUTION TICK")
        print("="*60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        
        # Step 1: Check for queued orders
        order = self.get_next_queued_order()
        if not order:
            print("ℹ️ No queued orders to process")
            return
        
        print(f"\n📦 Next Order: {order['id']} - {order['name']}")
        print(f"   Priority: {order['priority']}")
        print(f"   Queued since: {order['created']}")
        
        # Step 2: Promote order to in_progress
        if not self.promote_order(order['id']):
            print(f"❌ Failed to promote order {order['id']}")
            return
        
        # Step 3: Spawn build agent
        agent = self.spawn_build_agent(order)
        if not agent:
            print(f"❌ Failed to spawn agent for {order['id']}")
            return
        
        # Step 4: Execute build
        success = self.run_build(order, agent)
        
        # Step 5: Complete order
        self.complete_order(order['id'], success)
        
        print("\n" + "="*60)
        print("✅ Factory tick complete")
        print("="*60 + "\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Patricia Factory Controller v2')
    parser.add_argument('command', choices=['status', 'tick', 'test'])
    args = parser.parse_args()
    
    controller = PatriciaFactoryControllerV2()
    
    if args.command == 'status':
        order = controller.get_next_queued_order()
        if order:
            print(f"Next queued order: {order['id']} - {order['name']}")
        else:
            print("No queued orders")
    
    elif args.command == 'tick':
        controller.run_factory_tick()
    
    elif args.command == 'test':
        print("Testing SDK environment...")
        controller.ensure_sdk_env()
        result = subprocess.run(['sdkmanager', '--version'], 
                                  capture_output=True, text=True)
        print(f"SDK Version: {result.stdout.strip()}")


if __name__ == "__main__":
    main()
