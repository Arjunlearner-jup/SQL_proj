import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sqlalchemy import create_engine, text

st.set_page_config(
    page_title="Ecommerce Analytics Dashboard",
    page_icon="🛒",
    layout="wide"
)

TABLE_NAME = "ecommerce_customer_product_metrics"

DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "revenuemanagementsys"
DB_USER = "root"
DB_PASSWORD = "root1"

NUMERIC_COLS = [
    "orders_count", "line_items_count", "units_sold", "gross_item_revenue",
    "total_item_discount", "returned_items", "customer_avg_rating", "total_orders",
    "active_customers", "total_units_sold", "total_revenue", "total_discount",
    "avg_item_revenue", "total_returned_items", "monthly_avg_rating",
    "product_units_sold", "product_revenue", "product_returns", "product_avg_rating",
    "product_rank_in_category", "lifetime_orders", "lifetime_units",
    "lifetime_revenue", "customer_revenue_share_pct", "customer_order_share"
]


def fmt_num(value, prefix="", suffix="", decimals=0):
    if value is None or pd.isna(value):
        return "-"
    return f"{prefix}{value:,.{decimals}f}{suffix}"


def safe_div(a, b):
    return 0.0 if b in [0, None] or pd.isna(b) else a / b


@st.cache_resource
def get_engine():
    conn_str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(conn_str, pool_pre_ping=True)


@st.cache_data(ttl=600)
def load_data():
    engine = get_engine()
    query = text(f"SELECT * FROM {TABLE_NAME}")
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    df.columns = [c.lower() for c in df.columns]

    if "order_month" in df.columns:
        df["order_month"] = pd.to_datetime(df["order_month"], errors="coerce")
    if "first_order_date" in df.columns:
        df["first_order_date"] = pd.to_datetime(df["first_order_date"], errors="coerce")

    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    text_cols = [
        "customer_name", "customer_email", "customer_city", "customer_country",
        "customer_type", "customer_segment", "category", "brand", "product_name"
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    return df


@st.cache_data(ttl=600)
def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")


@st.cache_data(ttl=600)
def build_views(df):
    monthly = (
        df.sort_values(["order_month"])
        .drop_duplicates(subset=["order_month"])
        .copy()
    )

    customers_monthly = (
        df.sort_values(
            ["order_month", "customer_id", "gross_item_revenue"],
            ascending=[True, True, False]
        )
        .drop_duplicates(subset=["order_month", "customer_id"])
        .copy()
    )

    products_monthly = (
        df.sort_values(
            ["order_month", "category", "product_id", "product_revenue"],
            ascending=[True, True, True, False]
        )
        .drop_duplicates(subset=["order_month", "category", "product_id"])
        .copy()
    )

    customers_lifetime = (
        df.sort_values(["customer_id", "lifetime_revenue"], ascending=[True, False])
        .drop_duplicates(subset=["customer_id"])
        .copy()
    )

    return monthly, customers_monthly, products_monthly, customers_lifetime


st.title("🛒 Ecommerce Analytics Dashboard")
st.caption(f"Source table: {TABLE_NAME}")

with st.sidebar:
    st.header("MySQL connection")
    st.write(f"**Host:** {DB_HOST}")
    st.write(f"**Port:** {DB_PORT}")
    st.write(f"**Database:** {DB_NAME}")
    st.write(f"**User:** {DB_USER}")

try:
    raw_df = load_data()
except Exception as e:
    st.error(f"Database connection or query failed: {e}")
    st.stop()

if raw_df.empty:
    st.warning(f"No rows found in {TABLE_NAME}.")
    st.stop()

with st.sidebar:
    st.header("Filters")

    month_options = sorted(raw_df["order_month"].dropna().dt.strftime("%Y-%m").unique().tolist()) if "order_month" in raw_df.columns else []
    country_options = sorted(raw_df["customer_country"].dropna().unique().tolist()) if "customer_country" in raw_df.columns else []
    city_options = sorted(raw_df["customer_city"].dropna().unique().tolist()) if "customer_city" in raw_df.columns else []
    customer_type_options = sorted(raw_df["customer_type"].dropna().unique().tolist()) if "customer_type" in raw_df.columns else []
    segment_options = sorted(raw_df["customer_segment"].dropna().unique().tolist()) if "customer_segment" in raw_df.columns else []
    category_options = sorted(raw_df["category"].dropna().unique().tolist()) if "category" in raw_df.columns else []
    brand_options = sorted(raw_df["brand"].dropna().unique().tolist()) if "brand" in raw_df.columns else []

    selected_months = st.multiselect("Order month", month_options, default=month_options)
    selected_countries = st.multiselect("Country", country_options, default=country_options)
    selected_cities = st.multiselect("City", city_options, default=city_options)
    selected_types = st.multiselect("Customer type", customer_type_options, default=customer_type_options)
    selected_segments = st.multiselect("Customer segment", segment_options, default=segment_options)
    selected_categories = st.multiselect("Category", category_options, default=category_options)
    selected_brands = st.multiselect("Brand", brand_options, default=brand_options)

filtered_df = raw_df.copy()

if selected_months:
    filtered_df = filtered_df[filtered_df["order_month"].dt.strftime("%Y-%m").isin(selected_months)]
if selected_countries:
    filtered_df = filtered_df[filtered_df["customer_country"].isin(selected_countries)]
if selected_cities:
    filtered_df = filtered_df[filtered_df["customer_city"].isin(selected_cities)]
if selected_types:
    filtered_df = filtered_df[filtered_df["customer_type"].isin(selected_types)]
if selected_segments:
    filtered_df = filtered_df[filtered_df["customer_segment"].isin(selected_segments)]
if selected_categories:
    filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]
