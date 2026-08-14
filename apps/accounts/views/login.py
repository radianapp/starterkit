"""
View untuk login dan logout.
US: US-005 — Login
US: US-006 — Logout

TUJUAN: Autentikasi user via email+password, session management.

ALUR (Login GET):
  1. Render halaman login dengan LoginForm kosong

ALUR (Login POST):
  1. Validasi LoginForm — authenticate() di dalam form.clean()
  2. Jika invalid → re-render dengan error (HTTP 422 untuk HTMX)
  3. Jika valid → login() → redirect ke next atau dashboard

ALUR (Logout POST):
  1. logout() → redirect ke login page

DIPANGGIL DARI: apps/accounts/urls.py
DEPENDENSI: apps.accounts.forms.login.LoginForm
"""

from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from apps.accounts.forms.login import LoginForm

# Default redirect setelah login jika tidak ada ?next=
_LOGIN_REDIRECT = "/"
_LOGOUT_REDIRECT = "/"
# Durasi session saat remember_me=False: expire saat browser ditutup
_SESSION_EXPIRE_BROWSER_CLOSE = 0


@require_http_methods(["GET", "POST"])
def user_login(request):
    """
    TUJUAN: Handle login form — GET render, POST autentikasi.

    ALUR:
      1. Redirect ke dashboard jika sudah login
      2. GET → render login.html dengan form kosong
      3. POST → validasi form → login() + redirect atau re-render error

    DIPANGGIL DARI: accounts:login URL
    """
    # Sudah login — redirect ke target aman (bukan login page lagi)
    if request.user.is_authenticated:
        next_url = request.GET.get("next") or _LOGIN_REDIRECT
        if next_url and not next_url.startswith("/accounts/login"):
            return redirect(next_url)
        return redirect("admin:index")

    is_htmx = request.headers.get("HX-Request") == "true"

    next_url = request.GET.get("next") or request.POST.get("next") or _LOGIN_REDIRECT
    # Validasi next URL — hanya redirect ke path internal (cegah open redirect)
    if not next_url.startswith("/"):
        next_url = _LOGIN_REDIRECT

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if not form.is_valid():
            ctx = {"form": form, "next": next_url}
            # HTMX: return fragment saja agar target #login-form bisa di-swap
            template = "accounts/partials/login_form.html" if is_htmx else "accounts/login.html"
            return render(request, template, ctx, status=422)

        user = form.get_user()

        # KEPUTUSAN TEKNIS: Session expire saat browser tutup jika remember_me=False
        # ALASAN: Keamanan — tidak meninggalkan session aktif di shared computer
        # ALTERNATIF: Selalu pakai SESSION_COOKIE_AGE dari settings
        if not form.cleaned_data.get("remember_me"):
            request.session.set_expiry(_SESSION_EXPIRE_BROWSER_CLOSE)

        login(request, user)

        if is_htmx:
            response = render(request, "accounts/partials/login_success.html", {})
            response["HX-Redirect"] = next_url
            return response
        return redirect(next_url)

    from django.conf import settings

    form = LoginForm(request)
    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
            "next": request.GET.get("next", ""),
            "enable_registration": getattr(settings, "ENABLE_USER_REGISTRATION", True),
            "enable_google_auth": getattr(settings, "ENABLE_GOOGLE_AUTH", False),
        },
    )


@require_POST
def user_logout(request):
    """
    TUJUAN: Logout user dan redirect ke halaman login.

    ALUR:
      1. Panggil logout() — clear session
      2. Redirect ke login page

    DIPANGGIL DARI: accounts:logout URL
    """
    logout(request)
    return redirect(_LOGOUT_REDIRECT)
