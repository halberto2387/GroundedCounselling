#!/usr/bin/env python3
import json
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.main import app

# Generate OpenAPI spec
openapi_spec = app.openapi()

# Write to file with proper UTF-8 encoding
with open('openapi.json', 'w', encoding='utf-8') as f:
    json.dump(openapi_spec, f, indent=2, ensure_ascii=False)

print("OpenAPI spec generated successfully!")