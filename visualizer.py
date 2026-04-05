import plotly.express as px
import pandas as pd

def auto_visualize(df, question):
    # Only visualize if exactly 2 columns
    if df.shape[1] != 2:
        return None
    
    col1 = df.columns[0]  # labels
    col2 = df.columns[1]  # numbers

    # Check second column is numeric
    if not pd.api.types.is_numeric_dtype(df[col2]):
        return None

    fig = px.bar(
        df,
        x=col1,
        y=col2,
        title=question,
        color_discrete_sequence=["#37DD98"]
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    return fig

# Test it
if __name__ == "__main__":
    # Sample data to test
    test_df = pd.DataFrame({
        "customer_city": ["sao paulo", "rio de janeiro", "belo horizonte", "brasilia", "curitiba"],
        "total_orders": [15540, 6882, 2773, 2131, 1521]
    })
    
    fig = auto_visualize(test_df, "Top 5 cities by number of orders")
    if fig:
        fig.show()  # opens in browser