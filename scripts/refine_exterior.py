"""Refine an existing main model, preserving other scene objects and the source file.
blender -b output/model/f16c_block52_main_v02.blend --python scripts/refine_exterior.py -- --render
Photographic modeling estimates, NOT measured Block 52 engineering coordinates.
"""
import bpy, bmesh, math, json, hashlib, sys
from pathlib import Path
from mathutils import Vector
ROOT = Path(__file__).resolve().parents[1]
OUT, PRE = ROOT/'output/model', ROOT/'output/previews'
source = Path(bpy.data.filepath)
assert source.is_file(), 'Open an existing blend first'
version = 3
while (OUT/f'f16c_block52_main_v{version:02}.blend').exists(): version += 1
dest = OUT/f'f16c_block52_main_v{version:02}.blend'
source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
changed = []
# Preserve object identity, transforms, materials, parenting and custom properties.
def replace(name, verts, faces, collection='00_AIRFRAME', material='Paint_upper_slate_matte'):
    ob=bpy.data.objects.get(name)
    if ob is None:
        ob=bpy.data.objects.new(name,bpy.data.meshes.new(name));bpy.data.collections[collection].objects.link(ob)
        ob.data.materials.append(bpy.data.materials[material])
    assert ob.type=='MESH', name
    mats=list(ob.data.materials)
    me=bpy.data.meshes.new(name+'_refined')
    inv=ob.matrix_world.inverted()
    me.from_pydata([inv@Vector(v) for v in verts],[],faces)
    for m in mats:me.materials.append(m)
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(me);bm.free();me.update()
    ob.data=me;ob['geometry_basis']='Visual fit to SCANG photographs; coordinates estimated, not surveyed'
    changed.append(name)
    return ob

def loft(name, stations,n=20,cap=True):
    vs=[(rx*math.cos(2*math.pi*i/n),y,z+rz*math.sin(2*math.pi*i/n)) for y,rx,z,rz in stations for i in range(n)]
    fs=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(stations)-1) for i in range(n)]
    if cap:fs += [tuple(reversed(range(n))),tuple((len(stations)-1)*n+i for i in range(n))]
    return replace(name,vs,fs)

def foil(name, points, thickness, vertical=False):
    vs=[];n=len(points)
    for sign in [-1,1]:
        for x,y,z in points:
            t=thickness*(.4 if abs(x)>3 else 1)/2
            vs.append((x+sign*t,y,z) if vertical else (x,y,z+sign*t))
    fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    ob=replace(name,vs,fs)
    if not vertical and len(ob.data.materials)>1:ob.data.polygons[0].material_index=1
    return ob

def curve(name, points):
    ob=bpy.data.objects[name];cu=ob.data.copy();ob.data=cu
    cu.splines.clear();sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
    inv=ob.matrix_world.inverted()
    for p,v in zip(sp.points,points):p.co=(*(inv@Vector(v)),1)
    changed.append(name)

# A shared longitudinal grid eliminates the old unmatched shoulder seams.
# y, canopy half-width, canopy sill z, bubble height, body rx, body center z, body rz
can=[(-4.35,0,2.65,0,.64,2.15,.50),(-4.10,.36,2.635,.37,.675,2.14,.51),
     (-3.60,.51,2.62,.65,.705,2.12,.53),(-2.95,.55,2.60,.73,.75,2.09,.54),
     (-2.30,.50,2.585,.59,.79,2.06,.54),(-1.73,.34,2.57,.30,.84,2.035,.545),
     (-1.20,0,2.57,0,.90,2.02,.55)]
stations=[(-4.7,.54,2.15,.46)]+[(y,rx,zc,rz) for y,w,z,h,rx,zc,rz in can]+[(-.7,.98,2.005,.56),(.5,1.10,1.99,.60),(2.,1.04,1.97,.65),(3.6,.93,1.96,.65),(5.2,.80,1.97,.61),(6.35,.70,1.98,.56),(6.8,.66,1.99,.52)]
n=20
vs=[(rx*math.cos(2*math.pi*i/n),y,z+rz*math.sin(2*math.pi*i/n)) for y,rx,z,rz in stations for i in range(n)]
# Termination rings meet the shoulder in two straight slopes, with no sliver holes.
for j in [1,7]:
    y,rx,zc,rz=stations[j];tip=next(c[2] for c in can if c[0]==y)
    edge_x=rx*math.cos(math.pi/5);edge_z=zc+rz*math.sin(math.pi/5)
    for i in range(2,9):
        x=vs[j*n+i][0];vs[j*n+i]=(x,y,tip+(edge_z-tip)*abs(x)/edge_x)
