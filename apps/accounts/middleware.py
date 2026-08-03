from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class ForceChangePasswordMiddleware:
    """
    TUJUAN: Memaksa user yang memiliki flag must_change_password=True di extra_data
    untuk mengganti password sebelum bisa mengakses halaman lain (kecuali halaman ganti password & logout).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # URLs yang diizinkan saat harus ganti password
            allowed_urls = [
                reverse('accounts:force_password_change'),
                reverse('accounts:logout'),
            ]
            
            # Cek extra_data dari profile
            profile = getattr(request.user, 'profile', None)
            must_change = False
            if profile and isinstance(profile.extra_data, dict):
                must_change = profile.extra_data.get('must_change_password', False)
                
            if must_change and request.path not in allowed_urls:
                # Hindari redirect loop untuk static files / API yang tidak relevan
                if not request.path.startswith('/static/') and not request.path.startswith('/api/'):
                    messages.warning(request, "Anda harus mengubah password default Anda sebelum melanjutkan.")
                    return redirect('accounts:force_password_change')

        response = self.get_response(request)
        return response
