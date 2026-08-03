from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
import logging

logger = logging.getLogger(__name__)

# Role Configuration
ROLES = {
    "SuperAdmin": {
        "description": "Full access to everything, including user management.",
        "permissions": "__all__"
    },
    "Admin": {
        "description": "Full access to operational data, cannot manage users or settings.",
        "models": ["inventory.Produk", "inventory.Kategori", "inventory.Pemasok"],
        "permissions": ["add", "change", "delete", "view"]
    },
    "Editor": {
        "description": "Can create and edit data, but cannot delete.",
        "models": ["inventory.Produk", "inventory.Kategori", "inventory.Pemasok"],
        "permissions": ["add", "change", "view"]
    },
    "Viewer": {
        "description": "Can only view data.",
        "models": ["inventory.Produk", "inventory.Kategori", "inventory.Pemasok"],
        "permissions": ["view"]
    }
}

def initialize_roles():
    """
    TUJUAN: Menginisialisasi role (Group) dan permission berdasarkan konfigurasi ROLES.
    Mendukung penulisan model dalam format string 'app_label.ModelName' agar tidak error
    jika app tersebut dinonaktifkan atau belum diinstal.
    """
    for role_name, config in ROLES.items():
        group, _ = Group.objects.get_or_create(name=role_name)
        
        if config["permissions"] == "__all__":
            group.permissions.set(Permission.objects.all())
        else:
            perms_to_add = []
            for model_str in config.get("models", []):
                try:
                    app_label, model_name = model_str.split('.')
                    model_class = apps.get_model(app_label, model_name)
                    content_type = ContentType.objects.get_for_model(model_class)
                    
                    for action in config["permissions"]:
                        codename = f"{action}_{model_class._meta.model_name}"
                        try:
                            perm = Permission.objects.get(content_type=content_type, codename=codename)
                            perms_to_add.append(perm)
                        except Permission.DoesNotExist:
                            logger.warning(f"Permission {codename} for {model_str} not found.")
                            
                except ValueError:
                    logger.error(f"Invalid model string format: {model_str}. Expected 'app_label.ModelName'")
                except LookupError:
                    logger.warning(f"Model {model_str} not found or app is not installed. Skipping permissions.")
            
            group.permissions.set(perms_to_add)
            
    return "Roles initialized successfully."

def assign_user_to_role(user, role_name):
    """Assign a user to a specific role (Group)."""
    try:
        group = Group.objects.get(name=role_name)
        user.groups.clear()
        user.groups.add(group)
        return True
    except Group.DoesNotExist:
        return False
