"""
View untuk registration wizard.
US: US-004 — Register akun baru

TUJUAN: Multi-step registration wizard via session + HTMX partial swap.

ALUR:
  1. GET /accounts/register/ → render shell page (register.html) + step 0 (email)
  2. POST step 0 valid → simpan email ke session → render step berikutnya (partial)
  3. POST step 1..N (dynamic steps) valid → simpan ke session → advance
  4. POST step final (password) valid → create_user_from_wizard() → auto-login → redirect dashboard

Session key: 'reg_wizard' = {current: int, email: str, extra: dict}
HTMX: swap target #wizard-content — setiap POST return partial fragment saja

DIPANGGIL DARI: apps/accounts/urls.py
DEPENDENSI: settings.REGISTRATION_STEPS, forms.register, services.user_service
"""

from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.accounts.forms.register import DynamicStepForm, EmailStepForm, PasswordStepForm
from apps.accounts.services.email_service import send_verification_email
from apps.accounts.services.user_service import create_user_from_wizard

# Kunci session wizard — satu halaman saja, tidak perlu namespace lebih
_SESSION_KEY = "reg_wizard"


def _init_wizard(request) -> dict:
    """
    TUJUAN: Ambil atau inisialisasi state wizard dari session.
    """
    return request.session.get(_SESSION_KEY, {"current": 0, "email": "", "extra": {}})


def _save_wizard(request, wizard: dict):
    """
    TUJUAN: Simpan state wizard ke session dan tandai session modified.
    """
    request.session[_SESSION_KEY] = wizard
    request.session.modified = True


def _clear_wizard(request):
    """
    TUJUAN: Hapus state wizard dari session setelah selesai.
    """
    request.session.pop(_SESSION_KEY, None)


def _get_step_form(step_index: int, steps: list, data=None):
    """
    TUJUAN: Return form instance yang sesuai dengan step_index.

    ALUR:
      - step 0 → EmailStepForm
      - step 1..len(steps) → DynamicStepForm dengan step_def dari REGISTRATION_STEPS
      - step len(steps)+1 → PasswordStepForm (step terakhir)
    """
    if step_index == 0:
        return EmailStepForm(data)
    dynamic_count = len(steps)
    if step_index <= dynamic_count:
        step_def = steps[step_index - 1]
        return DynamicStepForm(step_def, data)
    return PasswordStepForm(data)


def _get_step_template(step_index: int, steps: list) -> str:
    """
    TUJUAN: Return path template partial sesuai step_index.
    """
    if step_index == 0:
        return "accounts/partials/step_email.html"
    if step_index <= len(steps):
        return "accounts/partials/step_dynamic.html"
    return "accounts/partials/step_password.html"


@require_http_methods(["GET", "POST"])
def register_wizard(request):
    """
    TUJUAN: Handle semua step registration wizard dalam satu URL.

    ALUR (GET):
      1. Inisialisasi / ambil state wizard dari session
      2. Render register.html (shell) + partial step saat ini

    ALUR (POST):
      1. Validasi form step saat ini
      2. Jika invalid → return partial dengan error (HTMX swap)
      3. Jika valid dan bukan step terakhir → advance step → return partial step berikutnya
      4. Jika valid dan step terakhir → create user → auto-login → redirect dashboard

    DIPANGGIL DARI: urls.py path("register/", ...)
    """
    steps = getattr(settings, "REGISTRATION_STEPS", [])
    total_steps = 2 + len(steps)  # email + N dynamic + password
    final_step = total_steps - 1

    wizard = _init_wizard(request)
    current = wizard["current"]

    is_htmx = request.headers.get("HX-Request") == "true"

    if request.method == "POST":
        form = _get_step_form(current, steps, request.POST)

        if not form.is_valid():
            # Error: return partial saja (HTMX swap target #wizard-content)
            ctx = _build_step_ctx(current, final_step, steps, wizard, form)
            return render(request, _get_step_template(current, steps), ctx, status=422)

        # Valid — simpan data ke session
        if current == 0:
            wizard["email"] = form.cleaned_data["email"]
        elif current <= len(steps):
            step_def = steps[current - 1]
            wizard["extra"][step_def["key"]] = form.cleaned_data[step_def["key"]]
        else:
            # Step terakhir: buat user
            password = form.cleaned_data["password1"]
            user = create_user_from_wizard(
                email=wizard["email"],
                password=password,
                extra=wizard["extra"],
            )
            _clear_wizard(request)
            # US-008: Kirim email verifikasi setelah user dibuat
            send_verification_email(user, request)
            login(request, user, backend="apps.accounts.backends.EmailOrUsernameBackend")
            if is_htmx:
                # HTMX redirect: set header HX-Redirect, return 200 kosong
                response = render(request, "accounts/partials/step_success.html", {})
                response["HX-Redirect"] = "/"
                return response
            return redirect("/")

        # Advance ke step berikutnya
        wizard["current"] = current + 1
        _save_wizard(request, wizard)

        next_step = current + 1
        form_next = _get_step_form(next_step, steps)
        ctx = _build_step_ctx(next_step, final_step, steps, wizard, form_next)
        return render(request, _get_step_template(next_step, steps), ctx)

    # GET — render shell page + partial step saat ini
    form = _get_step_form(current, steps)
    ctx = _build_step_ctx(current, final_step, steps, wizard, form)
    shell_ctx = {
        **ctx,
        "total_steps": total_steps,
        "step_labels": _get_step_labels(steps),
    }
    return render(request, "accounts/register.html", shell_ctx)


def _get_step_labels(steps: list) -> list:
    """
    TUJUAN: Return list label untuk progress bar.
    """
    return ["Email", *[s["label"] for s in steps], "Password"]


def _build_step_ctx(step: int, final_step: int, steps: list, wizard: dict, form) -> dict:
    """
    TUJUAN: Build context dict yang dipakai di semua step template.
    """
    ctx = {
        "form": form,
        "current_step": step,
        "final_step": final_step,
        "wizard": wizard,
        "is_last_step": step == final_step,
    }
    # Context tambahan untuk step dynamic
    if 0 < step <= len(steps):
        ctx["step_def"] = steps[step - 1]
    # Summary di step password
    if step == final_step and wizard.get("extra"):
        ctx["summary"] = [
            {"label": s["label"], "value": wizard["extra"].get(s["key"], "-")} for s in steps
        ]
    return ctx