fs=[]
for j in range(len(stations)-1):
    for i in range(n):
        if 1<=j<7 and 2<=i<=7:continue
        fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
fs += [tuple(reversed(range(n))),tuple((len(stations)-1)*n+i for i in range(n))]
body=replace('Fuselage_main_open_cockpit',vs,fs)
for p in body.data.polygons:
    if (body.matrix_world@p.center).z<2:p.material_index=1
# Nose has a fuller ogive and matches the forward body station exactly.
loft('Radome',[(-6.95,.018,2.05,.022),(-6.68,.12,2.07,.12),(-6.25,.26,2.10,.245),(-5.70,.405,2.125,.36),(-5.15,.50,2.145,.435),(-4.7,.54,2.15,.46)])
for sign,label in [(1,'L'),(-1,'R')]:
    vs=[]
    for y,w,z,h,rx,zc,rz in can:
        vs.extend([(sign*w,y,z),(sign*rx*math.cos(math.pi/5),y,zc+rz*math.sin(math.pi/5))])
    replace('Cockpit_shoulder_'+label,vs,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(can)-1)])
    curve('Canopy_sill_'+label,[(sign*w,y,z+.006) for y,w,z,h,rx,zc,rz in can])
    # The old tub wall protruded through the narrowed front/aft shoulder caps.
    wall=[(sign*w,y,zz) for y,w,z,h,rx,zc,rz in can for zz in (z-.008,2.18)]
    replace('Cockpit_inner_wall_'+label,wall,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(can)-1)])
# Bubble: triangular end fans avoid collapsed zero-area quads.
vs=[(0,can[0][0],can[0][2])];rings=[];steps=12
for y,w,z,h,*_ in can[1:-1]:
    rings.append(list(range(len(vs),len(vs)+steps+1)))
    vs.extend((w*math.cos(math.pi*i/steps),y,z+h*math.sin(math.pi*i/steps)) for i in range(steps+1))
end=len(vs);vs.append((0,can[-1][0],can[-1][2]));fs=[]
for i in range(steps):fs.append((0,rings[0][i+1],rings[0][i]))
for a,b in zip(rings,rings[1:]):
    for i in range(steps):fs.append((a[i],a[i+1],b[i+1],b[i]))
for i in range(steps):fs.append((rings[-1][i],rings[-1][i+1],end))
replace('Canopy_glass',vs,fs)
y,w,z,h,*_=can[-2]
curve('Canopy_aft_bow',[(w*math.cos(math.pi*i/12),y,z+h*math.sin(math.pi*i/12)) for i in range(13)])
# LEX with several transverse sections: raised root blends into the fuselage.
for s,label in [(1,'L'),(-1,'R')]:
    section=[(-4.35,.43,.63,2.31,2.19),(-2.9,.51,.96,2.30,2.15),(-1.2,.65,1.30,2.27,2.115),(-.38,.72,1.49,2.24,2.10),(1.65,.73,1.56,2.24,2.055),(2.92,.70,1.40,2.22,2.05)]
    vs=[]
    for y,inner,outer,zin,zout in section:
        vs.extend([(s*inner,y,zin),(s*outer,y,zout),(s*outer,y,zout-.05),(s*inner,y,zin-.10)])
    fs=[]
    for j in range(len(section)-1):
        for k in range(4):fs.append((j*4+k,j*4+(k+1)%4,(j+1)*4+(k+1)%4,(j+1)*4+k))
    fs += [(3,2,1,0),tuple((len(section)-1)*4+i for i in range(4))]
    replace('LEX_'+label,vs,fs)
    # Keep span, flatten trailing-edge planform; surfaces meet with a narrow seam.
    foil('Wing_'+label,[(s*1.08,-.45,2.08),(s*4.86,2.55,2.),(s*4.86,3.12,2.),(s*1.09,2.91,2.08)],.11)
    foil('Flaperon_'+label,[(s*1.12,2.935,2.075),(s*4.80,3.142,2.),(s*4.80,3.60,2.),(s*1.12,3.60,2.075)],.07)
    foil('Stabilator_'+label,[(s*.78,4.48,1.86),(s*2.80,6.10,1.75),(s*2.93,7.10,1.73),(s*.81,7.05,1.85)],.09)
# Intake uses one common outer ring for lip and fairing: no front rim mismatch.
n=32
ring=[]
for i in range(n):
    t=2*math.pi*i/n
    x=.69*math.cos(t);s=math.sin(t)
    z=1.50+(.25*(s**.6) if s>=0 else .44*s)
    ring.append((x,z))
