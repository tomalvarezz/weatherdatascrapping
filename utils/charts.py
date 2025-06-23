# utils/charts.py
import matplotlib.pyplot as plt
from io import BytesIO

def create_bar_chart(df, column, title, ylabel):
    fig, ax = plt.subplots()
    df_sorted = df.sort_values(column, ascending=False)
    ax.bar(df_sorted["City"], df_sorted[column])
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    return buffer
