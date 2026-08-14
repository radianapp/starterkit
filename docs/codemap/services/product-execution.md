# Code Map & Docs: Product Execution & Service Metering (Jalankan Service & Kuota)

**App Domain**: `services`  
**Event Category**: `Core Feature Execution`  
**User Story Ref**: `US-036` (Service Execution & Metering)

---

## 1. Developer View (Code Map & Tracing)

Pemetaan alur eksekusi dari Eksekusi Fitur Utama hingga ke Kalkulasi Penggunaan Kuota / Service Units.

### Entrypoint & Handlers
* **URL**: `/services/execute/`
* **HTTP Method**: `POST` (HTMX Async Execution)
* **View Class**: `ExecuteServiceView` (`apps.services.views.execute.ExecuteServiceView`)
* **HTMX Target**: `#execution-result-card`

### Execution Path (Function & Service Call Stack)
```text
[POST /services/execute/]
 └── ExecuteServiceView.post(request)
      ├── QuotaEnforcerService.check_user_quota(user, required_units=5.0)
      ├── ProductExecutionService.execute_service(user, service_id, payload)
      │    ├── TaskWorker.dispatch_job(service_id, payload)
      │    └── ProductExecutionService._process_data_payload()
      └── MeteringService.record_consumption(user, service_id, consumed_units=5.0)
           ├── ServiceUsageLog.objects.create(...)
           └── ResourceQuota.objects.filter(user=user).update(used=F('used') + 5.0)
```

### Data Models & DB Queries
| Model | Operation | Description |
|---|---|---|
| `services.ProductService` | `SELECT` | Validasi spesifikasi service yang dipanggil |
| `services.ResourceQuota` | `SELECT & UPDATE` | Pengecekan sisa kuota dan pembaruan jumlah terpakai |
| `services.ServiceUsageLog` | `INSERT` | Menulis catatan historis pengkonsumsian unit service |

### Telemetry & Resource Consumption Metrics
* **Expected Execution Time**: `120ms - 350ms`
* **Expected DB Queries**: `5 queries`
* **Service Units Consumed**: `5.0 units / execution`
* **CPU / Memory Impact**: `0.85s CPU time`, `128MB RAM`

---

## 2. User Guide (Panduan Pengguna)

### Cara Menjalankan Service Produk & Memantau Kuota
1. Buka halaman **"Services & Tools"** di menu utama dashboard.
2. Pilihlah service yang ingin Anda jalankan (contoh: **"Data Cleansing Service"**).
3. Unggah file dataset atau isi parameter input yang dibutuhkan.
4. Perhatikan estimasi konsumsi kuota yang tertera (contoh: **5 Service Units**).
5. Klik **"Jalankan Service"**.
6. Hasil pemrosesan akan langsung muncul pada layar dan kuota akun Anda akan berkurang secara otomatis.

---

## 3. FAQ (Pertanyaan Umum)

**Q: Bagaimana jika kuota saya habis di tengah-tengah pemrosesan?**  
*A: Sistem akan melakukan pengecekan kuota sebelum proses dimulai (*Pre-flight Quota Check*). Jika kuota tidak mencukupi, proses akan dibatalkan tanpa mengkonsumsi kuota Anda.*

**Q: Di mana saya bisa melihat riwayat pemakaian kuota service saya?**  
*A: Anda dapat melihat rincian pemakaian service di halaman **Dashboard Usage & Analytics**.*

---

## 4. Help & Troubleshooting (Pesan Error & Solusi)

| Error Code | HTTP Status | Pesan Error UI | Penyebab & Solusi |
|---|---|---|---|
| `QUOTA_EXCEEDED` | 422 | "Kuota service Anda tidak mencukupi." | Kuota akun telah mencapai batas maksimum. Silakan lakukan Top Up atau Upgrade Paket. |
| `INVALID_PAYLOAD` | 400 | "Format parameter input tidak valid." | File dataset yang diunggah korup atau parameter kosong. Perbaiki input lalu coba kembali. |
| `WORKER_TIMEOUT` | 504 | "Pemrosesan service membutuhkan waktu terlalu lama." | File terlalu besar. Pisahkan file menjadi beberapa bagian yang lebih kecil. |
