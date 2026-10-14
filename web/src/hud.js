import * as THREE from "three";

export class Hud {
  constructor(overlay) {
    this.hud = document.getElementById("hud");
    this.throttleFill = document.getElementById("throttle-fill");
    this.overlay = overlay;
    this.overlayTitle = overlay.querySelector("h1");
    this.overlayBody = overlay.querySelectorAll("p");
    this._crashShown = false;
  }

  update(physics, aircraft, locked) {
    if (physics.crashed) {
      if (!this._crashShown) {
        this._crashShown = true;
        this.overlayTitle.textContent = "Çakıldın";
        this.overlayBody[0].textContent = "Yeniden başlamak için R tuşuna bas";
        this.overlayBody[1].textContent = "";
        this.overlay.classList.remove("hidden");
      }
      return;
    }
    if (this._crashShown) {
      this._crashShown = false;
      this.overlayTitle.textContent = "F-16C Block 52 — İlk Uçuş";
      this.overlayBody[0].textContent = "Tıkla ve uçuşa başla (fare kilitlenir, ESC ile çıkar)";
      this.overlayBody[1].textContent = "Fare: yatış / yunuslama  |  W/S: gaz  |  G: iniş takımı";
    }

    const speed = physics.speed;
    const alt = physics.pos.y;
    const thr = Math.round(physics.throttle * 100);
    const gear = physics.gearDown ? "ACIK" : "KAPALI";
    const phase = physics.onGround ? "YERDE" : "HAVADA";
    _fwd.set(0, 0, 1).applyQuaternion(physics.quat);
    const hdg = ((THREE.MathUtils.radToDeg(Math.atan2(_fwd.x, _fwd.z)) + 360) % 360).toFixed(0).padStart(3, "0");

    this.hud.textContent =
      `HIZ ${Math.round(speed * 3.6)} km/s  YÜK ${alt.toFixed(0)} m  YÖN ${hdg}°\n` +
      `GAZ %${thr}  INIS TAKIMI ${gear}  ${phase}` +
      (aircraft.gearMoving ? "\nTAKIM HAREKET EDIYOR" : "");
    this.throttleFill.style.height = `${thr}%`;
  }

  show() {
    this.hud.classList.remove("hidden");
    document.getElementById("throttle-gauge").classList.remove("hidden");
  }
}

const _fwd = new THREE.Vector3();