vs=[]
for y,scale,cz in [(-3.65,1.,1.50),(-3.60,.91,1.50),(-3.24,.89,1.50),(-2.45,.80,1.56)]:
    vs.extend((x*scale,y,cz+(z-1.50)*scale) for x,z in ring)
fs=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(3) for i in range(n)]
ob=replace('NSI_intake_lip_and_tunnel',vs,fs)
for p in ob.data.polygons:p.material_index=0 if p.index<n else 1
replace('Intake_dark_depth',vs[-n:],[tuple(range(n))])
vs=[]
for y,scale,cz in [(-3.65,1,1.50),(-3.22,1.04,1.51),(-2.30,1.11,1.54),(-1.2,1.17,1.61),(.3,1.25,1.76),(1.5,1.25,1.90),(2.1,1.18,1.98)]:
    vs.extend((x*scale,y,cz+(z-1.50)*scale) for x,z in ring)
fs=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(6) for i in range(n)]
replace('Intake_lower_fairing',vs,fs)
# Rounded lip at the shared join; splitter follows upper contour above the opening.
foil('Intake_splitter',[(-.63,-3.70,1.83),(.63,-3.70,1.83),(.66,-3.08,1.87),(-.66,-3.08,1.87)],.045)
# Swept tail trailing edge: old nearly-vertical outline was visibly incorrect.
foil('Vertical_tail_fixed',[(0,2.1,2.52),(0,3.75,2.89),(0,5.87,4.8768),(0,6.65,4.8768),(0,5.64,2.61)],.15,True)
foil('Rudder',[(0,6.685,4.8768),(0,7.12,4.8768),(0,6.17,2.64),(0,5.675,2.64)],.08,True)
# Tail tip shape retains height/envelope while following the new leading edge.
ob=bpy.data.objects['Tail_tip_EW_fairing'];ob.location.y-=.18;changed.append(ob.name)
# Attach markings to the revised fixed tail interior without touching their design.
for name in ['Tail_flag_L','Tail_flag_R','Flag_crescent_L','Flag_crescent_R','Flag_star_L','Flag_star_R','Fictional_tail_ID_-1','Fictional_tail_ID_1']:
    ob=bpy.data.objects[name];ob.location.y-=.40;changed.append(name)
sc=bpy.context.scene
sc['stage']='Exterior proportions and seam refinement; cockpit and mechanisms pending'
sc['exterior_revision']=dest.stem
sc['exterior_source']=source.name
sc['exterior_reference_status']='SCANG 4548370, 4548358, 7403357 visual comparison; NASA general silhouette only. Dimensions remain provisional.'
bpy.data.texts['READ_ME_FIRST'].write('\n\nEXTERIOR REFINEMENT: '+dest.stem+'\nExisting file edited selectively. Source retained. Canopy/body, intake, LEX/wing and tail silhouette revised from visual references. Cockpit controls and mechanism validation remain pending.\n')
# Extra close-up camera isolates the three edited forward joins.
d=bpy.data.cameras.new('CAM_Forward_join');c=bpy.data.objects.new('CAM_Forward_join',d);bpy.data.collections['90_PREVIEW_STUDIO'].objects.link(c)
c.location=(6,-9,4.8);c.rotation_euler=(Vector((0,-2.8,2.05))-c.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=7.3
sc.camera=bpy.data.objects['CAM_Exterior']
bpy.context.view_layer.update()
report={'source':str(source),'source_sha256':source_hash,'output':str(dest),'changed_objects':changed,'basis':'Photographic modeling estimates; not measured technical data','untouched_scope':'Cockpit furnishings/controls (inner shell walls revised), landing gear, nozzles, pylons, materials'}
(OUT/f'exterior_revision_v{version:02}.json').write_text(json.dumps(report,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(dest))
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
print('REFINED',dest,flush=True)
if '--render' in sys.argv:
    sc.cycles.samples=16;sc.render.resolution_x=1260;sc.render.resolution_y=900
    for key,cam in [('exterior','CAM_Exterior'),('side','CAM_Side'),('top','CAM_Top'),('front','CAM_Front'),('forward_join','CAM_Forward_join'),('cockpit','CAM_Pilot_APPROX')]:
        sc.camera=bpy.data.objects[cam];sc.render.filepath=str(PRE/f'f16_v{version:02}_{key}.png');bpy.ops.render.render(write_still=True)
