import * as THREE from "three";

const G = 9.81;
const MAX_THRUST_ACC = 12.5;
const LIFT_K = G / (75 * 75);
const LIFT_CAP = 2.2 * G;
const DRAG_K = 1.3e-4;
const GEAR_DRAG_K = 1.6e-4;
const ROLL_FRICTION = 0.35;
const BRAKE_DEC = 6.0;
const PITCH_RATE = THREE.MathUtils.degToRad(45);
const ROLL_RATE = THREE.MathUtils.degToRad(130);
const VR = 68;
const STEER_MAX = 0.7;

const _fwd = new THREE.Vector3();
const _up = new THREE.Vector3();
const _right = new THREE.Vector3();
const _acc = new THREE.Vector3();
const _q = new THREE.Quaternion();
const _e = new THREE.Euler();
const _side = new THREE.Vector3();

export class FlightPhysics {
  constructor() {
    this.reset();
  }

  reset() {
    this.pos = new THREE.Vector3(0, 0, 120);
    this.quat = new THREE.Quaternion();
    this.vel = new THREE.Vector3();
    this.throttle = 0;
    this.gearDown = true;
    this.onGround = true;
    this.crashed = false;
    this.heading = 0;
    this.pitchAngle = 0;
  }

  get speed() {
    return this.vel.length();
  }

  update(dt, input, aircraft) {
    if (this.crashed) {
      if (input.resetRequest) {
        input.resetRequest = false;
        this.reset();
        aircraft.setGear(1, true);
        aircraft.resetControls();
      }
      return;
    }

    if (input.throttleUp) this.throttle = Math.min(1, this.throttle + dt * 0.45);
    if (input.throttleDown) this.throttle = Math.max(0, this.throttle - dt * 0.55);
    if (input.gearToggle) {
      this.gearDown = !this.gearDown;
      input.gearToggle = false;
    }
    input.resetRequest = false;

    const speed = this.speed;

    if (this.onGround) {
      this.updateGround(dt, input, speed);
    } else {
      this.updateAir(dt, input, speed);
    }

    this.integrate(dt);
  }

  updateGround(dt, input, speed) {
    const steer = STEER_MAX * (1 - Math.min(speed / 45, 1) * 0.85);
    this.heading -= input.roll * steer * dt * Math.min(speed / 3, 1);

    let pitchTarget = 0;
    if (speed > VR && input.pitch > 0.15) {
      pitchTarget = Math.min(input.pitch * 0.35, THREE.MathUtils.degToRad(14));
    }
    this.pitchAngle += (pitchTarget - this.pitchAngle) * (1 - Math.exp(-dt * 3));

    _e.set(-this.pitchAngle, this.heading, 0, "YXZ");
    this.quat.setFromEuler(_e);

    _fwd.set(0, 0, 1).applyQuaternion(this.quat);
    const thrust = this.throttle * MAX_THRUST_ACC;
    const drag = DRAG_K * speed * speed;
    const rolling = ROLL_FRICTION + (input.brake ? BRAKE_DEC : 0);
    let along = this.vel.dot(_fwd);
    along += (thrust - Math.sign(along) * drag) * dt;
    const dec = Math.min(Math.abs(along), rolling * dt);
    along -= Math.sign(along) * dec;
    this.vel.copy(_fwd).multiplyScalar(along);
    this.vel.y = Math.max(this.vel.y - G * dt, 0);

    if (this.pos.y > 0.05 || (speed > VR && this.pitchAngle > 0.03 && this.vel.y > 0.3)) {
      this.onGround = false;
    }
  }

  updateAir(dt, input, speed) {
    const eff = THREE.MathUtils.clamp((speed - 15) / 60, 0, 1);

    _q.setFromAxisAngle(new THREE.Vector3(1, 0, 0), -input.pitch * PITCH_RATE * eff * dt);
    this.quat.multiply(_q);
    _q.setFromAxisAngle(new THREE.Vector3(0, 0, 1), input.roll * ROLL_RATE * eff * dt);
    this.quat.multiply(_q);

    _right.set(-1, 0, 0).applyQuaternion(this.quat);
    const bank = Math.asin(THREE.MathUtils.clamp(-_right.y, -1, 1));
    if (Math.abs(bank) > 0.02 && speed > 30) {
      const turn = -(G / Math.max(speed, 55)) * Math.tan(THREE.MathUtils.clamp(bank, -1.2, 1.2)) * dt;
      _q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), turn);
      this.quat.premultiply(_q);
    }

    _fwd.set(0, 0, 1).applyQuaternion(this.quat);
    _up.set(0, 1, 0).applyQuaternion(this.quat);
    _right.set(-1, 0, 0).applyQuaternion(this.quat);

    _acc.set(0, -G, 0);
    _acc.addScaledVector(_fwd, this.throttle * MAX_THRUST_ACC);
    const lift = Math.min(LIFT_K * speed * speed, LIFT_CAP);
    _acc.addScaledVector(_up, lift);
    const dragK = DRAG_K + (this.gearDown ? GEAR_DRAG_K : 0);
    _acc.addScaledVector(this.vel, -dragK * speed);

    const lateral = this.vel.dot(_right);
    _acc.addScaledVector(_right, -lateral * 2.5);

    this.vel.addScaledVector(_acc, dt);

    const fwdSpeed = this.vel.dot(_fwd);
    _side.copy(this.vel).addScaledVector(_fwd, -fwdSpeed);
    this.vel.addScaledVector(_side, -Math.min(1, dt * 3.5));

    if (this.pos.y <= 0.05) {
      this.handleTouchdown();
    }
  }

  handleTouchdown() {
    const sink = -this.vel.y;
    _fwd.set(0, 0, 1).applyQuaternion(this.quat);
    const pitch = Math.asin(THREE.MathUtils.clamp(_fwd.y, -1, 1));
    const hardSink = !this.gearDown || sink > 7 || pitch < -0.12;
    if (hardSink) {
      this.crashed = true;
      return;
    }
    this.onGround = true;
    this.pos.y = 0;
    this.vel.y = 0;
    this.heading = Math.atan2(_fwd.x, _fwd.z);
    this.pitchAngle = Math.max(pitch, 0);
    _e.set(-this.pitchAngle, this.heading, 0, "YXZ");
    this.quat.setFromEuler(_e);
  }

  integrate(dt) {
    this.pos.addScaledVector(this.vel, dt);
    if (this.onGround) {
      if (this.pos.y < 0) {
        this.pos.y = 0;
        this.vel.y = Math.max(this.vel.y, 0);
      }
    }
    if (this.pos.y < -50) this.crashed = true;
  }
}
