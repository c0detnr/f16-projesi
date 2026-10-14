"""Add sourced, simplified cockpit furnishings to existing v04; save a new file.
DCS Block 50 is an auxiliary layout/control reference, NOT Block 52 certification.
"""
import bpy, math, json, sys, hashlib
from pathlib import Path
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/model';PRE=ROOT/'output/previews'
source=Path(bpy.data.filepath);source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
v=5
while (OUT/f'f16c_block52_main_v{v:02}.blend').exists():v+=1
DEST=OUT/f'f16c_block52_main_v{v:02}.blend'
col=bpy.data.collections['03_COCKPIT_BLOCKOUT'];col.name='03_COCKPIT'
labels=bpy.data.collections.new('08_COCKPIT_LABELS');bpy.context.scene.collection.children.link(labels)
controls=[]
M=bpy.data.materials
if 'Safety_yellow' not in M:
    m=M.new('Safety_yellow');m.diffuse_color=(.9,.6,.04,1);m.use_nodes=True
    m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.9,.6,.04,1)
    m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.8
DARK=M['Cockpit_charcoal'];PANEL=M['Panel_gray'];WHITE=M['Marking_white'];LOW=M['Paint_lower_light_gray'];METAL=M['Gear_light_metal'];RED=M['Turkish_red'];YELLOW=M['Safety_yellow'];SCREEN=M['Unpowered_display'];SEAT=M['Seat_olive']
def link(ob,c=col):
    for old in list(ob.users_collection):old.objects.unlink(ob)
    c.objects.link(ob);return ob

def box(name,loc,size,mat=PANEL,bevel=0):
    ob=bpy.data.objects.get(name)
    if ob:
        assert ob.type=='MESH';bpy.data.objects.remove(ob,do_unlink=True)
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat);link(o)
    if bevel:
        m=o.modifiers.new('Edge chamfer','BEVEL');m.width=bevel;m.segments=1
    return o

def rod(name,a,b,r,mat=METAL,n=10):
    a,b=Vector(a),Vector(b);d=b-a
    bpy.ops.mesh.primitive_cylinder_add(vertices=n,radius=r,depth=d.length,location=(a+b)/2)
    o=bpy.context.object;o.name=name;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();o.data.materials.append(mat);link(o);return o

def txt(name,body,loc,size=.018,front=False,mat=WHITE):
    cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.size=size;cu.align_x='CENTER';cu.align_y='CENTER';cu.resolution_u=1;cu.extrude=0;cu.materials.append(mat)
    o=bpy.data.objects.new(name,cu);labels.objects.link(o);o.location=loc;o.rotation_euler=(math.pi/2,0,math.pi) if front else (0,0,math.pi)
    return o

def parent_keep(o,p):
    bpy.context.view_layer.update()
    mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw

def meta(o,id,panel,states,initial,kind,page,role,scope='Auxiliary Block50 reference; Block52 fit pending'):
    o['control_id']=id;o['panel']=panel;o['states']=json.dumps(states);o['initial_state']=initial;o['control_type']=kind;o['source']=f'DCS F-16C manual 16 Aug 2026, pp. {page}';o['verification']=scope;o['planned_function']=role;o['motion_status']='Visual control; no aircraft system simulation'
    controls.append({'id':id,'object':o.name,'panel':panel,'kind':kind,'states':states,'initial':initial,'position_m':list(o.location),'source_pages':str(page),'verification':scope,'planned_function':role})
    return o

def pivot(o,p):
    bpy.context.view_layer.update();mw=o.matrix_world.copy();world=[mw@x.co for x in o.data.vertices];o.matrix_world=Matrix.Translation(Vector(p))
    inv=o.matrix_world.inverted()
    for x,co in zip(o.data.vertices,world):x.co=inv@co

# Remove only known obsolete cockpit placeholders in the new working copy.
for o in list(col.objects):
    if '_placeholder_switch_' in o.name or o.name.startswith(('MFD_L_button','MFD_R_button','ICP_key_')):
        bpy.data.objects.remove(o,do_unlink=True)
