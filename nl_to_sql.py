from groq import Groq
import os
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# This describes your Olist database to the LLM
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

def nl_to_sql(user_question):
    prompt = f"""
You are a PostgreSQL expert.

Given this database schema:
{SCHEMA}

Convert this question to a PostgreSQL SQL query.
Return ONLY the SQL query, nothing else.
No explanation, no markdown, just raw SQL.

Question: {user_question}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


# Test it with 3 questions
questions = [
    "What are the top 5 cities by number of orders?",
    "What is the average payment value?",
    "How many orders were delivered successfully?"
]

for q in questions:
    print(f"\nQuestion: {q}")
    print(f"SQL: {nl_to_sql(q)}")