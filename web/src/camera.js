import * as THREE from "three";

const FPS_POS = new THREE.Vector3(0, 3.04, 2.56);
const TPS_POS = new THREE.Vector3(0, 4.6, -19);

export class CameraRig {
  constructor(camera) {
    this.camera = camera;
    this.mode = "fps";
    this._target = new THREE.Vector3();
  }

  setAircraft(root, eye) {
    root.add(this.camera);
    if (eye) FPS_POS.set(eye[0], eye[1], eye[2]);
    this.snap();
  }

  toggle() {
    this.mode = this.mode === "fps" ? "tps" : "fps";
    this.snap();
  }

  snap() {
    this.camera.position.copy(this.mode === "fps" ? FPS_POS : TPS_POS);
    this.camera.rotation.set(0, Math.PI, 0);
  }

  update(dt) {
    if (this.mode === "tps") {
      this._target.copy(TPS_POS);
      this.camera.position.lerp(this._target, 1 - Math.exp(-dt * 5));
    }
  }
}
