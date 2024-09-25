import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}".format(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    db_name=os.getenv("POSTGRES_DB"),
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)

SECRET_KEY = "secret"