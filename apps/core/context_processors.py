from django.conf import settings


def debug_settings(request):
    """
    Context processor kustom untuk mengekspos variabel DEBUG, RDP_DEBUG_OVERLAY, dan brand variables ke template.
    """
    return {
        "DEBUG": settings.DEBUG,
        "RDP_DEBUG_OVERLAY": getattr(settings, "RDP_DEBUG_OVERLAY", settings.DEBUG),
        "SITE_NAME": getattr(settings, "SITE_NAME", "RDP Starter Kit"),
        "COMPANY_NAME": getattr(settings, "COMPANY_NAME", "Radian Data Platform"),
        "APP_BRAND_SHORT": getattr(settings, "APP_BRAND_SHORT", "RDP"),
        "COPYRIGHT_YEAR": getattr(settings, "COPYRIGHT_YEAR", "2026"),
        "RDP_UI_VERSION": getattr(settings, "RDP_UI_VERSION", "v1.0"),
        "RDP_UI_SELF_HOST": getattr(settings, "RDP_UI_SELF_HOST", False),
        "RDP_APP_ACCENT": getattr(settings, "RDP_APP_ACCENT", "navy"),
    }
