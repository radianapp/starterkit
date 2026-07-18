def get_app_from_args(args):
    """Mengekstrak nama dan parameter aplikasi dari argumen CLI."""
    if not args:
        return None, None
    name = args[0]
    app = None
    if "-a" in args:
        idx = args.index("-a")
        if idx + 1 < len(args):
            app = args[idx + 1]
    elif "--app" in args:
        idx = args.index("--app")
        if idx + 1 < len(args):
            app = args[idx + 1]
    return name, app

def run_new_component(args):
    if not args:
        print("[ERROR] Penggunaan: rdp new component <nama>")
        sys.exit(1)
    name = args[0]
    
    components_dir = os.path.join("templates", "cotton", "rdp")
    os.makedirs(components_dir, exist_ok=True)
    
    file_path = os.path.join(components_dir, f"{name}.html")
    if os.path.exists(file_path):
        print(f"[ERROR] Komponen '{name}' sudah ada di '{file_path}'.")
        sys.exit(1)
        
    content = f"""<c-vars />

<!-- Komponen: {name} -->
<div class="rdp-{name}">
    <c-slot />
</div>
"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"  [OK] Komponen Cotton '{name}' berhasil dibuat di {file_path}")

def run_new_htmx(args):
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new htmx <nama> -a <nama-app>")
        sys.exit(1)
        
    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)
        
    # Generate View
    views_dir = os.path.join(app_dir, "views")
    os.makedirs(views_dir, exist_ok=True)
    view_path = os.path.join(views_dir, f"{name}.py")
    
    class_name = "".join(x.capitalize() or "_" for x in name.split("_")) + "View"
    
    view_content = f"""from django.views.generic import TemplateView

class {class_name}(TemplateView):
    template_name = "{app}/partials/{name}.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Tambahkan context di sini
        return context
"""
    if not os.path.exists(view_path):
        with open(view_path, 'w', encoding='utf-8') as f:
            f.write(view_content)
        print(f"  [OK] View '{class_name}' berhasil dibuat di {view_path}")
    else:
        print(f"  [WARNING] View '{name}.py' sudah ada.")

    # Generate Partial HTML
    partials_dir = os.path.join("templates", app, "partials")
    os.makedirs(partials_dir, exist_ok=True)
    partial_path = os.path.join(partials_dir, f"{name}.html")
    
    if not os.path.exists(partial_path):
        with open(partial_path, 'w', encoding='utf-8') as f:
            f.write(f"<!-- Partial View: {name} -->\n<div>\n    Isi partial HTMX untuk {name}\n</div>\n")
        print(f"  [OK] Partial HTML berhasil dibuat di {partial_path}")
    else:
        print(f"  [WARNING] Partial HTML '{name}.html' sudah ada.")

def run_new_task(args):
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new task <nama> -a <nama-app>")
        sys.exit(1)
        
    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)
        
    tasks_path = os.path.join(app_dir, "tasks.py")
    
    task_content = f"""
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def {name}():
    \"\"\"Tugas background Celery untuk {name}.\"\"\"
    try:
        logger.info("Memulai task {name}")
        # Implementasi task di sini
        pass
    except Exception as e:
        logger.error(f"Error di task {name}: {{e}}")
        raise
"""
    if not os.path.exists(tasks_path):
        with open(tasks_path, 'w', encoding='utf-8') as f:
            f.write(task_content.lstrip())
    else:
        with open(tasks_path, 'a', encoding='utf-8') as f:
            f.write(task_content)
            
    print(f"  [OK] Task Celery '{name}' berhasil ditambahkan di {tasks_path}")

def run_new_service(args):
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new service <nama> -a <nama-app>")
        sys.exit(1)
        
    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)
        
    services_dir = os.path.join(app_dir, "services")
    os.makedirs(services_dir, exist_ok=True)
    service_path = os.path.join(services_dir, f"{name}.py")
    
    if os.path.exists(service_path):
        print(f"[ERROR] Service '{name}' sudah ada.")
        sys.exit(1)
        
    class_name = "".join(x.capitalize() or "_" for x in name.split("_")) + "Service"
    
    service_content = f"""from django.db import transaction

class {class_name}:
    \"\"\"Layanan bisnis untuk {name}.\"\"\"

    @staticmethod
    @transaction.atomic
    def execute():
        \"\"\"Eksekusi logika bisnis.\"\"\"
        pass
