from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator


@method_decorator(login_required, name="dispatch")
class ForcePasswordChangeView(PasswordChangeView):
    template_name = "accounts/force_password_change.html"
    success_url = reverse_lazy("dashboard:index")

    def form_valid(self, form):
        response = super().form_valid(form)

        # Clear must_change_password flag
        profile = getattr(self.request.user, "profile", None)
        if profile and isinstance(profile.extra_data, dict):
            if "must_change_password" in profile.extra_data:
                profile.extra_data.pop("must_change_password")
                profile.save(update_fields=["extra_data"])

        messages.success(self.request, "Password berhasil diubah. Selamat datang!")
        return response
