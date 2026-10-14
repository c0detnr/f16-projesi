# F-16 referans toplama

## Goal
Yalnızca ilk aşama: kaynakları bul, erişilebilir belgeleri/görselleri sakla, inceleme ve eksiklerini kaydet. Modelleme ve oyun işleri kapsam dışı.

### Phase 1: Mevcut kapsamı oku
**Status:** complete

### Phase 2: Dış geometri, varyant, kokpit ve boyama kaynaklarını topla
**Status:** complete

### Phase 3: Kaynak kataloğunu ve proje kayıtlarını doğrula
**Status:** complete

## Next Step
Bu görev tamamlandı. Kullanıcının talimatına göre burada dur; yeni modelleme veya doğrulama aşaması başlatma.

## Errors Encountered
- git diff --stat: klasör Git deposu değil; dosya içeriği ve yerel çıktı denetimi kullanılacak.
- Python bs4 modülü yok; standart HTMLParser/re ve mevcut PDF komutları kullanılacak.
- Galeri temas sayfasında DejaVu fontu bulunamadı; görseller etiketsiz incelendi, font yolu Liberation Sans olarak belirlendi.
- HTTP hataları: nozzle_169fw/hill_block52/usaf_facts 403; indirilen alternatif birincil belgeler ve web okunabilir AFMC kaydı kullanıldı. Ayrıntılar download_log.json içinde.

## GitHub yayınlama — 13 Ekim 2026

Kullanıcı mevcut projeyi `f16-projesi` adlı herkese açık depoda yayınlamayı ve gerekli commitleri oluşturmayı istedi. Referans toplama aşamalarının mevcut durumları korunur.

### Phase 4: Yayına hazırlık
**Status:** complete

Proje kökü ve dosyalar incelendi; README ve .gitignore eklendi. GitHub API ile doğrulanan güncel hesap c0detnr; yerel gh oturum kaydı eski Emirix adını gösteriyordu. Dosya taramasında bilinen gizli anahtar biçimleri bulunmadı.

### Phase 5: Commit ve GitHub yayını
**Status:** complete

### Phase 6: Yayını doğrula
**Status:** complete

## Next Step
GitHub yayını tamamlandı; son belge güncellemelerini commit edip gönder.

## Yayınlama kontrolleri
- Başlangıçta Git deposu yoktu; proje kökünde main dalında başlatıldı.
- Eski Emirix kullanıcı adıyla depo oluşturma 404 verdi; gh api user ile güncel c0detnr hesabı doğrulandı ve public repo oluşturuldu.
- İlk whitespace denetimi indirilen HTML arşivlerinde boşluk uyarıları verdi; kaynak dosyalar olduğu gibi korundu. Proje Markdown dosyaları ayrıca denetlendi.

## Validation
6 PDF açılabilir; 15 seçilmiş JPG ve 7 PNG okunabilir. Manifest SHA-256 ve tüm yerel proje Markdown bağlantıları geçerli. Ayrıntı: research/references/DOGRULAMA.txt.


## Ana model — 13 Ekim 2026

Kullanıcı 2. aşamaya geçilmesini ve Blender'da gerçek 3D çıktı istedi. Önceki referans toplama durma sınırı bu yeni talimatla sona erdi.

### Phase 7: Model kapsamı ve yerel referans incelemesi
**Status:** complete
Mevcut blend yok. SCANG yan/üst, NASA genel üç görünüş ve DCS kokpit görselleri tekrar incelendi. Ölçülü Block 52 çizimi/kokpit ölçeği hâlâ açık; ana model geçici ölçek girdilerini açıkça kaydedecek.

### Phase 8: Düzenlenebilir Blender ana modeli ve üretim betiği
**Status:** complete

### Phase 9: Render, yeniden açma, geometri kontrolü ve teslim kayıtları
**Status:** complete

## Next Step
Ana model teslimatı tamamlandı. Kullanıcıyla siluet ve kokpit ana hacimlerini değerlendir; ardından ayrıntı ve teknik doğrulama aşamasına geç.


