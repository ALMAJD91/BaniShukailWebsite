import os
import sys
import django
from django.core.management import call_command
from pathlib import Path

def setup_django():
    # Add the project root to the python path
    BASE_DIR = Path(__file__).resolve().parent
    sys.path.append(str(BASE_DIR))
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bani_shukail.settings')
    try:
        django.setup()
        print("✅ Django setup successful.")
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        sys.exit(1)

def ensure_migration_dir(app_name):
    path = Path(__file__).resolve().parent / app_name / "migrations"
    if not path.exists():
        print(f"📁 Creating migrations directory for {app_name}...")
        path.mkdir(parents=True, exist_ok=True)
        (path / "__init__.py").touch()
    else:
        print(f"✅ Migrations directory exists for {app_name}.")
        if not (path / "__init__.py").exists():
            (path / "__init__.py").touch()
            print(f"   Created missing __init__.py for {app_name}.")

def run_migrations():
    apps_to_fix = ['warehouse', 'invoices']
    
    print("\n--- 1. Ensuring Migration Directories ---")
    for app in apps_to_fix:
        ensure_migration_dir(app)

    print("\n--- 2. Making Migrations ---")
    try:
        # Make migrations for specific apps
        call_command('makemigrations', *apps_to_fix)
        print("✅ 'makemigrations' completed.")
    except Exception as e:
        print(f"❌ 'makemigrations' failed: {e}")
        # Continue anyway, maybe they exist?

    print("\n--- 3. Applying Migrations ---")
    try:
        call_command('migrate')
        print("✅ 'migrate' completed.")
    except Exception as e:
        print(f"❌ 'migrate' failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting Database Fix Script...")
    setup_django()
    run_migrations()
    print("\n🎉 Fix script completed. Check output for errors.")
