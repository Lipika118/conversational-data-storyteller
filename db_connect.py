import pandas as pd
from sqlalchemy import create_engine

# Put your actual password directly here to test
engine = create_engine("postgresql+psycopg2://postgres:lipika maji@localhost/postgres")

def run_query(sql):
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn)
    return df

df = run_query("SELECT * FROM orders LIMIT 5;")
print(df)