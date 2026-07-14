"""
Decorators untuk apps/core.
US: US-020 — Authorization (Permission & Group)
"""

from .auth_decorators import group_required, role_required

__all__ = [
    "group_required",
    "role_required",
]
