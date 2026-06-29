"""
URL configuration untuk accounts app.
US: US-004, US-005, US-006, US-007, US-008, US-009

TUJUAN: Route semua auth-related URLs.

ALUR:
  1. Setup login, register, logout, forgot-password, reset-password, profile, dll.
  2. Gunakan app_name="accounts" untuk reverse URL dengan namespace
  3. Setup path() untuk setiap view
"""

from django.urls import path

app_name = "accounts"

# 🚧 TODO: Views untuk auth belum diimplementasikan di Fase 1
# Akan ditambahkan di Fase 3 (US-004 sampai US-009)
urlpatterns = []