# Panel is closer to the pilot and extends down to the ADI/EHSI stack.
box('Instrument_panel',(0,-3.36,2.49),(1.12,.12,.59),PANEL,.045)
box('Center_instrument_pedestal',(0,-3.32,2.12),(.44,.16,.46),PANEL,.025)
box('Glare_shield',(0,-3.46,2.815),(1.15,.27,.065),DARK,.025)
# Independent 20 OSBs, five per edge, in documented numbering order.
for s,label in [(1,'L'),(-1,'R')]:
    x=s*.31;z=2.59;y=-3.27
    box('MFD_'+label+'_bezel',(x,y,z),(.267,.06,.29),DARK,.012)
    box('MFD_'+label+'_screen',(x,y+.034,z),(.190,.008,.213),SCREEN)
    coords=[]
    coords += [(x+.092-i*.046,z+.127) for i in range(5)]
    coords += [(x-.114,z+.092-i*.046) for i in range(5)]
    coords += [(x-.092+i*.046,z-.127) for i in range(5)]
    coords += [(x+.114,z-.092+i*.046) for i in range(5)]
    for k,(xx,zz) in enumerate(coords,1):
        o=box(f'MFD_{label}_OSB_{k:02}',(xx,y+.044,zz),(.023,.019,.022),LOW,.002)
        meta(o,f'mfd_{label.lower()}_{k:02}',f'MFD {label}',['RELEASED','PRESSED'],'RELEASED','pushbutton','123','Select adjacent display option')
    txt('MFD_'+label+'_ID','MFD '+label,(x,y+.046,z-.160),.019,True)
# ICP source page 99–100. Use readable short legends on individual keys.
box('ICP_keypad',(0,-3.26,2.765),(.285,.08,.292),DARK,.01)
keys=[('1','T-ILS'),('2','ALOW'),('3',''),('4','STPT'),('5','CRUS'),('6','TIME'),('7','MARK'),('8','FIX'),('9','A-CAL'),('RCL',''),('0','M-SEL'),('ENTR','')]
for i,(number,legend) in enumerate(keys):
    row,c=divmod(i,3);x=.073-c*.073;z=2.815-row*.045
    o=box('ICP_'+number,(x,-3.209,z),(.055,.018,.038),PANEL,.003)
    t=txt('ICP_label_'+number,number+ ('\n'+legend if legend else ''),(x,-3.198,z),.011,True);parent_keep(t,o)
    meta(o,'icp_'+number.lower(),'ICP',['RELEASED','PRESSED'],'RELEASED','pushbutton','99–100','DED input / priority page')
for i,name in enumerate(['COM 1','COM 2','IFF','LIST','A-A','A-G']):
    x=.115-i*.046;z=2.881
    o=box('ICP_'+name.replace(' ','_'),(x,-3.205,z),(.041,.021,.026),PANEL,.004)
    t=txt('ICP_label_'+name,name,(x,-3.192,z),.009,True);parent_keep(t,o)
    meta(o,'icp_'+name.lower().replace(' ','_'),'ICP',['RELEASED','PRESSED'],'RELEASED','pushbutton','99','UFC override / master mode')
for x,id,label in [(.122,'hud_sym','SYM'),(-.122,'ret_depr','RET')]:
    o=rod('CTRL_'+id,(x,-3.24,2.772),(x,-3.198,2.772),.016,DARK,10)
    txt('LBL_'+id,label,(x,-3.19,2.80),.010,True)
    meta(o,id,'ICP',['MIN','MAX'],'MIN','rotary','99','HUD brightness' if id=='hud_sym' else 'Reticle depression')
# Physical DED remains unpowered at the delivered cold state.
box('DED_housing',(-.335,-3.34,2.885),(.30,.16,.125),DARK,.012)
box('DED_unpowered',(-.335,-3.25,2.885),(.255,.012,.088),SCREEN)
txt('DED_label','DED',(-.335,-3.242,2.957),.018,True)
# HUD brought forward of the ICP; clean sight line, no invented flight symbology.
box('HUD_base',(0,-3.57,2.87),(.33,.26,.07),DARK,.014)
o=bpy.data.objects['HUD_combiner'];o.location=(0,-3.54,3.08);o.dimensions=(.32,.013,.29)
for s in [-1,1]:
    old=bpy.data.objects.get('HUD_support_'+str(s))
    if old:bpy.data.objects.remove(old,do_unlink=True)
    rod('HUD_support_'+str(s),(s*.164,-3.59,2.875),(s*.164,-3.50,3.22),.011,DARK,8)
