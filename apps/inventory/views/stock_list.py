from django.views.generic import TemplateView

class StockListView(TemplateView):
    template_name = "inventory/partials/stock_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Tambahkan context di sini
        return context
