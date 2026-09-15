// ============================================================
// OSY-7 — Orbital Shipyard v2 (Complete · Interior + Exterior)
// Units: meters · Merged from all design revisions
// ============================================================

$fn = 64;

// -------------------- Parameters --------------------
assembly_dia   = 180;
assembly_length = 250;
wall_thickness = 5.5;
inner_clear_dia = 85;
truss_size     = 44;
truss_length   = 480;
ring_dia       = 310;
ring_width     = 40;
ring_height    = 22;
module_size    = 30;
deck_thickness = 2.6;

// -------------------- Helpers --------------------
module rounded_cube(size, radius = 1.5) {
    minkowski() {
        cube(size - [radius*2, radius*2, radius*2], center = true);
        sphere(r = radius);
    }
}

// -------------------- Assembly Bay (double-sided mesh) --------------------
module assembly_bay_mesh() {
    // Exterior shell
    difference() {
        cylinder(h = assembly_length, d = assembly_dia, center = true);
        cylinder(h = assembly_length + 2, d = assembly_dia - wall_thickness*2, center = true);
    }
    // Interior wall surface
    difference() {
        cylinder(h = assembly_length - 1, d = assembly_dia - wall_thickness*2 + 0.8, center = true);
        cylinder(h = assembly_length + 2, d = assembly_dia - wall_thickness*2 - 1.5, center = true);
    }
    // Internal decks
    for (z = [-95, -35, 25, 85]) {
        translate([0, 0, z]) {
            // Deck ring
            difference() {
                cylinder(h = deck_thickness, d = assembly_dia - wall_thickness*2 - 1, center = true);
                cylinder(h = deck_thickness + 2, d = inner_clear_dia, center = true);
            }
            // Support spokes
            for (a = [0 : 30 : 330]) {
                rotate([0, 0, a])
                translate([(assembly_dia/2 + inner_clear_dia/2)/2 - 2, 0, 0])
                cube([(assembly_dia - inner_clear_dia)/2 - 6, 4.5, deck_thickness + 0.6], center = true);
            }
            // Inner safety ring / railing base
            difference() {
                cylinder(h = 1.8, d = inner_clear_dia + 9, center = true);
                cylinder(h = 3, d = inner_clear_dia + 4, center = true);
            }
        }
    }
    // Longitudinal interior stringers
    for (a = [0 : 45 : 315]) {
        rotate([0, 0, a])
        translate([assembly_dia/2 - wall_thickness - 3.5, 0, 0])
        cube([3, 5, assembly_length - 20], center = true);
    }
}

// -------------------- Main Truss (dual cross-bracing) --------------------
module main_truss() {
    cube([truss_size, truss_size, truss_length], center = true);
    for (z = [-210 : 40 : 210]) {
        translate([0, 0, z]) {
            rotate([0, 0, 45])  cube([truss_size*1.35, 4, 3.5], center = true);
            rotate([0, 0, -45]) cube([truss_size*1.35, 4, 3.5], center = true);
        }
    }
}

// -------------------- Habitat / Control Ring --------------------
module habitat_ring() {
    rotate([90, 0, 0])
    rotate_extrude()
    translate([ring_dia/2, 0, 0])
    square([ring_width, ring_height], center = true);
}

// -------------------- Multi-segment Robotic Arm (angle, length) --------------------
module robotic_arm(angle = 0, len = 95) {
    rotate([0, 0, angle]) {
        // Base mount
        cylinder(h = 16, d = 14, center = true);
        // Shoulder joint
        translate([0, 0, 12]) sphere(d = 12);
        // Upper arm (angled out)
        rotate([0, 28, 0]) {
            translate([0, 0, len*0.25]) cube([10, 10, len*0.5], center = true);
            // Elbow joint
            translate([0, 0, len*0.5]) sphere(d = 9);
            // Forearm
            rotate([0, -45, 0]) {
                translate([0, 0, len*0.18]) cube([7, 7, len*0.36], center = true);
                // Wrist + end effector
                translate([0, 0, len*0.36]) {
                    sphere(d = 7);
                    translate([0, 0, 4]) {
                        // Two-finger gripper
                        cube([6, 2.5, 8], center = true);
                        translate([3, 0, 0]) cube([2.5, 6, 8], center = true);
                        translate([-3, 0, 0]) cube([2.5, 6, 8], center = true);
                    }
                }
            }
        }
    }
}

