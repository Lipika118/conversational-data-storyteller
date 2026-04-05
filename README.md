# Conversational Data Storyteller

An NLP-powered web app that lets you query a real e-commerce database using plain English — no SQL knowledge needed.

## What it does

- Type a question in plain English
- App automatically generates the SQL query
- Runs it on the Olist Brazilian E-Commerce database
- Returns the result as a table
- Explains the result in plain English
- Auto-generates a chart

## Example questions you can ask

- "What are the top 5 cities by number of orders?"
- "Which product categories generate the most revenue?"
- "What is the average review score by category?"
- "Which sellers have the most orders?"
- "What is the average payment value by payment type?"

## Tech stack

| Component | Technology |
|---|---|
| Language | Python |
| LLM (primary) | Google Gemini 2.0 Flash |
| LLM (fallback) | Groq LLaMA 3.3-70B |
| Database | PostgreSQL (Supabase) |
| DB Connection | SQLAlchemy |
| Visualization | Plotly |
| UI | Streamlit |

## Project architecture
User question (plain English)
↓
Gemini/Groq API → generates SQL
↓
PostgreSQL database → returns data
↓
Gemini/Groq API → explains result
↓
Plotly → auto chart
↓
Streamlit UI → displays everything

## Dataset

[Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — 100k real orders from 2016–2018.

Tables used: customers, orders, order_items, payments, reviews, products, sellers

## Setup (local)

1. Clone the repo
```bash
git clone https://github.com/Lipika118/conversational-data-storyteller.git
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create `.env` file
GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
DB_PASSWORD=your_db_password

4. Run the app
```bash
streamlit run app.py
```

## Live demo

[Click here to try the app](your_streamlit_url_here)

## Author

Lipika — MSc Data Science, IIIT Lucknow
