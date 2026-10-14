# F-16C Block 52 — ana model

Bu teslimat düzenlenebilir ilk 3D ana modeldir. Gövde ve siluet kurulmuştur; nihai mühendislik ölçüleri, mekanizma doğrulaması, tam kokpit ve cold start kumandaları sonraki ayrıntı aşamasında ele alınacaktır.

## Blender'da açma

`f16c_block52_main_v04.blend` dosyasını aç. Dış model düzeltme teslimatıdır; v02 kaynak ve v03 ara kontrol sürümü korunmuştur. Ana varlık 00–07 koleksiyonlarında; zemin, ışıklar ve kameralar 90_PREVIEW_STUDIO içindedir. Stüdyo çalışma görünümünde gizlidir, renderda görünür. Numpad 1/3/7 ile ön/yan/üst görünüme, Numpad 0 ile dış kameraya geçilebilir. Kamera listesinde ayrıca arka, ortografik ve geçici pilot kameraları bulunur.

`READ_ME_FIRST` Blender metni ve sahne özel özellikleri doğrulama sınırlarını içerir. Düğmeler ve ekranlar bu aşamada görsel hacimlerdir; çalışır uçak sistemleri değildir.

## Ölçek ve referans sınırı

- 1 Blender birimi = 1 metre. +X sol kanat, -X sağ kanat, +Y arka, +Z yukarı; burun -Y yönünde, zemin Z=0.
- Genel F-16 kaynağından geçici ölçek girdileri: uzunluk 15,0622 m; açıklık 9,9568 m; yükseklik 4,8768 m. Block 52 için kesin uç noktalarla doğrulanmış veri değildir.
- Modelde uzunluk pitot–nozul, açıklık boş kanat ucu raylarının dış kenarları, yükseklik iniş takımı açık zemin–kuyruk ucu olarak yorumlandı. Gerçek uçak kaynaklarındaki ölçüm tanımları çözülmüş sayılmaz.
- Ana siluet NASA genel üç görünüş ve SCANG Block 52 fotoğraflarından sanatçı yorumu ile kuruldu. Kokpitin ana yerleşimi DCS Block 50 yardımcı kaynağına dayanır; fiziksel koordinatlar tahmindir.
- Küçük NSI tarzı hava alığı ve PW229 için sade nozul yorumu vardır; kesin kesit/yaprak ölçüleri doğrulanmadı.
- Türk görünümü kullanıcıya özel kurgudur. `TR-052` gerçek bir uçağın tescili değildir; renkler doğrulanmış FS boya standardı değildir.

## Düzenleme ve yeniden üretme

Üretim betiği proje kökünden:

```sh
blender --background --threads 8 --python scripts/build_f16.py -- --render
```

Betik ayrı Blender sürecinde yeni sahne oluşturur. Mevcut `.blend` dosyasının üzerine yazmaz; uygun yeni v03/v04 sürümünü seçer. Açık Blender oturumundaki kaydedilmemiş değişiklikleri okumaz; çalışmana devam ederken kendi dosyanı kaydet. Yeni sürüm eski modele yapılmış düzenlemeleri otomatik birleştirmez.

Kanopi camı, flaperonlar, ön kenar flapları, stabilatörler, dümen, hava frenleri ve nozul yaprakları ayrı nesnelerdir. Bazı ana yüzeylerde yaklaşık pivotlar vardır; iniş takımı animasyon hiyerarşisi, kanopi çerçevesinin ortak hareketi ve gerçek hareket aralıkları henüz kurulmamıştır.

Düz mat malzemeler ve düşük segmentli geometri kullanıldı. Render stüdyosunun Cycles CPU ayarları oyunun performans bütçesi değildir. Intel Iris Xe FPS testi yapılmadı. Geometri raporu temel ve yeniden açma sonrası değerlendirilmiş sayımları ayırır.

## Dış model düzeltme v04

Burun kesitleri, ortak kanopi/omuz kenarları, iç kabuk duvarı, NSI dudak/kaporta geçişi, LEX, kanat/flaperon arka planformu ve kuyruk silueti düzenlendi. 5.654 değerlendirilmiş üçgen. Yeniden açma ve birleşim/simetri/kaynak koruma kontrolleri sıfır hata verdi. 150 kapsam dışı nesne korundu.

Mevcut sahneyi seçici düzeltme komutu (v02 kaynak içindir; değişen nesnelerdeki özel düzenlemeler yeni kopyada bu koordinatlarla değiştirilir):

```sh
blender -b output/model/f16c_block52_main_v02.blend --python scripts/refine_exterior.py -- --render
```

Bu betik mevcut dosyayı korur; yeni sürümü seçer. `build_f16.py` eski ana hacim üreticisidir ve v04 düzeltmelerini kendi başına içermez. Yeni düzeltmeler için güncel teslim dosyası esas alınır.

Karşılaştırma: [DIS_MODEL_KARSILASTIRMA.md](../../research/DIS_MODEL_KARSILASTIRMA.md). Güncel doğrulama: [genel](f16c_block52_main_v04.validation.json), [birleşim/koruma](f16c_block52_main_v04.exterior_checks.json).
