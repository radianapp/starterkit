"""
Views untuk core module.
"""

from .dev import DevComponentsView
from .rdp_ui import RdpUiLandingView
from .rdp_ui_token_test import RdpUiTokenTestView
from .rdp_ui_layout_test import RdpUiLayoutTestView
from .rdp_ui_components_test import RdpUiComponentsTestView

__all__ = ["DevComponentsView", "RdpUiLandingView", "RdpUiTokenTestView", "RdpUiLayoutTestView", "RdpUiComponentsTestView"]
