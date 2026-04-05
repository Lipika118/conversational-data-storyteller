from groq import Groq
import pandas as pd
from sqlalchemy import create_engine

import os
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Database connection
engine = create_engine("postgresql+psycopg2://postgres:lipika maji@localhost/postgres")

# Olist schema
SCHEMA = """
Tables available:
- customers(customer_id, customer_city, customer_state)
- orders(order_id, customer_id, order_status, order_purchase_timestamp, order_estimated_delivery_date)
- order_items(order_id, product_id, seller_id, price, freight_value)
- payments(order_id, payment_type, payment_value)
- reviews(order_id, review_score, review_comment_message)
- products(product_id, product_category_name, product_weight_g)
- sellers(seller_id, seller_city, seller_state)
"""

# Step 1 — NL to SQL
def nl_to_sql(question):
    prompt = f"""
You are a PostgreSQL expert.
Given this database schema:
{SCHEMA}

Convert this question to a PostgreSQL SQL query.
Return ONLY the SQL query, nothing else.
No explanation, no markdown, just raw SQL.
Use proper JOINs, never use CROSS JOIN.

Question: {question}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Step 2 — Run SQL on database
def run_query(sql):
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn)
    return df

# Step 3 — Explain result
def explain_result(question, df):
    prompt = f"""
The user asked: "{question}"

The data result is:
{df.to_string(index=False)}

Write 2-3 sentences explaining this result simply.
Mention actual numbers from the data.
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# --- Test the full pipeline ---
question = "What are the top 5 cities by number of orders?"

print(f"Question: {question}")
print("\nGenerating SQL...")
sql = nl_to_sql(question)
print(f"SQL: {sql}")

print("\nRunning query...")
df = run_query(sql)
print(df)

print("\nGenerating explanation...")
explanation = explain_result(question, df)
print(f"\nInsight: {explanation}")