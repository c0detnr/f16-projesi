"""Reopen validation. Run with the delivered .blend, not on an empty scene."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
sc=bpy.context.scene
bpy.context.view_layer.update()
asset=[o for o in sc.objects if any(c.name[:2] in ('00','01','02','03','04','05','06','08') for c in o.users_collection)]
deps=bpy.context.evaluated_depsgraph_get()
triangles=0;vertices=0;errors=[];coords=[]
for o in asset:
    if o.type not in ('MESH','CURVE','FONT'):continue
    ev=o.evaluated_get(deps);me=ev.to_mesh()
    me.calc_loop_triangles();triangles+=len(me.loop_triangles);vertices+=len(me.vertices)
    for v in me.vertices:
        co=o.matrix_world@v.co
        if not all(math.isfinite(k) for k in co):errors.append('non-finite '+o.name)
        coords.append(co)
    for p in me.polygons:
        if p.area<1e-12:errors.append('zero-area '+o.name)
    ev.to_mesh_clear()
mn=[min(v[i] for v in coords) for i in range(3)];mx=[max(v[i] for v in coords) for i in range(3)]
required=['Fuselage_main_open_cockpit','Radome','Canopy_glass','Wing_L','Wing_R','NSI_intake_lip_and_tunnel','Stabilator_L','Stabilator_R','Side_stick_grip','Throttle_grip','MFD_L_screen','MFD_R_screen','Nose_tire','Main_tire_L','Main_tire_R']
errors += ['missing '+n for n in required if n not in bpy.data.objects]
errors += ['missing external '+i.filepath for i in bpy.data.images if i.source=='FILE' and not i.packed_file and i.filepath and not Path(bpy.path.abspath(i.filepath)).exists()]
if sc.unit_settings.scale_length!=1 or sc.unit_settings.system!='METRIC':errors.append('wrong scale')
size=[mx[i]-mn[i] for i in range(3)]
for actual,expected in zip(size,[9.9568,15.0622,4.8768]):
    if abs(actual-expected)>.02:errors.append('scale bbox mismatch')
report={'file':bpy.data.filepath,'opened_successfully':True,'asset_objects':len(asset),'evaluated_vertices':vertices,'evaluated_triangles':triangles,'bbox_size_m':size,'external_texture_files':[i.filepath for i in bpy.data.images if i.source=='FILE'],'errors':errors,'checks':['required main parts','finite geometry','nonzero polygon area','metric scale','provisional model envelope','external dependencies'],'limits':['No exact reference fit or collision/mechanism validation','No Iris Xe game benchmark']}
out=Path(bpy.data.filepath).with_suffix('.validation.json');out.write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if errors:raise RuntimeError('Model checks failed')
