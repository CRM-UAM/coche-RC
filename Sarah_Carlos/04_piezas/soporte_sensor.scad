$fn = 10;
MAX_CILINDROS = 45;

mirror()
union() {
    //relleno union
    translate([-9.5, -5.6, 5.9]) rotate([90, 0, 90]) linear_extrude(height = 40) square([3.4, 1.6]);


    difference() {
        //base
        translate([0, 3, 0]) cube([61, 12, 15], center = true);

        //sensor width
        translate([0, 4, 2]) cube([58, 6, 15], center = true);
        //translate([11, 1, 4]) rotate([-90, 0, 0]) cylinder(5, d = 18, true);
        //hueco micro/receptor
        translate([0, 7, 3]) cube([MAX_CILINDROS, 16, 15], center = true);
        
        translate([25, 2, 3]) rotate([-90, 0, 0]) cylinder(h = 15, d = 2, center = true);
        
        mirror([1, 0, 0]) translate([25, 2, 3]) rotate([-90, 0, 0]) cylinder(h = 15, d = 2, center = true);

        //    translate([-11.5, 1.9, 7.7]) rotate([42, 0, 0]) translate([0, -4, 1.5]) rotate([180, -90, 0]) linear_extrude(height = 40, scale = [1, 0.444]) square([1.3, 45]);
        //    translate([-41.5, 1.9, 7.7]) rotate([42, 0, 0]) translate([0, -4, 1.5]) rotate([180, -90, 0]) linear_extrude(height = 40, scale = [1, 0.444]) square([1.3, 45]);
    }

    translate([0, 0, 3.4]) difference() {
        //exterior enganche
        translate([-9.5, 3.7, -0.4]) rotate([42, 0, 0]) translate([0, -4, 1.5]) rotate([180, -90, 0]) linear_extrude(height = 40, scale = [1, 0.446]) square([8, 46]);
        
        //hueco enganche
        translate([-11.5, 2.9, 1.7]) rotate([42, 0, 0]) translate([0, -4, 1.5]) rotate([180, -90, 0]) linear_extrude(height = 40, scale = [1, 0.446]) square([4, 46]);

        //hueco micro/receptor
        translate([0, 7, 3]) cube([MAX_CILINDROS, 16, 15], center = true);
    }
}