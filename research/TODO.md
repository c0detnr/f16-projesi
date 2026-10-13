# Tamamlanması gereken F-16 araştırmaları

13 Ekim 2026 — Referans bulma paketi tamamlandı; teknik doğrulama işleri ayrı izlenir. İşaretlenmemiş maddeler açık kalır.

## Tamamlanan referans toplama teslimatı

- [x] Yerel belge/fotoğraf seti, kaynak ve kullanım kataloğu oluştur: [REFERANSLAR.md](REFERANSLAR.md), [manifest.json](references/manifest.json).
- [x] Block 52 dış görünüş fotoğrafları, genel üç görünüşler, hava alığı karşılaştırması, kokpit, Türk boyama ve VTOL VR stil kaynaklarını bul ve incelenen bölümleri kaydet. Bu madde kesin ölçüleri veya tüm varyant ayrıntılarını doğrulamış sayılmaz.


## Modellemeye başlamadan önce

- [ ] Standart tek koltuklu F-16C Block 52 için tutarlı bir dış görünüm ve aviyonik referans konfigürasyonu seç; farklı blok ve modernizasyonlardan ayrıntıları karıştırma.
- [ ] Block 52’ye doğrudan bağlı ölçülü üst, yan ve ön görünüşü doğrula. Genel ölçü işaretli NASA CR-4182 çizimi ve koşulları bulundu; 1979 konfigürasyonu hedef bloğu doğrulamıyor.
- [ ] Gerçek uzunluk, kanat açıklığı ve yükseklik uyuşmazlıklarını çöz. Pitot, kanat ucu rayı ve iniş takımı konumuna göre ölçüm uçlarını tanımla; `PLAN.md` içindeki geçici ölçüleri doğrulanmış değerlerle güncelle.
- [ ] Block 52 hava alığı, F100-PW-229 nozulu, kanopi, antenler, iniş takımı ve kapakları için doğru varyanta ait fotoğraf/çizim seti oluştur.
- [ ] Kokpit genişliği, panel konumları, koltuk yerleşimi/eğimi, pilot göz noktası, HUD ve kumanda erişimini gerçek ölçeğe bağlayan kaynakları bul. Fotoğraftan tahmin edilen ölçüleri açıkça işaretle.

## Kokpit ve düğme listesi

- [x] Resmî DCS F-16C kılavuzunu indir; 16 Ağustos 2026 kapak sürümü ve gerçekten incelenen sayfaları REFERANSLAR.md içinde kaydet.
- [ ] Referansın Block 50/52 farklarını ve hedef kokpit konfigürasyonuna uygunluğunu değerlendir.
- [ ] Temel cold start checklist'ini çıkar; gereken her kontrolün modelde bulunduğunu doğrula. Normal başlatma ile bakım/test ve acil durum işlemlerini belirgin biçimde etiketle.
- [ ] Ana güç, yakıt kumandaları, EPU, JFS, throttle OFF/IDLE geçişi, oksijen, kanopi kilidi, aviyonik güç ve INS kontrollerinin gerçek adlarını, kademelerini ve panel konumlarını doğrula.
- [ ] Her fiziksel kumanda için ad, panel, konum, kumanda türü, kademeler, başlangıç konumu, hareket ekseni ve sonraki oyun işlevini içeren nihai düğme haritasını oluştur.
- [ ] HUD, MFD, DED/ICP, uçuş ve motor göstergeleri ile uyarı lambalarının fiziksel yerleşimini ve görünümünü doğrula.
- [ ] Sık kullanılan uçuş kontrollerini doğrula: iniş takımı, hava freni, trim, ışıklar, fren/pedallar ve burun tekeri yönlendirmesi. F-16'da bulunmayan genel uçak kumandalarını yanlışlıkla ekleme.

## Hareketli parçalar ve malzemeler

- [ ] Kontrol yüzeylerini, menteşe/pivot yerlerini ve hareket aralıklarını doğrula; aileron/flaperon ve stabilizatör hareketlerini doğru isimlendir.
- [ ] Kanopi, iniş takımı/kapakları, tekerlekler ve nozul hareketleri için mekanizma referanslarını topla.
- [ ] Türk gri boyaması, işaret yerleşimi, panel yazıları ve gövde stencil referanslarını topla. Tarihsel bir Türk Block 52 iddiası oluşturmayan kurgusal kimlik kullan.
- [x] Resmî VTOL VR ekran görüntülerini incele; sade hacimler, yüzey ayrıntıları ve kokpit okunurluğu için görsel örnekleri REFERANSLAR.md içinde kaydet. Poligon/performans ölçümü yapılmadı.

## Sonraki oyun aşamasından önce

- [ ] Kullanıcıyla oyun motoru ve export biçimini seç; malzeme, animasyon ve parça aktarımını hedef motor üzerinde doğrula.
- [ ] Temel cold start durumlarını ve güç/yakıt/motor/INS bağımlılıklarını kaynaklara göre belirle.
- [ ] HUD ve MFD'nin ilk sürüm sayfalarını, uçuş verilerini, motor göstergelerini ve uyarı davranışlarını tanımla.
- [ ] Uçuş fiziği kapsamını ve masaüstü giriş eşlemelerini belirle; hedef donanım bilgisiyle geometri/malzeme performans bütçesini oluştur.
- [ ] Afterburner ve nozulun motor durumuyla ilişkisini, ışık ve görsel efekt referanslarını doğrula.

## Referans paketinden sonra kalan somut boşluklar

- [ ] PW229 nozulunun doğrulanmış yakın arka görünüşünü ve ölçülerini bul; test sehpası yan fotoğrafı yeterli değil.
- [ ] 169th FW dış görünüş setinin aviyonik dönemi ile kokpit yardımcı kaynağının farklarını eşleştir; tek bir fotoğraf seti tüm panel konfigürasyonunu doğrulamaz.
- [ ] Türk boya standardını ve üst/alt işaret-stencil kapsamını doğrula; fotoğraf ışığından kesin renk üretme.

Kullanıcı bu oturumda yalnızca referans bulmayı istedi. Model, nihai düğme haritası, checklist ve oyun aşaması başlatılmadı.
