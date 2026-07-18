"""
Views package untuk dashboard app.
US: US-032 — Dashboard default dengan demo data
"""

from .index import dashboard_index
from .changelog import SystemUpdateListView
from .stats import dashboard_stats_htmx

__all__ = [
    "dashboard_index",
    "SystemUpdateListView",
    "dashboard_stats_htmx",
]
