# Panduan Arsitektur & Deployment Django Monolith di Kubernetes (K8s)

Dokumen ini menjelaskan bagaimana aplikasi Django Monolith (seperti RDP Starter Kit) dapat dijalankan di atas **Kubernetes (K8s / k3s)** secara andal, skalabel, dan efisien dengan pemisahan database serta penanganan file persisten.

---

## 1. Mitos vs. Realitas: Django Monolith di Kubernetes

Banyak developer mengira Kubernetes *hanya untuk microservices*. **Ini keliru.**
Perusahaan raksasa dengan codebase Django monolith terbesar di dunia (seperti **Instagram**, **Sentry**, **Zapier**, dan **Mozilla**) menjalankan monolith Django mereka di atas Kubernetes.

Kuncinya adalah **bukan memecah kode menjadi ratusan repo microservice**, melainkan memecah **Peran Proses (Process Roles)** dari **satu image Docker yang sama** (*The 12-Factor App methodology*).

```mermaid
flowchart TD
    Client([Client Internet]) -->|HTTPS :443| Ingress[Kubernetes Ingress Controller / cert-manager]
    
    subgraph K8s Cluster [Kubernetes Cluster / Node Pool]
        Ingress -->|Load Balance| WebService[Service: rdp-web-svc]
        
        subgraph Web Pods [Auto-Scaling Pods: 2 hingga 20+ Replicas]
            WebService --> Pod1[Pod Web 1: Django Gunicorn]
            WebService --> Pod2[Pod Web 2: Django Gunicorn]
            WebService --> PodN[Pod Web N: Django Gunicorn]
        end

        subgraph Worker Pods [Async Workers]
            CeleryWorker1[Pod Celery Worker 1]
            CeleryWorker2[Pod Celery Worker 2]
            CeleryBeat[Pod Celery Beat: 1 Replica]
        end

        HPA[HPA: Horizontal Pod Autoscaler] -.->|Monitor CPU/RAM| WebPods
        Job[K8s Job: Pre-deploy Migration] -.->|Run Before Rolling Update| ExtDB
    end

    subgraph External Managed Infrastructure [Luar Cluster K8s]
        Pod1 -->|DATABASE_URL| ExtDB[(Managed PostgreSQL: AWS RDS / Cloud SQL)]
        Pod2 --> ExtDB
        Pod1 -->|CACHE_URL| ExtRedis[(Managed Redis / Memorystore)]
        CeleryWorker1 --> ExtRedis
        CeleryWorker1 --> ExtDB
        Pod1 -->|Media Uploads| ObjectStorage[(Cloud Object Storage: S3 / MinIO / GCS)]
    end
```

---

## 2. Empat Aturan Emas Django Monolith di Kubernetes

### 1. Database (PostgreSQL) Wajib di Luar K8s Pod (Managed DB)
- **Mengapa?** Pod Kubernetes didesain bersifat *ephemeral* (bisa mati, berpindah node, atau di-restart kapan saja). Menyimpan data database di dalam Pod tanpa setup volume dan replikasi multi-node yang kompleks sangat berisiko *data loss*.
- **Praktik Standar**: Gunakan **Managed PostgreSQL** (seperti AWS RDS, Google Cloud SQL, DigitalOcean Managed DB, atau dedicated database VM terpisah). Pod Django terhubung via variabel `DATABASE_URL`.

### 2. Media Uploads Wajib Menggunakan Object Storage (S3 / MinIO / GCS)
- **Mengapa?** Jika user mengunggah file avatar ke Pod Web 1, file tersebut tidak akan ada di Pod Web 2 jika disimpan di disk lokal.
- **Praktik Standar**: Gunakan pustaka `django-storages` yang mengarahkan media uploads langsung ke Cloud Object Storage (Amazon S3, Google Cloud Storage, atau MinIO).

### 3. Migrasi Database Menggunakan Kubernetes `Job`
- **Mengapa?** Jika Anda memiliki 10 replika Pod Web dan semuanya menjalankan `manage.py migrate` secara bersamaan saat startup, akan terjadi *race condition* dan penguncian tabel (*table lock error*).
- **Praktik Standar**: Jalankan `python manage.py migrate` sebagai **K8s Job** atau *Helm pre-upgrade hook* yang berjalan sekali sebelum Pod Web baru mulai di-*rolling update*.

### 4. File Statis di-Bake ke Image atau Dilayani via WhiteNoise / CDN
- RDP Starter Kit sudah dilengkapi **WhiteNoise** dan CDN, sehingga file statis otomatis tersedia di setiap Pod tanpa perlu volume NFS bersama yang lambat.

