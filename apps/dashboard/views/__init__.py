"""
Views package untuk dashboard app.
US: US-032 — Dashboard default dengan demo data
"""

from .changelog import SystemUpdateListView
from .index import dashboard_index
from .stats import dashboard_stats_htmx

__all__ = [
    "SystemUpdateListView",
    "dashboard_index",
    "dashboard_stats_htmx",
]
