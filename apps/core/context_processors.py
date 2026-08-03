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
        "FRAMEWORK_VERSION": getattr(settings, "FRAMEWORK_VERSION", "0.3.0"),
        "LOCAL_APP_VERSION": getattr(settings, "LOCAL_APP_VERSION", "1.0.0"),
        "APP_VERSION_DATE": getattr(settings, "LOCAL_APP_VERSION_DATE", ""),
        "APP_VERSION_BY": getattr(settings, "LOCAL_APP_VERSION_BY", "System"),
        "APP_VERSION_DESC": getattr(settings, "LOCAL_APP_VERSION_DESC", ""),
        "RDP_APP_THEME": getattr(settings, "RDP_APP_THEME", "default"),
        "RDP_THEME_LIST": getattr(settings, "RDP_THEME_LIST", [
            "default", "light", "dark", "midnight",
            "forest", "ocean", "nord", "dracula",
            "terminal", "corporate", "github",
        ]),
        "TURNSTILE_ENABLED": getattr(settings, "TURNSTILE_ENABLED", False),
        "TURNSTILE_SITE_KEY": getattr(settings, "TURNSTILE_SITE_KEY", ""),
    }
