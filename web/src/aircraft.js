import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

const GEAR_RATE = 1 / 2.5;

function makePivot(children, pivot) {
  const group = new THREE.Group();
  group.position.copy(pivot);
  children.forEach((c) => {
    c.parent.remove(c);
    c.position.sub(pivot);
    group.add(c);
  });
  return group;
}

export class Aircraft {
  constructor() {
    this.root = new THREE.Group();
    this.gearPos = 1;
    this.gearTarget = 1;
    this._pivots = {};
    this._throttleGrip = null;
    this._throttleBaseZ = 0;
    this._stick = null;
    this._stickPivot = null;
    this._surfaces = {};
  }

  async load(glbUrl, metaUrl) {
    const [gltf, meta] = await Promise.all([
      new GLTFLoader().loadAsync(glbUrl),
      fetch(metaUrl).then((r) => r.json()),
    ]);
    this.root.add(gltf.scene);
    this.meta = meta;
    this._buildGearPivots(meta);
    this._findCockpitParts();
    return this;
  }

  _obj(name) {
    return this.root.getObjectByName(name);
  }

  _buildGearPivots(meta) {
    const gear = meta.gear;

    const noseParts = ["Nose_gear_strut", "Nose_tire", "Nose_hub", "Nose_gear_fork_1", "Nose_gear_fork_-1"]
      .map((n) => this._obj(n))
      .filter(Boolean);
    this._pivots.nose = makePivot(noseParts, new THREE.Vector3(...gear["Nose_gear_strut"].pivot_gltf));
    this.root.add(this._pivots.nose);

    for (const side of ["L", "R"]) {
      const parts = ["Main_gear_strut_" + side, "Main_tire_" + side, "Main_hub_" + side, "Main_gear_brace_" + side]
        .map((n) => this._obj(n))
        .filter(Boolean);
      this._pivots["main" + side] = makePivot(parts, new THREE.Vector3(...gear["Main_gear_strut_" + side].pivot_gltf));
      this.root.add(this._pivots["main" + side]);
    }

    this._pivots.doorNose = this._obj("Nose_gear_door");
    this._pivots.doorL = this._obj("Main_gear_door_L");
    this._pivots.doorR = this._obj("Main_gear_door_R");

    for (const n of ["Flaperon_L", "Flaperon_R", "Stabilator_L", "Stabilator_R", "Rudder", "Leading_edge_flap_L", "Leading_edge_flap_R"]) {
      const o = this._obj(n);
      if (o) this._surfaces[n] = o;
    }
  }

  _findCockpitParts() {
    const grip = this._obj("Throttle_grip");
    if (grip) {
      this._throttleGrip = grip;
      this._throttleBaseZ = grip.position.z;
    }
    const stem = this._obj("Side_stick_stem");
    const stickGrip = this._obj("Side_stick_grip");
    if (stem && stickGrip) {
      const box = new THREE.Box3().setFromObject(stem);
      const pivot = new THREE.Vector3((box.min.x + box.max.x) / 2, box.min.y, (box.min.z + box.max.z) / 2);
      this._stickPivot = makePivot([stem, stickGrip], pivot);
      this.root.add(this._stickPivot);
    }
  }

  get gearMoving() {
    return Math.abs(this.gearPos - this.gearTarget) > 0.001;
  }

  setGear(pos, instant = false) {
    this.gearTarget = pos;
    if (instant) this.gearPos = pos;
  }

  resetControls() {
    this.gearPos = 1;
    this.gearTarget = 1;
    if (this._throttleGrip) this._throttleGrip.position.z = this._throttleBaseZ;
    if (this._stickPivot) this._stickPivot.rotation.set(0, 0, 0);
  }

  update(dt, input, physics) {
    this.gearTarget = physics.gearDown ? 1 : 0;
    const dir = Math.sign(this.gearTarget - this.gearPos);
    if (dir !== 0) {
      this.gearPos = THREE.MathUtils.clamp(this.gearPos + dir * GEAR_RATE * dt, 0, 1);
    }

    const retracted = 1 - this.gearPos;
    if (this._pivots.nose) this._pivots.nose.rotation.x = retracted * 1.75;
    if (this._pivots.mainL) this._pivots.mainL.rotation.z = -retracted * 1.75;
    if (this._pivots.mainR) this._pivots.mainR.rotation.z = retracted * 1.75;
    if (this._pivots.doorL) this._pivots.doorL.rotation.z = retracted * 1.6;
    if (this._pivots.doorR) this._pivots.doorR.rotation.z = -retracted * 1.6;
    if (this._pivots.doorNose) this._pivots.doorNose.rotation.x = -retracted * 1.6;

    if (this._throttleGrip) {
      this._throttleGrip.position.z = this._throttleBaseZ + physics.throttle * 0.18;
    }
    if (this._stickPivot) {
      this._stickPivot.rotation.x = input.pitch * 0.14;
      this._stickPivot.rotation.z = input.roll * 0.12;
    }

    const roll = input.roll;
    const pitch = input.pitch;
    if (this._surfaces["Flaperon_L"]) this._surfaces["Flaperon_L"].rotation.x = roll * 0.3;
    if (this._surfaces["Flaperon_R"]) this._surfaces["Flaperon_R"].rotation.x = -roll * 0.3;
    if (this._surfaces["Stabilator_L"]) this._surfaces["Stabilator_L"].rotation.x = -pitch * 0.25;
    if (this._surfaces["Stabilator_R"]) this._surfaces["Stabilator_R"].rotation.x = -pitch * 0.25;
    if (this._surfaces["Rudder"]) this._surfaces["Rudder"].rotation.y = roll * 0.25;
    if (this._surfaces["Leading_edge_flap_L"]) this._surfaces["Leading_edge_flap_L"].rotation.x = -pitch * 0.15;
    if (this._surfaces["Leading_edge_flap_R"]) this._surfaces["Leading_edge_flap_R"].rotation.x = -pitch * 0.15;
  }
}
