"""F-16C Block 52 ana model v01. Blender 5.2; 1 unit = 1 m.
Run: blender --background --python scripts/build_f16.py -- --render
Creates a NEW versioned file; never overwrites an existing .blend.
Geometry coordinates inferred from local reference silhouettes, NOT engineering data.
Axes: +X left wing, +Y aft, +Z up. Ground z=0, nose toward -Y.
"""
import bpy, math, json, sys
from pathlib import Path
from mathutils import Vector, Quaternion
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/model'
PRE = ROOT / 'output/previews'
OUT.mkdir(parents=True, exist_ok=True); PRE.mkdir(parents=True, exist_ok=True)
VERSION = 1
while (OUT / f'f16c_block52_main_v{VERSION:02}.blend').exists(): VERSION += 1
DEST = OUT / f'f16c_block52_main_v{VERSION:02}.blend'
# This reset affects only the new background process, never a user's open file.
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    if c.name != 'Collection': bpy.data.collections.remove(c)
base = bpy.data.collections.get('Collection'); base.name = '00_AIRFRAME'
COLS = {'airframe':base}
for key, name in [('surfaces','01_CONTROL_SURFACES'),('canopy','02_CANOPY'),('cockpit','03_COCKPIT_BLOCKOUT'),('gear','04_LANDING_GEAR'),('stations','05_EMPTY_STATIONS'),('marks','06_TURKISH_MARKINGS'),('helpers','07_ANCHORS'),('studio','90_PREVIEW_STUDIO')]:
    c=bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c); COLS[key]=c

def mat(name,color,metal=0,rough=.8,alpha=1):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,alpha); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*color,alpha)
    p.inputs['Roughness'].default_value=rough; p.inputs['Metallic'].default_value=metal
    if alpha<1:
        p.inputs['Alpha'].default_value=alpha
        m.surface_render_method='DITHERED'
    return m
UP=mat('Paint_upper_slate_matte',(.26,.30,.34))
LOW=mat('Paint_lower_light_gray',(.48,.53,.56))
NOSE=mat('Radome_gray',(.34,.38,.40))
DARK=mat('Cockpit_charcoal',(.025,.035,.044))
PANEL=mat('Panel_gray',(.09,.12,.14))
SEAT=mat('Seat_olive',(.14,.18,.12))
BLACK=mat('Rubber_and_intake',(.009,.014,.018))
METAL=mat('Gear_light_metal',(.55,.60,.62),.25,.65)
EXHAUST=mat('PW229_nozzle_simplified',(.16,.17,.18),.35,.65)
RED=mat('Turkish_red',(.66,.025,.033))
WHITE=mat('Marking_white',(.84,.86,.84))
YELLOW=mat('Safety_yellow',(.9,.6,.04))
GLASS=mat('Canopy_smoke_transparent',(.24,.38,.43),.05,.38,.24)
HUDMAT=mat('HUD_glass',(.18,.48,.31),0,.4,.18)
SCREEN=mat('Unpowered_display',(.012,.035,.026),0,.7)
GREEN=mat('Preview_display_green',(.1,.5,.24),0,.8)

def link(obj,col):
    for c in list(obj.users_collection):c.objects.unlink(obj)
    COLS[col].objects.link(obj); return obj

def mesh(name,verts,faces,material,col='airframe'):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
    ob=bpy.data.objects.new(name,me); COLS[col].objects.link(ob); me.materials.append(material)
    # Consistent outward normals for closed and open surfaces.
    import bmesh
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(me);bm.free();me.update()
    return ob

def box(name,loc,size,material,col='airframe',bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc); ob=bpy.context.object; ob.name=name
    ob.dimensions=size; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    ob.data.materials.append(material);link(ob,col)
    if bevel:
        mod=ob.modifiers.new('Small edge chamfer','BEVEL');mod.width=bevel;mod.segments=1
    return ob

def rod(name,a,b,r,material,col='airframe',vertices=10,r2=None):
    a,b=Vector(a),Vector(b);d=b-a
    bpy.ops.mesh.primitive_cone_add(vertices=vertices,radius1=r,radius2=r if r2 is None else r2,depth=d.length,location=(a+b)/2)
    o=bpy.context.object;o.name=name;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();o.data.materials.append(material);link(o,col);return o

