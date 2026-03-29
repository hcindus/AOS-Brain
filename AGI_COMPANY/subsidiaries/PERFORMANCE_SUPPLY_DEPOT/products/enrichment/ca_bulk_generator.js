#!/usr/bin/env node
/**
 * Bulk CA Lead Generator
 * Generates sample leads for all major CA cities
 */

const CASOSScraper = require('./ca_sos_scraper_fixed.js');
const fs = require('fs');
const path = require('path');

const CITIES = [
    "Los Angeles", "San Diego", "San Jose", "San Francisco", 
    "Fresno", "Sacramento", "Long Beach", "Oakland", 
    "Santa Ana", "Anaheim"
];

const BUSINESS_TYPES = [
    "restaurant", "cafe", "taqueria", "burger", "diner", 
    "breakfast", "mexican", "italian", "chinese", "thai"
];

async function main() {
    console.log('═══════════════════════════════════════════');
    console.log('  CA BULK LEAD GENERATOR');
    console.log('═══════════════════════════════════════════\n');
    
    const scraper = new CASOSScraper({ useSampleData: true });
    const allLeads = [];
    
    console.log(`🔄 Generating leads: ${BUSINESS_TYPES.length} types × ${CITIES.length} cities`);
    
    for (const city of CITIES) {
        process.stdout.write(`   ${city}... `);
        for (const type of BUSINESS_TYPES) {
            // Generate 5 leads per city/type combo
            const leads = scraper.generateSampleLeads(`${city} ${type}`, 5);
            // Update city and business name to be more realistic
            leads.forEach(lead => {
                lead.city = city;
                lead.business_name = `${type.charAt(0).toUpperCase() + type.slice(1)} ${Math.floor(Math.random() * 999) + 1}`;
                lead.source = 'CA_Bulk_Generator';
            });
            allLeads.push(...leads);
        }
        console.log('✓');
    }
    
    console.log(`\n✅ Generated ${allLeads.length} total leads`);
    
    // Save results
    const date = new Date().toISOString().split('T')[0];
    const filename = `CA_leads_${date}_bulk.json`;
    const outputPath = path.join(scraper.outputDir, filename);
    
    fs.writeFileSync(outputPath, JSON.stringify(allLeads, null, 2));
    console.log(`💾 Saved to: ${outputPath}`);
    
    // Summary
    console.log('\n📊 SUMMARY:');
    console.log(`   Total leads: ${allLeads.length}`);
    console.log(`   Cities: ${new Set(allLeads.map(l => l.city)).size}`);
    console.log(`   Business types: ${new Set(allLeads.map(l => l.business_type)).size}`);
    console.log(`   High priority: ${allLeads.filter(l => l.priority === 'high').length}`);
    
    // Sample
    console.log('\n📋 Sample leads:');
    allLeads.slice(0, 5).forEach(lead => {
        console.log(`   - ${lead.business_name} | ${lead.city}, ${lead.state} | ${lead.phone}`);
    });
    console.log(`   ... and ${allLeads.length - 5} more`);
}

main().catch(err => {
    console.error('❌ Error:', err.message);
    process.exit(1);
});
