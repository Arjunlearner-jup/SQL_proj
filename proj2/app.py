import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine, text

st.set_page_config(
    page_title="SaaS Subscription Dashboard",
    page_icon="📈",
    layout="wide"
)

TABLE_NAME = "saas_subscription_metrics"

DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "SaaSsubscriptionproject"
DB_USER = "root"
DB_PASSWORD = "root1"

NUMERIC_COLS = [
    "active_subscriptions",
    "is_active_customer",
    "current_mrr",
    "prev_mrr",
    "new_mrr",
    "expansion_mrr",
    "contraction_mrr",
    "churned_mrr",
    "total_mrr",
    "total_new_mrr",
    "total_expansion_mrr",
    "total_contraction_mrr",
    "total_churned_mrr",
    "total_active_customers"
]


def fmt_num(value, prefix="", suffix="", decimals=0):
    if value is None or pd.isna(value):
        return "-"
    return f"{prefix}{value:,.{decimals}f}{suffix}"


def safe_div(a, b):
    if b in [0, None] or pd.isna(b):
        return 0.0
    return a / b


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

    date_cols = ["metric_month", "signup_date", "cohort_month"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    text_cols = [
        "customer_name",
        "customer_email",
        "country",
        "industry",
        "company_size",
        "acquisition_channel",
        "revenue_change_type"
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
        df.sort_values(["metric_month"])
        .drop_duplicates(subset=["metric_month"])
        .copy()
    )

    customer_monthly = (
        df.sort_values(
            ["metric_month", "customer_id", "current_mrr"],
            ascending=[True, True, False]
        )
        .drop_duplicates(subset=["metric_month", "customer_id"])
        .copy()
    )

    customer_latest = (
        df.sort_values(["customer_id", "metric_month"])
        .drop_duplicates(subset=["customer_id"], keep="last")
        .copy()
    )

    return monthly, customer_monthly, customer_latest


st.title("📈 SaaS Subscription Dashboard")
st.caption(f"Source table: {TABLE_NAME}")

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

    month_options = sorted(
        raw_df["metric_month"].dropna().dt.strftime("%Y-%m").unique().tolist()
    ) if "metric_month" in raw_df.columns else []

    country_options = sorted(
        raw_df["country"].dropna().unique().tolist()
    ) if "country" in raw_df.columns else []

    industry_options = sorted(
        raw_df["industry"].dropna().unique().tolist()
    ) if "industry" in raw_df.columns else []

    size_options = sorted(
        raw_df["company_size"].dropna().unique().tolist()
    ) if "company_size" in raw_df.columns else []

    channel_options = sorted(
        raw_df["acquisition_channel"].dropna().unique().tolist()
    ) if "acquisition_channel" in raw_df.columns else []

    change_options = sorted(
        raw_df["revenue_change_type"].dropna().unique().tolist()
    ) if "revenue_change_type" in raw_df.columns else []

    selected_months = st.multiselect("Metric month", month_options, default=month_options)
    selected_countries = st.multiselect("Country", country_options, default=country_options)
    selected_industries = st.multiselect("Industry", industry_options, default=industry_options)
    selected_sizes = st.multiselect("Company size", size_options, default=size_options)
    selected_channels = st.multiselect("Acquisition channel", channel_options, default=channel_options)
    selected_changes = st.multiselect("Revenue change type", change_options, default=change_options)

filtered_df = raw_df.copy()

if selected_months:
    filtered_df = filtered_df[
        filtered_df["metric_month"].dt.strftime("%Y-%m").isin(selected_months)
    ]
if selected_countries:
    filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]
if selected_industries:
    filtered_df = filtered_df[filtered_df["industry"].isin(selected_industries)]
if selected_sizes:
    filtered_df = filtered_df[filtered_df["company_size"].isin(selected_sizes)]
if selected_channels:
    filtered_df = filtered_df[filtered_df["acquisition_channel"].isin(selected_channels)]
if selected_changes:
    filtered_df = filtered_df[filtered_df["revenue_change_type"].isin(selected_changes)]

if filtered_df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

filtered_monthly, filtered_customers, filtered_latest = build_views(filtered_df)

latest_month = filtered_monthly["metric_month"].max()
latest_snapshot = filtered_monthly[filtered_monthly["metric_month"] == latest_month]

total_mrr = latest_snapshot["total_mrr"].max() if "total_mrr" in latest_snapshot.columns else 0
new_mrr = latest_snapshot["total_new_mrr"].max() if "total_new_mrr" in latest_snapshot.columns else 0
expansion_mrr = latest_snapshot["total_expansion_mrr"].max() if "total_expansion_mrr" in latest_snapshot.columns else 0
contraction_mrr = latest_snapshot["total_contraction_mrr"].max() if "total_contraction_mrr" in latest_snapshot.columns else 0
churned_mrr = latest_snapshot["total_churned_mrr"].max() if "total_churned_mrr" in latest_snapshot.columns else 0
active_customers = latest_snapshot["total_active_customers"].max() if "total_active_customers" in latest_snapshot.columns else 0

