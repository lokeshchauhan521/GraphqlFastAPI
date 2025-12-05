import os
from dotenv import load_dotenv
load_dotenv()

#User db 
DB_USERNAME = os.environ.get('HISTORICAL_TLS_USERNAME')
DB_PASSWORD = os.environ.get('HISTORICAL_TLS_PASSWORD')
DB_HOST = os.environ.get('HISTORICAL_TLS_HOST')
DB_NAME = os.getenv("DB_NAME")
SSL_CA = os.getenv('GLOBAL_PEM_PATH')
