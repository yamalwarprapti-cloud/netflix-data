import csv
import io
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


REQUIRED_COLUMNS = {
    "Watch_Date",
    "Monthly_Revenue",
    "Region",
    "Rating",
    "Device",
    "Subscription_Plan",
    "Watch_Count",
    "Title",
    "Category",
    "Watch_Time_Minutes",
    "Payment_Method",
}
NETFLIX_RED = "#E50914"
BACKGROUND = "#080808"
PANEL_BACKGROUND = "#141414"
TEXT_COLOR = "#F5F5F1"
GRID_COLOR = "#383838"
PIE_COLORS = ["#E50914", "#B20710", "#80000A", "#510006", "#C44D56", "#777777"]


def load_netflix_data(source):
    if isinstance(source, Path):
        content = source.read_text(encoding="utf-8-sig")
    else:
        content = source.getvalue().decode("utf-8-sig")

    wrapped_rows = list(csv.reader(io.StringIO(content)))
    if wrapped_rows and all(len(row) == 1 for row in wrapped_rows):
        first_row = wrapped_rows[0][0]
        if "," in first_row:
            rows = list(csv.reader(io.StringIO("\n".join(row[0] for row in wrapped_rows))))
            if rows:
                return pd.DataFrame(rows[1:], columns=rows[0])

    return pd.read_csv(io.StringIO(content))


def show_percentage_bar_chart(data, category_column, value_column, total, horizontal=False):
    figure, axis = plt.subplots(figsize=(8, 4))
    figure.patch.set_facecolor(PANEL_BACKGROUND)
    axis.set_facecolor(PANEL_BACKGROUND)
    labels = data[category_column].astype(str)
    values = data[value_column].astype(float)
    axis.tick_params(colors=TEXT_COLOR)
    axis.xaxis.label.set_color(TEXT_COLOR)
    axis.yaxis.label.set_color(TEXT_COLOR)
    for spine in axis.spines.values():
        spine.set_color(GRID_COLOR)

    if horizontal:
        bars = axis.barh(labels, values, color=NETFLIX_RED)
        for bar, value in zip(bars, values):
            percentage = value / total * 100 if total else 0
            axis.annotate(
                f"{value:,.0f} ({percentage:.1f}%)",
                (bar.get_width(), bar.get_y() + bar.get_height() / 2),
                xytext=(4, 0),
                textcoords="offset points",
                va="center",
            )
        axis.margins(x=0.3)
    else:
        bars = axis.bar(labels, values, color=NETFLIX_RED)
        for bar, value in zip(bars, values):
            percentage = value / total * 100 if total else 0
            axis.annotate(
                f"{value:,.0f}\n{percentage:.1f}%",
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
            )
        axis.tick_params(axis="x", labelrotation=30)
        axis.margins(y=0.2)

    st.pyplot(figure)
    plt.close(figure)


def show_netflix_pie_chart(values):
    figure, axis = plt.subplots(figsize=(5, 4))
    figure.patch.set_facecolor(PANEL_BACKGROUND)
    axis.set_facecolor(PANEL_BACKGROUND)
    values.plot(
        kind="pie",
        autopct="%1.1f%%",
        ylabel="",
        colors=PIE_COLORS,
        textprops={"color": TEXT_COLOR},
        ax=axis,
    )
    st.pyplot(figure)
    plt.close(figure)


def show_netflix_line_chart(data, x_column, y_column):
    figure, axis = plt.subplots(figsize=(8, 4))
    figure.patch.set_facecolor(PANEL_BACKGROUND)
    axis.set_facecolor(PANEL_BACKGROUND)
    axis.plot(data[x_column], data[y_column], color=NETFLIX_RED, marker="o", linewidth=2)
    axis.set_xlabel(x_column, color=TEXT_COLOR)
    axis.set_ylabel(y_column, color=TEXT_COLOR)
    axis.tick_params(colors=TEXT_COLOR)
    axis.grid(axis="y", color=GRID_COLOR, linewidth=0.6)
    for spine in axis.spines.values():
        spine.set_color(GRID_COLOR)
    st.pyplot(figure)
    plt.close(figure)


st.set_page_config(page_title="Netflix Data Analysis", layout="wide")
st.markdown(
    """
    <style>
    .stApp { background: #080808; color: #F5F5F1; }
    [data-testid="stHeader"] { background: rgba(8, 8, 8, 0.96); }
    [data-testid="stSidebar"] { background: #141414; border-right: 1px solid #E50914; }
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 { color: #F5F5F1; }
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stWidgetLabel"] { color: #D5D5D2; }
    [data-testid="stFileUploaderDropzone"] { background: #141414; }
    [data-testid="stImage"] img { max-width: 100%; height: auto; object-fit: contain; }
    </style>
    """,
    unsafe_allow_html=True,
)

image_directory = Path(__file__).with_name("Images")
dashboard_images = (
    sorted(
        (
            path
            for path in image_directory.iterdir()
            if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
        ),
        key=lambda path: path.name.lower(),
    )
    if image_directory.is_dir()
    else []
)
st.title("Netflix Data Analysis")
st.caption("Viewing activity, revenue, ratings, and subscription trends")
if dashboard_images:
    for image_path in dashboard_images:
        st.image(str(image_path), width=400)

st.sidebar.header("Data and filters")
uploaded_file = st.sidebar.file_uploader("Upload a Netflix CSV", type=["csv", "txt"])
data_path = Path(__file__).with_name("netflix.csv")
if not data_path.exists():
    wrapped_data_path = Path(__file__).with_name("netflix.csv.txt")
    data_path = wrapped_data_path if wrapped_data_path.exists() else data_path

