import json

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from apps.accounts.models import PasskeyCredential
from apps.accounts.services.webauthn_service import (
    generate_authentication_challenge,
    generate_registration_challenge,
    verify_and_save_registration,
    verify_authentication,
)


@require_http_methods(["POST"])
@login_required
def register_challenge(request):
    """
    Men-generate challenge untuk registrasi passkey baru.
    (Khusus untuk user yang sudah login)
    """
    try:
        options = generate_registration_challenge(request, request.user)
        return JsonResponse(options)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@require_http_methods(["POST"])
@login_required
def register_verify(request):
    """
    Memverifikasi respons dari navigator.credentials.create()
    """
    try:
        data = json.loads(request.body)
        device_name = data.pop("device_name", "Passkey Device")

        verify_and_save_registration(request, request.user, data, device_name)

        # Kembalikan response untuk HTMX agar refresh list perangkat
        response = HttpResponse()
        response["HX-Trigger"] = "passkeyRegistered"
        return response
    except Exception as e:
        return HttpResponseBadRequest(str(e))


@require_http_methods(["POST"])
def login_challenge(request):
    """
    Men-generate challenge untuk login via passkey.
    (Bisa diakses tanpa login)
    """
    try:
        options = generate_authentication_challenge(request)
        return JsonResponse(options)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@require_http_methods(["POST"])
def login_verify(request):
    """
    Memverifikasi respons dari navigator.credentials.get() dan login.
    """
    try:
        data = json.loads(request.body)
        user = verify_authentication(request, data)

        if not user.is_active:
            return HttpResponseBadRequest("Akun tidak aktif.")

        login(request, user)

        # Trigger redirect via HTMX
        response = HttpResponse()
        response["HX-Redirect"] = "/dashboard/"
        return response
    except Exception as e:
        return HttpResponseBadRequest(str(e))


@require_http_methods(["DELETE"])
@login_required
def delete_passkey(request, pk):
    """
    Menghapus passkey (hanya milik user sendiri)
    """
    try:
        passkey = PasskeyCredential.objects.get(pk=pk, user=request.user)
        passkey.delete()

        response = HttpResponse()
        response["HX-Trigger"] = "passkeyDeleted"
        return response
    except PasskeyCredential.DoesNotExist:
        return HttpResponseBadRequest("Passkey tidak ditemukan.")
