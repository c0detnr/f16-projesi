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
**Status:** in_progress

### Phase 9: Render, yeniden açma, geometri kontrolü ve teslim kayıtları
**Status:** pending

## Next Step
Düşük poligonlu ana gövdeyi, ayrı parçaları, kokpit ana hacimlerini ve önizleme sahnesini oluştur.
