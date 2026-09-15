// ============================================================
// Modular Orbital Shipyard - Parametric Concept
// Scale: meters
// ============================================================

$fn = 64; // smoothness

// -------------------- Parameters (easy to tweak) --------------------
assembly_dia = 180; // diameter of central zero-g bay
assembly_length = 220; // length of open assembly volume
truss_size = 40; // square truss cross-section
truss_length = 420; // overall spine length
ring_dia = 280; // habitat/control ring diameter
ring_width = 35; // width of the rotating ring
ring_height = 18; // height of ring modules
module_size = 25; // size of service modules

// -------------------- Modules --------------------

// Central open assembly cylinder (thin wall representation)
module assembly_bay() {
 difference() {
 cylinder(h = assembly_length, d = assembly_dia, center = true);
 cylinder(h = assembly_length + 2, d = assembly_dia - 8, center = true);
 }
}

// Main structural truss spine
module main_truss() {
 color("LightGray")
 cube([truss_size, truss_size, truss_length], center = true);
}

// Habitat / control ring (simplified as a toroidal structure)
module habitat_ring() {
 rotate([90, 0, 0])
 rotate_extrude(angle = 360)
 translate([ring_dia/2, 0, 0])
 square([ring_width, ring_height], center = true);
}

// Service / docking module
module service_module() {
 cube([module_size, module_size, module_size*1.4], center = true);
}

// Simplified large robotic arm
module robotic_arm(length = 90) {
 // Base
 cube([8, 8, 12], center = true);
 // Upper arm
 translate([0, 0, length*0.4])
 rotate([0, 30, 0])
 cube([6, 6, length*0.55], center = true);
 // Forearm
 translate([length*0.35, 0, length*0.7])
 rotate([0, -40, 0])
 cube([5, 5, length*0.4], center = true);
}

// -------------------- Assembly --------------------

// Central zero-g assembly bay
color("SteelBlue")
translate([0, 0, 0])
assembly_bay();

// Main truss spine running through
main_truss();

// Habitat ring offset to one side of the assembly bay
color("DarkOliveGreen")
translate([0, 0, -assembly_length/2 - 60])
habitat_ring();

// Service modules along the truss
for (z = [-180 : 60 : 180]) {
 translate([truss_size/2 + module_size/2 + 5, 0, z])
 color("DimGray")
 service_module();
 
 translate([-(truss_size/2 + module_size/2 + 5), 0, z])
 color("DimGray")
 service_module();
}

// A few large robotic arms
translate([assembly_dia/2 - 10, 0, 40])
color("Orange")
robotic_arm(95);

translate([-assembly_dia/2 + 10, 0, -30])
rotate([0, 0, 180])
color("Orange")
robotic_arm(85);

translate([0, assembly_dia/2 - 10, 80])
rotate([0, 0, 90])
color("Orange")
robotic_arm(70);

// Simple end docking ports
module docking_port() {
 cylinder(h = 12, d = 28, center = true);
 translate([0, 0, 8])
 cylinder(h = 6, d = 22, center = true);
}

translate([0, 0, truss_length/2 - 10])
color("Silver")
docking_port();

translate([0, 0, -truss_length/2 + 10])
color("Silver")
docking_port();
