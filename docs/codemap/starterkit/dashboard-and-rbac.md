# Code Map & Tracing Matrix: Dashboard & RBAC Management

Dokumen ini mendokumentasikan pemetaan kode lengkap (*Code Map*) untuk alur **Dashboard Utama, Manajemen Pengguna, Audit Trail, & Granular RBAC Permissions**.

---

## 1. Tracing Matrix: Dashboard & Administrative Events

### A. Dashboard Utama & Widget Analytics (`US-010`) — Status: `[x] Selesai`

| Step | User Event (UI) | Route / URL Name | View Class / FBV | Service Layer | Data Model | Telemetry / Log | Status |
|---|---|---|---|---|---|---|---|
| 1 | Akses Halaman Dashboard | `/dashboard/` (`dashboard:index`) | [DashboardIndexView](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/dashboard/views/index.py) | `dashboard_service.py` | `User`, `UserActivityLog` | HTTP 200 | `[x]` |
| 2 | Partial Refresh Widget Stats | `hx-get="/dashboard/stats/"` | [DashboardStatsView](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/dashboard/views/stats.py) | - | Dynamic ORM Aggregations | HTMX Partial Render | `[x]` |
| 3 | Lihat System Changelog | `/dashboard/changelog/` | [ChangelogView](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/dashboard/views/changelog.py) | - | `SystemChangelog` | HTTP 200 | `[x]` |

---

### B. User Management & Granular Permissions (`US-011`, `US-012`) — Status: `[x] Selesai`

| Step | User Event (UI) | Route / URL Name | View Class / FBV | Service Layer | Data Model | Telemetry / Log | Status |
|---|---|---|---|---|---|---|---|
| 1 | List Seluruh User | `/dashboard/users/` (`accounts:user_list`) | [UserListView](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/views/users.py#L40) | `rbac_service.py` | `User` | Paged Search ORM | `[x]` |
| 2 | Modal Edit User & Roles | `hx-get="/dashboard/users/<id>/edit/"` | [UserEditView](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/views/users.py#L120) | [rbac_service.py](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/services/rbac_service.py) | `User`, `Group`, `Permission` | HTMX Modal Partial | `[x]` |
| 3 | Save User Permissions | `hx-post="/dashboard/users/<id>/edit/"` | [UserEditView.post](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/views/users.py#L150) | [update_user_permissions](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/services/rbac_service.py) | `User.user_permissions` | `UserActivityLog` | `[x]` |
| 4 | Toggle User Active Status | `hx-post="/dashboard/users/<id>/toggle-active/"` | [UserToggleActiveView](file:///c:/Users/rahad/Work/org/rdp/starterkit/apps/accounts/views/users.py#L200) | `user_service.py` | `User.is_active` | `HX-Trigger: userUpdated` | `[x]` |

---

### C. Audit Trail & System Log (`US-028`) — Status: `[x] Selesai`

| Step | User Event (UI) | Route / URL Name | View Class / FBV | Service Layer | Data Model | Telemetry / Log | Status |
|---|---|---|---|---|---|---|---|
| 1 | Monitoring Aktivitas User | `/dashboard/activities/` | `ActivityLogListView` | `activity_service.py` | `UserActivityLog` | Audit Log View | `[x]` |
| 2 | Telemetry Trace Logs | Internal API / Admin | - | `middleware.py` | `ExecutionTraceLog` | `X-Trace-ID` Tracing | `[x]` |

---

### D. Multi-Tenancy / Organization Isolation (`US-027`) — Status: `[-] Sebagian`

| Step | User Event (UI) | Route / URL Name | View Class / FBV | Service Layer | Data Model | Telemetry / Log | Status |
|---|---|---|---|---|---|---|---|
| 1 | Organization Model & FK | - | - | - | `Organization` Model | Schema DB | `[-]` |
| 2 | Tenant Middleware Isolation | Dynamic Subdomain | `TenantMiddleware` | - | Context Tenant | Subdomain Routing | `[ ]` |

---

## 2. Struktur Komponen Dashboard & Admin Codebase

```text
apps/dashboard/
├── admin.py                   ← Admin Interface untuk Activity & Changelog
├── models/
│   ├── activity.py            ← UserActivityLog (Model Pencatatan Audit Trail)
│   └── changelog.py           ← SystemChangelog (Pencatatan Versi Aplikasi)
├── urls.py                    ← Dashboard Routing Namespace (`dashboard:`)
└── views/
    ├── changelog.py           ← View Pengolahan Versi Aplikasi
    ├── index.py               ← Main Dashboard View (Overview Cards & Charts)
    └── stats.py               ← HTMX Partial Endpoint untuk Widget Refresh Fast-Path
```
