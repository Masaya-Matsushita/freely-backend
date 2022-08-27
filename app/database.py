import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

DATABASE = 'postgres'
USER = os.environ['DB_USER']
PASSWORD = os.environ['DB_PASSWORD']
HOST = os.environ['DB_HOST']
PORT = os.environ['DB_PORT']
DB_NAME = os.environ['DB_NAME']

DATABASE_URL = '{}://{}:{}@{}:{}/{}'.format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)

# SQLAlchemyからHeroku Postgresへアクセスするための処理
# https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
uri = os.getenv(DATABASE_URL)
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

# charsetの設定など
engine = create_engine(uri)

# autocommit, autoflushに何を設定すべきか
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 継承してModelを作成するためのインスタンス
Base = declarative_base()