## Ana model doğrulama sonucu
v02 yeniden açma başarılı, 5.206 değerlendirilmiş üçgen, eksik dış dosya yok. Altı render görsel incelendi. Masaüstü Blender doğru v02 dosyasıyla açık. Ana model kapsamı tamamlandı; nihai kokpit/mekanizma/kesin ölçü ve oyun aşaması açık.

## Ek işlem kaydı
- Blender 5.2 API `use_nodes` kullanımı için gelecekteki kaldırma uyarısı verdi; mevcut sürümde üretim başarılı.
- İlk nohup başlatma kalıcı pencere oluşturmadı; PTY süreciyle yeniden açıldı ve pencere başlığı doğrulandı.
- v02 üretim oturumunun araç dönüş kodu 143 gösterdi; Blender günlüğü dosya, altı render ve normal “Blender quit” kaydını içeriyor. Teslim blend bağımsız yeniden açma kontrolünden geçti.

- PNG paket kontrolünde Pillow yoktu; standart Python PNG imza/CRC/zlib denetimiyle 6 dosya doğrulandı. Teslim bağlantıları geçerli.

## Dış model düzeltme — 13 Ekim 2026

Kullanıcı sırası: dış oran/birleşimler → kokpit ayrıntıları/İngilizce etiketler → hareketli parça mekanizmaları. Bu çalışma önce dış modele odaklanır.

### Phase 10: Mevcut dosyayı koru ve referans karşılaştırması
**Status:** complete
### Phase 11: Mevcut blend üzerinde sürümlü dış geometri düzeltmesi
**Status:** complete
### Phase 12: Ön/yan/üst ve birleşim renderları, yeniden açma ve kayıtlar
**Status:** complete

## Next Step
v02 dosyasını yedekle; fotoğraf/üç görünüş karşılaştırmasına göre geometri revizyonu uygula.

## Yeni hata kaydı
- Etkileşimli Blender MCP localhost:9876 bağlantısı yok; pgrep çalışan Blender uygulaması göstermedi. Mevcut disk dosyası arka plan Blender sürecinde açılacak, kaynak dosyanın üzerine yazılmayacak.

Phase 10 complete: kaynak v02 ve aynı hashli yedek korundu, ön/yan/üst referanslar incelendi.
Phase 11 in_progress: mevcut sahne seçici mesh revizyonu ile v03 olarak kaydediliyor.
Ek hata: DVIDS web açma iki URL için erişim hatası verdi; yerel arşiv görselleri kullanıldı.

## Next Step
v03 renderlarını incele ve bağımsız Blender yeniden açma kontrolü uygula.

## Kullanıcı devam yetkisi — 13 Ekim 2026

### Phase 13: Kokpit kaynaklarını incele, kontrol haritasını çıkar
**Status:** in_progress
### Phase 14: Kokpit ayrıntılarını sürümlü sahneye uygula ve doğrula
**Status:** pending
### Phase 15: Hareketli parçaları hiyerarşi/pivot/animasyonla hazırla, doğrula
**Status:** pending
### Phase 16: Son teslimat, kaynak sınırları ve durum kayıtları
**Status:** pending

## Next Step
Yerel DCS kokpit ve başlatma sayfalarını oku; Block 52'ye aktarım sınırlarıyla İngilizce kumanda haritasını çıkar.

Kokpit üretim hata kaydı: v04 yeniden açılışında kullanılmayan Safety_yellow malzemesi Blender tarafından temizlendiği için KeyError oluştu; ihtiyaç halinde malzeme oluşturulacak şekilde düzeltildi. Hiçbir teslim dosyası bu başarısız denemede yazılmadı.

Kokpit görsel hata: v05 ICP etiketleri eksikti; parenting öncesi matrix_world güncellemesi eklendi. Pilot kamera görüşü ve sağ gösterge açıklığı render bulgusuna göre düzeltildi.
