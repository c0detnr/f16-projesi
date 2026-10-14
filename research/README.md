# Proje özeti ve sohbetler arası devam

Bu kayıtlar 13 Ekim 2026 planlama, referans toplama ve Blender ana model çalışmalarından hazırlanmıştır. Amaç hem kullanıcıya okunabilir bir özet sunmak hem de aynı proje klasörüne erişen başka Codex sohbetlerine bağlam bırakmaktır.

## Yapmak istediğimiz şey

Blender ile sıfırdan gerçek boyutlarda F-16C Block 52 oluşturacağız. VTOL VR görsel ve etkileşim referansı: düşük poligonlu geometri, düz renkli mat malzemeler, az doku, basit aydınlatma, doğru siluet ve okunabilir kokpit. Kullanıcı fotogerçekçi görünümü reddetti; Intel Iris Xe GPU ile rahat oynanabilirlik öncelikli. Gerçekçilik önceliği oranlar, kumanda yerleşimleri ve tam temel cold start için gereken fiziksel kontroller.

Model daha sonra kokpite girilebilen, düğmelere basılabilen, HUD ve göstergeleri çalışan bir oyunda kullanılacak. Kontrol yüzeyleri, iniş takımı, kanopi, motor nozulu ve afterburner da oyun aşamasında hareket ve işlev kazanacak.

## Kararların gerekçeleri

- Tek koltuklu standart Block 52 seçildi; çift kokpit ve Block 52+ kapsamı eklenmedi.
- Kullanıcı gerçek boyutları özellikle vurguladı. Ölçek 1 Blender birimi = 1 metre olacak; gerçek ölçülerdeki kaynak uyuşmazlıkları henüz çözülmedi.
- Kullanıcı Block 52'yi koruyup Türk boyaması istedi. Bu birleşimin tarihsel bir Türk Block 52 kopyası olmadığı açıklandı ve kullanıcı tarafından kabul edildi.
- Boş istasyonlar ve ayrı pilonlar seçildi. İlk varlığa silah veya harici yakıt tankı eklenmeyecek.
- Masaüstü önce seçildi. VTOL VR referansı ilk sürümün VR olacağı anlamına gelmiyor.
- Tam temel cold start ve uçuş odaklı ilk sürüm seçildi. Derin bakım/test simülasyonu veya savaş sistemleri ilk sürüm kapsamı olarak seçilmedi.
- Kullanıcı oyun motoru/export kararını açıkça sonraya bıraktı. Godot'un kurulu olması bir motor seçimi değildir.
- GPT-6 Astra Medium modelleme işi için önerildi; GPT-6.1 Sol High da alternatif olarak konuşuldu. Bu öneri bir Blender kalite ölçümü ya da mevcut sohbet modelini zorunlu kılan ayar değildir.

## Hangi dosya ne için?

| Dosya | Kullanım |
| --- | --- |
| [PLAN.md](../PLAN.md) | Kabul edilen kapsam, teslimatlar ve kalite ölçütleri |
| [REFERANSLAR.md](REFERANSLAR.md) | İndirilen referans paketi, sayfa indeksi, kullanım sınırları |
| [ARASTIRMA.md](ARASTIRMA.md) | Mevcut teknik bulgular, kaynaklar ve erişim sorunları |
| [TODO.md](TODO.md) | Tamamlanması gereken teknik araştırmalar |
| [DURUM.md](DURUM.md) | Gerçekte tamamlanan işler ve sonraki adım |
| [AGENTS.md](../AGENTS.md) | Codex için kısa proje yönlendirmesi |

Kararların asıl kaydı `PLAN.md` dosyasıdır. Buradaki özet, güncel planla çelişirse son kullanıcı talimatına göre belgeler birlikte düzeltilmelidir.

## Yeni Codex sohbetine yazılabilecek başlangıç mesajı

> Bu projede F-16C Block 52 modelini kaldığımız yerden sürdür. Önce AGENTS.md, PLAN.md ve research/DURUM.md dosyalarını oku. Gerekli araştırma için research/ARASTIRMA.md ve research/TODO.md dosyalarına bak. Önceki kararları koru, doğrulanmamış ölçüleri kesin kabul etme ve tamamlanmamış işleri yapılmış sayma. İstenen işi tamamladıktan sonra ilerleme kaydını güncelle.

Codex'in bu dosyalara erişmesi için aynı proje klasöründe çalışması gerekir. `AGENTS.md` proje talimatlarını keşfetmek için desteklenen dosyadır; diğer notlara buradan yönlendirme yapılır. Bu dosyalar tüm hesap veya başka klasörlerdeki sohbetler için otomatik ortak hafıza oluşturmaz. Kaynak: [OpenAI — AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).


## Görülebilir 3D çıktı

İlk ana model teslimatı: [f16c_block52_main_v02.blend](../output/model/f16c_block52_main_v02.blend). Üretim betiği: [build_f16.py](../scripts/build_f16.py); kullanım ve sınırlar: [MODEL_NOTES.md](../output/model/MODEL_NOTES.md). Bu dosya araştırma/konsept görseli değildir, düzenlenebilir 3D sahnedir. Geçici ölçü girdileri ve kokpit ana hacimleri henüz nihai teknik doğrulama sayılmaz.


Güncel dış düzeltme teslimatı [v04](../output/model/f16c_block52_main_v04.blend); v02 ilk ana model geçmişidir. Kullanıcı sonraki kokpit ve mekanizma aşamalarına devamı yetkilendirdi.
