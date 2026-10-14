"""Create editable visual mechanisms. Angles/linkage coordinates are modeling estimates.
Run on the detailed cockpit blend; original file is never overwritten.
"""
import bpy, bmesh, math, json, hashlib, sys
from pathlib import Path
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/model';PRE=ROOT/'output/previews'
source=Path(bpy.data.filepath);sh=hashlib.sha256(source.read_bytes()).hexdigest()
v=7
while (OUT/f'f16c_block52_main_v{v:02}.blend').exists():v+=1
DEST=OUT/f'f16c_block52_main_v{v:02}.blend'
sc=bpy.context.scene;rig=bpy.data.collections.new('09_MECHANISMS');sc.collection.children.link(rig)
gear=bpy.data.collections['04_LANDING_GEAR'];canopy=bpy.data.collections['02_CANOPY'];surfaces=bpy.data.collections['01_CONTROL_SURFACES']
manifest=[]
def parent_keep(o,p):
    bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw

def empty(name,loc,axis=(1,0,0)):
    o=bpy.data.objects.new(name,None);rig.objects.link(o);o.location=loc;o.empty_display_type='ARROWS';o.empty_display_size=.18
    # local X is always the hinge axis; drive local X without inherited object rotations.
    o.rotation_euler=Vector(axis).to_track_quat('X','Z').to_euler()
    return o
master=empty('RIG_CONTROLS',(0,0,3.5))
master['description']='Visual rig controls, not flight physics. Angles and timing are provisional.'
properties={'canopy':(0.,0.,1.),'gear':(0.,0.,1.),'flaperon':(0.,-1.,1.),'leading_edge':(0.,0.,1.),'pitch':(0.,-1.,1.),'rudder':(0.,-1.,1.),'speedbrake':(0.,0.,1.),'steering':(0.,-1.,1.),'wheel_spin':(0.,-100.,100.),'throttle':(0.,0.,1.)}
for name,(default,mn,mx) in properties.items():
    master[name]=default;master.id_properties_ui(name).update(min=mn,max=mx,description=('0 down / 1 up' if name=='gear' else 'Normalized visual control; unverified physical limits'))

def driven(o,data,index,expression,prop):
    f=o.driver_add(data,index);d=f.driver;d.type='SCRIPTED';var=d.variables.new();var.name='v';var.type='SINGLE_PROP';var.targets[0].id=master;var.targets[0].data_path=f'["{prop}"]';d.expression=expression

def hinge(name,objects,loc,axis,prop,angle,expression=None):
    # Static orientation parent plus zero-rotation child prevents Euler/axis coupling.
    base=empty(name+'_AXIS',loc,axis);joint=empty(name,loc);joint.rotation_euler=(0,0,0);parent_keep(joint,base)
    joint.matrix_parent_inverse=Matrix.Identity(4);joint.location=(0,0,0);joint.rotation_euler=(0,0,0)
    bpy.context.view_layer.update()
    for ob in objects:parent_keep(ob,joint)
    driven(joint,'rotation_euler',0,expression or f'v*{math.radians(angle)}',prop)
    joint['hinge_status']='Geometry-based modeling pivot. Physical axis/range unverified.'
    manifest.append({'hinge':joint.name,'objects':[o.name for o in objects],'position_m':list(loc),'axis':list(axis),'property':prop,'range_deg':angle,'status':'Provisional visual mechanism'})
    return joint

def mesh(name,verts,faces,col,mat):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.materials.append(mat);me.update();o=bpy.data.objects.new(name,me);col.objects.link(o)
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(me);bm.free();return o

def box(name,loc,size,col,mat):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    for c in list(o.users_collection):c.objects.unlink(o)
    col.objects.link(o)
    if mat:o.data.materials.append(mat)
    return o
M=bpy.data.materials;LOW=M['Paint_lower_light_gray'];DARK=M['Cockpit_charcoal'];METAL=M['Gear_light_metal']
# Partition transparent shell at its existing aft bow; aft pane stays fixed.
ob=bpy.data.objects['Canopy_glass'];bpy.context.view_layer.update();world=[ob.matrix_world@x.co for x in ob.data.vertices]
front=[];aft=[]
for p in ob.data.polygons:
    (aft if all(world[i].y>=-1.73001 for i in p.vertices) else front).append(tuple(p.vertices))
