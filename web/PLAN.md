# Web oyunu planı — Three.js

Hedef: en son Blender modelinin (v06) Three.js içinde oynanabilir ilk sürümü.
Kapsam: throttle (gaz), mouse ile pitch/roll kumandası, iniş takımı kontrolü, dümdüz pist.
Kamera: kokpit içi görüş (pilot göz noktası). Başlangıç: pist başında duran uçak.
Kurulum: Vite + Three.js (npm).

## 1. Model export hattı

- Betik: `scripts/export_gltf.py` (proje kökünde)
- Çalıştırma:
  ```sh
  blender -b output/model/f16c_block52_main_v06.blend --python scripts/export_gltf.py -- web/public/models/f16_v06.glb
  ```
- Yapacakları:
  - `90_PREVIEW_STUDIO`, kameralar ve ışıklar dışarıda bırakılır; uçak koleksiyonları (00–07) kalır.
  - FONT (etiket) nesneleri geçici kopyada mesh'e dönüştürülür; kokpit ayrıntısı korunsun.
  - glTF (.glb) export (Blender Y-up'a çevirir; burun +Z yönünde çıkar, kodda ona göre kullanılır).
  - Pilot göz noktası `CAM_Pilot_APPROX` konumundan okunup ayrı `f16_meta.json`'a yazılır (kokpit kamera konumu).

## 2. web/ projesi yapısı

```
web/
  package.json, vite.config.js, index.html
  public/models/f16_v06.glb
  src/
    main.js       başlatma, oyun döngüsü
    scene.js      gökyüzü, sis, ışıklar, zemin, pist
    aircraft.js   model yükleme, iniş takımı animasyonu, throttle/stick animasyonu
    physics.js    arkade uçuş fiziği + yerde taksi
    input.js      pointer-lock mouse + klavye
    hud.js        hız/irtifa/gaz/takım göstergesi (DOM overlay)
```

## 3. Pist ve dünya

- 3000 m düz pist (gri asfalt, beyaz eik çizgileri CanvasTexture ile), geniş yeşil zemin düzlemi,
  sisli sade gökyüzü. Hepsi prosedürel, ekstra model yok.

## 4. Kontroller

- Mouse (pointer lock): yatış/yunuslama — fare yönü hedef pitch/roll oranını belirler.
- W/S: throttle sürekli aç/kapa (kokpitte `Throttle_grip` nesnesi de hareket eder).
- G: iniş takımı aç/kapa — strut+tekerlek pivotları döner, kapaklar hareket eder;
  iniş takımı açıkken sürükleme artar.
- Yerdeyken mouse yunuslama + direksiyon ile taksi; hız düşük ve takım açıksa yere oturma.

## 5. Fizik (arkade düzeyi)

- Pozisyon/hız/kuaterniyon tabanlı basit model: itki (throttle), hıza bağlı kaldırma,
  yerçekimi, sürtünme, iniş takımı yer sürtünmesi.
- Uçak pist başında durarak başlar.

## 6. Doğrulama ve kayıt

- `npm install && npm run build` derleme kontrolü; `npm run dev` ile açılış.
- Sonra `research/DURUM.md`, `PLAN.md` ve `research/TODO.md` güncellenir.
