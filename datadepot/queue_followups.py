#!/usr/bin/env python3
"""
FOLLOW-UP QUEUE MANAGER
Queues Day 2 and Day 3 follow-up emails for prospects who received Day 1
"""

import csv
import json
import os
from datetime import datetime, timedelta

class FollowUpQueueManager:
    def __init__(self):
        self.crm_dir = "/root/.openclaw/workspace/datadepot/crm"
        self.queue_dir = "/root/.openclaw/workspace/datadepot/queue"
        self.templates_dir = "/root/.openclaw/workspace/datadepot/templates/email"
        
        # Ensure queue directory exists
        os.makedirs(self.queue_dir, exist_ok=True)
    
    def load_contacted_prospects(self):
        """Load prospects from today's pipeline"""
        pipeline_file = f"{self.crm_dir}/pipeline.csv"
        
        if not os.path.exists(pipeline_file):
            return []
        
        prospects = []
        try:
            with open(pipeline_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Status') == 'Contacted' or row.get('Status') == 'Demo Scheduled':
                        prospects.append(row)
        except Exception as e:
            print(f"Error loading pipeline: {e}")
        
        return prospects
    
    def load_template(self, template_file):
        """Load email template"""
        filepath = f"{self.templates_dir}/{template_file}"
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except:
            return None
    
    def personalize_email(self, template, prospect):
        """Personalize template with prospect data"""
        email = template
        
        # Extract first name
        contact = prospect.get('Prospect', 'there')
        first_name = contact.split()[0] if contact else 'there'
        
        # Simple replacements
        email = email.replace('{{First_Name}}', first_name)
        email = email.replace('{{first_name}}', first_name)
        email = email.replace('{{Company}}', prospect.get('Company', 'your company'))
        email = email.replace('{{company}}', prospect.get('Company', 'your company'))
        
        return email
    
    def parse_subject_and_body(self, template_content):
        """Parse subject line from template"""
        lines = template_content.split('\n')
        subject = "Following up"
        body_lines = []
        
        in_body = False
        for line in lines:
            if line.startswith('Subject:'):
                subject = line.replace('Subject:', '').strip()
            elif in_body or (line.strip() and not line.startswith('Subject:')):
                in_body = True
                body_lines.append(line)
        
        return subject, '\n'.join(body_lines)
    
    def create_follow_up_email(self, prospect, day, scheduled_date):
        """Create a follow-up email record"""
        template_file = f"email_{day}_value.txt" if day == 2 else f"email_{day}_close.txt"
        
        template = self.load_template(template_file)
        if not template:
            return None
        
        # Personalize
        personalized = self.personalize_email(template, prospect)
        subject, body = self.parse_subject_and_body(personalized)
        
        # Convert text body to simple HTML
        html_body = body.replace('\n', '<br>')
        
        email_record = {
            "to_name": prospect.get('Prospect', ''),
            "to_email": self.derive_email(prospect),
            "subject": subject,
            "html_body": html_body,
            "text_body": body,
            "template": f"day{day}_followup",
            "campaign_id": f"psdepot_outreach_2026_q2",
            "prospect_company": prospect.get('Company', ''),
            "scheduled_time": scheduled_date.isoformat(),
            "from": "Miles - Performance Supply Depot <miles@psdepot.com>",
            "created_at": datetime.now().isoformat(),
            "sequence_day": day,
            "original_contact_date": prospect.get('Last_Contact', ''),
            "estimated_value": prospect.get('Estimated_Value', '$97'),
            "priority_score": self.calculate_priority(prospect)
        }
        
        return email_record
    
    def derive_email(self, prospect):
        """Derive email from available data or generate likely one"""
        # In real system, this would be stored - here we generate from name patterns
        contact = prospect.get('Prospect', '')
        company = prospect.get('Company', '').lower().replace(' ', '').replace('-', '')
        
        name_parts = contact.lower().split()
        if len(name_parts) >= 2:
            patterns = [
                f"{name_parts[0]}.{name_parts[-1]}@{company}.com",
                f"{name_parts[0][0]}{name_parts[-1]}@{company}.com",
                f"{name_parts[0]}@{company}.com",
            ]
            return patterns[0]
        
        return f"contact@{company}.com"
    
    def calculate_priority(self, prospect):
        """Calculate priority based on value tier"""
        value = prospect.get('Estimated_Value', '$97')
        if '$297' in value or '$297' in value:
            return "HIGH"
        elif 'Demo' in prospect.get('Status', ''):
            return "URGENT"
        return "NORMAL"
    
    def queue_follow_ups(self):
        """Queue Day 2 and Day 3 follow-up emails"""
        print("=" * 60)
        print("FOLLOW-UP QUEUE MANAGER - STARTING")
        print("=" * 60)
        
        # Load contacted prospects
        prospects = self.load_contacted_prospects()
        print(f"\n📊 Loaded {len(prospects)} contacted prospects from pipeline")
        
        if not prospects:
            print("No prospects to queue follow-ups for")
            return
        
        # Calculate send dates
        today = datetime.now()
        day2_date = today + timedelta(days=2)  # Day 2 follow-up (48 hours)
        day3_date = today + timedelta(days=5)  # Day 3 follow-up (5 days later)
        
        print(f"   Day 2 emails scheduled for: {day2_date.strftime('%Y-%m-%d')}")
        print(f"   Day 3 emails scheduled for: {day3_date.strftime('%Y-%m-%d')}")
        
        # Generate follow-up emails
        follow_up_queue = []
        
        for prospect in prospects:
            # Skip if demo already booked (they get special nurturing)
            if 'Demo' in prospect.get('Status', ''):
                print(f"   ⏭️  Skipping {prospect.get('Prospect')} - Demo already booked")
                continue
            
            # Day 2 follow-up
            day2_email = self.create_follow_up_email(prospect, 2, day2_date)
            if day2_email:
                follow_up_queue.append(day2_email)
            
            # Day 3 follow-up (final)
            day3_email = self.create_follow_up_email(prospect, 3, day3_date)
            if day3_email:
                follow_up_queue.append(day3_email)
        
        print(f"\n📧 Generated {len(follow_up_queue)} follow-up emails")
        
        # Split by priority
        high_priority = [e for e in follow_up_queue if e['priority_score'] == 'HIGH']
        normal_priority = [e for e in follow_up_queue if e['priority_score'] == 'NORMAL']
        
        print(f"   High Priority (Tier 1): {len(high_priority)}")
        print(f"   Normal Priority (Tier 2): {len(normal_priority)}")
        
        # Save to queue file
        queue_file = f"{self.queue_dir}/followup_queue_{today.strftime('%Y%m%d')}.json"
        
        with open(queue_file, 'w') as f:
            json.dump(follow_up_queue, f, indent=2)
        
        # Also append to master pending queue
        master_queue = f"{self.queue_dir}/pending_emails.json"
        
        # Load existing
        existing = []
        if os.path.exists(master_queue):
            try:
                with open(master_queue, 'r') as f:
                    existing = json.load(f)
            except:
                existing = []
        
        # Merge and save
        combined = existing + follow_up_queue
        with open(master_queue, 'w') as f:
            json.dump(combined, f, indent=2)
        
        print(f"\n💾 Saved to:")
        print(f"   Follow-up batch: {queue_file}")
        print(f"   Master queue: {master_queue}")
        
        # Summary by day
        day2_count = len([e for e in follow_up_queue if e['sequence_day'] == 2])
        day3_count = len([e for e in follow_up_queue if e['sequence_day'] == 3])
        
        print(f"\n📅 Queue Summary:")
        print(f"   Day 2 follow-ups: {day2_count}")
        print(f"   Day 3 follow-ups: {day3_count}")
        print(f"   Total pipeline value: ${self.calculate_pipeline_value(follow_up_queue)}")
        
        print("\n" + "=" * 60)
        print("✅ FOLLOW-UP QUEUE COMPLETE")
        print("=" * 60)
        
        return follow_up_queue
    
    def calculate_pipeline_value(self, emails):
        """Calculate estimated value of queued emails"""
        total = 0
        for email in emails:
            value = email.get('estimated_value', '$97').replace('$', '').replace(',', '')
            try:
                total += int(value)
            except:
                total += 97
        return total

if __name__ == "__main__":
    manager = FollowUpQueueManager()
    queued = manager.queue_follow_ups()
    print(f"\n✅ {len(queued)} follow-up emails queued for automated delivery.")
