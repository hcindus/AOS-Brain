// SEG-1 Segmented Orbital Station — rotating wheel, segmented habitat ring
// Spin axis = Z (vertical). Ring rotates in XY plane.
$fn = 48;

RING_R = 140;   // radius to segment centers
N_SEG  = 8;     // number of habitat segments
SEG_L  = 62;    // segment length (tangential)
SEG_W  = 26;    // segment width (radial)
SEG_H  = 22;    // segment height (vertical)

// ---- Rounded capsule (long axis along X) ----
module capsule(l, w, h, r) {
  hull() {
    for (dx = [-1, 1])
      for (dy = [-1, 1])
        translate([dx*(l/2 - r), dy*(w/2 - r), 0])
          cylinder(r = r, h = h, center = true);
  }
}

// ---- Single habitat segment (tangential) ----
module segment() {
  // main pressure body
  capsule(SEG_L, SEG_W, SEG_H, 9);
  // end docking plates (toward neighbouring segments)
  for (dx = [-1, 1])
    translate([dx*(SEG_L/2 + 2), 0, 0])
      cylinder(r = 10, h = SEG_H + 2, center = true);
  // top window strip
  translate([0, 0, SEG_H/2])
    cube([SEG_L - 14, 5, 2], center = true);
  // bottom radiator strip
  translate([0, 0, -SEG_H/2 - 1])
    cube([SEG_L - 10, 12, 2], center = true);
}

// ---- Central hub (spin axis) ----
module hub() {
  // main cylinder
  cylinder(r = 22, h = 74, center = true);
  // tapered end caps
  for (dz = [-1, 1])
    translate([0, 0, dz*(37 + 7)])
      cylinder(r1 = 22, r2 = 7, h = 14, center = true);
  // docking ports top/bottom
  for (dz = [-1, 1])
    translate([0, 0, dz*(37 + 14 + 4)])
      cylinder(r = 8, h = 8, center = true);
  // collar rings
  for (dz = [-1, 1])
    translate([0, 0, dz*20])
      cylinder(r = 24, h = 4, center = true);
}

// ---- Spokes (hub -> each segment) ----
module spokes() {
  for (i = [0 : N_SEG - 1]) {
    let(a = i * 360 / N_SEG) {
      rotate([0, 0, a]) {
        // two thin truss members per spoke, offset in Z
        for (dz = [-6, 6])
          translate([RING_R/2 + 10, 0, dz])
            cube([RING_R - 24, 2.5, 2.5], center = true);
        // cross-brace
        translate([RING_R/2 + 10, 0, 0])
          cube([2.5, 2.5, 14], center = true);
      }
    }
  }
}

// ---- Solar arrays (4 panels on outer trusses) ----
module solar_arrays() {
  for (i = [0 : 3]) {
    let(a = i * 90 + 22.5) {
      rotate([0, 0, a]) {
        // truss extending outward
        translate([RING_R + 40, 0, 0])
          cube([90, 3, 3], center = true);
        // panel (large flat plate, tilted to catch sun)
        translate([RING_R + 95, 0, 0])
          rotate([0, 25, 0])
            cube([70, 60, 1.2], center = true);
        // second panel
        translate([RING_R + 145, 0, 0])
          rotate([0, 25, 0])
            cube([70, 60, 1.2], center = true);
      }
    }
  }
}

// ---- Radiators (flat fins off the hub) ----
module radiators() {
  for (i = [0 : 3]) {
    let(a = i * 90 + 45) {
      rotate([0, 0, a]) {
        translate([RING_R - 40, 0, 0])
          cube([60, 34, 1.2], center = true);
      }
    }
  }
}

// ---- Antennas + nav lights ----
module antennas() {
  for (dz = [-1, 1]) {
    translate([0, 0, dz*(37 + 14 + 8 + 6)]) {
      cylinder(r = 1.2, h = 14, center = true);
      translate([0, 0, dz*9]) sphere(r = 2.2);
    }
  }
  // nav lights (red/cyan) on segment ends
  for (i = [0 : N_SEG - 1]) {
    let(a = i * 360 / N_SEG) {
      rotate([0, 0, a]) {
        translate([RING_R, SEG_W/2 + 3, SEG_H/2 + 2])
          sphere(r = 2.5);
      }
    }
  }
}

// ---- Assemble ----
module seg_station() {
  hub();
  spokes();
  // segments placed tangentially around ring
  for (i = [0 : N_SEG - 1]) {
    let(a = i * 360 / N_SEG) {
      rotate([0, 0, a])
        translate([RING_R, 0, 0])
          rotate([0, 0, 90])   // rotate long axis to tangent
            segment();
    }
  }
  solar_arrays();
  radiators();
  antennas();
}

seg_station();
