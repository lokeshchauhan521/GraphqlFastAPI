from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from core.config.environment import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME, SSL_CA
from utils.logger import log_error, log_success, log_info

Base = declarative_base()

DATABASE_URL = 'mysql+pymysql://{user}:{password}@{server}/{database}?ssl_ca={ssl_ca}&ssl_verify_cert=true'.format(
                    user=DB_USERNAME,
                    password=DB_PASSWORD,
                    server=DB_HOST,
                    database=DB_NAME,
                    auth_plugin='mysql_native_password',
                    ssl_ca=SSL_CA
                )

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20, pool_timeout=30, connect_args={"ssl": {"ca": SSL_CA}})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try:
        db = SessionLocal()
        log_success("Connected to the database successfully")
        yield db
    except Exception as e:
        log_error(f"Error in get_db: {e}")
    finally:
        db.close()
