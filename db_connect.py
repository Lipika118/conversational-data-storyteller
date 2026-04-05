import pandas as pd
from sqlalchemy import create_engine
import os

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def run_query(sql):
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn)
    return df