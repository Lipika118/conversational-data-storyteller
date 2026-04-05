import streamlit as st
import pandas as pd
import google.generativeai as genai
from groq import Groq
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path
import os
import plotly.express as px

# Load .env file
load_dotenv(Path(__file__).parent / ".env")

# Keys from .env
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
GROQ_KEY   = os.getenv("GROQ_API_KEY")
DB_PASS    = os.getenv("DB_PASSWORD")

# API connections
gemini_client = genai.GenerativeModel('gemini-pro')
groq_client   = Groq(api_key=GROQ_KEY)

# Database connection
engine = create_engine(
    f"postgresql+psycopg2://postgres:{DB_PASS}@localhost/postgres"
)

SCHEMA = """
Tables:
- customers(customer_id, customer_city, customer_state)
- orders(order_id, customer_id, order_status, order_purchase_timestamp, order_estimated_delivery_date)
- order_items(order_id, product_id, seller_id, price, freight_value)
- payments(order_id, payment_type, payment_value)
- reviews(order_id, review_score, review_comment_message)
- products(product_id, product_category_name, product_weight_g)
- sellers(seller_id, seller_city, seller_state)
"""

def ask_llm(prompt):
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception:
        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content.strip()

def nl_to_sql(question):
    return ask_llm(f"""
You are a PostgreSQL expert.
Schema:
{SCHEMA}
Convert to PostgreSQL SQL. Return ONLY raw SQL, no markdown, no explanation.
Use proper JOINs. Never use CROSS JOIN.
Always add LIMIT 20 unless question asks for specific number.
Question: {question}
""")

def explain_result(question, df):
    return ask_llm(f"""
The user asked: "{question}"
Data:
{df.head(20).to_string(index=False)}
Write 2-3 sentences explaining this like a data analyst to a business manager.
Mention actual numbers.
""")

def auto_visualize(df, question):
    if df.shape[1] != 2:
        return None
    col1, col2 = df.columns[0], df.columns[1]
    if not pd.api.types.is_numeric_dtype(df[col2]):
        return None
    time_words = ["month", "year", "date", "trend", "time", "daily", "weekly"]
    if any(w in question.lower() for w in time_words):
        fig = px.line(df, x=col1, y=col2, title=question,
                      color_discrete_sequence=["#D237DD"])
    else:
        fig = px.bar(df, x=col1, y=col2, title=question,
                     color_discrete_sequence=["#DD37D8"])
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    return fig

# Streamlit UI
st.set_page_config(
    page_title="Conversational Data Storyteller",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Conversational Data Storyteller")
st.caption("Ask questions about the Olist e-commerce dataset in plain English")

st.markdown("**Try asking:**")
c1, c2 = st.columns(2)
with c1:
    st.code("Top 5 cities by number of orders")
    st.code("Average payment value by payment type")
with c2:
    st.code("How many orders were delivered?")
    st.code("Top 5 product categories by revenue")

st.divider()

question = st.text_input(
    "Your question:",
    placeholder="e.g. Top 5 cities by number of orders"
)

if st.button("Analyze") and question:
    with st.spinner("Working..."):
        sql = nl_to_sql(question)
        st.subheader("Generated SQL")
        st.code(sql, language="sql")
        try:
            df = pd.read_sql(sql, engine)
            st.subheader("Result")
            st.dataframe(df, use_container_width=True)
            st.subheader("Insight")
            st.info(explain_result(question, df))
            fig = auto_visualize(df, question)
            if fig:
                st.subheader("Chart")
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Query failed: {e}")
            st.caption("Try rephrasing your question.")