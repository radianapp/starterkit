"""
Utility helper functions untuk integrasi HTMX dengan Django.
US: US-037 — HTMX backend helpers (Extras)
"""

import json

from django.http import HttpResponse


def is_htmx(request) -> bool:
    """
    Memeriksa apakah request saat ini dikirimkan via HTMX.
    """
    return request.headers.get("HX-Request") == "true"


def htmx_redirect(url: str) -> HttpResponse:
    """
    Mengembalikan HttpResponse kosong yang memberi instruksi kepada HTMX
    untuk melakukan redirect penuh ke URL yang ditentukan client-side.
    """
    response = HttpResponse("")
    response["HX-Redirect"] = url
    return response


def htmx_refresh() -> HttpResponse:
    """
    Mengembalikan HttpResponse kosong yang memberi instruksi kepada HTMX
    untuk menyegarkan (refresh) halaman saat ini client-side.
    """
    response = HttpResponse("")
    response["HX-Refresh"] = "true"
    return response


def htmx_trigger(response: HttpResponse, event_name: str, params: dict = None) -> HttpResponse:
    """
    Menambahkan header HX-Trigger ke response untuk memicu event kustom di sisi client (browser).
    """
    trigger_data = {}

    # Ambil data trigger yang sudah ada jika ada
    if "HX-Trigger" in response:
        try:
            existing = response["HX-Trigger"]
            if existing.startswith("{"):
                trigger_data = json.loads(existing)
            else:
                trigger_data = {existing: ""}
        except Exception:
            pass

    if params is None:
        trigger_data[event_name] = ""
    else:
        trigger_data[event_name] = params

    response["HX-Trigger"] = json.dumps(trigger_data)
    return response
