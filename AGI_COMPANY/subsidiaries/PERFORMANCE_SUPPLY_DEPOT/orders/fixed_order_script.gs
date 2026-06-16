/***** FIXED COLUMN MAPPING *****/
const rowData = e.values;

// Updated column indices for current form structure
const timestampRaw = rowData[0];      // A
const customerEmail = rowData[1];    // B
const managerName = rowData[2];      // C
const businessName = rowData[3];     // D
const address = rowData[4];           // E
const city = rowData[5];              // F
const state = rowData[6];            // G
const zip = rowData[7];               // H - ZIP (was being read as qty!)
const orderDate = rowData[8];         // I

// Quantities now start at index 9
const qtyPF230 = Number(rowData[9] || 0);   // J
const qty13305 = Number(rowData[10] || 0);  // K
const qtyCC235 = Number(rowData[11] || 0);  // L
const qty62245 = Number(rowData[12] || 0);  // M
const qty67240 = Number(rowData[13] || 0);  // N

// Notes at index 14
const notes = rowData[14] || "";             // O

// Checkbox at index 15 (optional)
// const agreement = rowData[15] || "";

/***** BUILD SHIP TO *****/
const shipTo = `${address}\n${city}, ${state} ${zip}`;

/***** REST OF SCRIPT WORKS THE SAME *****/
// calculateTotals(), buildLineItems(), etc.