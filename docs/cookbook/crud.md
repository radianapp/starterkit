# Cookbook: Membuat Fitur CRUD Baru dengan HTMX

Resep ini menjelaskan langkah demi langkah untuk membuat fitur CRUD (Create, Read, Update, Delete) lengkap menggunakan pola Django + Django-Cotton + HTMX tanpa muat ulang halaman secara penuh.

## Skenario
Kita akan membuat modul pengelolaan data "Buku" (`Book`) dengan field `title`, `author`, dan `published_date`.

---

## Langkah 1: Buat Django App Baru (Mengikuti SOP Paket)
Jalankan perintah berikut untuk membuat app `books`:
```bash
uv run python manage.py startapp books --template=scripts/app_template
```
*Catatan: Pastikan struktur folder `books` menggunakan folder paket untuk `models/`, `views/`, `services/`, dll.*

---

## Langkah 2: Definisikan Model
Tambahkan model di `books/models/book.py`:
```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    def __str__(self):
        return self.title
```
Daftarkan pada `books/models/__init__.py`:
```python
from .book import Book
```

---

## Langkah 3: Buat Form
Di `books/forms/book_forms.py`:
```python
from django import forms
from books.models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date']
```

---

## Langkah 4: Tulis Logika Bisnis (Service)
Pisahkan logika penyimpanan data ke `books/services/book_service.py`:
```python
from books.models import Book

def create_book(title: str, author: str, published_date) -> Book:
    return Book.objects.create(title=title, author=author, published_date=published_date)

def update_book(book_id: int, **fields) -> Book:
    Book.objects.filter(id=book_id).update(**fields)
    return Book.objects.get(id=book_id)
```

---

## Langkah 5: Buat View & Kembalikan Response Parsial
Tulis View di `books/views/book_views.py` menggunakan HTMX response. Kembalikan form dengan status HTTP 422 jika tidak valid:
```python
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from books.models import Book
from books.forms.book_forms import BookForm

class BookListView(ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"

class BookCreateView(View):
    def get(self, request):
        form = BookForm()
        return render(request, "books/partials/book_form.html", {"form": form})

    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return render(request, "books/partials/book_row.html", {"book": book})
        
        # Kembalikan status 422 jika validasi gagal
        return render(request, "books/partials/book_form.html", {"form": form}, status=422)
```

---

## Langkah 6: Integrasi Template HTML
Desain halaman utama di `templates/books/book_list.html` dengan pemanggilan data dinamis:
```html
<c-layout.app title="Daftar Buku">
    <button hx-get="{% url 'books:create' %}" hx-target="#form-container">Tambah Buku</button>
    <div id="form-container"></div>

    <table>
        <thead>
            <tr>
                <th>Judul</th>
                <th>Penulis</th>
            </tr>
        </thead>
        <tbody id="book-list">
            {% for book in books %}
                {% include "books/partials/book_row.html" %}
            {% endfor %}
        </tbody>
    </table>
</c-layout.app>
```
Dan template baris data di `templates/books/partials/book_row.html`:
```html
<tr id="book-{{ book.id }}">
    <td>{{ book.title }}</td>
    <td>{{ book.author }}</td>
</tr>
```
