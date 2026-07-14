"""
View untuk halaman Token Test RDP UI.
Menampilkan semua token design system dan 11 tema secara bersamaan.
US: Phase 1 & 2 — Token & Theme showcase
"""

from django.views.generic import TemplateView


THEMES = [
    {"id": "default",   "label": "Default",    "swatch": "#15654E", "dark": False, "desc": "Warm paper · RDP original"},
    {"id": "light",     "label": "Light",      "swatch": "#2A5FA8", "dark": False, "desc": "Neutral cool blue"},
    {"id": "corporate", "label": "Corporate",  "swatch": "#24427C", "dark": False, "desc": "Slate & navy"},
    {"id": "ocean",     "label": "Ocean",      "swatch": "#0E7490", "dark": False, "desc": "Sea glass cyan"},
    {"id": "forest",    "label": "Forest",     "swatch": "#2F6B3C", "dark": False, "desc": "Moss & linen"},
    {"id": "github",    "label": "GitHub",     "swatch": "#0969DA", "dark": False, "desc": "Canonical GitHub light"},
    {"id": "dark",      "label": "Dark",       "swatch": "#5FA98C", "dark": True,  "desc": "Warm ink"},
    {"id": "midnight",  "label": "Midnight",   "swatch": "#8FA8EC", "dark": True,  "desc": "Deep indigo"},
    {"id": "nord",      "label": "Nord",       "swatch": "#88C0D0", "dark": True,  "desc": "Canonical Nord"},
    {"id": "dracula",   "label": "Dracula",    "swatch": "#BD93F9", "dark": True,  "desc": "Canonical Dracula"},
    {"id": "terminal",  "label": "Terminal",   "swatch": "#4ADE80", "dark": True,  "desc": "Phosphor green"},
]


class RdpUiTokenTestView(TemplateView):
    """
    Halaman showcase design tokens dan 11 tema RDP UI.

    Menampilkan:
    - Color swatches semua semantic tokens
    - Typography scale
    - Spacing, Radius, Shadow visual reference
    - Theme gallery: 11 mini-cards side by side
    - Live theme switcher
    """

    template_name = "rdp_ui/token_test.html"

    def get_context_data(self, **kwargs: object) -> dict:
        """Inject daftar tema dan token metadata ke context template."""
        context = super().get_context_data(**kwargs)
        context["themes"] = THEMES
        context["theme_count"] = len(THEMES)
        context["page_title"] = "RDP UI — Token & Theme Showcase"
        return context