gross_retention = safe_div((total_mrr - churned_mrr - contraction_mrr), total_mrr) * 100 if total_mrr else 0
net_revenue_retention = safe_div((total_mrr - churned_mrr - contraction_mrr + expansion_mrr), total_mrr) * 100 if total_mrr else 0

m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Current MRR", fmt_num(total_mrr, prefix="$", decimals=2))
m2.metric("Active Customers", fmt_num(active_customers))
m3.metric("New MRR", fmt_num(new_mrr, prefix="$", decimals=2))
m4.metric("Expansion MRR", fmt_num(expansion_mrr, prefix="$", decimals=2))
m5.metric("Churned MRR", fmt_num(churned_mrr, prefix="$", decimals=2))
m6.metric("Contraction MRR", fmt_num(contraction_mrr, prefix="$", decimals=2))

st.caption(
    f"Gross retention: {fmt_num(gross_retention, suffix='%', decimals=2)} | "
    f"Net revenue retention: {fmt_num(net_revenue_retention, suffix='%', decimals=2)}"
)
st.markdown("---")

overview_tab, customers_tab, revenue_tab, data_tab = st.tabs(
    ["Overview", "Customers", "Revenue Movement", "Data Export"]
)

with overview_tab:
    left, right = st.columns((1.5, 1))

    with left:
        mrr_trend = (
            filtered_monthly.groupby("metric_month", as_index=False)
            .agg(total_mrr=("total_mrr", "max"))
            .sort_values("metric_month")
        )
        fig = px.line(
            mrr_trend,
            x="metric_month",
            y="total_mrr",
            markers=True,
            title="Monthly MRR Trend"
        )
        fig.update_layout(xaxis_title="Month", yaxis_title="MRR")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        active_trend = (
            filtered_monthly.groupby("metric_month", as_index=False)
            .agg(total_active_customers=("total_active_customers", "max"))
            .sort_values("metric_month")
        )
        fig = px.bar(
            active_trend,
            x="metric_month",
            y="total_active_customers",
            title="Active Customers by Month"
        )
        fig.update_layout(xaxis_title="Month", yaxis_title="Customers")
        st.plotly_chart(fig, use_container_width=True)

with customers_tab:
    c1, c2 = st.columns(2)

    with c1:
        customer_by_industry = (
            filtered_latest.groupby("industry", as_index=False)
            .agg(customers=("customer_id", "nunique"))
            .sort_values("customers", ascending=False)
        )
        fig = px.pie(
            customer_by_industry,
            values="customers",
            names="industry",
            title="Customer Mix by Industry"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        customer_by_size = (
            filtered_latest.groupby("company_size", as_index=False)
            .agg(customers=("customer_id", "nunique"))
            .sort_values("customers", ascending=False)
        )
        fig = px.bar(
            customer_by_size,
            x="company_size",
            y="customers",
            title="Customers by Company Size",
            text_auto=True
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Customers by Current MRR")
    top_customers = (
        filtered_customers.sort_values("current_mrr", ascending=False)
        [["metric_month", "customer_name", "industry", "company_size", "current_mrr", "revenue_change_type"]]
        .head(10)
    )
    st.dataframe(top_customers, use_container_width=True, hide_index=True)

with revenue_tab:
    r1, r2 = st.columns(2)

    with r1:
        revenue_movement = (
            filtered_monthly.groupby("metric_month", as_index=False)
            .agg(
                new_mrr=("total_new_mrr", "max"),
                expansion_mrr=("total_expansion_mrr", "max"),
                contraction_mrr=("total_contraction_mrr", "max"),
                churned_mrr=("total_churned_mrr", "max")
            )
            .sort_values("metric_month")
        )

        melted = revenue_movement.melt(
            id_vars="metric_month",
            value_vars=["new_mrr", "expansion_mrr", "contraction_mrr", "churned_mrr"],
            var_name="metric",
            value_name="amount"
        )

        fig = px.bar(
            melted,
            x="metric_month",
            y="amount",
            color="metric",
            barmode="group",
            title="Revenue Movement by Month"
        )
        fig.update_layout(xaxis_title="Month", yaxis_title="Amount")
        st.plotly_chart(fig, use_container_width=True)

    with r2:
        change_mix = (
            filtered_customers.groupby("revenue_change_type", as_index=False)
            .agg(customers=("customer_id", "nunique"))
            .sort_values("customers", ascending=False)
        )
        fig = px.bar(
            change_mix,
            x="revenue_change_type",
            y="customers",
            title="Customer Revenue Status Mix",
            text_auto=True
        )
        st.plotly_chart(fig, use_container_width=True)

with data_tab:
    st.subheader("Filtered SaaS Metrics Data")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    st.download_button(
        "Download filtered CSV",
        data=to_csv_bytes(filtered_df),
        file_name="saas_subscription_metrics_filtered.csv",
        mime="text/csv"
    )