#!/usr/bin/env python3
"""
Parse the invoice dump and load into collections database
"""

import re
from datetime import datetime
from collections_db import CollectionsDB

# The raw invoice data from the message
RAW_DATA = """$17,672.36
● $12,122.09● $11,013.73● $3,980.00
Status
Today
Gregory Lachica
061326021
Not viewed
Thank you for your order
Unpaid
Due in 30 days
$80.61
Today
Tacos Sinaloa - Oakland Marlem
061326020
Not viewed
Thank you for your order.
Unpaid
Due today
$425.61
Today
Abe left msg
061326014
Not viewed
Paid
On 06/19/2026
$305.16
Today
Katie Rondeau
061326016
Viewed
ORDER # 651332
Unpaid
Due in 30 days
$632.00
Today
Katie Rondeau
061326015
Viewed
ORDER # 642281
Unpaid
Due in 30 days
$178.00
Today
Bitu Manager
061326013
Viewed
scanner
Overdue
By 1 day
$246.14
Yesterday
Robert Simon
061326022
Viewed
Overdue
By 1 day
$152.58
Yesterday
Marlem
061326019
Not viewed
Draft
Send now
$0.00
Yesterday
061326018
Not viewed
Draft
Send now
$0.00
Yesterday
Becky NCC
061326017
Viewed
Thank you for your order.
Unpaid
Due in 29 days
$98.66
Yesterday
Michael Owner
061326011
Viewed
Thank you for your order.
Paid
On 06/19/2026
$166.62
Yesterday
William Bishop
061326006
Viewed
If you approve, please process invoice
Overdue
By 4 days
$73.15
Yesterday
Nick Owner
061326012
Not viewed
Thank you for your order.
Paid
On 06/18/2026
$200.81
06/16/2026
Heather Manager
4276102
Viewed
Please find your courtesy invoice attached.
Overdue
By 20 days
$434.09
06/16/2026
Armando Alvarez MAITRE'D
061326010
Not viewed
Thank you for your order.
Paid
On 06/16/2026
$1,064.96
06/16/2026
Cindy or Beth Cd @ 2 months
061026005
Not viewed
Unpaid
Due in 23 days
$756.01
06/16/2026
Francesco open
061026004
Not viewed
Thank you for your order.
Paid
On 06/16/2026
$966.31
06/16/2026
Victor Sabido
061326009
Viewed
Thank you for your order.
Overdue
By 3 days
$348.62
06/16/2026
Morris Owner
061326002
Viewed
Sam4s POS system
Overdue
By 4 days
$4,883.85
06/16/2026
Brent Warehouse
061326008
Not viewed
Thank you for your order.
Unpaid
Due in 11 days
$2,962.42
06/15/2026
Sarah Willams
061326007
Viewed
Thank you for your order.
Overdue
By 4 days
$109.52
06/15/2026
Kevin Manager
061326005
Viewed
Thank you for your order.
Overdue
By 4 days
$402.90
06/15/2026
Kelly left msg
061326004
Not viewed
Thank you for your order.
Overdue
By 4 days
$300.73
06/15/2026
Bo Thompson SUPPLY ONLY
4166114
Viewed
Thank you for your order.
Overdue
By 28 days
$329.75
06/15/2026
Sam Owner
061326003
Viewed
Thank you for your continued business.
Overdue
By 4 days
$1,272.00
06/14/2026
Oona open store
060826003
Viewed
Thank you for your order.
Overdue
By 7 days
$575.63
06/14/2026
Ali Saleh
061326001
Viewed
Sam4s SPT 4740
Paid
On 06/15/2026
$500.00
06/14/2026
Gabby Park Caféb Group
061026002
Not viewed
Thank you for your order.
Undelivered
Due in 22 days
$410.19
06/12/2026
Gilbert General Manager
060826009
Not viewed
Thank you for your continued business.
Undelivered
Due in 19 days
$539.67
06/11/2026
Laura
061026003
Viewed
Thank you for your order.
Payment pending
Since 06/18/2026
$213.68
06/11/2026
Tony Salinas
052626007
Viewed
Thank you for your order.
Paid
On 06/19/2026
$457.99
06/11/2026
Myly
061026001
Viewed
Thank you for your order.
Unpaid
Due in 21 days
$929.23
06/10/2026
Sergio Frigerio NCC
060826008
Viewed
Thank you for your continued business.
Canceled
On 06/10/2026
$507.16
06/10/2026
Paolo Gomez
4246101
Viewed
Thank you for your order
Paid
On 06/10/2026
$230.24
06/09/2026
Nick Owner
060826004
Not viewed
Thank you for your order.
Paid
On 06/09/2026
$273.63
06/08/2026
Maria Abundiz
060826007
Viewed
Thank you for your order.
Unpaid
Due in 19 days
$290.84
06/08/2026
Lupe
060826006
Viewed
Thank you for your order.
Paid
On 06/08/2026
$231.84
06/08/2026
Caffe Greco
060826005
Viewed
Thank you for your order.
Unpaid
Due in 19 days
$104.63
06/08/2026
John Caine
060826002
Viewed
Thank you for your order.
Unpaid
Due in 19 days
$928.98
06/08/2026
Nick Owner
060826001
Not viewed
Thank you for your order.
Paid
On 06/08/2026
$285.00
06/07/2026
Nick Owner
060526002
Not viewed
Refunded
On 06/07/2026
$357.48
06/05/2026
Mario ECR
060526001
Viewed
Thank you for your order.
Paid
On 06/05/2026
$453.42
06/04/2026
Heather Owner
060226006
Viewed
Thank you for your continued business.
Paid
On 06/05/2026
$99.00
06/04/2026
Marco Manager
060226005
Viewed
Thank you for your order.
Paid
On 06/04/2026
$1,227.86
06/02/2026
Renee loscaporalestaqueria@outlook.com
000015
Not viewed
Thank you for your order
Unpaid
Due in 13 days
$360.45
06/02/2026
Ema Kye
060226004
Viewed
Thank you for your order.
Unpaid
Due in 13 days
$150.36
06/02/2026
Joycelin Magno
060226003
Viewed
Thank you for your order.
Unpaid
Due in 13 days
$230.93
06/02/2026
Izat
060126004
Viewed
Thank you for your order.
Paid
On 06/02/2026
$518.31
06/02/2026
Izat left msg
060126006
Not viewed
Thank you for your order.
Paid
On 06/02/2026
$65.34
06/02/2026
Izat left msg
060126007
Not viewed
Thank you for your order.
Paid
On 06/02/2026
$174.98
06/02/2026
Salam Naser CASIO
060126005
Not viewed
Draft
Send now
$0.00
06/02/2026
John
060126003
Not viewed
Thank you for your order.
Unpaid
Due in 13 days
$161.22
06/02/2026
Sam Manager
060126002
Viewed
Thank you.
Paid
On 06/05/2026
$232.53
06/02/2026
Margarito General Manager
060126001
Viewed
Thank you for your order.
Unpaid
Due in 10 days
$512.41
06/01/2026
Aldo Owner
052626009
Not viewed
Thank you for your continued business.
Paid
On 06/01/2026
$390.00
05/31/2026
Robert Guerra
052626010
Not viewed
Thank you for your order.
Draft
Send now
$3,980.00
05/29/2026
Sam Owner
052626008
Viewed
Thank you for your continued business.
Paid
On 06/15/2026
$285.00
05/29/2026
Cory Manager
052226002
Viewed
Thank you for your order.
Unpaid
Due in 2 days
$489.35
05/28/2026
Robert Guerra
05056104
Viewed
Thank you for your order.
Paid
On 06/08/2026
$898.62
05/27/2026
Becky NCC
052626006
Viewed
Thank you for your order.
Unpaid
Due in 7 days
$249.14
05/26/2026
Janet Clyde
052626005
Viewed
Thank you for your order
Paid
On 05/26/2026
$668.06
05/26/2026
Peter Schumacher SUPPLY ONLY
4166106
Viewed
Paid
On 06/03/2026
$496.00
05/26/2026
Bitu Manager
052626004
Not viewed
Paid
On 05/27/2026
$396.00
05/26/2026
Randy SUPPLY ONLY
052626003
Not viewed
Thank you for your order
Paid
On 05/26/2026
$755.70
05/26/2026
Travis Hauffman
052626001
Viewed
Thank you for your order
Unpaid
Due in 6 days
$149.90
05/26/2026
Travis Hauffman
052626002
Viewed
Thank you for your order
Unpaid
Due in 6 days
$149.90
05/26/2026
Robert Guerra
052226004
Not viewed
Thank you for your order.
Paid
On 05/26/2026
$694.47
05/23/2026
Michael General Manager
052226003
Viewed
Thank you for your order
Unpaid
Due in 3 days
$386.90
05/22/2026
Katie Rondeau
052226001
Viewed
ORDER # 639326
Unpaid
Due in 2 days
$553.00
05/20/2026
Katie Rondeau
052026001
Viewed
ORDER # 642281
Unpaid
Due today
$178.00
05/20/2026
Donato Owner
051326011
Not viewed
Paid
On 05/20/2026
$606.67
05/20/2026
Donato Owner
051326010
Not viewed
Paid
On 05/20/2026
$212.75
05/20/2026
Donato Owner
051326009
Not viewed
Canceled
On 05/20/2026
$606.67
05/20/2026
Mary T
000023
Viewed
Thank you for your continued business.
Paid
On 05/31/2026
$273.74
05/20/2026
Paige Sutter
000022
Viewed
POS Supplies
Paid
On 05/31/2026
$1,829.67
05/19/2026
Don Tom La Torre
051326008
Viewed
Paid
On 05/19/2026
$60.83
05/19/2026
Mario ECR
051326007
Not viewed
Thank you for your order.
Paid
On 05/19/2026
$525.72
05/15/2026
Myly
051326006
Viewed
Thank you for your order.
Paid
On 05/15/2026
$899.87
05/13/2026
Chris Davenport
051326005
Viewed
Thank you for your continued business.
Paid
On 05/26/2026
$232.07
05/13/2026
Chris Davenport
051326004
Not viewed
Thank you for your order.
Draft
Send now
$0.00
05/13/2026
Dan Ok for now
05056102
Viewed
Thank you!
Paid
On 05/31/2026
$296.65
05/13/2026
Joycelin Magno
05056105
Viewed
Thank you for your order.
Paid
On 05/31/2026
$62.48
05/13/2026
Fernando
5126103
Viewed
Thank you for your business
Overdue
By 37 days
$421.56
05/12/2026
Nancy Crane
5126102
Viewed
Thank you for your order.
Paid
On 05/12/2026
$1,262.79
05/12/2026
Becky NCC
5126101
Viewed
Thank you for your order.
Paid
On 06/15/2026
$312.24
05/12/2026
Aaron Weissman
05056106
Viewed
Thank you for your order.
Paid
On 05/29/2026
$114.56
05/12/2026
Aaron Weissman
05056107
Viewed
Thank you for your order.
Paid
On 05/29/2026
$114.56
05/11/2026
Robert Guerra
05056103
Not viewed
Thank you for your order.
Paid
On 05/11/2026
$151.34
05/11/2026
Katie Fryxell
4306101
Viewed
Thank you for your order
Canceled
On 05/29/2026
$99.16
05/07/2026
Scott Walsh
05056101
Viewed
Thank you for your order.
Overdue
By 13 days
$382.30
05/07/2026
Be Manager
4306105
Not viewed
Thank you for your order.
Paid
On 05/07/2026
$853.90
05/07/2026
Jen Yang SUPPLY ONLY
4306104
Viewed
Thank you for your order.
Paid
On 06/18/2026
$520.86
05/05/2026
John Guerra
4306103
Not viewed
Thank you for your order.
Paid
On 05/06/2026
$3,184.00
05/05/2026
Travis Hauffman
4306102
Viewed
Thank you for your order
Overdue
By 15 days
$163.24
04/27/2026
Fernando
4276101
Viewed
Thank you for your business
Paid
On 04/27/2026
$1,262.79
04/24/2026
Betsy SUPPLY ONLY
4246104
Not viewed
Thank you for your order.
Paid
On 04/24/2026
$110.06
04/24/2026
Michael General Manager
000025
Viewed
Thank you for your order
Paid
On 05/09/2026
$295.98
04/24/2026
Lawrence Kam
4246102
Viewed
Thank you for your order.
Paid
On 04/24/2026
$739.20
04/24/2026
Lawrence Kam
4246103
Viewed
Thank you for your continued business.
Paid
On 04/24/2026
$390.00
04/24/2026
Hector CASIO
6226102
Not viewed
Thank you for your order
Draft
Send now
$0.00
04/23/2026
Michael Dunsford NCC
4166113
Viewed
Thank you for your order.
Paid
On 05/16/2026
$249.14
04/23/2026
Travis Hauffman
4166108
Viewed
Thank you for your order
Overdue
By 30 days
$242.67
04/23/2026
Leslie Manager
4166111
Viewed
Thank you for your order
Paid
On 05/09/2026
$197.18
04/22/2026
Betsy SUPPLY ONLY
6226101
Not viewed
Thank you for your order.
Paid
On 04/23/2026
$657.37
04/20/2026
Arden Chenda
4166112
Viewed
Thank you for your order
Paid
On 04/21/2026
$151.14
04/20/2026
Sam Manager
4166109
Viewed
Thank you.
Paid
On 05/07/2026
$232.53
04/20/2026
Emilio Owner
4166107
Viewed
Paid
On 04/20/2026
$1,459.22
04/19/2026
Inder Bains
000016
Viewed
Cabling (4) Runs for total of $600.00 each additional run can be added for $150.00
Paid
On 04/23/2026
$600.00
04/18/2026
Margarito General Manager
000021
Viewed
Thank you for your order.
Paid
On 05/21/2026
$700.78
04/16/2026
Katie Rondeau
4166105
Viewed
ORDER # 630668
Paid
On 05/11/2026
$790.00
04/16/2026
Katie Rondeau
4166104
Viewed
ORDER # 630670
Paid
On 05/15/2026
$178.00
04/16/2026
James General Manager
4166103
Viewed
Thank you for your order
Paid
On 04/23/2026
$380.38
04/15/2026
Lauro Owner
000024
Viewed
Thank you for your order
Paid
On 04/15/2026
$967.48
04/14/2026
Matt GM
000020
Viewed
Thank you for your order.
Paid
On 05/01/2026
$384.60
04/14/2026
Marco SUPPLY ONLY
000019
Not viewed
Paid
On 04/14/2026
$232.99
04/14/2026
Chris Owner
000017
Viewed
NCC Customer
Paid
On 04/14/2026
$1,965.00
04/14/2026
Megan Manager
000018
Viewed
Blue Tag MP7001
Paid
On 04/24/2026
$590.00
04/14/2026
Betsy Delfiero
000013
Viewed
Supply Order
Paid
On 05/15/2026
$616.54
04/13/2026
Judy Manager
000011
Viewed
Paid
On 04/13/2026
$367.50
04/13/2026
Nick Owner
000012
Not viewed
Paid
On 04/13/2026
$1,179.50
04/11/2026
Emmanual
000008
Not viewed
CONNECTION ISSUES - MICROSALE
Overdue
By 69 days
$675.00
03/06/2026
Caffe Greco
000010
Viewed
ER-900 Cash Drawer issue / Back up reprogram.
Paid
On 03/06/2026
$285.00
02/26/2026
Hector CASIO
000007
Not viewed
Paid
On 02/26/2026
$510.00
01/15/2026
Derrick Owner
003206
Viewed
We look forward to working with you.
Paid
On 01/19/2026
$8,786.00
12/12/2025
Hari Shrestha
000005
Not viewed
Service call
Paid
On 12/12/2025
$480.00
07/09/2025
Don Tom La Torre
000003
Viewed
Powercable
Paid
On 07/09/2025
$336.74
07/09/2025
Don Tom La Torre
000002
Viewed
Clear sales totals and GT, cable repair
Canceled
On 07/09/2025
$312.16"""


