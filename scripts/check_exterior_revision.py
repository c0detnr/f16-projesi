"""Verify edited seams and preservation against the recorded source blend."""
import bpy, json, hashlib
from pathlib import Path
from mathutils import Vector
path=Path(bpy.data.filepath)
version=path.stem.rsplit('_v',1)[1]
revision=json.loads((path.parent/f'exterior_revision_v{version}.json').read_text())
changed=set(revision['changed_objects'])
bpy.context.view_layer.update()
def snapshot(ob):
    d={'type':ob.type,'location':list(ob.location),'rotation':list(ob.rotation_euler),'scale':list(ob.scale),'parent':ob.parent.name if ob.parent else None,'collections':sorted(c.name for c in ob.users_collection),'hide_render':ob.hide_render,'modifiers':[(m.name,m.type) for m in ob.modifiers]}
    if ob.type=='MESH':
        d.update(vertices=[list(v.co) for v in ob.data.vertices],faces=[list(p.vertices) for p in ob.data.polygons],materials=[m.name if m else None for m in ob.data.materials],material_indices=[p.material_index for p in ob.data.polygons])
    elif ob.type in ('CURVE','FONT'):
        d['materials']=[m.name if m else None for m in ob.data.materials]
        if ob.type=='FONT':d.update(text=ob.data.body,size=ob.data.size)
        else:d['splines']=[{'points':[list(p.co) for p in s.points],'bevel':ob.data.bevel_depth} for s in ob.data.splines]
    return hashlib.sha256(json.dumps(d,sort_keys=True).encode()).hexdigest()
current={o.name:snapshot(o) for o in bpy.data.objects}
def points(name):
    ob=bpy.data.objects[name];return [ob.matrix_world@v.co for v in ob.data.vertices]
def nearest_max(a,b):return max(min((p-q).length for q in b) for p in a)
body=points('Fuselage_main_open_cockpit');glass=points('Canopy_glass')
seams={}
for side in ['L','R']:
    shoulder=points('Cockpit_shoulder_'+side)
    seams['shoulder_body_'+side]=nearest_max(shoulder[1::2],body)
    seams['shoulder_glass_'+side]=nearest_max(shoulder[::2],glass)
seams['intake_lip_fairing']=nearest_max(points('NSI_intake_lip_and_tunnel')[:32],points('Intake_lower_fairing')[:32])
seams['radome_body']=nearest_max(points('Radome')[-20:],body[:20])
# Compare bilateral exterior geometry using world-space mirrored coordinates.
symmetry={}
for stem in ['Wing','LEX','Flaperon','Stabilator','Cockpit_shoulder']:
    symmetry[stem]=nearest_max([Vector((-p.x,p.y,p.z)) for p in points(stem+'_L')],points(stem+'_R'))
errors=[f'seam {n}: {d}' for n,d in seams.items() if d>1e-5]
errors += [f'asymmetry {n}: {d}' for n,d in symmetry.items() if d>1e-5]
source=Path(revision['source'])
if hashlib.sha256(source.read_bytes()).hexdigest()!=revision['source_sha256']:errors.append('Source hash changed')
bpy.ops.wm.open_mainfile(filepath=str(source))
original={o.name:snapshot(o) for o in bpy.data.objects}
unexpected=[name for name,h in original.items() if name not in changed and current.get(name)!=h]
missing=sorted(set(original)-set(current))
errors += ['unexpected modification '+n for n in unexpected]+['missing '+n for n in missing]
report={'file':str(path),'source':str(source),'source_hash_preserved':hashlib.sha256(source.read_bytes()).hexdigest()==revision['source_sha256'],'unchanged_objects_verified':len(set(original)-changed),'expected_changed_objects':len(changed),'missing_objects':missing,'unexpected_changes':unexpected,'seam_max_distance_m':seams,'bilateral_max_distance_m':symmetry,'errors':errors,'limits':'Shared seam and object-preservation checks only, not comprehensive intersections or engineering accuracy.'}
path.with_suffix('.exterior_checks.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
assert not errors,errors