def line(name,points,r,material,col):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=1;cu.bevel_depth=r;cu.bevel_resolution=0
    sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
    for p,v in zip(sp.points,points):p.co=(*v,1)
    ob=bpy.data.objects.new(name,cu);COLS[col].objects.link(ob);cu.materials.append(material);return ob

def pivot(ob,location,axis=None):
    delta=Vector(location)-ob.location
    if ob.type=='MESH':
        for v in ob.data.vertices:v.co-=delta
    ob.location=location
    ob['pivot_status']='Approximate modeling pivot; mechanism/range unverified'
    if axis:ob['suggested_rotation_axis']=axis
    return ob

def loft(name,stations,material,n=20,cap=True,col='airframe',cockpit=False):
    # station = longitudinal Y, lateral radius, vertical center, vertical radius
    vs=[(rx*math.cos(2*math.pi*i/n),y,z+rz*math.sin(2*math.pi*i/n)) for y,rx,z,rz in stations for i in range(n)]
    fs=[]
    for j in range(len(stations)-1):
        ymid=(stations[j][0]+stations[j+1][0])/2
        for i in range(n):
            # Open cockpit cut-out: upper central 108 degrees in designated stations.
            if cockpit and -4.35<ymid<-1.65 and 2<=i<=7:continue
            fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    if cap:fs.extend([tuple(reversed(range(n))),tuple((len(stations)-1)*n+i for i in range(n))])
    return mesh(name,vs,fs,material,col)

def foil(name,points,thickness,material,col='airframe',vertical=False):
    # Closed thin polygon, thickness tapers at outside edges.
    n=len(points);vs=[]
    for sign in [-1,1]:
        for x,y,z in points:
            t=thickness*(.4 if abs(x)>3 else 1)/2
            vs.append((x+sign*t,y,z) if vertical else (x,y,z+sign*t))
    fs=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]
    fs.extend((i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n))
    ob=mesh(name,vs,fs,material,col);ob.data.materials.append(LOW)
    if not vertical:ob.data.polygons[0].material_index=1
    return ob

# Main body, section-wise flat shaded; upper color separated from lower surface.
body=loft('Fuselage_main_open_cockpit',[
 (-4.7,.54,2.14,.45),(-4.35,.64,2.14,.49),(-3.9,.69,2.13,.51),(-3.2,.73,2.10,.53),(-2.3,.79,2.06,.54),(-1.65,.85,2.02,.54),(-.7,.98,1.99,.56),(.5,1.10,1.98,.60),(2.0,1.04,1.96,.65),(3.6,.93,1.95,.65),(5.2,.80,1.96,.61),(6.35,.70,1.98,.56),(6.8,.66,1.99,.52)],UP,cockpit=True)
body.data.materials.append(LOW)
for p in body.data.polygons:
    if p.center.z<2.0:p.material_index=1
loft('Radome', [(-6.95,.018,2.05,.022),(-6.55,.16,2.09,.16),(-5.85,.35,2.12,.30),(-5.15,.49,2.14,.40),(-4.7,.54,2.14,.45)],NOSE)
rod('Nose_pitot', (0,-7.5311,2.05),(0,-6.90,2.05),.006,METAL,vertices=8,r2=.016)
# LEX blends from cockpit shoulders to wing roots.
for s,label in [(1,'L'),(-1,'R')]:
    foil(f'LEX_{label}',[(s*.60,-4.35,2.16),(s*.86,-2.9,2.16),(s*1.19,-1.2,2.14),(s*1.50,.30,2.10),(s*1.05,2.1,2.04),(s*.75,-1.5,2.12)],.095,UP)
    foil(f'Wing_{label}',[(s*1.08,-.45,2.08),(s*4.86,2.55,2.00),(s*4.86,3.30,2.00),(s*1.09,3.0,2.08)],.11,UP)
    fl=foil(f'Flaperon_{label}',[(s*1.12,3.025,2.075),(s*4.80,3.325,2.00),(s*4.80,3.65,1.99),(s*1.12,3.65,2.065)],.07,UP,'surfaces')
    pivot(fl,(s*1.12,3.025,2.075),'local X / swept hinge approximated')
    # Leading edge flap, separate and aligned with sweep.
    le=foil(f'Leading_edge_flap_{label}',[(s*1.12,-.49,2.083),(s*4.84,2.48,2.002),(s*4.84,2.57,2.009),(s*1.12,-.31,2.095)],.045,LOW,'surfaces')
    pivot(le,(s*1.12,-.31,2.095),'swept hinge; unverified')
    rod(f'Wingtip_empty_rail_{label}',(s*4.90,2.05,2.0),(s*4.90,4.15,2.0),.0784,LOW,'stations',vertices=8)
    st=foil(f'Stabilator_{label}',[(s*.78,4.48,1.86),(s*2.65,6.10,1.75),(s*2.90,7.19,1.70),(s*.81,7.05,1.85)],.09,UP,'surfaces')
    pivot(st,(s*.85,5.95,1.85),'X')
    vf=foil(f'Ventral_fin_{label}',[(s*.64,4.15,1.50),(s*.82,4.74,.72),(s*.79,5.77,.90),(s*.66,5.77,1.45)],.06,UP,vertical=True)
    foil(f'Aft_speedbrake_{label}',[(s*.75,6.15,2.03),(s*1.02,6.7,2.03),(s*.99,7.1,2.0),(s*.68,6.95,2.0)],.045,LOW,'surfaces')