// -------------------- Solar Array (thick + segmented) --------------------
module solar_array(length = 150, width = 48) {
    // Backing panel
    cube([length, width, 2.5], center = true);
    // Frame rails
    translate([0, width/2 - 2, 0]) cube([length, 2, 2.5], center = true);
    translate([0, -(width/2 - 2), 0]) cube([length, 2, 2.5], center = true);
    // Panel segmentation
    for (i = [-length/2 + 12 : 24 : length/2 - 12]) {
        translate([i, 0, 1.3]) cube([2, width - 6, 0.6], center = true);
    }
}

// -------------------- Radiator (thick + framed) --------------------
module radiator(length = 90, width = 32) {
    cube([length, width, 1.6], center = true);
    translate([0, width/2 - 2, 0]) cube([length, 2.5, 1.6], center = true);
    translate([0, -(width/2 - 2), 0]) cube([length, 2.5, 1.6], center = true);
    for (i = [-length/2 + 8 : 16 : length/2 - 8]) {
        translate([i, 0, 0.9]) cube([2, width - 4, 0.6], center = true);
    }
}

// -------------------- Service / Pressurized Module --------------------
module service_module() {
    rounded_cube([module_size, module_size, module_size*1.5], 2);
}

// -------------------- Docking Port / Adapter --------------------
module docking_port() {
    cylinder(h = 16, d = 32, center = true);
    translate([0, 0, 10]) cylinder(h = 8, d = 26, center = true);
    translate([0, 0, 15]) cylinder(h = 3, d = 30, center = true);
}

// -------------------- Antenna / Sensor --------------------
module antenna() {
    cylinder(h = 20, d = 3);
    translate([0, 0, 20]) sphere(d = 5);
}

// ==================== ASSEMBLY ====================

// Assembly bay (double-sided)
color("SteelBlue") assembly_bay_mesh();

// Main truss
color("Gainsboro") main_truss();

// Habitat ring
translate([0, 0, -assembly_length/2 - 75])
color("DarkOliveGreen") habitat_ring();

// Service modules along truss
for (z = [-210 : 55 : 210]) {
    translate([ truss_size/2 + module_size/2 + 6, 0, z]) color("DimGray") service_module();
    translate([-(truss_size/2 + module_size/2 + 6), 0, z]) color("DimGray") service_module();
}

// Extra pressurized modules
translate([0,  truss_size/2 + 22,  110]) color("SlateGray") rounded_cube([38, 32, 44], 2);
translate([0, -(truss_size/2 + 22), -85]) color("SlateGray") rounded_cube([38, 32, 44], 2);

// Solar arrays
translate([0,  165, 0]) rotate([0, 0, 90]) color("MidnightBlue") solar_array(150, 48);
translate([0, -165, 0]) rotate([0, 0, 90]) color("MidnightBlue") solar_array(150, 48);

// Radiators
translate([ 95, 0,  145]) rotate([0, 90, 0]) color("Silver") radiator(90, 32);
translate([-95, 0, -145]) rotate([0, 90, 0]) color("Silver") radiator(90, 32);

// Robotic arms (articulated, angle + length)
translate([ assembly_dia/2 - 14, 0,  50]) color("DarkOrange") robotic_arm(0, 100);
translate([-assembly_dia/2 + 14, 0, -45]) color("DarkOrange") robotic_arm(180, 98);
translate([0,  assembly_dia/2 - 14,  95]) color("DarkOrange") robotic_arm(90, 85);
translate([0, -assembly_dia/2 + 14, -75]) color("DarkOrange") robotic_arm(-90, 88);

// End docking ports
translate([0, 0,  truss_length/2 - 14]) color("LightSteelBlue") docking_port();
translate([0, 0, -truss_length/2 + 14]) color("LightSteelBlue") docking_port();

// Antennas / sensors
for (z = [-180, 0, 180]) {
    translate([truss_size/2 + 6, truss_size/2 + 6, z]) color("Gray") antenna();
    translate([-(truss_size/2 + 6), -(truss_size/2 + 6), z]) color("Gray") antenna();
}
