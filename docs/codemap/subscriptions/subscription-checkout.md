# Code Map & Docs: Subscription Checkout & Payment (Langganan & Pembayaran)

**App Domain**: `subscriptions`  
**Event Category**: `Billing & Monetization`  
**User Story Ref**: `US-005` (Pilihan Paket & Payment Gateway)

---

## 1. Developer View (Code Map & Tracing)

Pemetaan alur eksekusi dari Pilihan Paket hingga ke Invoicing & Webhook Payment Gateway.

### Entrypoint & Handlers
* **URL**: `/subscriptions/checkout/`
* **HTTP Method**: `POST` (HTMX Trigger)
* **View Class**: `CheckoutView` (`apps.subscriptions.views.checkout.CheckoutView`)
* **HTMX Response Header**: `HX-Redirect` (Redirect ke Payment Gateway URL)

### Execution Path (Function & Service Call Stack)
```text
[POST /subscriptions/checkout/]
 └── CheckoutView.post(request)
      └── SubscriptionService.create_checkout_session(user=request.user, plan_id=...)
           ├── PlanService.get_active_plan(plan_id)
           ├── QuotaEnforcerService.validate_upgrade_eligibility(user, plan)
           ├── PaymentGatewayAdapter.create_invoice(amount, user_email)
           └── SubscriptionService.record_pending_transaction(invoice_id)
```

### Data Models & DB Queries
| Model | Operation | Description |
|---|---|---|
| `subscriptions.SubscriptionPlan` | `SELECT` | Mengambil rincian tarif paket |
| `subscriptions.PaymentTransaction` | `INSERT` | Menyiapkan rekam transaksi status `PENDING` |
| `subscriptions.UserSubscription` | `UPDATE` | Diperbarui menjadi `ACTIVE` saat Webhook callback diterima |

### Telemetry & Resource Consumption Metrics
* **Expected Execution Time**: `250ms - 400ms` (Termasuk Latency Payment Gateway)
* **Expected DB Queries**: `5 queries`
* **Service Units Consumed**: `0.0 units` (Finansial Event)
* **External Calls**: `1 REST API Call to Midtrans / Xendit Gateway`

---

## 2. User Guide (Panduan Pengguna)

### Cara Memilih Paket Langganan & Membayar
1. Masuk ke menu **"Billing & Subscription"** di sidebar dashboard.
2. Pilihlah paket yang sesuai kebutuhan Anda (misal: Paket **Starter**, **Pro**, atau **Enterprise**).
3. Klik tombol **"Pilih Paket Ini"**.
4. Anda akan diarahkan ke halaman halaman pembayaran aman (Payment Gateway).
5. Selesaikan pembayaran menggunakan QRIS, Transfer Bank, atau Kartu Kredit.
6. Setelah sukses, status akun Anda akan langsung berubah menjadi **Pro / Active**.

---

## 3. FAQ (Pertanyaan Umum)

**Q: Berapa lama waktu yang dibutuhkan sampai paket aktif setelah membayar?**  
*A: Pembayaran via QRIS dan Transfer Virtual Account terkonfirmasi secara instan (< 10 detik) melalui sistem Webhook otomatis.*

**Q: Bisakah saya melakukan downgrade paket di tengah jalan?**  
*A: Bisa. Downgrade paket akan berlaku di akhir periode penagihan bulan berjalan.*

---

## 4. Help & Troubleshooting (Pesan Error & Solusi)

| Error Code | HTTP Status | Pesan Error UI | Penyebab & Solusi |
|---|---|---|---|
| `INVALID_PLAN` | 400 | "Paket langganan tidak ditemukan." | ID paket tidak valid atau sudah kadaluarsa. Pilih kembali dari tabel harga. |
| `PAYMENT_GATEWAY_TIMEOUT` | 504 | "Layanan pembayaran sedang sibuk." | API Payment Gateway rintangan. Coba beberapa saat lagi atau hubungi support. |
| `PAYMENT_EXPIRED` | 422 | "Batas waktu pembayaran telah habis." | Transaksi kedaluwarsa. Silakan lakukan checkout ulang. |
