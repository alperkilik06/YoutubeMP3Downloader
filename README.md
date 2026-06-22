# 🎵 YouTube MP3 Şarkı İndirici

Bu proje, YouTube videolarını veya çalma listelerini (playlist) bilgisayarınıza en yüksek kalitede **MP3** olarak indirmenizi sağlayan, modern ve kullanıcı dostu arayüze sahip açık kaynaklı bir Python aracıdır.

---

## ✨ Özellikler

* **Gelişmiş Arayüz:** Kullanıcı dostu ve modern Tkinter tasarımı.
* **Canlı İlerleme Takibi:** İndirme yüzdesini ve durumunu anlık olarak arayüzden takip edin.
* **Çalma Listesi (Playlist) Desteği:** Tek tek video yerine tüm çalma listesini tek tıkla indirin.
* **Klasör Seçimi:** Şarkıların bilgisayarınızda nereye kaydedileceğini dinamik olarak belirleyin.
* **Esnek FFmpeg Yönetimi:** İster sisteminize kurun, ister arayüzden dosya yolunu gösterin.

---

## 🛠️ Kurulum ve Gereksinimler

Programın çalışması için bilgisayarınızda **Python**, gerekli kütüphaneler ve **FFmpeg** yazılımının bulunması gerekir.

### 1. Bağımlılıkları Kurun
Terminal veya Komut İstemi'ni (CMD) açarak proje klasöründeyken aşağıdaki komutla gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```
---

## 2. FFmpeg Kurulumu ve Yapılandırılması (Zorunlu)
YouTube'dan indirilen seslerin gerçek MP3 formatına dönüştürülebilmesi için FFmpeg gereklidir.

Gyan.dev adresinden ffmpeg-release-essentials.7z (veya .zip) dosyasını indirin.
Klasöre ayıklayın.
Programı çalıştırdıktan sonra arayüzdeki "FFmpeg Seç" butonuna basarak ayıkladığınız klasörün içindeki bin klasöründe yer alan ffmpeg.exe dosyasını seçin.

---

## 3.Çalıştırma
Gereksinimleri tamamladıktan sonra terminal üzerinden şu komutla programı başlatabilirsiniz:
python ss.py

---

### 4.Lisans
Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için LICENSE dosyasına göz atabilirsiniz.

---

### Sorumluluk Reddi Beyanı 
Bu proje sadece eğitim ve kişisel kullanım amacıyla geliştirilmiştir. YouTube üzerindeki içeriklerin indirilmesi, içerik üreticilerinin telif haklarına ve YouTube Kullanım Şartları'na tabi olabilir. Bu yazılımın ticari amaçlarla veya telif hakkı içeren materyalleri izinsiz indirmek için kullanılmasından doğabilecek tüm yasal sorumluluk kullanıcıya aittir. Geliştirici, yazılımın uygunsuz veya yasalara aykırı kullanımından dolayı hiçbir sorumluluk kabul etmez.
