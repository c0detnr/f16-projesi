import * as THREE from "three";
import { createRenderer, createScene } from "./scene.js";
import { Aircraft } from "./aircraft.js";
import { FlightPhysics } from "./physics.js";
import { Input } from "./input.js";
import { Hud } from "./hud.js";
import { CameraRig } from "./camera.js";
import { EngineSound } from "./sound.js";

const overlay = document.getElementById("overlay");
const renderer = createRenderer();
const scene = createScene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.05, 30000);
const rig = new CameraRig(camera);

const input = new Input(overlay);
const physics = new FlightPhysics();
const hud = new Hud(overlay);
const aircraft = new Aircraft();
const sound = new EngineSound();
document.addEventListener("pointerdown", () => sound.init());
document.addEventListener("keydown", () => sound.init());

async function start() {
  await aircraft.load("models/f16_v06.glb", "models/f16_v06_meta.json");

  const eye = aircraft.meta.pilot_eye;
  rig.setAircraft(aircraft.root, eye);

  scene.add(aircraft.root);
  hud.show();

  let wasGround = physics.onGround;
  let wasCrashed = physics.crashed;
  const clock = new THREE.Clock();
  renderer.setAnimationLoop(() => {
    const dt = Math.min(clock.getDelta(), 1 / 30);
    input.update(dt);
    if (input.cameraToggle) {
      input.cameraToggle = false;
      rig.toggle();
    }
    rig.update(dt);
    physics.update(dt, input, aircraft);
    aircraft.root.position.copy(physics.pos);
    aircraft.root.quaternion.copy(physics.quat);
    aircraft.update(dt, input, physics);
    if (!wasCrashed && physics.crashed) sound.crash();
    if (!wasGround && physics.onGround) sound.touchdown(-physics.vel.y);
    wasGround = physics.onGround;
    wasCrashed = physics.crashed;
    sound.update(dt, physics);
    hud.update(physics, aircraft, input.locked);
    renderer.render(scene, camera);
  });
}

start();
