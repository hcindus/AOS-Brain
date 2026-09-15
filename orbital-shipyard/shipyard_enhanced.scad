// ============================================================
// Enhanced Modular Orbital Shipyard
// Scale: meters
// ============================================================

$fn = 48;

// Parameters
assembly_dia = 180;
assembly_length = 240;
truss_size = 42;
truss_length = 460;
ring_dia = 300;
ring_width = 38;
ring_height = 20;
module_size = 28;

// Central assembly bay
module assembly_bay() {
 difference() {
 cylinder(h = assembly_length, d = assembly_dia, center = true);
 cylinder(h = assembly_length + 4, d = assembly_dia - 10, center = true);
 }
 // Internal ring decks (simplified)
 for (z = [-80, 0, 80]) {
 translate([0, 0, z])
 difference() {
 cylinder(h = 3, d = assembly_dia - 12, center = true);
 cylinder(h = 4, d = 90, center = true);
 }
 }
}

// Main truss
module main_truss() {
 color("Gainsboro")
 cube([truss_size, truss_size, truss_length], center = true);
 // Cross bracing indication
 for (z = [-200 : 50 : 200]) {
 translate([0, 0, z])
 rotate([0, 0, 45])
 cube([truss_size*1.3, 3, 3], center = true);
 }
}

// Habitat ring
module habitat_ring() {
 color("DarkOliveGreen")
 rotate([90, 0, 0])
 rotate_extrude()
 translate([ring_dia/2, 0, 0])
 square([ring_width, ring_height], center = true);
}

// Service module
module service_module() {
 cube([module_size, module_size, module_size*1.5], center = true);
}

// Solar array wing
module solar_array(length = 120, width = 40) {
 color("MidnightBlue")
 cube([length, width, 1.5], center = true);
 // Panel segmentation
 for (i = [-length/2 + 10 : 20 : length/2 - 10]) {
 translate([i, 0, 1])
 cube([1, width-2, 0.5], center = true);
 }
}

// Radiator panel
module radiator(length = 80, width = 25) {
 color("Silver")
 cube([length, width, 1], center = true);
}

// Robotic arm
module robotic_arm(len = 95) {
 color("DarkOrange") {
 cube([9, 9, 14], center = true);
 translate([0, 0, len*0.38])
 rotate([0, 25, 0])
 cube([7, 7, len*0.5], center = true);
 translate([len*0.32, 0, len*0.65])
 rotate([0, -35, 0])
 cube([6, 6, len*0.38], center = true);
 }
}

// Docking port
module docking_port() {
 color("LightSteelBlue") {
 cylinder(h = 14, d = 30, center = true);
 translate([0, 0, 9])
 cylinder(h = 7, d = 24, center = true);
 }
}

// -------------------- Build --------------------

// Assembly bay
color("SteelBlue")
assembly_bay();

// Truss
main_truss();

// Habitat ring
translate([0, 0, -assembly_length/2 - 70])
habitat_ring();

// Service modules
for (z = [-200 : 55 : 200]) {
 translate([truss_size/2 + module_size/2 + 6, 0, z])
 color("DimGray") service_module();
 translate([-(truss_size/2 + module_size/2 + 6), 0, z])
 color("DimGray") service_module();
}

// Extra pressurized modules
translate([0, truss_size/2 + 20, 100])
color("SlateGray")
cube([35, 30, 40], center = true);

translate([0, -(truss_size/2 + 20), -80])
color("SlateGray")
cube([35, 30, 40], center = true);

// Solar arrays
translate([0, 160, 0])
rotate([0, 0, 90])
solar_array(140, 45);

translate([0, -160, 0])
rotate([0, 0, 90])
solar_array(140, 45);

// Radiators
translate([90, 0, 140])
rotate([0, 90, 0])
radiator(90, 30);

translate([-90, 0, -140])
rotate([0, 90, 0])
radiator(90, 30);

// Robotic arms
translate([assembly_dia/2 - 12, 0, 50])
robotic_arm(100);

translate([-assembly_dia/2 + 12, 0, -40])
rotate([0, 0, 180])
robotic_arm(90);

translate([0, assembly_dia/2 - 12, 90])
rotate([0, 0, 90])
robotic_arm(75);

translate([0, -assembly_dia/2 + 12, -70])
rotate([0, 0, -90])
robotic_arm(80);

// End docking ports
translate([0, 0, truss_length/2 - 12])
docking_port();

translate([0, 0, -truss_length/2 + 12])
docking_port();