if selected_brands:
    filtered_df = filtered_df[filtered_df["brand"].isin(selected_brands)]

if filtered_df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

filtered_monthly, filtered_customers, filtered_products, filtered_lifetime = build_views(filtered_df)

revenue = filtered_monthly["total_revenue"].sum()
orders = filtered_monthly["total_orders"].sum()
active_customers = filtered_monthly["active_customers"].sum()
units_sold = filtered_monthly["total_units_sold"].sum()
returned_items = filtered_monthly["total_returned_items"].sum()
aov = safe_div(revenue, orders)
return_rate = safe_div(returned_items, units_sold) * 100
avg_rating = filtered_monthly["monthly_avg_rating"].mean()

m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Revenue", fmt_num(revenue, prefix="€", decimals=2))
m2.metric("Orders", fmt_num(orders))
m3.metric("Active Customers", fmt_num(active_customers))
m4.metric("Units Sold", fmt_num(units_sold))
m5.metric("AOV", fmt_num(aov, prefix="€", decimals=2))
m6.metric("Return Rate", fmt_num(return_rate, suffix="%", decimals=2))

st.caption(f"Average monthly rating: {fmt_num(avg_rating, decimals=2)}")
st.markdown("---")

overview_tab, customers_tab, products_tab, data_tab = st.tabs(
    ["Overview", "Customers", "Products", "Data Export"]
)

with overview_tab:
    left, right = st.columns((1.6, 1))

    with left:
        monthly_trend = (
            filtered_monthly.groupby("order_month", as_index=False)
            .agg(total_revenue=("total_revenue", "sum"))
            .sort_values("order_month")
        )
        fig = px.line(
            monthly_trend,
            x="order_month",
            y="total_revenue",
            markers=True,
            title="Monthly revenue trend"
        )
        fig.update_layout(xaxis_title="Month", yaxis_title="Revenue")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        revenue_by_country = (
            filtered_customers.groupby("customer_country", as_index=False)
            .agg(gross_item_revenue=("gross_item_revenue", "sum"))
            .sort_values("gross_item_revenue", ascending=False)
            .head(10)
        )
        fig = px.bar(
            revenue_by_country,
            x="gross_item_revenue",
            y="customer_country",
            orientation="h",
            title="Revenue by country"
        )
        fig.update_layout(xaxis_title="Revenue", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

with customers_tab:
    c1, c2 = st.columns(2)

    with c1:
        segment_mix = (
            filtered_lifetime.groupby("customer_segment", as_index=False)
            .agg(customers=("customer_id", "nunique"))
            .sort_values("customers", ascending=False)
        )
        fig = px.pie(
            segment_mix,
            values="customers",
            names="customer_segment",
            title="Customer segment mix"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        type_mix = (
            filtered_customers.groupby("customer_type", as_index=False)
            .agg(customers=("customer_id", "nunique"))
        )
        fig = px.bar(
            type_mix,
            x="customer_type",
            y="customers",
            title="New vs repeat customers",
            text_auto=True
        )
        st.plotly_chart(fig, use_container_width=True)

with products_tab:
    p1, p2 = st.columns(2)

    with p1:
        top_products = (
            filtered_products.groupby(["product_name", "category"], as_index=False)
            .agg(
                product_revenue=("product_revenue", "sum"),
                product_units_sold=("product_units_sold", "sum")
            )
            .sort_values("product_revenue", ascending=False)
            .head(10)
        )
        fig = px.bar(
            top_products,
            x="product_revenue",
            y="product_name",
            color="category",
            orientation="h",
            title="Top 10 products by revenue"
        )
        fig.update_layout(xaxis_title="Revenue", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

with data_tab:
    st.subheader("Filtered data")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    st.download_button(
        "Download filtered CSV",
        data=to_csv_bytes(filtered_df),
        file_name="ecommerce_customer_product_metrics_filtered.csv",
        mime="text/csv"
    )