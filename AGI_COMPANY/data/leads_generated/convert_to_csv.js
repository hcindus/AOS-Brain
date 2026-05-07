#!/usr/bin/env node
/**
 * Convert JSON lead files to CSV and consolidate
 */

const fs = require('fs');
const path = require('path');

const INPUT_DIR = '/root/.openclaw/workspace/AGI_COMPANY/data/leads_generated';
const OUTPUT_DIR = INPUT_DIR;

// CSV header
const CSV_HEADER = 'business_name,status,jurisdiction,incorporation_date,agent,address,city,state,zip,county,phone,email,sos_id,business_type,source,priority,discovered_at,enrichment_status\n';

function escapeCsv(value) {
  if (value === null || value === undefined) return '';
  const str = String(value);
  if (str.includes(',') || str.includes('"') || str.includes('\n')) {
    return '"' + str.replace(/"/g, '""') + '"';
  }
  return str;
}

function jsonToCsv(leads) {
  return leads.map(lead => {
    return [
      lead.business_name || lead.BusinessName || '',
      lead.status || lead.Status || '',
      lead.jurisdiction || 'California',
      lead.incorporation_date || lead.IncorporationDate || '',
      lead.agent || lead.AgentName || '',
      lead.address || lead.Address || '',
      lead.city || lead.City || '',
      lead.state || lead.State || 'CA',
      lead.zip || lead.ZipCode || '',
      lead.county || '',
      lead.phone || '',
      lead.email || '',
      lead.sos_id || lead.SOSID || '',
      lead.business_type || '',
      lead.source || 'CA_SOS_Scraper',
      lead.priority || 'normal',
      lead.discovered_at || new Date().toISOString(),
      lead.enrichment_status || 'pending'
    ].map(escapeCsv).join(',');
  }).join('\n');
}

function extractJsonFromOutput(content) {
  // Try to find JSON array in the output
  const jsonMatch = content.match(/\[\s*\{[\s\S]*\}\s*\]/);
  if (jsonMatch) {
    try {
      return JSON.parse(jsonMatch[0]);
    } catch (e) {
      // Try to find individual objects
      const objects = [];
      const objMatches = content.match(/\{[^{}]*"business_name"[^{}]*\}/g);
      if (objMatches) {
        for (const match of objMatches) {
          try {
            objects.push(JSON.parse(match));
          } catch (e2) {
            // Skip invalid
          }
        }
      }
      return objects;
    }
  }
  return [];
}

// Process all JSON files
const allLeads = [];
const files = fs.readdirSync(INPUT_DIR).filter(f => f.endsWith('.json') && f.startsWith('CA_'));

console.log(`📁 Found ${files.length} JSON files to process`);

for (const file of files) {
  const filepath = path.join(INPUT_DIR, file);
  const content = fs.readFileSync(filepath, 'utf8');
  
  let leads = [];
  try {
    // Try direct JSON parse first
    leads = JSON.parse(content);
  } catch (e) {
    // Extract from mixed output
    leads = extractJsonFromOutput(content);
  }
  
  if (Array.isArray(leads) && leads.length > 0) {
    allLeads.push(...leads);
    console.log(`  ✅ ${file}: ${leads.length} leads`);
  } else {
    console.log(`  ⚠️  ${file}: No leads found`);
  }
}

// Deduplicate by business_name + city
const seen = new Set();
const uniqueLeads = allLeads.filter(lead => {
  const key = `${lead.business_name || lead.BusinessName}_${lead.city || lead.City}`;
  if (seen.has(key)) return false;
  seen.add(key);
  return true;
});

console.log(`\n📊 Total leads before dedup: ${allLeads.length}`);
console.log(`📊 Total leads after dedup: ${uniqueLeads.length}`);

// Save individual county CSVs
const countyGroups = {};
for (const lead of uniqueLeads) {
  const county = lead.county || lead.County || 'Unknown';
  if (!countyGroups[county]) countyGroups[county] = [];
  countyGroups[county].push(lead);
}

// Save consolidated CSV
const timestamp = new Date().toISOString().split('T')[0];
const consolidatedPath = path.join(OUTPUT_DIR, `CA_ALL_COUNTIES_${timestamp}.csv`);
fs.writeFileSync(consolidatedPath, CSV_HEADER + jsonToCsv(uniqueLeads));
console.log(`\n💾 Consolidated CSV: ${consolidatedPath} (${uniqueLeads.length} leads)`);

// Save individual county CSVs
let countyCsvCount = 0;
for (const [county, leads] of Object.entries(countyGroups)) {
  const countyFile = path.join(OUTPUT_DIR, `CA_${county.replace(/\s+/g, '_')}_Leads.csv`);
  fs.writeFileSync(countyFile, CSV_HEADER + jsonToCsv(leads));
  countyCsvCount++;
}
console.log(`💾 County CSVs: ${countyCsvCount} files`);

// Save as JSON too
const jsonPath = path.join(OUTPUT_DIR, `CA_ALL_COUNTIES_${timestamp}.json`);
fs.writeFileSync(jsonPath, JSON.stringify(uniqueLeads, null, 2));
console.log(`💾 JSON backup: ${jsonPath}`);

// Summary
console.log('\n=== SUMMARY ===');
console.log(`Total unique CA leads: ${uniqueLeads.length}`);
console.log(`Counties covered: ${Object.keys(countyGroups).length}`);
console.log(`Files generated: ${countyCsvCount + 2}`);
