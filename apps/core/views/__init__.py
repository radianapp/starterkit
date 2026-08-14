"""
Views untuk core module.
"""

from .dev import DevComponentsView
from .rdp_ui import RdpUiLandingView

try:
    from .starter import (
        StarterComponentsView,
        StarterDocsView,
        StarterExamplesView,
        StarterLayoutView,
    )
except ImportError:
    StarterComponentsView = StarterDocsView = StarterExamplesView = StarterLayoutView = None

__all__ = [
    "DevComponentsView",
    "RdpUiLandingView",
    "StarterComponentsView",
    "StarterDocsView",
    "StarterExamplesView",
    "StarterLayoutView",
]
