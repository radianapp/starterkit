# Cookbook: Form Multi-Step (Wizard) Menggunakan HTMX

Resep ini menjelaskan cara membuat alur pengisian form multi-step (wizard) tanpa memuat ulang halaman secara penuh.

---

## Prinsip Kerja
Setiap langkah (*step*) dalam wizard adalah fragmen HTML parsial. HTMX menukar konten kontainer wizard berdasarkan langkah aktif yang diminta oleh pengguna.

---

## Langkah 1: Buat Halaman Induk Wizard
Halaman ini bertindak sebagai penampung langkah pertama:
```html
{# templates/wizard/wizard_index.html #}
<c-layout.app title="Wizard Pendaftaran">
    <div class="wizard-steps-indicator">
        <!-- Indikator visual progres -->
    </div>
    
    <div id="wizard-container" hx-target="this" hx-swap="innerHTML">
        {% include "wizard/partials/step_1.html" %}
    </div>
</c-layout.app>
```

---

## Langkah 2: Buat Template untuk Setiap Langkah

### Langkah 1 (`templates/wizard/partials/step_1.html`):
```html
<form hx-post="{% url 'wizard:step_1' %}">
    {% csrf_token %}
    <h3>Langkah 1: Informasi Dasar</h3>
    <label>Nama Lengkap:
        <input type="text" name="full_name" value="{{ data.full_name }}" required>
    </label>
    <button type="submit">Lanjut</button>
</form>
```

### Langkah 2 (`templates/wizard/partials/step_2.html`):
```html
<form hx-post="{% url 'wizard:step_2' %}">
    {% csrf_token %}
    <h3>Langkah 2: Informasi Tambahan</h3>
    <label>Alamat:
        <input type="text" name="address" value="{{ data.address }}" required>
    </label>
    
    <button type="button" class="secondary" hx-get="{% url 'wizard:step_1' %}">Kembali</button>
    <button type="submit">Simpan & Selesai</button>
</form>
```

---

## Langkah 3: Mengelola State di Django View
Gunakan sesi (`request.session`) untuk mempertahankan data antar langkah:

```python
from django.shortcuts import render
from django.views import View

class Step1View(View):
    def get(self, request):
        data = request.session.get('wizard_data', {})
        return render(request, "wizard/partials/step_1.html", {"data": data})

    def post(self, request):
        # Ambil data lama & update
        data = request.session.get('wizard_data', {})
        data['full_name'] = request.POST.get('full_name')
        request.session['wizard_data'] = data
        
        # Lanjut ke langkah 2
        return render(request, "wizard/partials/step_2.html", {"data": data})

class Step2View(View):
    def post(self, request):
        data = request.session.get('wizard_data', {})
        data['address'] = request.POST.get('address')
        
        # Simpan ke Database
        # UserProfile.objects.create(**data)
        
        # Bersihkan session
        request.session['wizard_data'] = {}
        
        return render(request, "wizard/partials/success.html")
```