def parse_invoice_data(text):
    """Parse invoice data from text format"""
    records = []
    lines = text.strip().split('\n')
    
    current = {}
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Match amount pattern like "$425.61" or "$4,883.85"
        if re.match(r'^\$[\d,]+\.\d{2}$', line):
            amount = float(line.replace('$', '').replace(',', ''))
            
            # Initialize new record
            current = {
                'amount': amount,
                'raw_lines': [line],
                'status': 'Unpaid',  # default
                'viewed': False
            }
            
            i += 1
            
            # Collect all lines for this record until next amount or end
            while i < len(lines):
                next_line = lines[i].strip()
                
                # Check if this is the start of a new record (amount followed by date)
                if re.match(r'^\$[\d,]+\.\d{2}$', next_line):
                    if i + 1 < len(lines) and re.match(r'^\d{2}/\d{2}/\d{4}$', lines[i + 1].strip()):
                        break
                
                # Check for Today/Yesterday markers
                if next_line in ['Today', 'Yesterday']:
                    current['date_marker'] = next_line
                    i += 1
                    continue
                
                # Check for date pattern MM/DD/YYYY
                if re.match(r'^\d{2}/\d{2}/\d{4}$', next_line):
                    current['invoice_date'] = next_line
                    current['raw_lines'].append(next_line)
                    i += 1
                    continue
                
                # Check for invoice ID (6+ digits)
                if re.match(r'^\d{6,}$', next_line) and 'invoice_id' not in current:
                    current['invoice_id'] = next_line
                    current['raw_lines'].append(next_line)
                    i += 1
                    continue
                
                # Check for customer name (if no invoice_id yet, this might be customer)
                if not re.match(r'^(Paid|Unpaid|Overdue|Draft|Canceled|Viewed|Not viewed|On |Due |By \d+ days?|Thank you|ORDER|Please find|If you approve|Clear sales|CONNECTION|ER-900|Cabling|scanner|Powercable|POS Supplies|We look|Service call|Blue Tag|NCC Customer|Supply Order|Refunded|Undelivered|Payment pending|Draft|Sam4s|Sam4s SPT|Sam4s POS|open store|CASIO|SUPPLY ONLY|left msg)', next_line):
                    if 'customer_name' not in current and next_line:
                        current['customer_name'] = next_line
                        current['raw_lines'].append(next_line)
                        i += 1
                        continue
                
                # Check for status
                if next_line in ['Paid', 'Unpaid', 'Overdue', 'Draft', 'Canceled', 'Refunded', 'Undelivered', 'Payment pending']:
                    current['status'] = next_line
                    current['raw_lines'].append(next_line)
                    i += 1
                    continue
                
                # Check for viewed/not viewed
                if next_line == 'Viewed':
                    current['viewed'] = True
                    current['raw_lines'].append(next_line)
                    i += 1
                    continue
                elif next_line == 'Not viewed':
                    current['viewed'] = False
                    current['raw_lines'].append(next_line)
                    i += 1
                    continue
                
                # Check for "On MM/DD/YYYY" (paid date)
                if next_line.startswith('On '):
                    date_part = next_line.replace('On ', '')
                    current['paid_date'] = date_part
                    current['raw_lines'].append(next_line)
                    i += 1
                    continue
                
                # Check for "Due..." dates
                if next_line.startswith('Due '):
                    current['due_note'] = next_line
                    current['raw_lines'].append(next_line)
                    i += 1
                    continue
                
                # Check for overdue days
                overdue_match = re.match(r'^By (\d+) days?$', next_line)
                if overdue_match:
                    current['days_overdue'] = int(overdue_match.group(1))
                    current['status'] = 'Overdue'
                    current['raw_lines'].append(next_line)
                    i += 1
                    continue
                
                # Collect notes
                if len(next_line) > 5:
                    if 'notes' not in current:
                        current['notes'] = next_line
                    else:
                        current['notes'] += '; ' + next_line
                    current['raw_lines'].append(next_line)
                
                i += 1
            
            # Save valid record
            if 'invoice_id' in current and 'customer_name' in current:
                records.append(current)
                print(f"Parsed: {current['invoice_id']} - {current['customer_name']}")
        else:
            i += 1
    
    return records


