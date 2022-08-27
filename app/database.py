import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

# SQLAlchemy(1.4.x以降)からHeroku Postgresへアクセスするため、postgres -> postgresql
# https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
DATABASE = 'postgresql'
USER = os.environ['DB_USER']
PASSWORD = os.environ['DB_PASSWORD']
HOST = os.environ['DB_HOST']
PORT = os.environ['DB_PORT']
DB_NAME = os.environ['DB_NAME']

DATABASE_URL = '{}://{}:{}@{}:{}/{}'.format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)

# TODO: charsetの設定など
engine = create_engine(DATABASE_URL)

# TODO: autocommit, autoflushに何を設定すべきか
# TODO: scoped_session()を使用すべき？
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 継承してModelを作成するためのインスタンス
Base = declarative_base()