# Dial faces with separate pointers for later binding; scales are schematic, not flight-calibrated.
def dial(id,title,x,z,r=.072,attitude=False):
    y=-3.213
    rod('Gauge_'+id+'_bezel',(x,y-.045,z),(x,y-.01,z),r,DARK,24)
    rod('Gauge_'+id+'_face',(x,y-.009,z),(x,y,z),r*.86,SCREEN,24)
    for k in range(12):
        a=math.radians(40+k*25);xx=x+math.sin(a)*r*.72;zz=z+math.cos(a)*r*.72
        tick=box('Gauge_'+id+f'_tick_{k}',(xx,y+.002,zz),(.0025,.002,.008),WHITE)
        tick.rotation_euler.y=a
    needle=box('Gauge_'+id+'_needle',(x,y+.005,z+r*.24),(.003,.004,r*.52),WHITE)
    pivot(needle,(x,y+.005,z));needle.rotation_euler.y=math.radians(-125)
    needle['indication_status']='Schematic cold-state pointer; scale and PW229 calibration pending'
    txt('Gauge_'+id+'_legend',title,(x,y+.008,z-r*.25),r*.19,True)
    if attitude:
        # Fixed horizon illustration, explicitly flagged as unpowered / not a flight indication.
        box('Gauge_'+id+'_horizon',(x,y+.011,z),(r*1.18,.004,.003),WHITE)
        txt('Gauge_'+id+'_off','OFF',(x,y+.013,z+r*.33),r*.20,True,RED)
    return needle
# Main flight arrangement follows p44: airspeed/altimeter above ADI, EHSI below.
dial('airspeed','KNOTS',.105,2.415,.081)
dial('altimeter','ALT',-.105,2.415,.081)
dial('adi','ADI',0,2.225,.085,True)
dial('ehsi','EHSI',0,2.035,.082)
dial('sai','SAI',-.338,2.795,.042,True)
for z,id,title in [(2.69,'oil','OIL'),(2.58,'nozzle','NOZ'),(2.47,'rpm','RPM'),(2.36,'ftit','FTIT')]:dial(id,title,-.494,z,.039)
box('Fuel_flow_window',(-.52,-3.258,2.811),(.091,.03,.041),DARK)
txt('Fuel_flow_legend','FUEL FLOW',(-.52,-3.235,2.841),.011,True)
for x,id,title in [(.155,'aoa','AOA'),(-.155,'vvi','VVI')]:dial(id,title,x,2.222,.044)
# Left auxiliary landing gear panel and right auxiliary fuel quantity.
box('LG_panel',(.36,-3.18,2.295),(.28,.16,.22),PANEL,.012)
for x in [.285,.36,.435]:rod('LG_indicator', (x,-3.08,2.355),(x,-3.071,2.355),.012,SCREEN,12)
txt('Wheels_label','WHEELS',(.36,-3.065,2.388),.018,True)
o=rod('CTRL_gear_handle',(.40,-3.08,2.285),(.40,-3.005,2.285),.014,LOW)
knob=rod('LG_handle_grip',(.37,-3.005,2.285),(.43,-3.005,2.285),.028,LOW,12);parent_keep(knob,o)
pivot(o,(.40,-3.08,2.285));meta(o,'landing_gear','LEFT AUX',['UP','DOWN'],'DOWN','lever','56','Landing gear command')
txt('Gear_label','UP    DN',(.39,-3.065,2.235),.016,True)
dial('fuel_qty','FUEL',-.36,2.30,.074)
# Canopy rails define the console width; furnishing dimensions remain estimates.
for s,label in [(1,'L'),(-1,'R')]:box('Console_'+label,(s*.475,-2.46,2.285),(.35,1.73,.16),PANEL,.018)
# Compact panel layouts; titles and switch labels face the seated pilot.
def panel(id,title,x,y,w=.30,h=.25):
    box('Panel_'+id,(x,y,2.383),(w,h,.025),DARK,.004)
    txt('Panel_title_'+id,title,(x,y-h/2+.026,2.398),.018)
    return (x,y)