# Tail base and large swept F-16C fin.
foil('Vertical_tail_fixed',[(0,2.1,2.50),(0,4.20,2.88),(0,6.24,4.8768),(0,6.85,4.8768),(0,6.97,2.55)],.15,UP,vertical=True)
rudder=foil('Rudder',[(0,6.91,4.8768),(0,7.13,4.8768),(0,7.09,2.58),(0,6.98,2.58)],.08,UP,'surfaces',vertical=True)
pivot(rudder,(0,6.95,2.65),'Z (simplified slanted hinge)')
box('Tail_base_fairing',(0,5.15,2.56),(.37,3.4,.21),UP,bevel=.06)
rod('Tail_tip_EW_fairing',(0,6.09,4.78),(0,7.24,4.78),.092,UP,vertices=8)
foil('Dorsal_antenna',[(0,1.42,2.54),(0,1.38,2.91),(0,1.73,2.61)],.045,UP,vertical=True)
# NSI-style smaller intake, curved lip, short visible tunnel and dark inner termination.
n=24
shape=[]
for i in range(n):
    t=2*math.pi*i/n
    # near-flat upper lip, U shaped lower bowl
    x=.64*math.cos(t);z=1.46+.48*math.sin(t)
    z=min(z,1.79)
    shape.append((x,z))
vs=[]
for y,f in [(-3.60,1.0),(-3.55,.90),(-2.50,.84)]:
    vs.extend((x*f,y,1.46+(z-1.46)*f) for x,z in shape)
fs=[]
for i in range(n):
    j=(i+1)%n;fs.append((i,j,n+j,n+i));fs.append((n+i,n+j,2*n+j,2*n+i))
intake=mesh('NSI_intake_lip_and_tunnel',vs,fs,LOW);intake.data.materials.append(PANEL)
for p in intake.data.polygons:
    if p.index%2:p.material_index=1
mesh('Intake_dark_depth',vs[2*n:],[tuple(range(n))],BLACK)
loft('Intake_lower_fairing',[(-3.55,.61,1.43,.42),(-2.5,.65,1.47,.48),(-1.5,.68,1.48,.51),(.3,.75,1.49,.48),(1.5,.73,1.54,.42)],LOW,cap=False)
# Remove front-interior blockage: fairing starts behind the intake tunnel opening.
# Upper splitter gap visibly detached from fuselage nose.
box('Intake_splitter',(0,-3.38,1.88),(1.20,.67,.06),UP,bevel=.035)
# Nozzle annulus, open rear with separate simplified petal objects.
loft('Engine_nozzle_collar',[(6.75,.65,1.99,.52),(7.00,.67,1.99,.54)],EXHAUST,cap=False)
for i in range(16):
    a0=2*math.pi*i/16+.012;a1=2*math.pi*(i+1)/16-.012
    points=[]
    for y,r in [(6.99,.64),(7.5311,.49)]:
        for a in [a0,a1]:points.append((r*math.cos(a),y,1.99+r*math.sin(a)))
    pet=mesh(f'Nozzle_petal_{i+1:02}',points,[(0,1,3,2)],EXHAUST,'surfaces')
    sol=pet.modifiers.new('Petal thickness','SOLIDIFY');sol.thickness=.018
