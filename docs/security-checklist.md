# Security Checklist (DevSecOps)

Dokumen ini melacak status implementasi alat pengujian dan kontrol keamanan (Security Controls) di siklus pengembangan (SDLC) RDP Starter Kit. Hal ini sejalan dengan prinsip *Shift-Left Security* (menguji sedini mungkin) dan *Shift-Right Security* (melindungi di *production*).

## Kategori Prioritas

| Area / Jenis Test                           | Status | Tools / Implementasi                    | Prioritas     |
| ------------------------------------------- | ------ | --------------------------------------- | ------------- |
| **Secret Scanning**                         | ✅ Ada | Gitleaks (via Pre-commit)               | ⭐⭐⭐⭐⭐ Wajib |
| **SAST (Static Code Analysis)**             | ✅ Ada | Bandit (via Pre-commit)                 | ⭐⭐⭐⭐⭐ Wajib |
| **Security Regression Test**                | ✅ Ada | Pytest (`tests/test_security.py`)       | ⭐⭐⭐⭐⭐ Wajib |
| **Dependency Scanning (SCA)**               | ✅ Ada | Trivy Action (via GitHub Actions CI)    | ⭐⭐⭐⭐⭐ Wajib |
| **DAST (Dynamic Security Testing)**         | ❌ Belum| OWASP ZAP (direkomendasikan via CI/CD)  | ⭐⭐⭐⭐⭐ Wajib |
| **Container Image Scan**                    | ❌ Belum| Trivy Image Scan (bisa di CI/CD)        | ⭐⭐⭐⭐⭐ Wajib |
| **Code Quality & Security**                 | ❌ Belum| SonarQube Community                     | ⭐⭐⭐⭐ Disarankan |
| **IaC Scan (Terraform / K8s)**              | ❌ Belum| Checkov / Terrascan                     | ⭐⭐⭐⭐ Disarankan |
| **API Security Test**                       | ❌ Belum| Schemathesis / Postman                  | ⭐⭐⭐⭐ Disarankan |
| **SBOM (Software Bill of Materials)**       | ❌ Belum| Trivy SBOM / Syft                       | ⭐⭐⭐⭐ Disarankan |
| **Penetration Test**                        | ❌ Belum| Burp Suite / Manual Pentest             | ⭐⭐⭐ Enterprise |
| **Infrastructure & Network Scan**           | ❌ Belum| Nessus / OpenVAS                        | ⭐⭐⭐ Enterprise |
| **Kubernetes Security**                     | ❌ Belum| Kubescape / kube-bench                  | ⭐⭐⭐ Enterprise |
| **SIEM / Runtime Monitoring**               | ❌ Belum| Wazuh / Splunk / Elastic Security       | ⭐⭐⭐ Enterprise |
| **RASP (Runtime Application Self-Protection)** | ❌ Belum| (Belum ditentukan)                      | ⭐⭐⭐ Enterprise |

---

## Detail Implementasi Aktif

### 1. Gitleaks (Secret Scanning)
- **Posisi:** Pre-commit Hook (`.pre-commit-config.yaml`)
- **Tujuan:** Mencegah API Key, password basis data, JWT secret, dan rahasia lainnya ter-commit ke dalam repositori secara tidak sengaja.
- **Eksekusi Lokal:** `uv run pre-commit run gitleaks --all-files`

### 2. Bandit (SAST untuk Python/Django)
- **Posisi:** Pre-commit Hook (`.pre-commit-config.yaml`)
- **Tujuan:** Memeriksa kelemahan keamanan di kode sumber Python, seperti penggunaan fungsi `eval()`, *hardcoded password*, modul kriptografi yang rentan, dan kelemahan spesifik *framework* Django.
- **Eksekusi Lokal:** `uv run pre-commit run bandit --all-files`

### 3. Trivy (Dependency Vulnerability Scanner)
- **Posisi:** CI/CD Workflow (`.github/workflows/ci.yml`)
- **Tujuan:** Memindai file-file seperti `uv.lock` atau `pyproject.toml` untuk menemukan modul Python yang memiliki CVE (*Common Vulnerabilities and Exposures*) dengan tingkat keparahan HIGH atau CRITICAL.
- **Eksekusi:** Otomatis berjalan setiap kali ada *Push* atau *Pull Request*.

### 4. Pytest Security Regression
- **Posisi:** Suite Pengujian (`tests/test_security.py`)
- **Tujuan:** Memastikan konfigurasi `settings.production` aman. Memvalidasi bahwa fitur seperti `SECURE_SSL_REDIRECT`, HTTPS Cookies, X-Frame-Options, dan HSTS aktif.
- **Eksekusi:** `uv run pytest tests/test_security.py`

---

## Roadmap / Langkah Selanjutnya

1. **OWASP ZAP (DAST):** Menambahkan pemindaian pasif/aktif ke environment *staging* setelah aplikasi berhasil dideploy oleh GitHub Actions.
2. **Container Scan:** Jika ke depannya akan melakukan *build image* di CI/CD, tambahkan langkah `trivy image` sebelum melakukan *push* ke *container registry*.
3. **API Scan:** Tambahkan pengujian spesifik keamanan API (seperti JWT Bypass, Rate Limiting Bypass) di skrip Pytest atau menggunakan alat seperti Schemathesis.
