import plotly.express as px
import pandas as pd

def auto_visualize(df, question):
    if df.empty:
        return None

    # Get numeric and non-numeric columns
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    non_numeric_cols = df.select_dtypes(exclude='number').columns.tolist()

    if not numeric_cols:
        return None

    # Determine x axis
    if non_numeric_cols:
        x_col = non_numeric_cols[0]
    else:
        x_col = df.columns[0]

    y_col = numeric_cols[0]

    # Choose chart type based on x column type
    if pd.api.types.is_datetime64_any_dtype(df[x_col]):
        fig = px.line(df, x=x_col, y=y_col, title=question,
                      color_discrete_sequence=["#E91E8C"])
    elif df.shape[0] <= 20 and df.shape[1] == 2:
        fig = px.bar(df, x=x_col, y=y_col, title=question,
                     color_discrete_sequence=["#37DD98"])
    else:
        fig = px.line(df, x=x_col, y=y_col, title=question,
                      color_discrete_sequence=["#E91E8C"])

    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    return fig