def toggle(id,label,x,y,states,initial,panel_name,page,kind='toggle',role='',front=False):
    z=2.408
    o=rod('CTRL_'+id,(x,y,z),(x,y,z+.039),.006,METAL,8)
    pivot(o,(x,y,z));o.rotation_euler.x=math.radians(-20 if initial in ('OFF','DOWN') else 0)
    cap=box('Cap_'+id,(x,y,z+.037),(.016,.016,.015),LOW,.002);parent_keep(cap,o)
    txt('LBL_'+id,label,(x,y-.041,z-.008),.014)
    # Compact station legends establish kademes while full list remains metadata.
    txt('POS_'+id,' / '.join(states),(x,y+.041,z-.008),.0095)
    return meta(o,id,panel_name,states,initial,kind,page,role or label)
def knob(id,label,x,y,states,initial,panel_name,page):
    z=2.408;o=rod('CTRL_'+id,(x,y,z),(x,y,z+.025),.019,DARK,10)
    stripe=box('Stripe_'+id,(x,y-.004,z+.026),(.003,.024,.003),WHITE);parent_keep(stripe,o)
    txt('LBL_'+id,label,(x,y-.043,z-.008),.014)
    txt('POS_'+id,' / '.join(states),(x,y+.043,z-.008),.009)
    return meta(o,id,panel_name,states,initial,'rotary',page,label)
panel('elec','ELEC',.475,-2.49,h=.25)
toggle('main_power','MAIN PWR',.42,-2.48,['OFF','BATT','MAIN PWR'],'OFF','ELEC','64',role='Select electrical power source')
toggle('elec_reset','RESET',.565,-2.48,['RELEASED','PRESSED'],'RELEASED','ELEC','65',kind='pushbutton')
panel('fuel','FUEL',.475,-2.17,h=.30)
toggle('fuel_master','MASTER',.40,-2.16,['OFF','MASTER'],'MASTER','FUEL','67',role='Engine fuel shutoff')
knob('engine_feed','ENG FEED',.565,-2.16,['OFF','NORM','AFT','FWD'],'NORM','FUEL','67')
panel('epu','EPU',.475,-1.87,h=.23)
toggle('epu','EPU',.47,-1.85,['OFF','NORM','ON'],'NORM','EPU','64')
panel('eng_start','JET FUEL',.50,-2.77,h=.23)
o=toggle('jfs','JFS',.52,-2.76,['START 1','OFF','START 2'],'OFF','ENG START','63',role='Jet fuel starter command; PW229 operating sequence pending')
o['verification']='DCS GE129 panel source only; PW229 panel compatibility pending'
controls[-1]['verification']=o['verification']
# Rebuild throttle as a recognizable grip with attached speedbrake and cutoff gate.
box('Throttle_track',(.365,-2.96,2.40),(.095,.35,.025),DARK)
box('Throttle_grip',(.365,-2.94,2.48),(.15,.105,.09),DARK,.018)
meta(bpy.data.objects['Throttle_grip'],'throttle','LEFT HOTAS',['OFF','IDLE','MIL','MAX'],'OFF','lever','87–89','Throttle and cutoff gate; PW229 response unmodeled')
toggle('speedbrake','SPD BRK',.36,-2.945,['CLOSE','HOLD','OPEN'],'HOLD','THROTTLE','89',role='Speedbrake command')
# Place the small rocker on the actual throttle top, preserving its child parts/labels.
ctrl=bpy.data.objects['CTRL_speedbrake'];ctrl.location.z+=.125
for n in ['LBL_speedbrake','POS_speedbrake']:bpy.data.objects[n].location.z+=.125
parent_keep(ctrl,bpy.data.objects['Throttle_grip'])
# Canopy actuation and seal-lock handle forward/outboard of the throttle.
toggle('canopy_switch','CANOPY',.57,-3.035,['UP','STOP','DOWN'],'STOP','LEFT WALL','73')
o=box('CTRL_canopy_lock',(.58,-2.96,2.545),(.025,.14,.03),YELLOW,.004)
meta(o,'canopy_lock','LEFT WALL',['UNLOCKED','LOCKED'],'LOCKED','lever','73','Canopy seal and latch')
# Right: illumination forward; oxygen and avionics aft of side stick.
panel('lighting','LIGHTING',-.475,-2.99,h=.24)
knob('console_light','CONSOLES',-.405,-2.97,['OFF','BRT'],'OFF','INT LIGHTING','76')
knob('instrument_light','INST PNL',-.555,-2.97,['OFF','BRT'],'OFF','INT LIGHTING','76')
panel('oxygen','OXYGEN',-.475,-2.62,h=.28)
toggle('oxygen_supply','SUPPLY',-.40,-2.59,['OFF','ON','PBG'],'OFF','OXYGEN','77')
toggle('oxygen_diluter','DILUTER',-.555,-2.59,['NORM','100%'],'NORM','OXYGEN','77')
panel('avionics','AVIONICS POWER',-.475,-2.15,h=.57)
for row,names in enumerate([['MMC','ST STA','MFD'],['UFC','GPS','DL']]):
    for i,name in enumerate(names):
        toggle('av_'+name.lower().replace(' ','_'),name,-.365-i*.105,-2.27+row*.14,['OFF',name],'OFF','AVIONICS','78–79')
