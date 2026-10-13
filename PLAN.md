# F-16C Block 52 Blender modeli

Plan tarihi: 13 Ekim 2026
Çalışma klasörü: `/home/mami/Projects/bl`

## Hedef ve ilk teslimat

Blender ile sıfırdan, gerçek ölçekte, VTOL VR tarzında sade grafiklere sahip bir F-16C Block 52 modeli oluşturulacak. Kullanıcı 13 Ekim 2026'da fotogerçekçi konsepti reddetti; öncelik Intel Iris Xe GPU ile rahat oynanabilecek düşük poligonlu geometri, düz renkler, az doku ve basit aydınlatma. Gerçekçilik uçak oranları, kokpit yerleşimi ve kumanda işlevlerinde aranacak. Kokpitin önemli kumandaları okunabilir ve ayrı nesneler olacak; yüzey ayrıntıları sade tutulacak.

İlk teslimat düzenlenebilir `.blend` dosyası, modeli yeniden kuran Blender betiği, kokpit düğme konum/işlev haritası ve dış görünüm ile pilot bakışından önizlemeler olacak. Oyun motoru seçimi ve export sonraki aşamada yapılacak. Önerilen Codex modeli GPT-6 Astra Medium; bu seçim Blender çıktısı için ölçülmüş bir kalite garantisi değildir.

## Kullanıcı tarafından kabul edilen tercihler

- Varyant: tek koltuklu, standart F-16C Block 52; Block 52+ veya çift koltuklu F-16D değil.
- Boyutlar: gerçek ölçek; Blender'da 1 birim = 1 metre.
- Görsel stil: VTOL VR tarzında sade, düşük poligonlu geometri; düz renkli mat malzemeler, az doku, basit aydınlatma ve okunaklı kokpit. Gerçekçi aşınma, yoğun küçük geometri ve pahalı görsel efektler görsel hedefe dahil değil.
- Kullanıcının onayladığı görsel stil referansı: [pilot bakışı v2](output/concepts/f16c-pilot-view-v2.png). Modelleme bu görseldeki sadeliği hedefleyecek; görseldeki panel konumları ve gösterge içerikleri teknik referans olarak kabul edilmeyecek.
- Hedef GPU: Intel Iris Xe; rahat oynanabilirlik öncelikli. Kesin GPU varyantı, çözünürlük ve FPS hedefi henüz belirlenmedi. Geometri, çizim çağrısı, ekran güncelleme, gölge ve efekt bütçeleri oyun aşamasında gerçek donanım üzerinde ölçülerek belirlenecek; konsept görsel performans kanıtı değildir.
- Boyama: Türk Hava Kuvvetleri görünümü. Block 52 ile Türk işaretlerinin birleşimi kullanıcıya özel kurgu olarak kabul edildi; tarihsel bir Türk Block 52'nin kopyası olmayacak.
- Dış yükler: boş istasyonlar ve ayrı pilonlar; ilk modelde silah veya harici yakıt tankı bulunmayacak.
- Sonraki oyun aşaması: masaüstü kullanım öncelikli.
- İlk oynanabilir sürüm: tam temel cold start sırası ve uçuş odaklı işlevler.
- Oyun motoru ve export biçimi henüz seçilmedi; kullanıcı bunları sonraya bıraktı.

## Uygulama sırası ve güncel çalışma sınırı

13 Ekim 2026 ilk talimatı yalnızca referans toplamaktı; yeni talimat: 2. aşama olan ana modeli Blender’da kur ve görülebilir 3D sonuç teslim et.

1. Referans bulma: kaynakları topla, erişilebilir belge/görselleri yerelde sakla, inceleme ve kullanım sınırlarını kaydet. Teslimat: [research/REFERANSLAR.md](research/REFERANSLAR.md).
2. Modelleme öncesi açık teknik doğrulamaları çöz: kesin ölçü tanımları, kokpit ölçeği, Block 52 panel/nozul uyumu.
3. Blender gövde/kokpit ana hacimleri, ayrıntılar ve kabul kontrolleri.
4. Sonraki oyun/export aşaması.

Yeni talimat Blender ana modelini oluşturmayı yetkilendirir. Kesin ölçü ve kokpit kaynakları beklenirken ilk ana model, açıkça geçici ölçek ve fotoğraf yorumlarıyla kurulacak; araştırma boşlukları kapanmış sayılmayacak. 169th Fighter Wing 2018 Block 52 fotoğrafları dış görünüşün ana araştırma seti; DCS Block 50/2007 kokpiti yardımcı kaynaktır. Bu kaynak seçimi, tarihsel bir Türk Block 52 veya tamamen doğrulanmış bir aviyonik konfigürasyon iddiası değildir. Geçici ölçüler kesinleştirilmedi.

## Gövde ve hareketli parçalar