loft('Nozzle_inner_tunnel',[(7.48,.475,1.99,.475),(6.7,.41,1.99,.41)],BLACK,cap=False)
mesh('Engine_dark_depth',[(.41*math.cos(2*math.pi*i/24),6.65,1.99+.41*math.sin(2*math.pi*i/24)) for i in range(24)],[tuple(range(24))],BLACK)
# Single-seat canopy bubble. Stations give an inferred silhouette, no blueprint claim.
canstations=[(-4.38,.10,.035),(-4.10,.38,.39),(-3.60,.52,.65),(-2.95,.54,.73),(-2.30,.48,.56),(-1.73,.26,.20),(-1.55,.05,.015)]
# Bridge the body cutout to the canopy perimeter, with a dark inside wall.
for sign,label in [(1,'L'),(-1,'R')]:
    strip=[]
    for y,w,h in canstations:
        rx=.64+(y+4.35)/2.7*.21
        strip.extend([(sign*w,y,2.582),(sign*rx*.83,y,2.40)])
    mesh('Cockpit_shoulder_'+label,strip,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(canstations)-1)],UP)
    inside=[(sign*w,y,z) for y,w,h in canstations for z in [2.58,2.18]]
    mesh('Cockpit_inner_wall_'+label,inside,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(canstations)-1)],DARK,'cockpit')

vs=[];nn=12
for y,w,h in canstations:
    for i in range(nn+1):
        a=math.pi*i/nn;vs.append((w*math.cos(a),y,2.59+h*math.sin(a)))
fs=[]
for j in range(len(canstations)-1):
    for i in range(nn):fs.append((j*(nn+1)+i,j*(nn+1)+i+1,(j+1)*(nn+1)+i+1,(j+1)*(nn+1)+i))
canopy=mesh('Canopy_glass',vs,fs,GLASS,'canopy');pivot(canopy,(0,-1.58,2.59),'X')
for s,label in [(1,'L'),(-1,'R')]:line(f'Canopy_sill_{label}',[(s*w,y,2.585) for y,w,h in canstations],.035,UP,'canopy')
y,w,h=canstations[-2];line('Canopy_aft_bow',[(w*math.cos(math.pi*i/12),y,2.59+h*math.sin(math.pi*i/12)) for i in range(13)],.027,UP,'canopy')
# Blockout cockpit, references establish arrangement only.
box('Cockpit_tub_floor',(0,-2.95,2.08),(1.02,2.35,.11),DARK,'cockpit')
for s,label in [(1,'L'),(-1,'R')]:
    box(f'Console_{label}',(s*.42,-2.86,2.30),(.25,1.30,.21),PANEL,'cockpit',.025)
seat=box('Ejection_seat_back',(0,-2.32,2.57),(.49,.14,.86),DARK,'cockpit',.045);seat.rotation_euler.x=math.radians(-30)
box('Seat_cushion',(0,-2.65,2.22),(.48,.52,.13),SEAT,'cockpit',.035)
head=box('Seat_headrest',(0,-2.04,2.94),(.35,.18,.28),DARK,'cockpit',.04)
for s in [-1,1]:
    line('Seat_harness_'+str(s),[(s*.16,-2.36,2.88),(s*.14,-2.49,2.64),(s*.10,-2.66,2.32)],.025,SEAT,'cockpit')
# Main panel facing aft toward pilot, front at y=-3.73.
box('Instrument_panel',(0,-3.73,2.52),(1.02,.16,.48),PANEL,'cockpit',.08)
for s,label in [(1,'L'),(-1,'R')]:
    x=s*.32
    box('MFD_'+label+'_bezel',(x,-3.623,2.52),(.27,.052,.27),DARK,'cockpit',.017)
    box('MFD_'+label+'_screen',(x,-3.592,2.52),(.205,.012,.205),SCREEN,'cockpit')
    for k in range(4):
        for side in [-1,1]:
            box(f'MFD_{label}_button_{k}_{side}',(x+side*.119,-3.577,2.445+k*.05),(.022,.02,.022),LOW,'cockpit')
            box(f'MFD_{label}_button_h_{k}_{side}',(x-.075+k*.05,-3.577,2.52+side*.119),(.022,.02,.022),LOW,'cockpit')
