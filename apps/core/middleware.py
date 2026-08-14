"""
Middleware kustom RDP Starter Kit.
US: US-008 — Verifikasi email

TUJUAN: Enforce email verification jika REQUIRE_EMAIL_VERIFICATION=True.
User yang belum verify diarahkan ke halaman "cek email" — kecuali URL
yang diizinkan (login, logout, verify email, admin, static).

DIPANGGIL DARI: config/settings/base.py MIDDLEWARE list
DEPENDENSI: settings.REQUIRE_EMAIL_VERIFICATION
"""

from django.conf import settings
from django.shortcuts import redirect

# URL prefix yang diizinkan tanpa verifikasi
_ALLOWED_PREFIXES = (
    "/accounts/login/",
    "/accounts/logout/",
    "/accounts/verify-email/",
    "/accounts/password-reset/",
    "/admin/",
    "/static/",
    "/media/",
    "/__debug__/",
)


class EmailVerificationMiddleware:
    """
    TUJUAN: Redirect user terautentikasi yang belum verifikasi email
    ke halaman verify_required jika REQUIRE_EMAIL_VERIFICATION=True.

    ALUR:
      1. Cek REQUIRE_EMAIL_VERIFICATION — skip jika False
      2. Cek user authenticated — skip jika tidak
      3. Cek email_verified — skip jika sudah
      4. Cek URL — skip jika di _ALLOWED_PREFIXES
      5. Redirect ke accounts:verify_required

    DIPANGGIL DARI: Django middleware pipeline (setiap request)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            getattr(settings, "REQUIRE_EMAIL_VERIFICATION", False)
            and request.user.is_authenticated
            and not getattr(request.user, "email_verified", True)
            and not any(request.path.startswith(p) for p in _ALLOWED_PREFIXES)
        ):
            return redirect("accounts:verify_required")

        return self.get_response(request)


import threading
import uuid

_trace_context = threading.local()


def get_current_trace_id() -> str | None:
    """Mengambil trace_id dari konteks thread saat ini."""
    return getattr(_trace_context, "trace_id", None)


def set_current_trace_id(trace_id: str) -> None:
    """Mengatur trace_id untuk konteks thread saat ini."""
    _trace_context.trace_id = trace_id


class TraceMiddleware:
    """
    Inject Correlation ID (trace_id) ke setiap HTTP request untuk kebutuhan
    reverse engineering, observability, dan debug tracing.
    US: US-014 — Telemetry & Logging Terstruktur
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
        set_current_trace_id(trace_id)
        request.trace_id = trace_id

        response = self.get_response(request)
        response["X-Trace-ID"] = trace_id
        return response
