"""
    tls_light_mod_installer: Install light mod for Toliss A3xx family aircraft.
        The light mod of Gus Rodrigues can be downloaded from
        https://forums.x-plane.org/files/file/93337-a320-light-mod/ .

    Copyright (C) 2025  Holger Teutsch

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
    USA
"""

VERSION = "--TAG--"

import sys,os, os.path, shutil, logging

log = logging.getLogger("tls_light_mod_installer")

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler(filename="tls_light_mod_installer.log", mode="w"),
        logging.StreamHandler(),
    ],
)

log.info(f"Version: {VERSION}")
log.info(f"args: {sys.argv}")

def usage():
    log.error(
        """
        usage:
            tls_light_mod_installer
                -acf_dir     dir to acf, e.g. e:/X-Plane-12/Aircraft/ToLissA320Neo
                -mod_dir     dir of lighting mod, e.g. e:/XPL-Tools/a20n-light_mod
                -type        current|new|led

        Example:
            tls_light_mod_installer -acf_dir e:/X-Plane-12/Aircraft/ToLissA320Neo -mod_dir e:/XPL-Tools/a20n-light_mod -type led
        """
    )
    sys.exit(2)

acf_dir = None
light_mod_dir = None
light_type = None
acf_type = None

i = 1
while i < len(sys.argv):
    if sys.argv[i] == "-acf_dir":
        i = i + 1
        if i >= len(sys.argv):
            usage()

        acf_dir = sys.argv[i]
    elif sys.argv[i] == "-mod_dir":
        i = i + 1
        if i >= len(sys.argv):
            usage()

        light_mod_dir = sys.argv[i]
    elif sys.argv[i] == "-type":
        i = i + 1
        if i >= len(sys.argv):
            usage()

        light_type = sys.argv[i]
    else:
        usage()
    i = i + 1

if acf_dir is None or light_mod_dir is None or light_type is None:
    usage()

if light_type not in ["current", "new", "led"]:
    log.error(f"Unknown light type: {light_type}")
    usage()

if os.path.isfile(os.path.join(acf_dir, "a320.acf")):
    acf_type = "320"
elif os.path.isfile(os.path.join(acf_dir, "a321.acf")):
    acf_type = "321"
elif os.path.isfile(os.path.join(acf_dir, "a319.acf")):
    acf_type = "319"
else:
    log.error(f"Cannot determine acf type in dir: {acf_dir}")
    usage()

log.info(f"Detected acf type: A{acf_type}")

rgb_table = {
    "current": [1.0, 0.37, 0.16],
    "new": [0.8, 0.55, 0.3],
    "led": [0.82, 0.82, 1.0]
}

rgb = rgb_table[light_type]

metallness_files = [
    f"cab{acf_type}_0.obj",
    f"cab{acf_type}_1.obj",
    f"cab{acf_type}_2.obj",
    f"cab{acf_type}_3.obj",
    "cargo.obj",
    f"cargo{acf_type}.obj",
    "chairs.obj",
    "chars321.obj",
    "Copilot.obj",
    "DCDUs.obj",
    "engines.obj",
    "fuselage.obj",
    f"fuselage{acf_type}.obj",
    "fuselage321_1.obj",
    "fuselage321_2.obj",
    "fuselage321_3.obj",
    "gear.obj",
    "GlassInterior.obj",
    "Ipad.obj",
    "kitchens.obj",
    "knobs.obj",
    "neo.obj",
    "panels_main.obj",
    "panels_overhead.obj",
    "panels_pedestal.obj",
    "pedals_details.obj",
    "pedals_seats.obj",
    "pedals_tables.obj",
    "SatAnt.obj",
    "SunShades.obj",
    "walls_bottom.obj",
    "walls_outer.obj",
    "walls_top.obj",
    "wingL.obj",
    "wingR.obj"
    "wing321L.obj",
    "wing321R.obj"
]

translucency_files = [
    "knobs.obj",
    "SunShades.obj",
    "fuselage.obj",
    "fuselage321_1.obj",
    "fuselage321_2.obj",
    "fuselage321_3.obj",
    "GlassInterior.obj",
    "DCDUs.obj"
]

