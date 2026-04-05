# Square Customer Database Import Guide

## File Format
CSV files formatted for Square Customer Directory import

## Required Columns (Square Format)
- First Name
- Last Name
- Email
- Phone
- Company
- Address Line 1 (optional)
- City
- State
- Postal Code (optional)
- Tags
- Notes

## Import Process
1. Open Square Dashboard
2. Go to Customers → Import Customers
3. Upload the CSV file
4. Map columns to Square fields
5. Review and confirm

## File Naming Convention
- COMPLETED_[STATE]_leads.csv (by state)
- COMPLETED_ALL_STATES.csv (master file)

## Data Sources
- CREAM: Real estate agents (1,000)
- TX: Texas businesses (Secretary of State)
- CA: California businesses (Secretary of State)
- Other states as available

## Notes
- All emails are unique (deduplicated)
- Phone numbers formatted consistently
- Companies linked to contact person
- Tags indicate source and priority