box('ICP_keypad',(0,-3.598,2.66),(.23,.07,.24),DARK,'cockpit',.015)
for row in range(4):
    for col in range(3):box(f'ICP_key_{row}_{col}',(-.07+col*.07,-3.55,2.58+row*.05),(.045,.021,.032),LOW,'cockpit')
box('DED_housing',(-.35,-3.73,2.79),(.25,.14,.12),DARK,'cockpit')
box('DED_unpowered',(-.35,-3.65,2.79),(.20,.01,.075),SCREEN,'cockpit')
# HUD tilted transparent combiner with side supports.
hud=box('HUD_combiner',(0,-3.76,3.02),(.32,.013,.29),HUDMAT,'cockpit');hud.rotation_euler.x=math.radians(-14)
for s in [-1,1]:rod('HUD_support_'+str(s),(s*.16,-3.82,2.72),(s*.16,-3.72,3.15),.014,DARK,'cockpit',8)
rod('Side_stick_stem',(-.43,-2.80,2.43),(-.43,-2.81,2.66),.032,DARK,'cockpit')
box('Side_stick_grip',(-.43,-2.81,2.68),(.072,.09,.14),DARK,'cockpit',.02)
box('Throttle_track',(.42,-2.83,2.45),(.13,.44,.05),DARK,'cockpit')
box('Throttle_grip',(.42,-2.94,2.52),(.17,.11,.12),DARK,'cockpit',.02)
for s in [-1,1]:box('Rudder_pedal_'+str(s),(s*.15,-3.51,2.15),(.18,.11,.07),METAL,'cockpit')
# Sparse visual switches; no unverified functional cold-start labels.
for s,label in [(1,'L'),(-1,'R')]:
    for k in range(5):
        rod(f'Console_{label}_placeholder_switch_{k}',(s*.42,-3.26+k*.16,2.42),(s*.42,-3.26+k*.16,2.46),.008,METAL,'cockpit',6)
# Undercarriage posed down, rods and doors separate, pivots approximate.
for s,label in [(1,'L'),(-1,'R')]:
    rod(f'Main_gear_strut_{label}',(s*.71,1.32,1.54),(s*1.20,1.85,.38),.056,METAL,'gear')
    rod(f'Main_gear_brace_{label}',(s*.68,2.17,1.50),(s*1.20,1.85,.44),.032,METAL,'gear')
    rod(f'Main_tire_{label}',(s*1.20-.115,1.85,.34),(s*1.20+.115,1.85,.34),.34,BLACK,'gear',20)
    rod(f'Main_hub_{label}',(s*1.20-.121,1.85,.34),(s*1.20+.121,1.85,.34),.16,METAL,'gear',12)
    door=box(f'Main_gear_door_{label}',(s*.94,1.55,1.10),(.06,.92,.66),LOW,'gear');door.rotation_euler.y=s*.3
    pivot(door,(s*.82,1.55,1.45),'Y')
rod('Nose_gear_strut',(0,-2.72,1.1),(0,-2.96,.28),.043,METAL,'gear')
for s in [-1,1]:rod('Nose_gear_fork_'+str(s),(s*.10,-2.90,.48),(s*.10,-2.96,.23),.022,METAL,'gear',8)
rod('Nose_tire',(-.095,-2.96,.23),(.095,-2.96,.23),.23,BLACK,'gear',16)
rod('Nose_hub',(-.101,-2.96,.23),(.101,-2.96,.23),.10,METAL,'gear',12)
box('Nose_gear_door',(0,-2.42,.80),(.38,.07,.53),LOW,'gear')
# Empty wing pylons; no external tanks or missiles.
for s,label in [(1,'L'),(-1,'R')]:
    for k,(x,y,h) in enumerate([(1.65,1.70,.32),(2.75,2.47,.28),(3.85,2.99,.20)],start=1):
        foil(f'Empty_pylon_{label}_{k}',[(s*x,y-.48,1.96),(s*x,y-.29,1.96-h),(s*x,y+.48,1.96-h),(s*x,y+.60,1.96)],.075,LOW,'stations',vertical=True)
