# MQTT Tester
---
## Config
Programın çalışması için 9 değer verilmeli:
- ip
- port
- username
- password
- sub_topic: topic to subscribe
- pub_topic: topic to publish
- payload_file_path: Payload dosyasının relative ya da absolute adresi.
- interval: Milisaniye cinsinden 2 ardışık MQTT publishi arasında beklenmesi gereken süre.
- count: Art arda gönderilecek mesaj sayısı.

Bu değerler "config.json" dosyasında verilebilir ya da program çalışırken girilebilir. Girilen veriler program tarafından config.json'a kaydedilir.

---
## Çalışma Modları
 - ### Mode 1
   Verilen payload dosyasının içeriğini aralarına verilen interval kadar süre koyarak verilen count kere verilen pub_topic'e gönderir. Count'ın 0 verilmesi durumunda mesajı sonsuz bir döngünün içinde durdurulana kadar gönderir.

 - ### Mode 2: Echo Test
   sub_topic'e subscribe olur ve payload içeriğini verilen aralıklarla pub_topic'e gönderir. Gönderilen her mesajın sonuna bir ID eklenir. Bu ID'ler gönderilen her mesajın sub_topic'ten alınıp alınmadığını görmek için kullanılır. Programın sonunda hangi mesajların geri dönmediğini ve geri dönmeyen toplam mesaj sayısı görüntülenir.

---
dist/mqtt_tester: Linux Executable

dist/mqtt_tester.exe: Windows Executable