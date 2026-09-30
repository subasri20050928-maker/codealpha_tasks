import os
import json
from decimal import Decimal

# Ensure directories exist
os.makedirs("store/static/css", exist_ok=True)
os.makedirs("store/static/js", exist_ok=True)
os.makedirs("store/static/images", exist_ok=True)
os.makedirs("store/templates/store/auth", exist_ok=True)

print("Directories verified.")
