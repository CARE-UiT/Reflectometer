import os
import json

SECRET_KEY = "6944036b9f42f24c3e63970078e38e90f2878161110563abaf477f5b14f96f25"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2*60

try:
    DB_HOST = os.environ['DB_HOST'] if 'DB_HOST' in os.environ.keys() else "" 
    DB_PORT = os.environ['DB_INTERNAL_PORT'] if 'DB_INTERNAL_PORT' in os.environ.keys() else "" 

    DEV = os.environ['BACKEND_DEV'] == "True" if 'BACKEND_DEV' in os.environ.keys() else "" 
    CORS_ORIGIN = json.loads(os.environ['BACKEND_CORS_ORIGIN']) if 'BACKEND_CORS_ORIGIN' in os.environ.keys() else "" 
except:
    TEST = True