Genel F-16C referansındaki orijinal fit/inç değerlerinin dönüşümü yaklaşık 15,06 m uzunluk, 9,96 m kanat açıklığı ve 4,88 m yükseklik verir. Bunlar ilk ölçek referansıdır. Block 52'ye özgü boyutlar, ölçüm uçları ve iniş takımı durumunun etkisi modelleme öncesinde doğrulanacak; araştırma notlarındaki metrik tutarsızlık sessizce göz ardı edilmeyecek.

Block 52'ye uygun Pratt & Whitney F100-PW-229 motor görünümü, hava alığı, tek koltuklu kanopi, kokpit, iniş takımı, kanatlar ve kuyruk kurulacak. Siluete ve oranlara öncelik verilecek; küçük yüzey ayrıntıları geometri, malzeme veya etiketlerle ekonomik biçimde aktarılacak.

Kanopi, iniş takımı ve kapakları, tekerlekler, yatay stabilizatörler, aileronlar/flaperonlar, ön kenar flapları, dümen, hava frenleri, motor nozulu, gaz kolu ve joystick ayrı parçalar olarak hazırlanacak. Her parçanın hareket ekseni ve pivotu gerçek mekanizmaya göre yerleştirilecek. Afterburner için sonraki oyun aşamasında kullanılabilecek bağlantı noktası hazırlanacak.

## Kokpit düğme planı

Gerçek kokpit yerleşimi korunacak; sık kullanılan kumandalar ve temel cold start için gereken kontroller ayrı, hareket ettirilebilir nesneler olacak. Az kullanılan paneller görsel ayrıntı olarak kalabilecek. Panel etiketleri gerçek uçaktaki İngilizce adları kullanacak.

| Grup | Modellenmesi planlanan kontroller ve göstergeler |
| --- | --- |
| Güç ve motor | Ana güç, yakıt kumandaları, EPU, JFS, gaz kolu ve OFF/IDLE geçişi; RPM, sıcaklık ve motor durum göstergeleri |
| Cold start ve hazırlık | Oksijen, kanopi açma/kapama ve kilit, aviyonik güç paneli, INS kumandası ve hizalama göstergesi |
| Aviyonik ve gösterim | HUD ve parlaklık kumandası, iki MFD ve çerçeve tuşları, DED/ICP, temel uçuş ve yakıt göstergeleri |
| Uçuş ve yer hareketi | Joystick, gaz kolu, pedallar, iniş takımı kumandası, hava freni, trim, burun tekeri yönlendirme kumandası ve ilgili durum ışıkları |
| Aydınlatma | Kokpit, dış aydınlatma ve iniş/taksi ışığı kumandaları |

Bu tablo işlev kapsamını belirler; eksiksiz ve doğrulanmış bir Block 52 checklist'i değildir. Nihai düğme listesinde her kontrolün gerçek adı, paneli, konumu, türü, kademeleri, başlangıç durumu ve planlanan işlevi bulunacak. Cold start için gereken tüm temel kontrollerin kapsandığı kaynaklarla doğrulanacak.

## Sonraki oyun aşaması

Kokpite girilebilecek ve fare/klavye ile kumandalar kullanılabilecek. Güç, yakıt, JFS, motor, aviyonik, INS ve kanopi işlemleri göstergelere bağlı bir temel cold start sırası oluşturacak. İlk sürüm uçuşa odaklanacak: çalışan HUD, temel MFD sayfaları, uçuş/motor göstergeleri, iniş takımı, fren, trim, ışıklar, hareketli kontrol yüzeyleri ve afterburner.

Blender modeli bu işlevler için ayrı ve tutarlı biçimde adlandırılmış nesnelerle hazırlanacak. Simülasyon mantığı, uçuş fiziği ve çalışan ekranlar sonraki oyun aşamasının teslimatıdır.

## Doğrulama ve kabul ölçütleri

- Model gerçek ölçekte olacak; uzunluk, kanat açıklığı ve yükseklik doğrulanmış referansla karşılaştırılacak.
- Ön, yan ve üst ortografik görünümlerde gövde oranları, kanopi, hava alığı, kanat ve kuyruk biçimleri incelenecek.
- Hareketli parçaların pivotları ve hareketleri Blender'da kontrol edilecek; belirgin kesişmeler düzeltilecek.
- Pilot bakışından HUD/MFD görüşü, düğmelere erişim ve etiket okunurluğu kontrol edilecek.
- Dış görünüm ve kokpit renderları incelenip siluet, yüzey, malzeme ve yerleşim hataları düzeltilecek.
- `.blend` dosyası yeniden açılacak; teslimatta gereken kaynaklar ve malzemeler eksiksiz olacak.

Araştırma kayıtları: [research/ARASTIRMA.md](research/ARASTIRMA.md)
Eksik araştırmalar: [research/TODO.md](research/TODO.md)
Proje özeti ve yeni sohbet başlangıcı: [research/README.md](research/README.md)
Güncel ilerleme: [research/DURUM.md](research/DURUM.md)
