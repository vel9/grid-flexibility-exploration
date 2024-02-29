import pandas as pd
import plotly.express as px


def show_line_chart(data, x_col, y_col, chart_title):
    fig = px.line(data, x=x_col, y=y_col, title=chart_title)
    fig.show("svg")


def show_bar_chart(data, x_col, y_col, chart_title):
    data_df = pd.DataFrame(data, columns=[x_col, y_col])
    fig = px.bar(data_df, x=x_col, y=y_col, title=chart_title)
    fig.show("svg")


def show_bar_chart_with_color(data, color_col, x_col, y_col, chart_title):
    data_df = pd.DataFrame(data, columns=[color_col, x_col, y_col])
    fig = px.bar(data_df, x=x_col, y=y_col, title=chart_title, color=color_col)
    fig.show("svg")


def get_average_in_column(chunk, column_to_average):
    if chunk.empty:
        raise ValueError("Dataframe is empty")
    return chunk.loc[:, column_to_average].mean()