def main():
    print("Parsing invoice data...")
    print("=" * 50)
    
    records = parse_invoice_data(RAW_DATA)
    print(f"\nParsed {len(records)} records")
    
    print("\nInitializing database...")
    db = CollectionsDB()
    
    print("\nLoading records...")
    success = 0
    failed = 0
    
    for record in records:
        if db.upsert_invoice(record):
            success += 1
        else:
            failed += 1
    
    print(f"\nLoaded: {success} successful, {failed} failed")
    
    # Generate summary
    print("\n" + "=" * 50)
    print("COLLECTIONS SUMMARY")
    print("=" * 50)
    
    summary, priority = db.get_summary()
    
    total_outstanding = 0
    for status, count, amount in summary:
        if amount:
            print(f"{status}: {count} invoices, ${amount:,.2f}")
            if status in ['Unpaid', 'Overdue']:
                total_outstanding += amount
    
    print(f"\nTotal Outstanding: ${total_outstanding:,.2f}")
    
    print("\n--- PRIORITY COLLECTIONS ---")
    for row in priority[:10]:
        inv_id, customer, amount, status, days = row[1], row[2], row[3], row[4], row[9]
        days_str = f"({days} days overdue)" if days else ""
        print(f"{customer}: ${amount:,.2f} - {status} {days_str}")
    
    # Export backup
    db.export_to_json("/root/.openclaw/workspace/collections/backup_2026-06-19.json")
    
    print("\n" + "=" * 50)
    print("Database saved to: /root/.openclaw/workspace/collections/collections.db")
    print("Backup saved to: /root/.openclaw/workspace/collections/backup_2026-06-19.json")


if __name__ == "__main__":
    main()
