import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine, text

st.set_page_config(
    page_title="Hospital Analytics Dashboard",
    page_icon="🏥",
    layout="wide"
)

TABLE_NAME = "hospital_analytics_metrics"

DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "hospitalmanagementsys"
DB_USER = "root"
DB_PASSWORD = "root1"

NUMERIC_COLS = [
    "age",
    "length_of_stay",
    "is_discharged",
    "is_readmitted",
    "treatment_count",
    "total_treatment_cost",
    "avg_treatment_cost",
    "follow_up_flag"
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

    date_cols = ["report_month", "admission_date", "discharge_date"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    text_cols = [
        "patient_name",
        "gender",
        "city",
        "department",
        "diagnosis",
        "admission_type",
        "insurance_provider",
        "doctor_name",
        "specialization"
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    return df


@st.cache_data(ttl=600)
def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")


st.title("🏥 Hospital Analytics Dashboard")
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

    month_options = sorted(raw_df["report_month"].dropna().dt.strftime("%Y-%m").unique().tolist()) if "report_month" in raw_df.columns else []
    city_options = sorted(raw_df["city"].dropna().unique().tolist()) if "city" in raw_df.columns else []
    department_options = sorted(raw_df["department"].dropna().unique().tolist()) if "department" in raw_df.columns else []
    diagnosis_options = sorted(raw_df["diagnosis"].dropna().unique().tolist()) if "diagnosis" in raw_df.columns else []
    admission_options = sorted(raw_df["admission_type"].dropna().unique().tolist()) if "admission_type" in raw_df.columns else []
    insurance_options = sorted(raw_df["insurance_provider"].dropna().unique().tolist()) if "insurance_provider" in raw_df.columns else []
    doctor_options = sorted(raw_df["doctor_name"].dropna().unique().tolist()) if "doctor_name" in raw_df.columns else []

    selected_months = st.multiselect("Report month", month_options, default=month_options)
    selected_cities = st.multiselect("City", city_options, default=city_options)
    selected_departments = st.multiselect("Department", department_options, default=department_options)
    selected_diagnoses = st.multiselect("Diagnosis", diagnosis_options, default=diagnosis_options)
    selected_admissions = st.multiselect("Admission type", admission_options, default=admission_options)
    selected_insurance = st.multiselect("Insurance provider", insurance_options, default=insurance_options)
    selected_doctors = st.multiselect("Doctor", doctor_options, default=doctor_options)

filtered_df = raw_df.copy()

if selected_months:
    filtered_df = filtered_df[filtered_df["report_month"].dt.strftime("%Y-%m").isin(selected_months)]
if selected_cities:
    filtered_df = filtered_df[filtered_df["city"].isin(selected_cities)]
if selected_departments:
    filtered_df = filtered_df[filtered_df["department"].isin(selected_departments)]
if selected_diagnoses:
    filtered_df = filtered_df[filtered_df["diagnosis"].isin(selected_diagnoses)]
if selected_admissions:
    filtered_df = filtered_df[filtered_df["admission_type"].isin(selected_admissions)]
if selected_insurance:
    filtered_df = filtered_df[filtered_df["insurance_provider"].isin(selected_insurance)]
if selected_doctors:
    filtered_df = filtered_df[filtered_df["doctor_name"].isin(selected_doctors)]

if filtered_df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

total_patients = filtered_df["patient_id"].nunique()
avg_stay = filtered_df["length_of_stay"].mean()
readmissions = filtered_df["is_readmitted"].sum()
discharged = filtered_df["is_discharged"].sum()
total_cost = filtered_df["total_treatment_cost"].sum()
follow_ups = filtered_df["follow_up_flag"].sum()

readmission_rate = safe_div(readmissions, total_patients) * 100
follow_up_rate = safe_div(follow_ups, total_patients) * 100

m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Patients", fmt_num(total_patients))
m2.metric("Avg Length of Stay", fmt_num(avg_stay, decimals=1))
m3.metric("Readmissions", fmt_num(readmissions))
m4.metric("Total Cost", fmt_num(total_cost, prefix="$", decimals=2))
m5.metric("Readmission Rate", fmt_num(readmission_rate, suffix="%", decimals=2))
m6.metric("Follow-Up Rate", fmt_num(follow_up_rate, suffix="%", decimals=2))

st.markdown("---")

overview_tab, patients_tab, doctors_tab, export_tab = st.tabs(
    ["Overview", "Patients", "Doctors", "Data Export"]
)

with overview_tab:
    left, right = st.columns(2)

    with left:
        admissions_trend = (
            filtered_df.groupby("report_month", as_index=False)
            .agg(patients=("patient_id", "nunique"))
            .sort_values("report_month")
        )
        fig = px.line(
            admissions_trend,
            x="report_month",
            y="patients",
            markers=True,
            title="Monthly Patient Admissions"
        )
        fig.update_layout(xaxis_title="Month", yaxis_title="Patients")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        dept_cost = (
            filtered_df.groupby("department", as_index=False)
            .agg(total_treatment_cost=("total_treatment_cost", "sum"))
            .sort_values("total_treatment_cost", ascending=False)
        )
        fig = px.bar(
            dept_cost,
            x="department",
            y="total_treatment_cost",
            title="Treatment Cost by Department",
            text_auto=True
        )
        fig.update_layout(xaxis_title="Department", yaxis_title="Cost")
        st.plotly_chart(fig, use_container_width=True)

with patients_tab:
    p1, p2 = st.columns(2)

    with p1:
        diagnosis_mix = (
            filtered_df.groupby("diagnosis", as_index=False)
            .agg(patients=("patient_id", "nunique"))
            .sort_values("patients", ascending=False)
        )
        fig = px.pie(
            diagnosis_mix,
            values="patients",
            names="diagnosis",
            title="Diagnosis Mix"
        )
        st.plotly_chart(fig, use_container_width=True)

    with p2:
        city_patients = (
            filtered_df.groupby("city", as_index=False)
            .agg(patients=("patient_id", "nunique"))
            .sort_values("patients", ascending=False)
        )
        fig = px.bar(
            city_patients,
            x="city",
            y="patients",
            title="Patients by City",
            text_auto=True
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Patient Detail")
    patient_view = filtered_df[
        [
            "report_month",
            "patient_name",
            "age",
            "gender",
            "department",
            "diagnosis",
            "length_of_stay",
            "is_readmitted",
            "total_treatment_cost"
        ]
    ].sort_values(["report_month", "total_treatment_cost"], ascending=[True, False])

    st.dataframe(patient_view, use_container_width=True, hide_index=True)

with doctors_tab:
    d1, d2 = st.columns(2)

    with d1:
        doctor_workload = (
            filtered_df.groupby("doctor_name", as_index=False)
            .agg(
                patients=("patient_id", "nunique"),
                total_treatment_cost=("total_treatment_cost", "sum")
            )
            .sort_values("patients", ascending=False)
        )
        fig = px.bar(
            doctor_workload,
            x="doctor_name",
            y="patients",
            title="Doctor Workload",
            text_auto=True
        )
        st.plotly_chart(fig, use_container_width=True)

    with d2:
        specialization_cost = (
            filtered_df.groupby("specialization", as_index=False)
            .agg(total_treatment_cost=("total_treatment_cost", "sum"))
            .sort_values("total_treatment_cost", ascending=False)
        )
        fig = px.bar(
            specialization_cost,
            x="specialization",
            y="total_treatment_cost",
            title="Cost by Specialization",
            text_auto=True
        )
        st.plotly_chart(fig, use_container_width=True)

with export_tab:
    st.subheader("Filtered Hospital Metrics")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    st.download_button(
        "Download filtered CSV",
        data=to_csv_bytes(filtered_df),
        file_name="hospital_analytics_metrics_filtered.csv",
        mime="text/csv"
    )