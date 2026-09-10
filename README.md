# NetTUI - Network & Telemetry Interactive TUI

**NetTUI** هي أداة مراقبة وتشخيص شبكات واتصالات طرفية حديثة وخفيفة الوزن، مصممة لأنظمة **Linux** والأنظمة المدمجة (**Embedded Linux** / Raspberry Pi / ARM boards)، ومخصصة للعمل بكفاءة داخل توزيعات مثل **Kali Linux**.

تعتمد الأداة على واجهة نصية تفاعلية متقدمة (**TUI**) مبنية بواسطة مكتبة **Textual** ومحرك غير متزامن بالكامل (`asyncio`)، مما يسمح بمراقبة الشبكات وتحليل البيانات السريالية دون تجميد الواجهة أو استهلاك موارد الذاكرة والمعالج.

---

## 🚀 المميزات الرئيسية (Key Features)

- **مراقبة الاتصال الحي (Async ICMP/Ping):**
  - قياس فوري لمعدل زمن الاستجابة (RTT Latency).
  - احتساب دقيق لنسبة فقدان الحزم (Packet Loss Percentage) بشكل لحظي.
- **فاحص المقابس والمنافذ (Socket & Port Diagnostics):**
  - فحص منافذ TCP و UDP غير المتزامن.
  - قياس زمن مصافحة الاتصال (Handshake / Connection Time).
- **مراقب المنافذ التسلسلية (Serial / UART Console):**
  - قراءة واستقبال البيانات التسلسلية للعتاد المدمج (Baudrate configurable).
  - دعم منافذ `/dev/ttyUSB*` و `/dev/ttyACM*`.
- **فحص والتقاط الحزم الخفيف (Packet Sniffer):**
  - مراقبة حركة المرور عبر الواجهات (`eth0`, `wlan0`, إلخ).
  - تصفية الحزم على مستوى البروتوكول وعرض تدفق البيانات مباشرة.
- **واجهة Textual عصرية:**
  - دعم كامل للتنقل بالفأرة ولوحة المفاتيح.
  - استهلاك موارد منخفض جداً يناسب الأجهزة المصغرة والعمل عبر جلسات SSH.

---

## 📁 بنية المشروع (Project Structure)

```text
net_tui/
├── core/
│   ├── __init__.py
│   ├── ping_runner.py    # إرسال Ping وحساب التأخير والـ Packet Loss
│   ├── socket_client.py  # اختبار اتصالات TCP/UDP
│   ├── serial_reader.py  # قراءة منافذ UART/Serial غير المتزامنة
│   └── sniffer.py        # فحص الحزم السطحية (Scapy / Raw Sockets)
├── ui/
│   ├── __init__.py
│   ├── styles.tcss       # ملف تنسيق الواجهة بنمط CSS
│   └── screens.py        # شاشات وأدوات العرض (Widgets)
├── main.py               # نقطة الدخول وتنسيق أحداث Textual
├── requirements.txt      # التبعيات والحزم المطلوبة
└── README.md             # دليل وتوثيق المشروع
