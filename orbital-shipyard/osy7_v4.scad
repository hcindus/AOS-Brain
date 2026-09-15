// ============================================================
// Orbital Shipyard – OSY-7 v4 (Full Version)
// + Floor grating, handrails, cable trays, lighting
// + Detailed habitat interior modules + exterior nav lights
// Units: meters
// ============================================================

$fn = 48; // raise to 64-80 for final export

// -------------------- Parameters --------------------
assembly_dia   = 180;
assembly_length = 250;
wall_thickness = 5.5;
inner_clear_dia = 82;
truss_size     = 44;
truss_length   = 480;
deck_thickness = 2.5;
habitat_radius = 155; // centerline radius of habitat ring

// -------------------- Modules --------------------

// --- Assembly Bay with Grating, Handrails, Cable Trays & Lighting ---
module assembly_bay() {
    // Exterior shell
    difference() {
        cylinder(h = assembly_length, d = assembly_dia, center = true);
        cylinder(h = assembly_length + 2, d = assembly_dia - wall_thickness*2, center = true);
    }
    // Interior wall surface
    difference() {
        cylinder(h = assembly_length - 1, d = assembly_dia - wall_thickness*2 + 0.7, center = true);
        cylinder(h = assembly_length + 2, d = assembly_dia - wall_thickness*2 - 1.8, center = true);
    }
    // Internal Decks + Grating + Handrails
    for (z = [-95, -35, 25, 85]) {
        translate([0, 0, z]) {
            // Solid deck base
            difference() {
                cylinder(h = deck_thickness, d = assembly_dia - wall_thickness*2 - 1, center = true);
                cylinder(h = deck_thickness + 2, d = inner_clear_dia, center = true);
            }
            // Floor grating pattern
            color("Gray") {
                for (r = [inner_clear_dia/2 + 6 : 8 : assembly_dia/2 - wall_thickness - 8]) {
                    for (a = [0 : 12 : 359]) {
                        rotate([0, 0, a])
                        translate([r, 0, deck_thickness/2 + 0.15])
                        cube([1.1, 5.5, 0.35], center = true);
                    }
                }
            }
            // Support spokes
            for (a = [0 : 30 : 330]) {
                rotate([0, 0, a])
                translate([(assembly_dia + inner_clear_dia)/4 - 1, 0, 0])
                cube([(assembly_dia - inner_clear_dia)/2 - 8, 4.2, deck_thickness + 0.5], center = true);
            }
            // Inner safety ring
            difference() {
                cylinder(h = 1.6, d = inner_clear_dia + 10, center = true);
                cylinder(h = 3, d = inner_clear_dia + 5, center = true);
            }
            // Handrails
            color("Silver") {
                difference() {
                    cylinder(h = 4.5, d = inner_clear_dia + 7, center = false);
                    cylinder(h = 5.5, d = inner_clear_dia + 5.8, center = false);
                    translate([0, 0, -1]) cylinder(h = 2, d = inner_clear_dia + 9, center = false);
                }
                for (a = [0 : 30 : 330]) {
                    rotate([0, 0, a])
                    translate([inner_clear_dia/2 + 3.2, 0, 0])
                    cylinder(h = 4.5, d = 0.7);
                }
            }
        }
    }
    // Longitudinal stringers
    for (a = [0 : 45 : 315]) {
        rotate([0, 0, a])
        translate([assembly_dia/2 - wall_thickness - 4, 0, 0])
        cube([3.2, 5, assembly_length - 25], center = true);
    }
    // Cable trays
    color("DarkSlateGray") {
        for (a = [0 : 45 : 315]) {
            rotate([0, 0, a])
            translate([assembly_dia/2 - wall_thickness - 7.5, 0, 0])
            cube([2.2, 3.5, assembly_length - 30], center = true);
        }
        for (z = [-95, -35, 25, 85]) {
            translate([0, 0, z + 1.8]) {
                difference() {
                    cylinder(h = 1.4, d = assembly_dia - wall_thickness*2 - 8, center = true);
                    cylinder(h = 2.5, d = assembly_dia - wall_thickness*2 - 14, center = true);
                }
            }
        }
    }
    // Interior lighting
    color("LightYellow") {
        for (z = [-95, -35, 25, 85]) {
            for (a = [0 : 45 : 315]) {
                rotate([0, 0, a])
                translate([assembly_dia/2 - wall_thickness - 11, 0, z + 2.2])
                sphere(d = 2.8);
            }
        }
        for (a = [22.5 : 45 : 360]) {
            rotate([0, 0, a])
            translate([assembly_dia/2 - wall_thickness - 6, 0, 0])
            cube([1.2, 1.2, assembly_length - 40], center = true);
        }
    }
}

