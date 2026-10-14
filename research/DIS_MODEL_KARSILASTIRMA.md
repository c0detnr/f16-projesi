# Dış model oran ve birleşim incelemesi

13 Ekim 2026. Kullanıcı önceliği: dış model, sonra kokpit ayrıntıları, sonra mekanizmalar.

## İncelenen kaynaklar ve sınırları

- `references/scang_4548370.jpg`: 169th FW Block 52 yan/alt çapraz fotoğrafı. Burun, kanopi ve eğimli dik kuyruk için görsel karşılaştırma. Perspektif var; pikselden kesin metre ölçülmedi.
- `references/scang_4548358.jpg`: önden Block 52; NSI ağzının geniş U görünümü, dudak, gövde altı aralığı ve omuzlar.
- `references/scang_top_7403357.jpg`: kanopi ve LEX–kanat kökü üstten görünüşü. Tanker arka gövdeyi örter; kuyruk için kullanılmadı.
- `references/nasa_three_view_p42.png`: CR-186016 Fig.1 genel F-16 silueti. Deneysel konfigürasyon; Block 52 boyut şartnamesi değil.

Bunlar bu oturumda gerçekten görsel olarak incelendi. DVIDS web açma girişimleri erişim hatası verdi; önceden indirilmiş orijinal kaynak görselleri kullanıldı. Kaynak bağlantıları ve kimlikleri [REFERANSLAR.md](REFERANSLAR.md) içindedir.

## Modelleme kararları

| Bölge | v02 gözlemi | Revizyon | Bilgi türü |
| --- | --- | --- | --- |
| Burun | Sivri, az kesitli radom | Ara kesitler ve daha dolgun eğri; son kesit gövdeye ortak | Fotoğraf yorumu; geçici koordinatlar |
| Kanopi/omuz | Farklı boyuna kesitler, yan açıklık ve arka kısa bitiş | Ortak kesit ızgarası, aynı kenar koordinatları, uzatılan arka geçiş | Geometrik birleşim ölçülebilir; gerçek kesit ölçüsü açık |
| İç kabuk | Yeni ön çevreden dışarı çıkan eski duvar | İç yan duvarları yeni eşik çevresine eşleme | Renderda saptanan hata düzeltmesi |
| Hava alığı | Dudağa uymayan ayrı kaporta, uzun düz boru etkisi | Geniş U profil, ortak dudak/kaporta halkası, arkaya yükselerek gövdeye giren kaporta | NSI görsel yorumu; kesit/metre doğrulaması değil |
| Kanat kökü | İnce plakadan LEX geçişi | Hacimli, çok kesitli LEX; düzenlenen kanat/flaperon arka planformu | Fotoğraf/üç görünüş yorumu |
| Kuyruk | Neredeyse dik arka kenar | Geriye yatık dümen ve arka kenar; stabilatör uç biçimi düzenlendi | Fotoğraf siluetine uyum, menteşe doğrulanmadı |

Geçici toplam uzunluk/açıklık/yükseklik korunur. Kokpit donanımı, nozul, iniş takımı ve pilonlar bu revizyonun ayrıntılandırma kapsamına alınmadı. Kanopi arka sabit camı ile hareketli camın mekanik ayrımı ve güncellenmiş dümen menteşesi sonraki mekanizma aşamasında ele alınacak; mevcut eski pivotlar nihai kabul edilmez.

## Koruma ve doğrulama

Kaynak v02 üzerine yazılmaz; aynı hashli yedeği `output/model/backups/` içindedir. `scripts/refine_exterior.py` mevcut sahneyi açar ve yalnızca listelenmiş nesnelerin geometri verisini değiştirir. Tüm sahneyi sıfırdan üretmez. Değişen nesne listesi sürümlü `exterior_revision` JSON raporuna yazılır.

`check_model.py` yeniden açma, metrik ölçek, sonlu geometri, sıfır alan ve bağımlılık kontrollerini yapar. `check_exterior_revision.py` ortak birleşim noktalarını, iki taraf simetrisini, kaynak hashini ve kapsam dışındaki nesnelerin korunmasını denetler. Bu kontroller tüm yüzey kesişmelerini ya da gerçek uçak ölçülerini doğrulamaz.
