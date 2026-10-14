"""v06 blend dosyasını oyun için .glb olarak dışa aktarır.

Kullanım:
    blender -b output/model/f16c_block52_main_v06.blend \
        --python scripts/export_gltf.py -- web/public/models/f16_v06.glb

- 90_PREVIEW_STUDIO, kameralar ve ışıklar dışarıda bırakılır.
- FONT nesneleri geçici olarak mesh'e dönüştürülür (dosya kaydedilmez).
- Pilot göz noktası ve iniş takımı pivot bilgileri ayrı JSON'a yazılır.
"""

import bpy
import json
import mathutils
import sys

argv = sys.argv[sys.argv.index("--") + 1:]
out_glb = argv[0]
out_meta = argv[1] if len(argv) > 1 else out_glb.rsplit(".", 1)[0] + "_meta.json"

EXCLUDED_COLLECTIONS = {"90_PREVIEW_STUDIO"}


def excluded(o):
    for c in o.users_collection:
        if c.name in EXCLUDED_COLLECTIONS:
            return True
    return False


def to_gltf(v):
    # Blender (x, y, z) -> glTF (x, z, -y); burun -Y -> +Z
    return [round(v.x, 4), round(v.z, 4), round(-v.y, 4)]


def world_bbox(o):
    if o.type != "MESH":
        return None
    deps = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(deps)
    corners = [o.matrix_world @ mathutils.Vector(c) for c in ev.bound_box]
    lo = [min(c[i] for c in corners) for i in range(3)]
    hi = [max(c[i] for c in corners) for i in range(3)]
    return lo, hi


bpy.context.view_layer.objects.active = None

# Studio, kamera ve ışık nesnelerini kaldır (kaydetmiyoruz, kalıcı değil)
kill = [o for o in bpy.data.objects if o.type in {"CAMERA", "LIGHT"} or excluded(o)]
with bpy.context.temp_override(selected_objects=kill, active_object=None):
    bpy.ops.object.delete()

# FONT nesnelerini mesh'e çevir (etiketler glTF'e girsin)
fonts = [o for o in bpy.data.objects if o.type == "FONT"]
with bpy.context.temp_override(selected_objects=fonts, active_object=fonts[0] if fonts else None):
    bpy.ops.object.convert(target="MESH")

meta = {
    "source": "f16c_block52_main_v06.blend",
    "convention": "glTF: +Z ileri (burun), +Y yukarı, +X sağ. 1 birim = 1 m.",
    "pilot_eye": None,
    "gear": {},
}

eye = bpy.data.objects.get("Pilot_eye_APPROX")
if eye:
    meta["pilot_eye"] = to_gltf(eye.matrix_world.translation)

for name in [
    "Nose_gear_strut", "Nose_tire", "Nose_hub", "Nose_gear_door",
    "Main_gear_strut_L", "Main_tire_L", "Main_hub_L", "Main_gear_door_L", "Main_gear_brace_L",
    "Main_gear_strut_R", "Main_tire_R", "Main_hub_R", "Main_gear_door_R", "Main_gear_brace_R",
]:
    o = bpy.data.objects.get(name)
    if not o:
        continue
    bb = world_bbox(o)
    entry = {"origin": to_gltf(o.matrix_world.translation)}
    if bb:
        lo, hi = bb
        entry["bbox_min"] = to_gltf(mathutils.Vector(lo))
        entry["bbox_max"] = to_gltf(mathutils.Vector(hi))
        # Pivot: strut üst bağlantısı (Y'de en yüksek uç, glTF uzayında)
        top = mathutils.Vector((o.matrix_world.translation.x, o.matrix_world.translation.y, hi[2]))
        entry["pivot_gltf"] = to_gltf(top)
    meta["gear"][name] = entry

bpy.ops.export_scene.gltf(
    filepath=out_glb,
    export_format="GLB",
    export_yup=True,
)

with open(out_meta, "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2)

tri = 0
for o in bpy.data.objects:
    if o.type == "MESH":
        tri += sum(p.loop_total for p in o.data.polygons)
print(f"EXPORT_OK glb={out_glb} meta={out_meta} tri={tri} fonts_converted={len(fonts)}")