def subset(name,faces):
    used=sorted({i for f in faces for i in f});ix={old:i for i,old in enumerate(used)}
    return mesh(name,[world[i] for i in used],[tuple(ix[i] for i in f) for f in faces],canopy,ob.data.materials[0])
fixed=subset('Canopy_aft_fixed_glass',aft);moving=subset('Canopy_moving_glass',front)
bpy.data.objects.remove(ob,do_unlink=True);moving.name='Canopy_glass'
can_objects=[moving,bpy.data.objects['Canopy_aft_bow']]
for side in ['L','R']:
    old=bpy.data.objects['Canopy_sill_'+side];bpy.context.view_layer.update()
    points=[old.matrix_world@Vector(p.co[:3]) for p in old.data.splines[0].points]
    for suffix,pts in [('moving',[p for p in points if p.y<=-1.72999]),('fixed',[p for p in points if p.y>=-1.73001])]:
        cu=old.data.copy();cu.splines.clear();sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
        for p,co in zip(sp.points,pts):p.co=(*co,1)
        new=bpy.data.objects.new('Canopy_sill_'+side+'_'+suffix,cu);canopy.objects.link(new)
        if suffix=='moving':can_objects.append(new)
    bpy.data.objects.remove(old,do_unlink=True)
hinge('HINGE_Canopy',can_objects,(0,-1.73,2.57),(1,0,0),'canopy',-45)
bpy.data.objects['Canopy_hinge_APPROX'].location=(0,-1.73,2.57)
# Rudder follows the swept seam; stabilators and flaps follow their own hinge lines.
for s,side in [(1,'L'),(-1,'R')]:
    hinge('HINGE_Flaperon_'+side,[bpy.data.objects['Flaperon_'+side]],(s*1.12,2.935,2.075),(s*3.68,.207,-.075),'flaperon',-s*20)
    hinge('HINGE_LEF_'+side,[bpy.data.objects['Leading_edge_flap_'+side]],(s*1.12,-.31,2.095),(s*3.72,2.88,-.086),'leading_edge',s*15)
    hinge('HINGE_Stabilator_'+side,[bpy.data.objects['Stabilator_'+side]],(s*.85,5.95,1.85),(1,0,0),'pitch',-18)
hinge('HINGE_Rudder',[bpy.data.objects['Rudder']],(0,5.675,2.64),(0,1.01,2.2368),'rudder',20)
# Split speedbrake leaves, both sides of aft fuselage, kept separate for export.
for s,side in [(1,'L'),(-1,'R')]:
    upper=bpy.data.objects['Aft_speedbrake_'+side];upper.name='Speedbrake_'+side+'_upper'
    lower=upper.copy();lower.data=upper.data.copy();surfaces.objects.link(lower);lower.name='Speedbrake_'+side+'_lower';lower.location.z-=.13
    hinge('HINGE_Speedbrake_'+side+'_upper',[upper],(s*.77,6.15,2.03),(1,0,0),'speedbrake',35)
    hinge('HINGE_Speedbrake_'+side+'_lower',[lower],(s*.77,6.15,1.90),(1,0,0),'speedbrake',-35)
# Wheel-well openings. Simple production mesh booleans, not a structural reconstruction.
cutters=[]
for s,side in [(1,'L'),(-1,'R')]:
    cutters.append(box('CUT_Main_'+side,(s*.76,2.30,1.39),(.74,2.24,1.70),rig,None))