# Vector geometry Turkish roundels / flag: zero bitmap textures.
def disk(name,center,r,material,normal='Z'):
    verts=[center]+[(center[0]+r*math.cos(2*math.pi*i/32),center[1]+r*math.sin(2*math.pi*i/32),center[2]) for i in range(32)]
    # Match wing upper plane so no part of the marking is buried.
    verts=[(x,y,2.135+(abs(x)-1.08)/3.78*(2.022-2.135)+.008+(z-center[2])) for x,y,z in verts]
    # Layer offsets are given by caller through center Z.
    layer=max(0,center[2]-2.073)
    verts=[(x,y,z+layer) for x,y,z in verts]
    return mesh(name,verts,[(0,i+1,(i+1)%32+1) for i in range(32)],material,'marks')
for s,label in [(1,'L'),(-1,'R')]:
    x=s*3.3;y=2.77;z=2.073
    disk('Roundel_outer_'+label,(x,y,z),.25,RED)
    disk('Roundel_middle_'+label,(x,y,z+.002),.175,WHITE)
    disk('Roundel_inner_'+label,(x,y,z+.004),.107,RED)
# Flat flag planes on both tail sides, crescent made as open arc ribbon.
for s,label in [(1,'L'),(-1,'R')]:
    x=s*.078;y=6.25;z=4.13
    mesh('Tail_flag_'+label,[(x,y-.29,z-.18),(x,y+.29,z-.18),(x,y+.29,z+.18),(x,y-.29,z+.18)],[(0,1,2,3)],RED,'marks')
    vs=[]
    for i in range(25):
        a=math.radians(55+250*i/24)
        for r,shift in [(.125,0),(.103,.038)]:vs.append((x+s*.002,y-.065+r*math.cos(a)+shift,z+r*math.sin(a)))
    mesh('Flag_crescent_'+label,vs,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(24)],WHITE,'marks')
    vs=[(x+s*.003,y+.14,z)]
    for i in range(10):
        a=math.pi/2+i*math.pi/5;r=.066 if i%2==0 else .028
        vs.append((x+s*.003,y+.14+r*math.cos(a),z+r*math.sin(a)))
    mesh('Flag_star_'+label,vs,[(0,i+1,(i+1)%10+1) for i in range(10)],WHITE,'marks')
# Fictional identity, not a historical registration.
def tailtext(name,text,s,y,z,size):
    cu=bpy.data.curves.new(name,'FONT');cu.body=text;cu.size=size;cu.align_x='CENTER';cu.extrude=0;cu.materials.append(WHITE)
    ob=bpy.data.objects.new(name,cu);COLS['marks'].objects.link(ob);ob.location=(s*.082,y,z)
    ob.rotation_euler=(math.pi/2,0,s*math.pi/2)
    return ob
for s in [-1,1]:tailtext('Fictional_tail_ID_'+str(s),'TR-052',s,6.1,3.65,.15)
# Anchors and metadata communicate unverified geometry within the blend itself.
for name,loc in [('Pilot_eye_APPROX',(0,-2.60,2.96)),('Afterburner_attach',(0,7.53,1.99)),('Canopy_hinge_APPROX',(0,-1.58,2.59))]:
    o=bpy.data.objects.new(name,None);COLS['helpers'].objects.link(o);o.location=loc;o.empty_display_size=.12
    o['status']='Approximate, reference validation pending'
sc=bpy.context.scene;sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1
sc['stage']='Main 3D model v01, NOT final / flight-ready'
sc['reference_length_m']=15.0622;sc['reference_span_m']=9.9568;sc['reference_height_m']=4.8768
sc['measurement_status']='Provisional general F-16 scale; not verified Block 52 endpoints. Model: pitot to nozzle, rails inclusive, gear down.'
sc['cockpit_status']='Arrangement from DCS Block50 auxiliary reference; coordinates inferred, Block52 fit unverified.'
sc['livery_status']='User fictional Turkish Block52; TR-052 is fictional.'
sc['performance_status']='Low poly geometry; no Iris Xe game benchmark performed.'
readme=bpy.data.texts.new('READ_ME_FIRST');readme.write('F-16C Block 52 / ANA MODEL v01\n1 unit = 1 metre. +Y aft, -Y nose.\n\nGeometry is a first editable blockout, not a verified engineering reconstruction.\nDimensions provisional: 15.0622 / 9.9568 / 4.8768 m.\nCockpit controls are visual placeholders. No flight or cold-start simulation.\nPivots and mechanism ranges require further reference validation.\nTR-052 fictional Turkish scheme; not a historical aircraft.\nCollections 00-07 aircraft, 90 preview studio.\nSee research/DURUM.md, output/model/MODEL_NOTES.md.\n')
# Simple studio. Ground and cameras kept apart from the asset.
FLOOR=mat('Studio_ground',(.095,.12,.15))
mesh('Studio_floor',[(-100,-100,-.01),(100,-100,-.01),(100,100,-.01),(-100,100,-.01)],[(0,1,2,3)],FLOOR,'studio')
world=bpy.data.worlds.new('Neutral_studio') if not bpy.data.worlds else bpy.data.worlds[0];sc.world=world;world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.32,.40,.48,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.55
for name,loc,power,size in [('Key',(-6,-6,12),2300,8),('Fill',(7,-1,8),1600,7),('Rim',(1,9,11),2600,6)]:
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size
    o=bpy.data.objects.new(name,data);COLS['studio'].objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,2))-o.location).to_track_quat('-Z','Y').to_euler()