---

## 3. Contoh Manifest Kubernetes Siap Pakai

Berikut adalah spesifikasi K8s manifest untuk RDP Starter Kit:

### A. ConfigMap & Secret (`k8s/01-config.yaml`)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: rdp-secrets
type: Opaque
stringData:
  SECRET_KEY: "django-insecure-production-super-secret-key"
  DATABASE_URL: "postgresql://rdpuser:password@managed-db.internal:5432/rdp_db"
  CACHE_URL: "redis://managed-redis.internal:6379/0"
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: rdp-config
data:
  DEBUG: "False"
  ALLOWED_HOSTS: "app.example.com"
  CSRF_TRUSTED_ORIGINS: "https://app.example.com"
  SECURE_SSL_REDIRECT: "True"
  EMAIL_BACKEND: "smtp"
```

---

### B. Pre-Deployment Migration Job (`k8s/02-migration-job.yaml`)
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: rdp-migration-job
spec:
  ttlSecondsAfterFinished: 300
  template:
    spec:
      containers:
        - name: migrate
          image: registry.example.com/rdp-starterkit:latest
          command: ["python", "manage.py", "migrate", "--noinput"]
          envFrom:
            - configMapRef:
                name: rdp-config
            - secretRef:
                name: rdp-secrets
      restartPolicy: OnFailure
```

---

### C. Web Deployment, Service & HPA (`k8s/03-web.yaml`)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rdp-web
spec:
  replicas: 2
  selector:
    matchLabels:
      app: rdp-web
  template:
    metadata:
      labels:
        app: rdp-web
    spec:
      containers:
        - name: web
          image: registry.example.com/rdp-starterkit:latest
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: rdp-config
            - secretRef:
                name: rdp-secrets
          resources:
            requests:
              memory: "256Mi"
              cpu: "200m"
            limits:
              memory: "768Mi"
              cpu: "1000m"
          readinessProbe:
            httpGet:
              path: /
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /
              port: 8000
            initialDelaySeconds: 15
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: rdp-web-service
spec:
  selector:
    app: rdp-web
  ports:
    - port: 80
      targetPort: 8000
---
# Horizontal Pod Autoscaler: Auto scale dari 2 hingga 10 Pod saat CPU > 75%
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: rdp-web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: rdp-web
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 75
```

---

### D. Celery Worker & Beat Deployment (`k8s/04-celery.yaml`)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rdp-celery-worker
spec:
  replicas: 2
  selector:
    matchLabels:
      app: rdp-celery-worker
  template:
    metadata:
      labels:
        app: rdp-celery-worker
    spec:
      containers:
        - name: worker
          image: registry.example.com/rdp-starterkit:latest
          command: ["celery", "-A", "config", "worker", "--loglevel=INFO"]
          envFrom:
            - configMapRef:
                name: rdp-config
            - secretRef:
                name: rdp-secrets
          resources:
            requests:
              memory: "256Mi"
              cpu: "150m"
            limits:
              memory: "512Mi"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rdp-celery-beat
spec:
  replicas: 1 # Celery Beat WAJIB tepat 1 replika agar tidak memicu duplikasi tugas
  selector:
    matchLabels:
      app: rdp-celery-beat
  template:
    metadata:
      labels:
        app: rdp-celery-beat
    spec:
      containers:
        - name: beat
          image: registry.example.com/rdp-starterkit:latest
          command: ["celery", "-A", "config", "beat", "--loglevel=INFO"]
          envFrom:
            - configMapRef:
                name: rdp-config
            - secretRef:
                name: rdp-secrets
```

---

### E. Ingress & SSL Auto-Cert (`k8s/05-ingress.yaml`)
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: rdp-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/proxy-body-size: "25m"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - app.example.com
      secretName: rdp-tls-cert
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: rdp-web-service
                port:
                  number: 80
```

---

## 4. Rekomendasi: Jalur Transisi Bertahap (k3s)

Jika Anda ingin mencoba kekuatan Kubernetes tanpa biaya ribuan dollar per bulan:
1. **Gunakan k3s (Lightweight Kubernetes)**: k3s dapat diinstall di 1 VPS murah (misal 4GB RAM) hanya dengan 1 perintah:
   ```bash
   curl -sfL https://get.k3s.io | sh -
   ```
2. Anda mendapatkan seluruh fitur Kubernetes asli (kubectl, ingress, cert-manager, auto-healing) dengan konsumsi resource yang sangat ramah kantong.
