"""
Crear usuarios para los dashboards de Kronautomation.

Uso:
    python tools/create_user.py <email> <proyecto> [password] [role]

Ejemplos:
    # Crear usuario de Bareño (password autogenerado)
    python tools/create_user.py asistente.bareno@correo.com bareno

    # Con password específico
    python tools/create_user.py admin.marfil@correo.com marfil "Marfil2026!"

    # Con rol admin
    python tools/create_user.py owner@kronautomation.com bareno "Pass123!" admin

Proyectos válidos: bareno, marfil, youarenotalone, research, seo
Roles válidos: viewer, admin
"""
import os
import sys
import secrets
import string
from pathlib import Path

try:
    from dotenv import load_dotenv
    from supabase import create_client
except ImportError:
    print("Faltan dependencias. Corre: pip install -r requirements.txt")
    sys.exit(1)

# Cargar .env del root del proyecto
ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

URL    = os.getenv("SUPABASE_URL")
SECRET = os.getenv("SUPABASE_SECRET_KEY")

if not URL or not SECRET:
    print("ERROR: Faltan SUPABASE_URL o SUPABASE_SECRET_KEY en .env")
    print(f"Buscando .env en: {ROOT / '.env'}")
    sys.exit(1)

VALID_PROJECTS = {"bareno", "marfil", "youarenotalone", "research", "seo"}
VALID_ROLES    = {"viewer", "admin"}


def gen_password(n=14) -> str:
    """Genera password seguro: letras, dígitos y un símbolo seguro."""
    alphabet = string.ascii_letters + string.digits
    pwd = "".join(secrets.choice(alphabet) for _ in range(n - 1))
    return pwd + "!"  # garantiza que cumple políticas comunes


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    email   = sys.argv[1].strip().lower()
    project = sys.argv[2].strip().lower()
    password = sys.argv[3] if len(sys.argv) > 3 else gen_password()
    role     = sys.argv[4] if len(sys.argv) > 4 else "viewer"

    if project not in VALID_PROJECTS:
        print(f"ERROR: proyecto '{project}' inválido. Válidos: {sorted(VALID_PROJECTS)}")
        sys.exit(1)
    if role not in VALID_ROLES:
        print(f"ERROR: role '{role}' inválido. Válidos: {sorted(VALID_ROLES)}")
        sys.exit(1)

    sb = create_client(URL, SECRET)

    # 1) Crear usuario en auth.users (o reutilizar si ya existe)
    print(f"→ Creando usuario en Supabase Auth: {email}")
    try:
        sb.auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True,
        })
        print(f"  ✓ Usuario creado")
    except Exception as e:
        msg = str(e).lower()
        if "already" in msg or "exists" in msg or "duplicate" in msg:
            print(f"  ⚠ Usuario ya existía en auth.users (se reutiliza)")
        else:
            print(f"  ✗ Error creando usuario: {e}")
            sys.exit(1)

    # 2) Insertar acceso al proyecto en app_users (upsert)
    print(f"→ Otorgando acceso al proyecto '{project}' (rol: {role})")
    try:
        sb.table("app_users").upsert({
            "email":   email,
            "project": project,
            "role":    role,
        }, on_conflict="email,project").execute()
        print(f"  ✓ Acceso otorgado")
    except Exception as e:
        print(f"  ✗ Error insertando en app_users: {e}")
        sys.exit(1)

    # Resumen
    subdomain = f"{project}.kronautomation.co"
    print()
    print("═" * 56)
    print(f"  ✓ Listo. Credenciales del usuario:")
    print(f"  ─────────────────────────────────────────")
    print(f"  URL:      https://{subdomain}")
    print(f"  Email:    {email}")
    print(f"  Password: {password}")
    print(f"  Proyecto: {project} (rol: {role})")
    print("═" * 56)
    print(f"  ⚠ Guarda esta info en un password manager")
    print(f"    y mándale las credenciales al cliente.")


if __name__ == "__main__":
    main()