"""
    with open(service_path, 'w', encoding='utf-8') as f:
        f.write(service_content)
        
    print(f"  [OK] Service '{class_name}' berhasil dibuat di {service_path}")

def run_new_command(args):
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new command <nama> -a <nama-app>")
        sys.exit(1)
        
    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)
        
    commands_dir = os.path.join(app_dir, "management", "commands")
    os.makedirs(commands_dir, exist_ok=True)
    
    # __init__.py files
    open(os.path.join(app_dir, "management", "__init__.py"), 'a').close()
    open(os.path.join(commands_dir, "__init__.py"), 'a').close()
    
    command_path = os.path.join(commands_dir, f"{name}.py")
    if os.path.exists(command_path):
        print(f"[ERROR] Command '{name}' sudah ada.")
        sys.exit(1)
        
    command_content = f"""from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Deskripsi command {name}'

    def add_arguments(self, parser):
        # parser.add_argument('--force', action='store_true', help='Force execution')
        pass

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Command {name} berhasil dijalankan.'))
"""
    with open(command_path, 'w', encoding='utf-8') as f:
        f.write(command_content)
        
    print(f"  [OK] Custom command '{name}' berhasil dibuat di {command_path}")

def run_new_test(args):
    name, app = get_app_from_args(args)
    if not name or not app:
        print("[ERROR] Penggunaan: rdp new test <nama> -a <nama-app>")
        sys.exit(1)
        
    app_dir = os.path.join("apps", app)
    if not os.path.exists(app_dir):
        print(f"[ERROR] Aplikasi '{app}' tidak ditemukan.")
        sys.exit(1)
        
    tests_dir = os.path.join(app_dir, "tests")
    os.makedirs(tests_dir, exist_ok=True)
    open(os.path.join(tests_dir, "__init__.py"), 'a').close()
    
    test_path = os.path.join(tests_dir, f"test_{name}.py")
    if os.path.exists(test_path):
        print(f"[ERROR] Test 'test_{name}' sudah ada.")
        sys.exit(1)
        
    test_content = f"""import pytest

@pytest.mark.django_db
def test_{name}():
    # Setup
    
    # Execute
    
    # Assert
    assert True
"""
    with open(test_path, 'w', encoding='utf-8') as f:
        f.write(test_content)
        
    print(f"  [OK] File test 'test_{name}.py' berhasil dibuat di {test_path}")

def run_build_demo(args):
    print("=" * 60)
    print("Membangun Demo Aplikasi RDP 'inventory'...")
    print("=" * 60)
    
    commands = [
        ["new", "app", "inventory"],
        ["new", "api", "inventory"],
        ["new", "component", "status_badge"],
        ["new", "service", "stock_manager", "-a", "inventory"],
        ["new", "task", "sync_stock", "-a", "inventory"],
        ["new", "command", "import_stock", "-a", "inventory"],
        ["new", "htmx", "stock_list", "-a", "inventory"],
        ["new", "test", "stock_service", "-a", "inventory"]
    ]
    
    for cmd in commands:
        print(f"\\n> rdp {' '.join(cmd)}")
        # Untuk command new app dan new api kita perlu bypass prompt Y/n dengan Monkey Patch sementara
        if cmd[1] in ("app", "api"):
            # Mock get_input khusus untuk build-demo
            global get_input
            original_get_input = get_input
            get_input = lambda prompt, default=None: "Y"
        try:
            if cmd[1] == "app":
                run_new_app(cmd[2:])
            elif cmd[1] == "api":
                run_new_api(cmd[2:])
            elif cmd[1] == "component":
                run_new_component(cmd[2:])
            elif cmd[1] == "service":
                run_new_service(cmd[2:])
            elif cmd[1] == "task":
                run_new_task(cmd[2:])
            elif cmd[1] == "command":
                run_new_command(cmd[2:])
            elif cmd[1] == "htmx":
                run_new_htmx(cmd[2:])
            elif cmd[1] == "test":
                run_new_test(cmd[2:])
        finally:
            if cmd[1] in ("app", "api"):
                get_input = original_get_input
                
    print("\\n" + "=" * 60)
    print("  [OK] Demo 'inventory' berhasil dibangun sepenuhnya!")
    print("=" * 60)

