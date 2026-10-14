// Prosedürel F-16 (F100-PW-229 tarzı) turbofan sesi — Web Audio, örnek dosya yok
// Katmanlar: türbin çınlaması, çekirdek gurlemesi, jet uğultusu, yüksek güç
// çıtırtısı, rüzgâr, pist yuvarlanması, iniş/kaza vuruşları.

function makeNoiseBuffer(ctx, seconds, brown) {
  const len = Math.floor(seconds * ctx.sampleRate);
  const buf = ctx.createBuffer(1, len, ctx.sampleRate);
  const d = buf.getChannelData(0);
  if (!brown) {
    for (let i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
  } else {
    let last = 0;
    for (let i = 0; i < len; i++) {
      const w = Math.random() * 2 - 1;
      last = (last + 0.02 * w) / 1.02;
      d[i] = last * 3.5;
    }
  }
  return buf;
}

function loopSource(ctx, buffer) {
  const s = ctx.createBufferSource();
  s.buffer = buffer;
  s.loop = true;
  s.start();
  return s;
}

function softClipCurve(k = 6) {
  const n = 256;
  const c = new Float32Array(n);
  for (let i = 0; i < n; i++) {
    const x = (i / (n - 1)) * 2 - 1;
    c[i] = Math.tanh(k * x) / Math.tanh(k);
  }
  return c;
}

function clamp(v, a, b) {
  return Math.min(b, Math.max(a, v));
}

const MASTER_GAIN = 0.9;
const IDLE_RPM = 0.18;
const SPOOL_UP = 1.7;
const SPOOL_DOWN = 2.3;

export class EngineSound {
  constructor() {
    this.ctx = null;
    this.ready = false;
    this.muted = false;
    this.rpm = 0;
    this._t = 0;
    this._crackIn = 0;
    document.addEventListener("keydown", (e) => {
      if (e.code === "KeyM") this.toggleMute();
    });
  }

  init() {
    if (this.ready) {
      if (this.ctx.state === "suspended") this.ctx.resume();
      return;
    }
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    this.ctx = ctx;

    this.brownBuf = makeNoiseBuffer(ctx, 4, true);
    this.whiteBuf = makeNoiseBuffer(ctx, 3, false);

    const master = ctx.createGain();
    master.gain.value = this.muted ? 0 : MASTER_GAIN;
    const comp = ctx.createDynamicsCompressor();
    comp.threshold.value = -18;
    comp.ratio.value = 6;
    master.connect(comp);
    comp.connect(ctx.destination);
    this.master = master;

    // Kokpit içi boğukluk: her şey bu alçak geçiren süzgeçten geçer
    const canopy = ctx.createBiquadFilter();
    canopy.type = "lowpass";
    canopy.frequency.value = 4500;
    canopy.connect(master);

    const white = loopSource(ctx, this.whiteBuf);
    const brown = loopSource(ctx, this.brownBuf);

    // 1) Türbin çınlaması: testere dişli iki osilatör + dar bant geçiren
    const whineBP = ctx.createBiquadFilter();
    whineBP.type = "bandpass";
    whineBP.Q.value = 6;
    const osc1 = ctx.createOscillator();
    osc1.type = "sawtooth";
    const osc1G = ctx.createGain();
    osc1G.gain.value = 1;
    const osc2 = ctx.createOscillator();
    osc2.type = "sawtooth";
    const osc2G = ctx.createGain();
    osc2G.gain.value = 0.4;
    const whineGain = ctx.createGain();
    whineGain.gain.value = 0;
    osc1.connect(osc1G);
    osc1G.connect(whineBP);
    osc2.connect(osc2G);
    osc2G.connect(whineBP);
    whineBP.connect(whineGain);
    whineGain.connect(canopy);
    osc1.start();
    osc2.start();

    // 2) Çekirdek gurlemesi: kahverengi gürültü + alçak geçiren
    const rumbleLP = ctx.createBiquadFilter();
    rumbleLP.type = "lowpass";
    const rumbleGain = ctx.createGain();
    rumbleGain.gain.value = 0;
    brown.connect(rumbleLP);
    rumbleLP.connect(rumbleGain);
    rumbleGain.connect(canopy);

    // 3) Jet uğultusu: beyaz gürültü + bant geçiren + yumuşak kırpma
    const roarBP = ctx.createBiquadFilter();
    roarBP.type = "bandpass";
    roarBP.Q.value = 0.7;
    const shaper = ctx.createWaveShaper();
    shaper.curve = softClipCurve();
    const roarGain = ctx.createGain();
    roarGain.gain.value = 0;
    white.connect(roarBP);
    roarBP.connect(shaper);
    shaper.connect(roarGain);
    roarGain.connect(canopy);

    // 4) Yüksek güç / art yakıcı çıtırtısı
    const abLP = ctx.createBiquadFilter();
    abLP.type = "lowpass";
    abLP.frequency.value = 900;
    const abGain = ctx.createGain();
    abGain.gain.value = 0;
    white.connect(abLP);
    abLP.connect(abGain);
    abGain.connect(canopy);

    // 5) Rüzgâr (hızla artar)
    const windBP = ctx.createBiquadFilter();
    windBP.type = "bandpass";
    windBP.Q.value = 0.4;
    const windHP = ctx.createBiquadFilter();
    windHP.type = "highpass";
    windHP.frequency.value = 150;
    const windGain = ctx.createGain();
    windGain.gain.value = 0;
    white.connect(windBP);
    windBP.connect(windHP);
    windHP.connect(windGain);
    windGain.connect(master);

    // 6) Pist yuvarlanma sesi
    const groundLP = ctx.createBiquadFilter();
    groundLP.type = "lowpass";
    groundLP.frequency.value = 110;
    const groundGain = ctx.createGain();
    groundGain.gain.value = 0;
    brown.connect(groundLP);
    groundLP.connect(groundGain);
    groundGain.connect(master);

    this.osc1 = osc1;
    this.osc2 = osc2;
    this.whineBP = whineBP;
    this.whineGain = whineGain;
    this.rumbleLP = rumbleLP;
    this.rumbleGain = rumbleGain;
    this.roarBP = roarBP;
    this.roarGain = roarGain;
    this.abGain = abGain;
    this.windBP = windBP;
    this.windGain = windGain;
    this.groundGain = groundGain;

    this.ready = true;
    if (ctx.state === "suspended") ctx.resume();
  }

  toggleMute() {
    if (!this.ready) return;
    this.muted = !this.muted;
    this.master.gain.setTargetAtTime(
      this.muted ? 0 : MASTER_GAIN,
      this.ctx.currentTime,
      0.05
    );
  }

  // s: { throttle, speed, onGround, crashed }
  update(dt, s) {
    if (!this.ready) return;
    this._t += dt;

    // Motor gaz kolu gecikmesiyle döner (spool)
    const target = s.crashed ? 0 : Math.max(IDLE_RPM, s.throttle);
    const tau = target > this.rpm ? SPOOL_UP : SPOOL_DOWN;
    this.rpm += (target - this.rpm) * (1 - Math.exp(-dt / tau));
    const rpm = this.rpm;

    const j = 1 + 0.015 * Math.sin(this._t * 11.3) + 0.01 * Math.sin(this._t * 29.7);
    const f = (280 + rpm * 2500) * j;
    const now = this.ctx.currentTime;
    const set = (p, v, tc = 0.06) => p.setTargetAtTime(v, now, tc);

    set(this.osc1.frequency, f, 0.08);
    set(this.osc2.frequency, f * 2.02, 0.08);
    set(this.whineBP.frequency, f * 1.5, 0.08);
    set(this.rumbleLP.frequency, 70 + rpm * 320, 0.1);
    set(this.roarBP.frequency, (240 + rpm * 1150) * j, 0.1);
    set(this.windBP.frequency, 350 + s.speed * 7, 0.15);

    set(this.whineGain.gain, 0.02 * rpm + 0.025 * rpm * rpm);
    set(this.rumbleGain.gain, 0.55 * Math.pow(rpm, 1.6));
    set(this.roarGain.gain, 0.7 * Math.pow(rpm, 2.4));

    const windL = clamp((s.speed - 25) / 260, 0, 1);
    set(this.windGain.gain, 0.4 * windL * windL, 0.15);

    const gL = s.onGround && !s.crashed ? clamp(s.speed / 45, 0, 1) : 0;
    set(this.groundGain.gain, 0.55 * gL * gL, 0.12);

    // Gaz %82 üstünde çıtırtı (mil gücü / AB hissi)
    const abl = clamp((s.throttle - 0.82) / 0.18, 0, 1);
    if (abl > 0 && !s.crashed) {
      this._crackIn -= dt;
      if (this._crackIn <= 0) {
        this._crackIn = 0.02 + Math.random() * 0.14;
        const spike = 0.25 + Math.random() * 0.55;
        const gp = this.abGain.gain;
        gp.cancelScheduledValues(now);
        gp.setValueAtTime(gp.value, now);
        gp.linearRampToValueAtTime(spike * abl, now + 0.012);
        gp.setTargetAtTime(0.15 * abl, now + 0.012, 0.05);
      }
    } else {
      set(this.abGain.gain, 0, 0.1);
    }
  }

  touchdown(sink) {
    if (!this.ready) return;
    const ctx = this.ctx;
    const now = ctx.currentTime;
    const amp = 0.25 + 0.6 * clamp(sink / 8, 0, 1);
    const src = ctx.createBufferSource();
    src.buffer = this.brownBuf;
    const lp = ctx.createBiquadFilter();
    lp.type = "lowpass";
    lp.frequency.value = 180;
    const g = ctx.createGain();
    g.gain.setValueAtTime(amp, now);
    g.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
    src.connect(lp);
    lp.connect(g);
    g.connect(this.master);
    src.start(now);
    src.stop(now + 0.4);
  }

  crash() {
    if (!this.ready) return;
    const ctx = this.ctx;
    const now = ctx.currentTime;
    const src = ctx.createBufferSource();
    src.buffer = this.brownBuf;
    const lp = ctx.createBiquadFilter();
    lp.type = "lowpass";
    lp.frequency.value = 500;
    const g = ctx.createGain();
    g.gain.setValueAtTime(0.9, now);
    g.gain.exponentialRampToValueAtTime(0.001, now + 1.6);
    src.connect(lp);
    lp.connect(g);
    g.connect(this.master);
    src.start(now);
    src.stop(now + 1.7);

    const src2 = ctx.createBufferSource();
    src2.buffer = this.whiteBuf;
    const bp = ctx.createBiquadFilter();
    bp.type = "bandpass";
    bp.frequency.value = 900;
    bp.Q.value = 2;
    const g2 = ctx.createGain();
    g2.gain.setValueAtTime(0.4, now);
    g2.gain.exponentialRampToValueAtTime(0.001, now + 0.6);
    src2.connect(bp);
    bp.connect(g2);
    g2.connect(this.master);
    src2.start(now);
    src2.stop(now + 0.7);
  }
}
