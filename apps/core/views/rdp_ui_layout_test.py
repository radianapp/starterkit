from django.views.generic import TemplateView


class RdpUiLayoutTestView(TemplateView):
    template_name = "rdp_ui/layout_test.html"
