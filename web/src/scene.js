import * as THREE from "three";

const SKY = 0x9ec8e8;
const FOG_NEAR = 2000;
const FOG_FAR = 22000;

export function createRenderer() {
  const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
  document.getElementById("app").appendChild(renderer.domElement);
  window.addEventListener("resize", () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
  });
  return renderer;
}

export function createScene() {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(SKY);
  scene.fog = new THREE.Fog(SKY, FOG_NEAR, FOG_FAR);

  const hemi = new THREE.HemisphereLight(0xdfeaff, 0x50603f, 0.9);
  scene.add(hemi);
  const sun = new THREE.DirectionalLight(0xffffff, 1.6);
  sun.position.set(-600, 900, -400);
  scene.add(sun);

  scene.add(createGround());
  scene.add(createRunway());
  return scene;
}

function createGround() {
  const geo = new THREE.PlaneGeometry(40000, 40000);
  const mat = new THREE.MeshLambertMaterial({ color: 0x57713a });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.rotation.x = -Math.PI / 2;
  mesh.position.y = -0.05;
  return mesh;
}

function createRunwayTexture() {
  const c = document.createElement("canvas");
  c.width = 256;
  c.height = 4096;
  const g = c.getContext("2d");
  g.fillStyle = "#3c3f42";
  g.fillRect(0, 0, 256, 4096);
  for (let i = 0; i < 2600; i++) {
    const v = 52 + Math.random() * 14;
    g.fillStyle = `rgb(${v},${v + 1},${v + 2})`;
    g.fillRect(Math.random() * 256, Math.random() * 4096, 2 + Math.random() * 3, 2 + Math.random() * 3);
  }
  g.fillStyle = "#e8e8e8";
  for (let y = 180; y < 3900; y += 90) {
    g.fillRect(124, y, 8, 48);
  }
  for (let y = 20; y < 160; y += 22) {
    g.fillRect(20, y, 70, 10);
    g.fillRect(166, y, 70, 10);
  }
  for (let y = 3936; y < 4076; y += 22) {
    g.fillRect(20, y, 70, 10);
    g.fillRect(166, y, 70, 10);
  }
  g.fillRect(0, 0, 6, 4096);
  g.fillRect(250, 0, 6, 4096);
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  return tex;
}

function createRunway() {
  const geo = new THREE.PlaneGeometry(60, 3000);
  const mat = new THREE.MeshLambertMaterial({ map: createRunwayTexture() });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.rotation.x = -Math.PI / 2;
  mesh.position.set(0, 0, 1500);
  return mesh;
}
