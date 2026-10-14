import * as THREE from "three";

export class Input {
  constructor(overlay) {
    this.overlay = overlay;
    this.pitch = 0;
    this.roll = 0;
    this.throttleUp = false;
    this.throttleDown = false;
    this.gearToggle = false;
    this.cameraToggle = false;
    this.brake = false;
    this.locked = false;
    this.demo = window.location.hash === "#demo";
    this._elapsed = 0;
    if (this.demo) {
      this.locked = true;
      overlay.classList.add("hidden");
      document.getElementById("hud").classList.remove("hidden");
      document.getElementById("throttle-gauge").classList.remove("hidden");
    }

    this._pointerX = 0;
    this._pointerY = 0;
    this._keys = {};

    overlay.addEventListener("click", () => document.body.requestPointerLock());
    document.addEventListener("pointerlockchange", () => {
      this.locked = document.pointerLockElement === document.body;
      if (this.locked) {
        overlay.classList.add("hidden");
      } else {
        overlay.classList.remove("hidden");
      }
    });
    document.addEventListener("mousemove", (e) => {
      if (!this.locked) return;
      this._pointerX = THREE.MathUtils.clamp(this._pointerX + e.movementX * 0.003, -1, 1);
      this._pointerY = THREE.MathUtils.clamp(this._pointerY + e.movementY * 0.003, -1, 1);
    });
    document.addEventListener("keydown", (e) => {
      if (!this.locked) return;
      this._keys[e.code] = true;
      if (e.code === "KeyG") this.gearToggle = true;
      if (e.code === "KeyV") this.cameraToggle = true;
      if (e.code === "KeyR") this.resetRequest = true;
    });
    document.addEventListener("keyup", (e) => {
      this._keys[e.code] = false;
    });
  }

  update(dt) {
    this._elapsed += dt;
    if (!this.locked) return;
    const recenter = Math.exp(-dt * 1.2);
    this._pointerX *= recenter;
    this._pointerY *= recenter;

    const targetRoll = this._pointerX;
    const targetPitch = this._pointerY;
    const follow = 1 - Math.exp(-dt * 6);
    this.roll += (targetRoll - this.roll) * follow;
    this.pitch += (targetPitch - this.pitch) * follow;

    this.throttleUp = this._keys["KeyW"] === true || (this.demo && this._elapsed > 3);
    this.throttleDown = this._keys["KeyS"] === true;
    this.brake = this._keys["Space"] === true;
  }
}
