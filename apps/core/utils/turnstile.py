import json
import urllib.request
import urllib.parse
from django.conf import settings

def verify_turnstile(token: str, remoteip: str = None) -> bool:
    """
    Memverifikasi token Cloudflare Turnstile ke API Cloudflare.
    Mengembalikan True jika sukses/valid, False jika invalid atau error.
    Jika TURNSTILE_ENABLED = False, maka selalu mengembalikan True.
    """
    if not getattr(settings, "TURNSTILE_ENABLED", False):
        return True

    secret_key = getattr(settings, "TURNSTILE_SECRET_KEY", "")
    if not secret_key:
        return False

    if not token:
        return False

    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    data = {
        "secret": secret_key,
        "response": token
    }
    
    if remoteip:
        data["remoteip"] = remoteip

    encoded_data = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=encoded_data, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("success", False)
    except Exception:
        # Jika API Cloudflare down atau timeout, asumsikan validasi gagal
        # atau bisa diset return True untuk fail-open jika diinginkan.
        return False
