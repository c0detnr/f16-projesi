# Referans toplama bulguları

Mevcut notlar okundu. Ölçüler geçici; DCS önceki PDF bağlantıları erişilememiş. Yeni bulgular research/REFERANSLAR.md ve research/ARASTIRMA.md içine işlenecek.

İlk tarama: NASA 19920012114 üç görünüş adayı bulundu (Block 52 olduğu doğrulanmadı); F-16XL çizimleri hedefe uygun değil. USAF kökenli Commons SVG metadata üst görünüşün ayna hatasını bildiriyor; ölçülü Block 52 çizimi olarak kullanılmamalı. DCS liste sayfası 16.08.2026 güncellemesi gösteriyor; belgenin kendisi henüz incelenmedi.

ED resmi duyurusu DCS referansını 2007 dönemi CCIP Block 50 olarak tanımlıyor; hedef Block 52 kokpitinin doğrulaması değil. LM Block 70/72 kartındaki 31 ft açıklık ve 16.7 ft yükseklik farklı varyant kaynağı: mevcut ölçü çelişkisini çözmüş sayılmayacak. Web açılışlarında DCS/LM/Shaw 403; doğrudan indirme denenecek.

NASA PDF ve DCS belge liste sayfası doğrudan HTTP ile indirildi. NASA CR-186016 çalışma uçağı deneysel motor/tahrik yönlendirme bağlamında; çizim sadece genel siluet karşılaştırması. AFMC Block 52 fotoğraf açıklaması ve DVIDS Türk F-16 8913466 sayfası incelendi. Thunderbirds duman sistemi/silah sökümü nedeniyle standart savaş uçağı ayrıntıları için tek başına yeterli değil.

DCS güncel liste HTML içinde yeni e78 dizinli PDF bağlantısı bulundu. 169th Fighter Wing 2018 DVIDS 4548370 seti standart Block 52 dış görünüş için ana aday; Thunderbirds yardımcı kaynak. NASA Elegance in Flight s.84 LM kökenli NSI/LNSI kesit karşılaştırması içeriyor; XL gövde geometrisi kullanılmayacak. USAF seat-back 30 derece kaynağı bulundu, kokpit genişliği ve göz noktası hâlâ ölçülmemiş.

DCS F-16C PDF başarıyla indirildi (58,324,381 bayt); kapak 16 August 2026, giriş Block 50/2007. Kokpit bölümü basılı s.43, sol konsol s.62, sağ konsol s.75; başlatma bölümü s.135–137. NASA CR-4182 Fig.23 s.75 ölçülü F-16 araştırma konfigürasyonu bulundu; Block 52 sertifikalı çizimi değil.

Görsel inceleme: SCANG 4548358 önden NSI, burun takımı ve kapaklar; 4548350 kanopi/HUD/ön antenler; 4548370 yan siluet; 4548379 ön çapraz. Hepsi aynı tarihli set fakat farklı seri numaraları: tek uçak ölçüm seti değil. 4548393 C-17 olduğu için reddedildi. Türk 8913466 boyama/işaret için uygun, hava alığı Block 52 yerine kullanılmayacak.

NASA CR-4182 Fig.23 görselinde 15.09 m uzunluk, 9.45 m açıklık, 5.01 m yükseklik yazıyor; ölçüm uçları/Block 52 bağı belirsiz. NSI şekli NASA s.84 üzerinde görsel incelendi. DCS s.43 ekran/HUD/konsol yerleşimi incelendi. VTOL 1/4 kokpitte büyük etiket ve basit hacim, VTOL 3 dış yüzeyde sade panel/normal görünümü: bunlar sanat yorumu, poligon ölçümü değil.

CR-4182 çiziminin Ref.38 kaynağı NASA TP-1538 (1979); böylece Block 52 üretim çizimi olmadığı netleşti. DCS sol/sağ konsol sayfaları ve başlatma bölümü metin olarak okundu; nihai düğme haritası çıkarılmadı. Yeni kaynak toplama yalnızca ilk aşama kapsamındadır.

169th motor test görseli DVIDS 7427090 bulundu; motor varyantı başlıkta açık değil, PW229 eşlemesi birim kaynağına dayalı çıkarım olarak kalacak. Üst gövde için 7403357 tanker fotoğrafı indiriliyor.

Üst fotoğraf 7403357 görsel incelendi: kanat/LEX/kanopi/ön antenler, tanker arka gövdeyi örtüyor. 4548353 ve 4548377 ön-yan pilon/gövde profili sağlar. DCS s.63 doğrudan F110-GE-129 kontrol panelini anlatıyor: motor başlatma değerleri Block 52 için doğrudan alınmayacak.

GitHub yayınlama kontrolü: proje kökü /home/mami/Projects/bl; toplam yaklaşık 96 MB. En büyük dosya DCS kılavuzu (58.324.381 bayt); mevcut tüm dosyalar 100 MB altında. GitHub hesabı Emirix; f16-projesi hedef deposu henüz mevcut değil.

Kaynak kataloğu research/REFERANSLAR.md yazıldı. Motor test fotoğrafı görsel olarak incelendi: nozul yandan kısmen seçiliyor; yaprak/çap ölçüsünü doğrulayacak arka görünüş değil. Kesin ölçüler ve kokpit fiziksel ölçeği açık tutuldu.

GitHub API kullanıcı sorgusu güncel hesabın c0detnr olduğunu doğruladı; gh auth status eski Emirix adını gösteriyordu. Public depo: https://github.com/c0detnr/f16-projesi (main).

