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

# NOTE: AttributeError: 'NoneType' object has no attribute 'startswith'
# NOTE: 一旦SQLAlchemyをv1.3.9へダウンすることで対応
# TODO: v1.4.40(現在)までバージョンアップしたい
# SQLAlchemy(1.4.x以降)からHeroku Postgresへアクセスするための処理
# https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
# REPLACED_URL = os.getenv(DATABASE_URL)
# if REPLACED_URL.startswith("postgres://"):
#     REPLACED_URL = REPLACED_URL.replace("postgres://", "postgresql://", 1)

# TODO: charsetの設定など
engine = create_engine(DATABASE_URL)

# TODO: autocommit, autoflushに何を設定すべきか
# TODO: scoped_session()を使用すべき？
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 継承してModelを作成するためのインスタンス
Base = declarative_base()