def camera(name,loc,target,ortho=None,lens=50):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);COLS['studio'].objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.lens=lens
    if ortho:d.type='ORTHO';d.ortho_scale=ortho
    d.clip_start=.03;d.clip_end=300;return o
cams={
 'exterior':camera('CAM_Exterior', (13,-17,11),(0,.1,1.9),20),
 'rear':camera('CAM_Rear',(-11,15,8),(0,1.3,2.0),19),
 'top':camera('CAM_Top',(0,0,30),(0,0,0),24),
 'side':camera('CAM_Side',(25,0,2.5),(0,0,2.5),18),
 'front':camera('CAM_Front',(0,-25,2.4),(0,0,2.4),12),
 'cockpit':camera('CAM_Pilot_APPROX',(0,-2.58,2.97),(0,-3.85,2.65),None,20),
}
sc.camera=cams['exterior'];sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=24;sc.cycles.use_denoising=True
sc.render.resolution_x=1400;sc.render.resolution_y=1000;sc.render.resolution_percentage=100
sc.view_settings.view_transform='AgX';sc.render.image_settings.file_format='PNG'
# Save a useful solid-mode opening view; studio hidden in viewport only.
COLS['studio'].hide_viewport=True
for screen in bpy.data.screens:
    for a in screen.areas:
        if a.type=='VIEW_3D':
            a.spaces.active.region_3d.view_distance=20
            a.spaces.active.region_3d.view_location=(0,0,2)
            a.spaces.active.region_3d.view_rotation=cams['exterior'].rotation_euler.to_quaternion()
            a.spaces.active.shading.type='SOLID';a.spaces.active.shading.color_type='MATERIAL'
            a.spaces.active.clip_end=300
# Collect geometry report excluding studio and helpers.
obs=[o for k,c in COLS.items() if k not in ('studio','helpers') for o in c.objects if o.type=='MESH']
coords=[o.matrix_world@v.co for o in obs for v in o.data.vertices]
mins=[min(v[i] for v in coords) for i in range(3)];maxs=[max(v[i] for v in coords) for i in range(3)]
report={'blend':DEST.name,'units':'meters','axis':'+X left, +Y aft, +Z up', 'measurement_status':'provisional, not verified Block52 dimensions','mesh_objects':len(obs),'vertices':sum(len(o.data.vertices) for o in obs),'base_triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in obs),'bbox_min':mins,'bbox_max':maxs,'bbox_size':[maxs[i]-mins[i] for i in range(3)],'materials':len(bpy.data.materials),'external_texture_images':len([im for im in bpy.data.images if im.source=='FILE']),'open_surfaces_intentional':['cockpit opening','canopy bubble','intake tunnel','nozzle petals and tunnel'],'note':'Base count excludes text/curves/modifier evaluation. Evaluated count checked on reopen.'}
(OUT/f'model_report_v{VERSION:02}.json').write_text(json.dumps(report,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(DEST))
print('MODEL_SAVED',str(DEST),json.dumps(report))
if '--render' in sys.argv:
    for key in ['exterior','rear','top','side','front','cockpit']:
        sc.camera=cams[key]
        sc.render.resolution_x=1400 if key!='cockpit' else 1200
        sc.render.resolution_y=1000 if key!='cockpit' else 900
        sc.render.filepath=str(PRE/f'f16_v{VERSION:02}_{key}.png')
        bpy.ops.render.render(write_still=True)
    sc.camera=cams['exterior']
