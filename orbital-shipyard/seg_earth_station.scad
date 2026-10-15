// ============================================================
// SEG-EARTH — Segmented Modular Orbital Station (Earth orbit)
// Same detail language as OSY-7: internal decks + habitat rooms,
// solar arrays, radiators, docking ports, robotic arms, nav lights.
// Units: meters. Long axis = Z.
// ============================================================

$fn = 48;

// --- Parameters ---
hull_dia      = 150;   // main cylinder diameter
hull_len      = 480;   // total length
wall          = 6;     // hull wall thickness
inner_dia     = hull_dia - wall*2;   // 138
deck_thick    = 2.5;
N_SEG         = 8;     // number of hull segments
seg_gap       = 6;     // visible gap between segments

// --- Hollow segmented hull (ring divisions visible) ---
module hull() {
    color("LightSteelBlue") {
        seg_len = (hull_len - (N_SEG-1)*seg_gap) / N_SEG;
        for (i = [0 : N_SEG-1]) {
            z = -hull_len/2 + seg_len/2 + i*(seg_len + seg_gap);
            translate([0,0,z]) difference() {
                cylinder(h = seg_len, d = hull_dia, center = true);
                cylinder(h = seg_len + 2, d = hull_dia - wall*2, center = true);
            }
        }
        // end caps (tapered)
        for (dz = [-1,1]) translate([0,0,dz*(hull_len/2 + 18)])
            cylinder(h = 36, d1 = hull_dia, d2 = hull_dia*0.55, center = true);
    }
}

// --- Internal decks with grating + handrails + central shaft ---
module decks() {
    for (z = [-150, -50, 50, 150]) {
        translate([0,0,z]) {
            // solid deck (annulus)
            difference() {
                cylinder(h = deck_thick, d = inner_dia - 1, center = true);
                cylinder(h = deck_thick + 2, d = 40, center = true); // central shaft
            }
            // floor grating
            color("Gray")
            for (r = [26 : 9 : inner_dia/2 - 8])
                for (a = [0 : 14 : 359])
                    rotate([0,0,a]) translate([r,0,deck_thick/2+0.2]) cube([1,5,0.4], center=true);
            // handrail around central shaft
            color("Silver") difference() {
                cylinder(h = 4.5, d = 46, center = false);
                cylinder(h = 5.5, d = 43, center = false);
            }
        }
    }
    // central access shaft (walkable vertical corridor)
    color("DimGray") difference() {
        cylinder(h = hull_len - 4, d = 40, center = true);
        cylinder(h = hull_len - 2, d = 34, center = true);
    }
}

// --- Habitat / modular rooms around the central shaft (per deck) ---
module habitat_rooms() {
    for (z = [-150, -50, 50, 150]) {
        for (a = [0 : 90 : 270]) {
            rotate([0,0,a]) translate([inner_dia/2 - 12, 0, z]) {
                // room box
                color("OliveDrab") cube([16, 20, 22], center = true);
                // window strip (outward)
                color("LightSkyBlue") translate([8.6, 0, 0]) cube([1, 14, 7], center = true);
                // door toward shaft
                color("SaddleBrown") translate([-8, 0, 0]) cube([2, 10, 18], center = true);
            }
        }
    }
}

// --- Solar array wing ---
module solar_wing(rot = 0) {
    color("MidnightBlue") rotate([0,0,rot]) {
        translate([hull_dia/2 + 30, 0, 0]) cube([70, 46, 3], center = true);
        translate([hull_dia/2 + 15, 0, 0]) cube([8, 4, 4], center = true); // mast
        translate([hull_dia/2 + 65, 0, 0]) cube([70, 46, 3], center = true);
    }
}

// --- Radiator fin ---
module radiator(rot = 0) {
    color("Silver") rotate([0,0,rot]) {
        translate([hull_dia/2 + 40, 0, 0]) cube([54, 28, 1.5], center = true);
    }
}

// --- Docking port (end) ---
module docking_port(dz = 1) {
    color("LightSteelBlue") translate([0,0,dz*(hull_len/2 + 38)]) {
        cylinder(h = 18, d = 30, center = true);
        cylinder(h = 10, d = 22, center = true);
    }
}

// --- Robotic arm (reused from OSY-7) ---
module robotic_arm(base_rot = 0, arm_len = 90) {
    color("DarkOrange") rotate([0,0,base_rot]) {
        cylinder(h = 14, d = 13, center = true);
        translate([0,0,10]) rotate([0,28,0]) {
            cylinder(h = 9, d = 10, center = true);
            translate([0,0,arm_len*0.38]) cube([8,8,arm_len*0.55], center = true);
            translate([0,0,arm_len*0.55]) rotate([0,-48,0]) {
                cylinder(h = 8, d = 8, center = true);
                translate([0,0,arm_len*0.28]) cube([6,6,arm_len*0.38], center = true);
                translate([0,0,arm_len*0.38]) cylinder(h = 6, d = 6, center = true);
            }
        }
    }
}

// --- Nav / warning lights ---
module nav_lights() {
    color("Red") {
        translate([0,0, hull_len/2 + 4]) sphere(d = 4);
        translate([0,0,-hull_len/2 - 4]) sphere(d = 4);
    }
    color("LightYellow") {
        for (z = [-160, 0, 160])
            for (a = [0:90:270])
                rotate([0,0,a]) translate([hull_dia/2 + 3, 0, z]) sphere(d = 3);
    }
}

// ==================== Assembly ====================
hull();
decks();
habitat_rooms();

for (a = [0:90:270]) solar_wing(a);
for (a = [45:90:315]) radiator(a);

docking_port(1);
docking_port(-1);

translate([hull_dia/2 + 2, 0, 120]) robotic_arm(0, 90);
translate([-hull_dia/2 - 2, 0, -120]) robotic_arm(180, 90);

nav_lights();