knob('ins','INS',-.475,-1.955,['OFF','STOR HDG','NORM','NAV','CAL','IN FLT','ATT'],'OFF','AVIONICS','79')
# Document full detent labels even though the small model legend is abbreviated.
controls[-1]['states']=['OFF','ALIGN STOR HDG','ALIGN NORM','NAV','CAL','IN FLT ALIGN','ATT'];bpy.data.objects['CTRL_ins']['states']=json.dumps(controls[-1]['states'])
# Front left aux switches with own raised shelf, comfortable visual reach.
panel('landing','LANDING',.485,-3.27,w=.27,h=.18)
toggle('landing_light','LIGHTS',.53,-3.25,['LANDING','OFF','TAXI'],'OFF','LEFT AUX','57')
toggle('parking_brake','BRAKES',.415,-3.25,['PARK','ANTI-SKID','OFF'],'PARK','LEFT AUX','56')
# Cold-start test controls, aft left, kept distinct from normal operating controls.
panel('test','TEST',.475,-1.65,h=.18)
toggle('flcs_power_test','FLCS PWR',.405,-1.63,['MAINT','NORM','TEST'],'NORM','TEST','73',role='Pre-start FLCS battery test; MAINT reserved for maintenance')
toggle('lights_test','MAL / IND',.56,-1.63,['RELEASED','PRESSED'],'RELEASED','TEST','72',kind='pushbutton',role='Indicator lamp test')
# Seat: retain 30-degree approximate back angle; add pan, bolsters, headbox and rails.
box('Seat_pan',(0,-2.64,2.16),(.53,.57,.09),DARK,.025)
for s in [-1,1]:
    box('Seat_side_bolster_'+str(s),(s*.246,-2.61,2.29),(.065,.48,.15),SEAT,.018)
    rod('Seat_guide_rail_'+str(s),(s*.255,-2.48,2.12),(s*.255,-2.00,2.97),.018,METAL,8)
    box('Seat_head_wing_'+str(s),(s*.198,-2.06,2.97),(.065,.23,.16),DARK,.018)
# Ejection handle and safing lever are visual props, not a simulation sequence.
cu=bpy.data.curves.new('Seat_handle','CURVE');cu.dimensions='3D';cu.bevel_depth=.009;cu.bevel_resolution=0
sp=cu.splines.new('POLY');sp.points.add(7)
for i,p in enumerate(sp.points):
    a=2*math.pi*i/8;p.co=(.09*math.cos(a),-2.89,2.29+.07*math.sin(a),1)
