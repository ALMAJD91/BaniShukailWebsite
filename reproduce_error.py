import os
import django
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bani_shukail.settings")
django.setup()

from assets.models import Asset

try:
    print("Querying Assets...")
    assets = list(Asset.objects.all())
    print(f"Found {len(assets)} assets.")
    for a in assets:
        print(f"Asset: {a.code}, Location: {a.location}")
except Exception as e:
    print(f"Error: {e}")
