# Güncel proje durumu

Son güncelleme: 13 Ekim 2026

## Tamamlanan işler

- Kullanıcı `output/concepts/f16c-pilot-view-v2.png` görselinin sade VTOL VR tarzını beğenip onayladı; kabul edilen stil referansı olarak `PLAN.md` içine kaydedildi. Bu onay kokpitin teknik doğruluğu veya GPU performansının doğrulanması anlamına gelmez.

- Kullanıcı tercihleri ve ilk Blender teslimatının kapsamı belirlendi; `PLAN.md` oluşturuldu.
- F-16 motor/varyant, Türk boyaması ve genel ölçüler üzerine ilk kaynak taraması kaydedildi.
- Araştırma eksikleri `research/TODO.md` içinde toplandı.
- Araştırma klasörü `research` olarak güncellendi; plan bağlantıları düzeltildi.
- Sohbetler arası devam için proje özeti ve kök `AGENTS.md` yönlendirmesi oluşturuldu.
- Plan temel alınarak imagegen ile pilot gözünden bir görsel konsept üretildi: `output/concepts/f16c-pilot-view-v1.png`. Görsel, açık ekranlarla sonraki oyun aşamasının görünümünü tasvir eder; Blender renderı veya tamamlanmış model değildir. Görselde iki MFD, HUD ve yan kumandalar bulunması kontrol edildi; panel yerleşimleri, yazılar, gösterge değerleri ve ölçüler teknik olarak doğrulanmadı ve modelleme referansı kabul edilmemelidir. Üretim istemi: `output/concepts/f16c-pilot-view-v1-prompt.txt`.

## Henüz tamamlanmayan işler

Görsel hedef düzeltmesi: kullanıcı ilk konsepti fazla gerçekçi buldu. VTOL VR tarzında daha sade grafikler ve Intel Iris Xe üzerinde rahat oynanabilirlik hedefi plana işlendi. Yeni imagegen konsepti: `output/concepts/f16c-pilot-view-v2.png`; istemi: `output/concepts/f16c-pilot-view-v2-prompt.txt`. Düz renkler, sade geometri ve azaltılmış yüzey ayrıntıları görsel olarak incelendi. Bu görsel bir Blender modeli, doğrulanmış kokpit haritası veya GPU performans ölçümü değildir.

- Blender modeli, üretim betiği, render veya oyun kodu henüz oluşturulmadı.
- Nihai düğme listesi ve eksiksiz temel cold start checklist'i henüz doğrulanmadı.
- Block 52'ye özgü ölçülü referans seti ve kokpit ölçüleri henüz hazırlanmadı.
- Genel boyut kaynaklarının çelişen metrik değerleri ve farklı yükseklikleri henüz çözülemedi.
- Resmi DCS kılavuzunun tam PDF'i indirilemedi; önceki bağlantılar 403/404 hataları verdi. Arama sonuçları tam belge incelemesi sayılmıyor.
- Oyun motoru, export biçimi, kesin Iris Xe varyantı, çözünürlük ve FPS hedefleri seçilmedi; genel donanım hedefi Intel Iris Xe olarak belirlendi.

## Sonraki modelleme adımı

Önce `research/TODO.md` içindeki modelleme öncesi araştırmaları tamamla: hedef Block 52 konfigürasyonu, ölçülü görünüşler, dış boyutlar, motor/hava alığı ayrımı ve kokpit yerleşimi. Doğrulanan bilgileri kaynaklarıyla kaydet. Ardından gerçek ölçekli gövde ve kokpit ana hacimlerini kurup ortografik görüntüler ve pilot bakışıyla değerlendir; ayrıntıları bunun üzerine ekle.

## Ortam kaydı

13 Ekim 2026'da `/home/mami/Projects/bl` içinde Blender 5.2.1 LTS kullanılabilir bulundu. Godot ve Git çalıştırılabilir dosyaları mevcut; klasör henüz Git deposu değil. Bunlar sonraki sohbetlerde yeniden kontrol edilebilecek ortam gözlemleridir.

## Güncelleme biçimi

Bu dosya çalışma ilerledikçe güncel durumu göstermeli. Üretilen dosyaların yollarını, gerçekten yapılan görsel/teknik doğrulamaları, kalan somut sorunları ve sıradaki adımı yaz. Bir işin yalnızca planlanmış olması onu tamamlanan işler bölümüne taşımak için yeterli değildir.