sp.use_cyclic_u=True;cu.materials.append(YELLOW);o=bpy.data.objects.new('Seat_ejection_handle',cu);col.objects.link(o)
# Right force-sensing stick: small trim/NWS buttons; no large joystick throw.
box('Side_stick_grip',(-.435,-2.83,2.66),(.074,.105,.145),DARK,.014)
o=box('CTRL_stick_trim',(-.435,-2.845,2.74),(.026,.025,.017),LOW,.004)
meta(o,'stick_trim','RIGHT HOTAS',['NEUTRAL','NOSE UP','NOSE DOWN','ROLL L','ROLL R'],'NEUTRAL','hat','83','Pitch/roll trim')
o=box('CTRL_nws',(-.476,-2.816,2.675),(.012,.026,.025),LOW,.003)
meta(o,'nosewheel_steering','RIGHT HOTAS',['RELEASED','PRESSED'],'RELEASED','pushbutton','83–84','Ground NWS toggle; multifunction in flight')
box('Right_armrest',(-.43,-2.49,2.40),(.16,.28,.05),DARK,.016)
# Warning annunciators are dark in cold state. Avoid GE-specific SEC/EEC choice.
for x,title in [(.455,'MASTER\nCAUTION'),(-.50,'ENG FIRE'),(-.565,'CANOPY')]:
    box('Annunciator_'+title.replace('\n','_'),(x,-3.32,2.91),(.065,.025,.046),DARK,.004)
    txt('Annunciator_label_'+title,title,(x,-3.303,2.91),.009,True,LOW)
# Eye remains explicitly an estimate. Two pilot cameras provide forward and down views.
eye=bpy.data.objects['Pilot_eye_APPROX'];eye.location=(0,-2.56,3.04);eye['status']='Estimated eye point; no anthropometric/Block52 dimension validation'
studio=bpy.data.collections['90_PREVIEW_STUDIO']
def camera(name,loc,target,lens=24):
    ob=bpy.data.objects.get(name)
    if not ob:
        ob=bpy.data.objects.new(name,bpy.data.cameras.new(name));studio.objects.link(ob)
    ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();ob.data.type='PERSP';ob.data.lens=lens;ob.data.clip_start=.02;return ob
camera('CAM_Pilot_APPROX',eye.location,(0,-3.5,2.67),17)
camera('CAM_Console_L',(.04,-2.05,3.12),(.475,-2.53,2.39),30)
camera('CAM_Console_R',(-.04,-2.00,3.12),(-.475,-2.47,2.39),30)
camera('CAM_Cockpit_overview',(1.9,-.4,5.7),(0,-2.75,2.43),42)
# Register all controls with final world-space positions after placement.
bpy.context.view_layer.update()
for row in controls:row['position_m']=list(bpy.data.objects[row['object']].matrix_world.translation)
manifest={'blend':DEST.name,'source':source.name,'source_sha256':source_hash,'reference':'Local DCS F-16C manual, 16 August 2026','scope':'Names/states reviewed in Block50 auxiliary reference; Block52 installation and physical coordinates remain unverified','controls':controls,'indicators':'Cold unpowered displays; analogue needles schematic, no flight/system logic','ergonomics':'Modeling estimate, eye at (0,-2.56,3.04), 1 unit=1m'}
(OUT/f'cockpit_controls_v{v:02}.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
sc=bpy.context.scene;sc['cockpit_status']='Detailed simplified controls with source metadata; Block52 transfer and ergonomic dimensions pending';sc['stage']='Exterior refined and cockpit detailed; mechanisms pending'
sc['controls_manifest']=f'cockpit_controls_v{v:02}.json'
bpy.data.texts['READ_ME_FIRST'].write('\nCOCKPIT DETAIL: '+DEST.stem+'\nLabels/control states sourced to DCS auxiliary Block50 manual. NOT a verified Block52 checklist. GE129 start thresholds not copied. All displays unpowered. No simulation logic.\n')
sc.camera=bpy.data.objects['CAM_Exterior'];bpy.ops.wm.save_as_mainfile(filepath=str(DEST));assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
print('COCKPIT_SAVED',DEST,'CONTROLS',len(controls),flush=True)
if '--render' in sys.argv:
    sc.cycles.samples=20;sc.render.resolution_x=1500;sc.render.resolution_y=1100
    for key,cam in [('cockpit','CAM_Pilot_APPROX'),('console_l','CAM_Console_L'),('console_r','CAM_Console_R'),('cockpit_overview','CAM_Cockpit_overview')]:
        sc.camera=bpy.data.objects[cam];sc.render.filepath=str(PRE/f'f16_v{v:02}_{key}.png');bpy.ops.render.render(write_still=True)