Son doğrulama başarılı: 6 PDF, 15 JPG, 7 PNG; kaynak hashleri ve yerel bağlantılar geçerli. Referans toplama bitti, tüm teknik araştırmanın tamamlandığı iddia edilmedi. research/references/DOGRULAMA.txt kayıtlandı.

Ana model başlangıcı: mevcut .blend bulunmadı. Yerel NASA genel silueti ve SCANG fotoğrafları görsel olarak tekrar incelendi. DCS kokpitinde sağ side-stick, sol throttle, iki MFD ve merkezi ICP/HUD ana hacimleri esas alınacak. Fiziksel konumlar modelleme tahmini.

Blender kamera pilot bakışı -Y yönünde olduğunda görüntünün sağı -X olur. Ana model eksen belgesi +X sol, -X sağ olarak düzeltildi; side-stick sağda, throttle solda ve DED sağda yerleştirildi. Bu koordinat kararı gerçek kokpit boyut doğrulaması değildir.

Dış model incelemesi: v02 yan görünüşte kanopi alt omuzunda siyah açıklık, uzun boru gibi hava alığı kaportası, dik kuyruk arka kenarı ve gövdeden kopuk ince LEX/kanat plakası görünümü var. NASA CR-186016 genel üç görünüşündeki eğimli kuyruk arka kenarı ve SCANG 4548370 Block 52 fotoğrafı bunları görsel olarak değerlendirmeye yarıyor. NASA araştırma konfigürasyonu kesin Block 52 ölçüsü değil. Kaynak blend yeniden üretmek yerine seçili dış meshleri revize eden betikle işlenecek; kokpit/kullanıcı nesneleri korunacak.

SCANG 4548358 ön fotoğrafı: hava alığı geniş U biçimli, üst kenarı hafif eğrisel ve gövde altında ayırıcı aralığı var. v02'nin elipse yakın dar görünümü ve dudak/kaporta süreksizliği düzeltilecek. 7403357 üst fotoğrafı LEX–kanat kökü genişleyen yumuşak geçişini ve kanopinin arka sabit cam bölümünü gösteriyor; tanker arka gövdeyi örttüğü için kuyruk ölçüsü çıkarılmayacak. v02 renderları incelendi; kokpit ve iniş takımı bu teslimatta ana hacim düzeyinde korunacak.

v03 dış/yan/üst render kontrolü: kuyruk arka kenarı artık eğimli, kanopi arka geçişi uzatıldı ve eski uzun omuz açıklığı kayboldu. Hava alığı arka kaportası gövdeye doğru yükseliyor; mevcut poligon üslubu korundu. Yeniden açma kontrolü sıfır hata ve 5.654 değerlendirilmiş üçgen verdi. Yakın birleşim ve pilot renderı kontrolü bekleniyor.

Yakın v03 renderı eski kokpit iç yan duvarının yeni daralan ön omuzdan dışarı taştığını gösterdi. v04 için iç kabuk duvarı yeni kanopi çevresine eşlenecek; koltuk/panel/kumanda geometrileri korunacak. Bu görsel bulgu yeniden üretim ve kontrolü gerektiriyor.

v04 yeniden açma ve ek kontroller başarılı: 5.654 değerlendirilmiş üçgen, 3.885 köşe; kaynak hash korundu; kapsam dışı 150 nesnenin kaydedilen geometri/transform/malzeme özellikleri değişmedi. Kontrol edilen kanopi–omuz–gövde, radom–gövde ve hava alığı dudak–kaporta ortak noktalarında fark 0; kanat/LEX/flaperon/stabilatör/omuz ikili simetrisi başarılı. Bütün yüzey çarpışmaları veya gerçek ölçek referans uyumu doğrulanmış sayılmaz.


v04 ön/yakın/pilot renderları incelendi. Eski iç duvar taşması giderildi; kokpit HUD/MFD görünümü korunuyor. Kesin göz noktası ve ergonomi doğrulanmış değil.

Kokpit kaynak incelemesi: DCS basılı s.43, 62, 75 görselleri ve s.63–64, 67, 73, 77–79, 135–138 metinleri okundu. MAIN PWR OFF/BATT/MAIN PWR; FUEL MASTER ve ENG FEED; EPU OFF/NORM/ON; OXYGEN SUPPLY OFF/ON/PBG; aviyonik MMC/ST STA/MFD/UFC/GPS ve INS konumları belgede doğrulandı. Ancak s.63 motor paneli açıkça F110-GE-129, hedef PW229 değil. Başlatma RPM/sıcaklık eşikleri Block52 işletme verisi olarak aktarılmayacak. Model İngilizce ad/kademeleri kaynak sayfasıyla ilişkilendirecek; Block52 aktarım durumu ayrıca belirtilecek.

v05 kokpit renderı: 20 OSB yerleşimi görünüyor, ancak ICP etiketleri parent ataması öncesinde dependency graph güncellenmediği için yanlış konuma taşınmış; HUD/alt gösterge kadrajı dar ve sağ motor göstergeleri çerçeveye yakındı. parent_keep güncellemesi, daha geniş pilot kamera açısı ve MFD/motor sütunu açıklığı düzeltildi. v06 üretilecek.

Mekanizma araştırması: yeni aramalarda kesin Block52 menteşe/iniş takımı açısı bulunmadı. NASA XL kumanda açıları hedefe aktarılmayacak. GAO/NSIAD-95-145 parça listesi F-16C arka sabit kanopi camını adlandıran yardımcı kaynak; kesit veya açı kaynağı değil. Akademik F16 dönen teker düzlemli iniş takımı makalesi arama sonucu bulundu, sayfa zaman aşımına uğradı; incelenmiş mekanizma kanıtı sayılmadı. Görsel rig açıları açıkça modelleme tahmini kalacak.