// --- Detailed Habitat Ring with Modular Interiors + Artificial Gravity Cues ---
module habitat_ring() {
    // Main structural torus
    color("DarkOliveGreen") {
        rotate([90, 0, 0])
        rotate_extrude()
        translate([habitat_radius, 0, 0])
        square([44, 26], center = true);
    }
    // Modular interior units (floor oriented outward = spin gravity "down")
    for (a = [0 : 30 : 330]) {
        rotate([0, a, 0]) {
            translate([habitat_radius, 0, 0]) {
                if (a % 90 == 0) {
                    // Crew quarters (with bunks)
                    color("OliveDrab") rotate([90, 0, 0]) cube([22, 32, 20], center = true);
                    color("SaddleBrown") translate([9, 0, 0]) rotate([90, 0, 0]) cube([2, 28, 18], center = true);
                    color("Tan") translate([5, 8, 0]) rotate([90, 0, 0]) cube([8, 10, 6], center = true);
                    color("Tan") translate([5, -8, 0]) rotate([90, 0, 0]) cube([8, 10, 6], center = true);
                }
                else if (a % 60 == 0) {
                    // Workstation / lab
                    color("DarkKhaki") rotate([90, 0, 0]) cube([22, 32, 20], center = true);
                    color("SaddleBrown") translate([9, 0, 0]) rotate([90, 0, 0]) cube([2, 28, 18], center = true);
                    color("DimGray") translate([4, 0, 0]) rotate([90, 0, 0]) cube([6, 20, 8], center = true);
                }
                else {
                    // Corridor / life support
                    color("Olive") rotate([90, 0, 0]) cube([18, 30, 16], center = true);
                    color("SaddleBrown") translate([7, 0, 0]) rotate([90, 0, 0]) cube([2, 26, 14], center = true);
                }
                // Window strip
                color("LightSkyBlue") translate([11.5, 0, 0]) rotate([90, 0, 0]) cube([1.2, 16, 9], center = true);
            }
        }
    }
    // Exterior lights
    color("LightYellow") {
        for (a = [0 : 30 : 330]) {
            rotate([0, a, 0]) translate([178, 0, 0]) sphere(d = 3.5);
        }
    }
    // --- Artificial gravity visual cues ---
    // Red arrows pointing outward = gravity vector ("down")
    color("Red") {
        for (a = [0 : 60 : 300]) {
            rotate([0, a, 0]) translate([habitat_radius + 28, 0, 0]) {
                rotate([0, 90, 0]) cylinder(h = 12, d = 1.8);
                translate([12, 0, 0]) rotate([0, 90, 0]) cylinder(h = 6, d1 = 4.5, d2 = 0);
            }
        }
    }
    // Cyan spin direction indicators
    color("Cyan") {
        for (a = [15 : 60 : 360]) {
            rotate([0, a, 0]) translate([habitat_radius + 22, 8, 0]) rotate([90, 0, 0]) cylinder(h = 5, d = 1.5);
        }
    }
}

// --- Main Truss ---
module main_truss() {
    color("Gainsboro") {
        cube([truss_size, truss_size, truss_length], center = true);
        for (z = [-210 : 40 : 210]) {
            translate([0, 0, z]) {
                rotate([0, 0, 45]) cube([truss_size*1.35, 4, 3.5], center = true);
                rotate([0, 0, -45]) cube([truss_size*1.35, 4, 3.5], center = true);
            }
        }
    }
}

// --- Robotic Arm ---
module robotic_arm(base_rot = 0, arm_len = 100) {
    color("DarkOrange")
    rotate([0, 0, base_rot]) {
        cylinder(h = 16, d = 14, center = true);
        translate([0, 0, 12])
        rotate([0, 28, 0]) {
            cylinder(h = 10, d = 11, center = true);
            translate([0, 0, arm_len*0.38]) cube([9, 9, arm_len*0.55], center = true);
            translate([0, 0, arm_len*0.55])
            rotate([0, -48, 0]) {
                cylinder(h = 9, d = 9, center = true);
                translate([0, 0, arm_len*0.28]) cube([7, 7, arm_len*0.38], center = true);
                translate([0, 0, arm_len*0.38]) {
                    cylinder(h = 7, d = 7, center = true);
                    translate([4.2, 0, 5]) cube([2.2, 6.5, 10], center = true);
                    translate([-4.2, 0, 5]) cube([2.2, 6.5, 10], center = true);
                }
            }
        }
    }
}

// --- Solar Array ---
module solar_array(length = 135, width = 50, thickness = 3.2) {
    color("MidnightBlue") {
        cube([length, width, thickness], center = true);
        translate([0, 0, thickness/2 + 0.5]) color("Gray") cube([length+3, width+3, 1], center = true);
    }
}

// --- Service Module ---
module service_module() {
    color("DimGray") cube([30, 30, 46], center = true);
}

// --- Docking Port ---
module docking_port() {
    color("LightSteelBlue") {
        cylinder(h = 16, d = 32, center = true);
        translate([0, 0, 10]) cylinder(h = 8, d = 25, center = true);
    }
}

// ==================== Final Assembly ====================

color("SteelBlue") assembly_bay();
main_truss();
translate([0, 0, -assembly_length/2 - 90]) habitat_ring();

for (z = [-210 : 52 : 210]) {
    translate([ truss_size/2 + 23, 0, z]) service_module();
    translate([-truss_size/2 - 23, 0, z]) service_module();
}

translate([0, 180, 15]) rotate([0, 0, 90]) solar_array();
translate([0,-180, 15]) rotate([0, 0, 90]) solar_array();

translate([110, 0, 145]) rotate([0, 90, 0]) color("Silver") cube([100, 34, 2.8], center = true);
translate([-110, 0,-145]) rotate([0, 90, 0]) color("Silver") cube([100, 34, 2.8], center = true);

translate([ assembly_dia/2 - 15, 0, 55]) robotic_arm(0, 105);
translate([-assembly_dia/2 + 15, 0, -45]) robotic_arm(180, 98);
translate([0, assembly_dia/2 - 15, 90]) robotic_arm(90, 88);
translate([0, -assembly_dia/2 + 15, -70]) robotic_arm(-90, 90);

translate([0, 0, truss_length/2 - 14]) docking_port();
translate([0, 0, -truss_length/2 + 14]) docking_port();

// Exterior warning / navigation lights
color("Red") {
    translate([0, 0, truss_length/2 - 5]) sphere(d = 4);
    translate([0, 0, -truss_length/2 + 5]) sphere(d = 4);
}
color("LightYellow") {
    for (z = [-150, 0, 150]) {
        translate([truss_size/2 + 5, truss_size/2 + 5, z]) sphere(d = 3);
        translate([-truss_size/2 - 5, -truss_size/2 - 5, z]) sphere(d = 3);
    }
}
