import os
import json

DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_INTERNAL_PORT']

DEV = os.environ['BACKEND_DEV'] == "True"
CORS_ORIGIN = json.loads(os.environ['BACKEND_CORS_ORIGIN'])