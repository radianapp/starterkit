"""
Error views untuk handling HTTP errors (403, 404, 500).
US: US-015 — Error pages kustom (403, 404, 500)

TUJUAN: Menampilkan halaman error yang konsisten dengan branding project.
"""

from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token


@requires_csrf_token
def permission_denied_view(request, exception=None):
    """
    TUJUAN: Handle HTTP 403 Forbidden error.

    ALUR:
      1. Log permission denied event
      2. Render template 403.html dengan context
      3. Return response dengan status 403

    DIPANGGIL DARI: Django error handler (config/urls.py)
    DEPENDENSI: templates/errors/403.html
    """
    return render(request, "errors/403.html", status=403)


def page_not_found_view(request, exception=None):
    """
    TUJUAN: Handle HTTP 404 Not Found error.

    ALUR:
      1. Log page not found event
      2. Render template 404.html dengan context
      3. Return response dengan status 404

    DIPANGGIL DARI: Django error handler (config/urls.py)
    DEPENDENSI: templates/errors/404.html
    """
    return render(request, "errors/404.html", status=404)


@requires_csrf_token
def server_error_view(request):
    """
    TUJUAN: Handle HTTP 500 Internal Server Error.

    ALUR:
      1. Log server error dengan full traceback
      2. Render template 500.html (tidak ekspos traceback ke user)
      3. Return response dengan status 500

    DIPANGGIL DARI: Django error handler (config/urls.py)
    DEPENDENSI: templates/errors/500.html
    """
    return render(request, "errors/500.html", status=500)