source = uploaded_file if uploaded_file is not None else data_path
if uploaded_file is None and not data_path.exists():
    st.info("Upload your Netflix CSV in the sidebar to view the dashboard.")
    st.stop()

try:
    netflix = load_netflix_data(source)
except (csv.Error, pd.errors.ParserError, UnicodeDecodeError, OSError) as error:
    st.error(f"Could not read this CSV: {error}")
    st.stop()

missing_columns = sorted(REQUIRED_COLUMNS.difference(netflix.columns))
if missing_columns:
    st.error("The CSV is missing required columns: " + ", ".join(missing_columns))
    st.stop()

netflix = netflix.drop_duplicates().copy()
netflix["Watch_Date"] = pd.to_datetime(netflix["Watch_Date"], errors="coerce")
for column in ("Monthly_Revenue", "Rating", "Watch_Count"):
    netflix[column] = pd.to_numeric(netflix[column], errors="coerce")
if "Watch_Time_Minutes" in netflix.columns:
    netflix["Watch_Time_Minutes"] = pd.to_numeric(
        netflix["Watch_Time_Minutes"], errors="coerce"
    )
netflix = netflix.dropna(subset=["Watch_Date"])

if netflix.empty:
    st.warning("No rows with valid watch dates were found in this CSV.")
    st.stop()

source_name = uploaded_file.name if uploaded_file is not None else data_path.name
st.sidebar.caption(f"Source: {source_name} | {len(netflix):,} records")
min_date = netflix["Watch_Date"].min().date()
max_date = netflix["Watch_Date"].max().date()
date_range = st.sidebar.date_input(
    "Watch date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

filtered = netflix.copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[filtered["Watch_Date"].dt.date.between(start_date, end_date)]

filter_columns = (
    ("Region", "Region"),
    ("Device", "Device"),
    ("Subscription_Plan", "Subscription plan"),
    ("Category", "Category"),
    ("Type", "Content type"),
)
for column, label in filter_columns:
    if column not in filtered.columns:
        continue
    options = sorted(filtered[column].dropna().unique().tolist(), key=str)
    selected = st.sidebar.multiselect(label, options, default=options, format_func=str)
    filtered = filtered[filtered[column].isin(selected)]

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

st.divider()
left_chart, right_chart = st.columns(2)

with left_chart:
    st.subheader("Monthly revenue")
    monthly_revenue = (
        filtered.assign(Month=filtered["Watch_Date"].dt.to_period("M").dt.to_timestamp())
        .groupby("Month", as_index=False)["Monthly_Revenue"]
        .sum()
    )
    show_percentage_bar_chart(
        monthly_revenue,
        "Month",
        "Monthly_Revenue",
        filtered["Monthly_Revenue"].sum(),
    )

with right_chart:
    st.subheader("Rating distribution")
    ratings = (
        filtered.dropna(subset=["Rating"])
        .groupby("Rating", as_index=False)
        .size()
        .rename(columns={"size": "Records"})
        .sort_values("Rating")
    )
    show_percentage_bar_chart(ratings, "Rating", "Records", len(filtered))

left_chart, right_chart = st.columns(2)
with left_chart:
    st.subheader("Region-wise rating")
    region_ratings = filtered.groupby("Region")["Rating"].sum()
    show_netflix_pie_chart(region_ratings)

with right_chart:
    st.subheader("Device-wise revenue")
    device_revenue = (
        filtered.groupby("Device", as_index=False)["Monthly_Revenue"]
        .sum()
        .sort_values("Device")
    )
    show_netflix_line_chart(device_revenue, "Device", "Monthly_Revenue")

left_chart, right_chart = st.columns(2)
with left_chart:
    st.subheader("Region-wise revenue")
    region_revenue = (
        filtered.groupby("Region", as_index=False)["Monthly_Revenue"]
        .sum()
        .sort_values("Monthly_Revenue", ascending=False)
    )
    show_percentage_bar_chart(
        region_revenue,
        "Region",
        "Monthly_Revenue",
        filtered["Monthly_Revenue"].sum(),
    )

with right_chart:
    st.subheader("Subscription plan-wise watch count")
    plan_watches = filtered.groupby("Subscription_Plan")["Watch_Count"].sum()
    show_netflix_pie_chart(plan_watches)

left_chart, right_chart = st.columns(2)
with left_chart:
    st.subheader("Watch time by category")
    category_watch_time = (
        filtered.groupby("Category", as_index=False)["Watch_Time_Minutes"]
        .sum()
        .sort_values("Watch_Time_Minutes", ascending=False)
    )
    show_percentage_bar_chart(
        category_watch_time,
        "Category",
        "Watch_Time_Minutes",
        filtered["Watch_Time_Minutes"].sum(),
    )

with right_chart:
    st.subheader("Top 10 titles by watch count")
    top_titles = (
        filtered.groupby("Title", as_index=False)["Watch_Count"]
        .sum()
        .nlargest(10, "Watch_Count")
        .sort_values("Watch_Count")
    )
    show_percentage_bar_chart(
        top_titles,
        "Title",
        "Watch_Count",
        filtered["Watch_Count"].sum(),
        horizontal=True,
    )

left_chart, _ = st.columns(2)
with left_chart:
    st.subheader("Revenue by payment method")
    payment_revenue = (
        filtered.groupby("Payment_Method", as_index=False)["Monthly_Revenue"]
        .sum()
        .sort_values("Monthly_Revenue", ascending=False)
    )
    show_percentage_bar_chart(
        payment_revenue,
        "Payment_Method",
        "Monthly_Revenue",
        filtered["Monthly_Revenue"].sum(),
    )