cutters.append(box('CUT_Nose',(0,-2.00,1.05),(.49,2.20,1.14),rig,None))
for name in ['Fuselage_main_open_cockpit','Intake_lower_fairing']:
    ob=bpy.data.objects[name]
    for cutter in cutters:
        mod=ob.modifiers.new('Gear well opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
        bpy.context.view_layer.objects.active=ob;bpy.ops.object.modifier_apply(modifier=mod.name)
for cutter in cutters:bpy.data.objects.remove(cutter,do_unlink=True)
# Dark ceilings and simple bulkheads make the opened wells readable.
for s,side in [(1,'L'),(-1,'R')]:
    box('Main_well_roof_'+side,(s*.73,2.30,2.23),(.65,2.10,.035),gear,DARK)
    box('Main_well_inboard_'+side,(s*.395,2.30,1.83),(.025,2.10,.78),gear,DARK)
    box('Main_gear_mount_'+side,(s*.71,1.32,1.57),(.23,.15,.17),gear,METAL)
box('Nose_well_roof',(0,-2.00,1.63),(.46,2.14,.025),gear,DARK)
# Main legs fold aft/inboard about an oblique axis. Angles are a fit to this model only.
for s,side in [(1,'L'),(-1,'R')]:
    parts=[bpy.data.objects[n+'_'+side] for n in ['Main_gear_strut','Main_tire','Main_hub']]
    leg=hinge('HINGE_Main_gear_'+side,parts,(s*.71,1.32,1.54),(1,s*.55,0),'gear',90)
    # Move tire/hub under an axle for independent wheel rotation.
    axle=hinge('AXLE_Main_'+side,[bpy.data.objects['Main_tire_'+side],bpy.data.objects['Main_hub_'+side]],(s*1.20,1.85,.34),(1,0,0),'wheel_spin',360)
    parent_keep(bpy.data.objects[axle.name+'_AXIS'],leg)
    # Brace is an editable telescoping visual actuator between two explicit anchors.
    brace=bpy.data.objects['Main_gear_brace_'+side]
    target=empty('Main_actuator_end_'+side,(s*1.20,1.85,.44));parent_keep(target,leg)
    bpy.context.view_layer.update();base=Vector((s*.68,2.17,1.50));end=target.matrix_world.translation
    length=(end-base).length
    # Rebuild cylinder along local +Y so STRETCH_TO can keep the base fixed.
    bpy.data.objects.remove(brace,do_unlink=True)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8,radius=.032,depth=length,location=(0,0,0));brace=bpy.context.object;brace.name='Main_gear_brace_'+side
    for vert in brace.data.vertices:
        x,y,z=vert.co;vert.co=(x,z+length/2,-y)
    brace.location=base;brace.rotation_euler=(end-base).to_track_quat('Y','Z').to_euler();brace.data.materials.append(METAL)
    for c in list(brace.users_collection):c.objects.unlink(brace)
    gear.objects.link(brace)
    con=brace.constraints.new('STRETCH_TO');con.target=target;con.rest_length=length;con.volume='NO_VOLUME'
    brace['mechanism_status']='Telescoping visual simplification, not a solved downlock linkage'
# Nose group retracts aft into its own well; steering and wheel axle are nested.
noseparts=[bpy.data.objects[n] for n in ['Nose_gear_strut','Nose_gear_fork_-1','Nose_gear_fork_1','Nose_tire','Nose_hub']]
nose=hinge('HINGE_Nose_gear',noseparts,(0,-2.72,1.10),(1,0,0),'gear',110)
steer=hinge('HINGE_Nose_steering',[bpy.data.objects[n] for n in ['Nose_gear_fork_-1','Nose_gear_fork_1','Nose_tire','Nose_hub']],(0,-2.96,.44),(0,0,1),'steering',25)
parent_keep(bpy.data.objects[steer.name+'_AXIS'],nose)
axle=hinge('AXLE_Nose',[bpy.data.objects['Nose_tire'],bpy.data.objects['Nose_hub']],(0,-2.96,.23),(1,0,0),'wheel_spin',360)
parent_keep(bpy.data.objects[axle.name+'_AXIS'],steer)
# Doors modeled in closed position; gear=0 opens them, gear=1 closes after stowing.
for s,side in [(1,'L'),(-1,'R')]:
    old=bpy.data.objects['Main_gear_door_'+side];bpy.data.objects.remove(old,do_unlink=True)
    verts=[(s*x,y,z) for x,y,z in [(.39,1.18,1.37),(1.13,1.18,1.85),(1.13,3.42,1.85),(.39,3.42,1.37)]]
    ob=mesh('Main_gear_door_'+side,verts,[(0,1,2,3)],gear,LOW);sol=ob.modifiers.new('Door thickness','SOLIDIFY');sol.thickness=.025
    hinge('HINGE_Main_door_'+side,[ob],(s*1.13,2.30,1.85),(0,1,0),'gear',-s*70,expression=f'{math.radians(-s*70)}*(1-min(1,max(0,(v-.78)/.22)))')
