# 🛰️ ArivLogBasic

Gelişmiş terminal arayüzü ve IP loglama özelliklerine sahip sade ama güçlü bir Python tabanlı HTTP sunucusu. Kullanıcıların sistem bilgilerini, IP adreslerini, konumlarını ve tarayıcı detaylarını kayıt altına alır. Özellikle siber güvenlik hobileri, test ortamları ve analizler için idealdir.

---

## 🚀 Özellikler

- ✅ Gerçek zamanlı IP ve konum bilgisi tespiti (`ip-api.com`)
- ✅ Kullanıcı sistem bilgilerini ayrıntılı şekilde loglar
- ✅ Cookie ile kullanıcı takibi (UUID tabanlı)
- ✅ Şık ve sade HTML arayüz
- ✅ Cloudflare Tunneling desteği (Uzaktan erişim kolaylığı)
- ✅ Platformlar arası uyumluluk (Linux, Termux, Windows)

---

## ⚙️ Kurulum

**Gereksinimler:**

```bash
pip install rich colorama requests psutil
```

Başlatmak için:

```bash
 python arivlogbasic.py
```

Sunucu çalıştıktan sonra aşağıdaki komutla dış dünyaya açabilirsiniz:

```bash 
cloudflared tunnel --url http://localhost:8000
```

> Eğer cloudflared yüklü değilse, Termux veya Linux ortamında şu komutla yükleyebilirsiniz:
>  ```bash
>  pkg install cloudflared
> ```


📌 Kullanım Notları

Script çalıştığında bağlantı yapan her istemcinin:

IP ve lokasyon bilgisi

Tarayıcı bilgileri (User-Agent)

Sistem bilgisi (Platform, RAM, CPU sayısı)

Cookie ID (ilk girişte oluşturulur)

Ziyaret zamanı gibi bilgiler terminale JSON formatında loglanır.


Görsel arayüzde karşılama mesajı ve çerez durumu gösterilir.


🗣️ Topluluk ve İletişim

Bize katılmak ve daha fazla araç hakkında bilgi almak için Telegram kanallarımıza göz atın:

💬 Sohbet & Destek: t.me/siberdunyanizsohbet

🛠️ Araç Paylaşımları: t.me/arivatools

📄 Lisans

Bu proje yalnızca eğitim ve araştırma amaçlıdır. Kullanım tamamen kullanıcı sorumluluğundadır.
