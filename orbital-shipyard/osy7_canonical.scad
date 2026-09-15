// ============================================================
// OSY-7 — Modular Orbital Shipyard (Canonical)
// Scale: meters · Watertight build · Parametric kit
// ============================================================

$fn = 96;

// ---------- Parameters (tweak to scale the whole yard) ----------
assembly_dia    = 180;   // central zero-g bay diameter
assembly_length = 240;   // open assembly volume length
wall_thickness  = 5;     // bay shell wall
truss_size      = 42;    // square truss cross-section
truss_length    = 460;   // overall spine length
ring_dia        = 300;   // habitat/control ring diameter
ring_width      = 38;    // rotating ring width
ring_height     = 20;    // ring module height
module_size     = 28;    // service module size

// ---------- Module Library ----------

// Central open assembly bay (hollow thin-wall cylinder + internal decks)
module assembly_bay() {
    difference() {
        cylinder(h = assembly_length, d = assembly_dia, center = true);
        cylinder(h = assembly_length + 2, d = assembly_dia - 2*wall_thickness, center = true);
    }
    // Internal ring decks
    for (z = [-80, 0, 80]) {
        translate([0, 0, z])
        difference() {
            cylinder(h = 3, d = assembly_dia - 2*wall_thickness - 2, center = true);
            cylinder(h = 4, d = 90, center = true);
        }
    }
}

// Main structural truss spine (with cross bracing)
module main_truss() {
    cube([truss_size, truss_size, truss_length], center = true);
    for (z = [-200 : 50 : 200]) {
        translate([0, 0, z])
        rotate([0, 0, 45])
        cube([truss_size * 1.3, 3, 3], center = true);
    }
}

// Habitat / control ring (proper torus, offset clear of axis)
module habitat_ring() {
    rotate([90, 0, 0])
    rotate_extrude()
    translate([ring_dia / 2, 0, 0])
    square([ring_width, ring_height], center = true);
}

// Service / docking module
module service_module() {
    cube([module_size, module_size, module_size * 1.5], center = true);
}

// Solar array wing (segmented)
module solar_array(length = 140, width = 45) {
    cube([length, width, 1.5], center = true);
    for (i = [-length/2 + 10 : 20 : length/2 - 10]) {
        translate([i, 0, 1])
        cube([1, width - 2, 0.5], center = true);
    }
}

// Radiator panel
module radiator(length = 90, width = 30) {
    cube([length, width, 1], center = true);
}

// Robotic arm (segmented, angled)
module robotic_arm(len = 95) {
    cube([9, 9, 14], center = true);
    translate([0, 0, len * 0.38])
    rotate([0, 25, 0])
    cube([7, 7, len * 0.5], center = true);
    translate([len * 0.32, 0, len * 0.65])
    rotate([0, -35, 0])
    cube([6, 6, len * 0.38], center = true);
}

// Docking port
module docking_port() {
    cylinder(h = 14, d = 30, center = true);
    translate([0, 0, 9])
    cylinder(h = 7, d = 24, center = true);
}

// ---------- Assembly ----------

assembly_bay();

color("Gainsboro") main_truss();

// Habitat ring offset to one end
translate([0, 0, -assembly_length/2 - 70])
color("DarkOliveGreen") habitat_ring();

// Service modules along the truss (both sides)
for (z = [-200 : 55 : 200]) {
    translate([ truss_size/2 + module_size/2 + 6, 0, z]) color("DimGray") service_module();
    translate([-(truss_size/2 + module_size/2 + 6), 0, z]) color("DimGray") service_module();
}

// Extra pressurized modules
translate([0,  truss_size/2 + 20,  100]) color("SlateGray") cube([35, 30, 40], center = true);
translate([0, -(truss_size/2 + 20), -80]) color("SlateGray") cube([35, 30, 40], center = true);

// Solar arrays (both sides)
translate([0,  160, 0]) rotate([0, 0, 90]) color("MidnightBlue") solar_array(140, 45);
translate([0, -160, 0]) rotate([0, 0, 90]) color("MidnightBlue") solar_array(140, 45);

// Radiators
translate([ 90, 0,  140]) rotate([0, 90, 0]) color("Silver") radiator(90, 30);
translate([-90, 0, -140]) rotate([0, 90, 0]) color("Silver") radiator(90, 30);

// Robotic arms
translate([ assembly_dia/2 - 12, 0,  50]) color("DarkOrange") robotic_arm(100);
translate([-assembly_dia/2 + 12, 0, -40]) rotate([0,0,180]) color("DarkOrange") robotic_arm(90);
translate([0,  assembly_dia/2 - 12,  90]) rotate([0,0,90])  color("DarkOrange") robotic_arm(75);
translate([0, -assembly_dia/2 + 12, -70]) rotate([0,0,-90]) color("DarkOrange") robotic_arm(80);

// End docking ports
translate([0, 0,  truss_length/2 - 12]) color("LightSteelBlue") docking_port();
translate([0, 0, -truss_length/2 + 12]) color("LightSteelBlue") docking_port();