old=bpy.data.objects['Nose_gear_door'];bpy.data.objects.remove(old,do_unlink=True)
verts=[(-.25,-3.1,1.13),(.25,-3.1,1.13),(.25,-.9,1.20),(-.25,-.9,1.20)]
ob=mesh('Nose_gear_door',verts,[(0,1,2,3)],gear,LOW);sol=ob.modifiers.new('Door thickness','SOLIDIFY');sol.thickness=.018
hinge('HINGE_Nose_door',[ob],(.25,-2.,1.165),(0,1,0),'gear',-85,expression=f'{math.radians(-85)}*(1-min(1,max(0,(v-.80)/.20)))')
# Throttle has a visible, modest travel; children move with the grip.
throttle=bpy.data.objects['Throttle_grip'];rest=throttle.location.y;driven(throttle,'location',1,f'{rest}-v*.18','throttle')
# Named demo poses on a single action; custom sliders can be edited after unlinking it.
poses={1:{},35:{'canopy':1},65:{'canopy':1},90:{},125:{'gear':1},155:{'gear':1,'flaperon':1,'leading_edge':1,'pitch':1,'rudder':1,'speedbrake':1,'throttle':1},185:{'gear':1,'flaperon':-1,'pitch':-1,'rudder':-1},215:{'gear':1},250:{},280:{'steering':.7,'wheel_spin':2},310:{}}
for frame,values in poses.items():
    for name,(default,mn,mx) in properties.items():master[name]=values.get(name,default);master.keyframe_insert(data_path=f'["{name}"]',frame=frame)
if master.animation_data and master.animation_data.action:master.animation_data.action.name='DEMO_Mechanisms_310f'
for name,frame in [('PARK_CLOSED',1),('CANOPY_OPEN',35),('CANOPY_CLOSED',90),('GEAR_STOWED',125),('SURFACES_POSITIVE',155),('SURFACES_NEGATIVE',185),('GEAR_DOWN',250),('STEERING',280),('RESET',310)]:sc.timeline_markers.new(name,frame=frame)
sc.frame_start=1;sc.frame_end=310;sc.render.fps=30;sc.frame_set(1)
# Store neutral display as default. Remove accidental selections for a clean viewport.
bpy.ops.object.select_all(action='DESELECT');master.select_set(True);bpy.context.view_layer.objects.active=master
sc['stage']='Exterior + detailed cockpit + visual mechanism rig; engineering/flight validation pending'
sc['mechanism_status']='Editable axes, drivers and demo action; angles, gear wells and telescoping brace are modeling estimates'
sc['rig_controls']='RIG_CONTROLS custom properties; DEMO_Mechanisms_310f; see MECHANISMS.md'
bpy.data.texts['READ_ME_FIRST'].write('\nVISUAL MECHANISMS: '+DEST.stem+'\nTimeline 1–310: canopy, gear, flaps/tail/speedbrakes, steering. RIG_CONTROLS owns normalized properties. Aft canopy pane remains fixed. Physical angles, gear wells and linkage remain provisional. No flight dynamics or aircraft systems.\n')
report={'blend':DEST.name,'source':source.name,'source_sha256':sh,'controller':master.name,'action':'DEMO_Mechanisms_310f','frames':[1,310],'joints':manifest,'limits':['Visual ranges and timings only; not engineering limits','Gear bays simplified; not production structural geometry','Main braces use telescoping constraint rather than exact lock linkage','No flight-control mixing or hydraulic simulation']}
(OUT/f'mechanisms_v{v:02}.json').write_text(json.dumps(report,indent=2))
sc.camera=bpy.data.objects['CAM_Exterior'];bpy.ops.wm.save_as_mainfile(filepath=str(DEST));assert hashlib.sha256(source.read_bytes()).hexdigest()==sh
print('RIG_SAVED',DEST,len(manifest),flush=True)
if '--render' in sys.argv:
    sc.cycles.samples=16;sc.render.resolution_x=1400;sc.render.resolution_y=1000
    for key,frame,cam in [('exterior',1,'CAM_Exterior'),('canopy_open',35,'CAM_Forward_join'),('gear_stowed',125,'CAM_Exterior'),('surfaces',155,'CAM_Rear')]:
        sc.frame_set(frame);sc.camera=bpy.data.objects[cam];sc.render.filepath=str(PRE/f'f16_v{v:02}_{key}.png');bpy.ops.render.render(write_still=True)
