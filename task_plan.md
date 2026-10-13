# F-16 referans toplama

## Goal
Yalnızca ilk aşama: kaynakları bul, erişilebilir belgeleri/görselleri sakla, inceleme ve eksiklerini kaydet. Modelleme ve oyun işleri kapsam dışı.

### Phase 1: Mevcut kapsamı oku
**Status:** complete

### Phase 2: Dış geometri, varyant, kokpit ve boyama kaynaklarını topla
**Status:** in_progress

### Phase 3: Kaynak kataloğunu ve proje kayıtlarını doğrula
**Status:** pending

## Next Step
Resmi ve birincil kaynaklarda dış görünüş ve kokpit referanslarını bul.

## Errors Encountered
- git diff --stat: klasör Git deposu değil; dosya içeriği ve yerel çıktı denetimi kullanılacak.
- Python bs4 modülü yok; standart HTMLParser/re ve mevcut PDF komutları kullanılacak.
- Galeri temas sayfasında DejaVu fontu bulunamadı; görseller etiketsiz incelendi, font yolu Liberation Sans olarak belirlendi.
- HTTP hataları: nozzle_169fw/hill_block52/usaf_facts 403; indirilen alternatif birincil belgeler ve web okunabilir AFMC kaydı kullanıldı. Ayrıntılar download_log.json içinde.

## GitHub yayınlama — 13 Ekim 2026

Kullanıcı mevcut projeyi `f16-projesi` adlı herkese açık depoda yayınlamayı ve gerekli commitleri oluşturmayı istedi. Referans toplama aşamalarının mevcut durumları korunur.

### Phase 4: Yayına hazırlık
**Status:** complete

Proje kökü ve dosyalar incelendi; README ve .gitignore eklendi. GitHub hesabı Emirix. Dosya taramasında bilinen gizli anahtar biçimleri bulunmadı.

### Phase 5: Commit ve GitHub yayını
**Status:** in_progress

### Phase 6: Yayını doğrula
**Status:** pending

## Next Step
Git deposunu başlat, ilk commiti oluştur ve Emirix/f16-projesi public deposuna gönder.

## Yayınlama kontrolleri
- Başlangıçta Git deposu yoktu; proje kökünde başlatılacak.
- GitHub depo sorgusu 404 verdi; hedef isim mevcut hesapta kullanılabilir.