def patch_acf_file():
    """Patch the acf file to adjust light parameters."""
    log.info(f"Patching {acf_path}...")

    lines = open(acf_path_bck, 'r').readlines()

    with open(acf_path, 'w', newline='\n') as acf_file:
        for line in lines:
            if line.startswith("P acf/_spot1_3d_rgb/0"):
                line = f"P acf/_spot1_3d_rgb/0 {rgb[0]}\n"
            elif line.startswith("P acf/_spot1_3d_rgb/1"):
                line = f"P acf/_spot1_3d_rgb/1 {rgb[1]}\n"
            elif line.startswith("P acf/_spot1_3d_rgb/2"):
                line = f"P acf/_spot1_3d_rgb/2 {rgb[2]}\n"

            elif line.startswith("P acf/_spot2_3d_rgb/0"):
                line = f"P acf/_spot2_3d_rgb/0 {rgb[0]}\n"
            elif line.startswith("P acf/_spot2_3d_rgb/1"):
                line = f"P acf/_spot2_3d_rgb/1 {rgb[1]}\n"
            elif line.startswith("P acf/_spot2_3d_rgb/2"):
                line = f"P acf/_spot2_3d_rgb/2 {rgb[2]}\n"

            elif line.startswith("P acf/_spot3_3d_rgb/0"):
                line = f"P acf/_spot3_3d_rgb/0 {rgb[0]}\n"
            elif line.startswith("P acf/_spot3_3d_rgb/1"):
                line = f"P acf/_spot3_3d_rgb/1 {rgb[1]}\n"
            elif line.startswith("P acf/_spot3_3d_rgb/2"):
                line = f"P acf/_spot3_3d_rgb/2 {rgb[2]}\n"

            elif line.startswith("P acf/_spot1_3d_xyz/1"):
                line = f"P acf/_spot1_3d_xyz/1 4.0\n"

            elif line.startswith("P acf/_spot_angle/0"):
                line = f"P acf/_spot_angle/0 -60.0\n"
            elif line.startswith("P acf/_spot_psi/0"):
                line = f"P acf/_spot_psi/0 180.0\n"
            elif line.startswith("P acf/_spot_the/0"):
                line = f"P acf/_spot_the/0 -60.0\n"

            elif line.startswith("P acf/_spot_size/0"):
                line = f"P acf/_spot_size/0 8.0\n"
            elif line.startswith("P acf/_spot_size/1"):
                line = f"P acf/_spot_size/1 9.0\n"
            elif line.startswith("P acf/_spot_size/2"):
                line = f"P acf/_spot_size/2 10.0\n"

            acf_file.write(line)


def add_attributes_to_obj(obj_name, add_translucency=False):
    """Add attributes to the given .obj file."""
    obj_path = os.path.join(acf_dir, "objects", obj_name)
    if not os.path.isfile(obj_path):
        return

    obj_path_bck = os.path.join(bck_dir, "objects", obj_name)

    if not os.path.isfile(obj_path_bck):
        log.info(f"Backing up {obj_path} to {obj_path_bck}...")
        shutil.copy2(obj_path, obj_path_bck)

    log.info(f"Adding attributes to {obj_name}...")
    lines = open(obj_path_bck, 'r').readlines()

    have_metalness = False
    have_specular = False
    have_shiny_rat = False
    have_blend_glass = False

    for line in lines:
        if line.startswith("POINT_COUNT"):
            break
        if line.startswith("NORMAL_METALNESS"):
            have_metalness = True
        elif line.startswith("GLOBAL_specular"):
            have_specular = True
        elif line.startswith("ATTR_shiny_rat"):
            have_shiny_rat = True
        elif line.startswith("BLEND_GLASS"):
            have_blend_glass = True

    in_header = True
    with open(obj_path, 'w') as obj_file:
        for line in lines:
            if in_header and line.startswith("POINT_COUNT"):
                in_header = False
                if not have_metalness:
                    log.info(f"  Adding NORMAL_METALNESS to {obj_name}...")
                    obj_file.write("NORMAL_METALNESS\n")
                if not have_specular:
                    log.info(f"  Adding GLOBAL_specular to {obj_name}...")
                    obj_file.write("GLOBAL_specular	1.0\n")
                if add_translucency and not have_blend_glass:
                    log.info(f"  Adding BLEND_GLASS to {obj_name}...")
                    obj_file.write("BLEND_GLASS\n")
                if not have_shiny_rat:
                    log.info(f"  Adding ATTR_shiny_rat to {obj_name}...")
                    obj_file.write("ATTR_shiny_rat 1.0\n")

            obj_file.write(line)

################################################################################
bck_dir = os.path.join(acf_dir, "tls_light_mod_installer-bck")
os.makedirs(os.path.join(bck_dir, "objects"), exist_ok=True)

acf_fn = f"a{acf_type}.acf"
acf_path = os.path.join(acf_dir, acf_fn)
acf_path_bck = os.path.join(bck_dir, acf_fn)
if not os.path.isfile(acf_path_bck):
    log.info(f"Backing up {acf_path} to {acf_path_bck}...")
    shutil.copy2(acf_path, acf_path_bck)


patch_acf_file()

mod_obj_dir = os.path.join(light_mod_dir, "objects")
for _, _, files in os.walk(mod_obj_dir):
    for f in files + ["lights_inn.obj"]:
        obj_path = os.path.join(acf_dir, "objects", f)
        obj_path_bck = os.path.join(bck_dir, "objects", f)
        if os.path.isfile(obj_path) and not os.path.isfile(obj_path_bck):
            log.info(f"Backing up {obj_path} to {obj_path_bck}...")
            shutil.copy2(obj_path, obj_path_bck)

for _, _, files in os.walk(mod_obj_dir):
    for f in files:
        if f.startswith("lights_inn"):
            continue

        obj_path = os.path.join(acf_dir, "objects", f)
        mod_obj_path = os.path.join(mod_obj_dir, f)
        log.info(f"Installing {mod_obj_path} to {obj_path}...")
        shutil.copy2(mod_obj_path, obj_path)

mod_obj_path = os.path.join(mod_obj_dir, f"lights_inn_{light_type}.obj")
obj_path = os.path.join(acf_dir, "objects", "lights_inn.obj")

log.info(f"Installing {mod_obj_path} to {obj_path}...")
shutil.copy2(mod_obj_path, obj_path)

for file in metallness_files:
    add_attributes_to_obj(file, file in translucency_files)
