// Focused: Assembly Bay + Main Truss only
$fn = 64;

assembly_dia = 180;
assembly_length = 240;
truss_size = 42;
truss_length = 420;

module assembly_bay() {
 difference() {
 cylinder(h = assembly_length, d = assembly_dia, center = true);
 cylinder(h = assembly_length + 2, d = assembly_dia - 9, center = true);
 }
}

color("SteelBlue")
assembly_bay();

color("Gainsboro")
cube([truss_size, truss_size, truss_length], center = true);
