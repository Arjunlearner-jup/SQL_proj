# Hospital Analytics Project

A hospital analytics project built with **MySQL 8.0**, **SQL**, **Python**, and **Streamlit** to analyze patient admissions, treatment cost, readmissions, length of stay, follow-up activity, and doctor workload.

This project uses two source tables:
- `patients`
- `treatments`

It then creates a final analytics table:
- `hospital_analytics_metrics`

The final table powers an interactive Streamlit dashboard for hospital operations and patient care analysis.

## Project overview

This is an end-to-end data analytics project focused on hospital operations. It covers:

- relational database design
- SQL data modeling
- realistic healthcare seed data
- advanced SQL transformations
- dashboard development with Streamlit

The project is designed to answer questions such as:

- How many patients were admitted each month?
- What is the average length of stay?
- Which departments generate the highest treatment cost?
- Which diagnoses are most common?
- Which doctors handle the most patients?
- How many patients are readmitted?
- How many cases require follow-up?

## Tech stack

- **MySQL 8.0** for database storage and SQL transformations
- **SQL** for schema design, seed data, and analytics queries
- **Python** for the dashboard application
- **Streamlit** for interactive dashboard development
- **Pandas** for data loading and filtering
- **SQLAlchemy + PyMySQL** for MySQL connectivity
- **Plotly** for data visualization

## Database structure

### 1. `patients`
Stores patient-level hospital admission details.

Suggested columns:
- `patient_id`
- `patient_name`
- `gender`
- `age`
- `city`
- `admission_date`
- `discharge_date`
- `department`
- `diagnosis`
- `admission_type`
- `insurance_provider`

### 2. `treatments`
Stores treatment-level activity for each patient.

Suggested columns:
- `treatment_id`
- `patient_id`
- `doctor_name`
- `specialization`
- `treatment_date`
- `treatment_type`
- `treatment_cost`
- `treatment_status`
- `follow_up_required`

### 3. `hospital_analytics_metrics`
The final reporting table used by the Streamlit dashboard.

Example metrics:
- `report_month`
- `patient_id`
- `patient_name`
- `department`
- `diagnosis`
- `doctor_name`
- `specialization`
- `length_of_stay`
- `is_discharged`
- `is_readmitted`
- `treatment_count`
- `total_treatment_cost`
- `avg_treatment_cost`
- `follow_up_flag`

## SQL files

### `01_schema.sql`
Creates the database tables:
- `patients`
- `treatments`

### `02_seed_data.sql`
Loads realistic sample hospital data including:
- emergency and scheduled admissions
- multiple departments and diagnoses
- doctor and specialization records
- treatment costs
- repeat admissions for readmission analysis

### `03_final_table.sql`
Builds the final analytics table:
- `hospital_analytics_metrics`

This file uses:
- joins
- CTEs
- date logic
- `DATEDIFF()` for length of stay
- readmission logic with `LAG()`
- treatment-level aggregation

## Key metrics included

The project focuses on important hospital performance metrics:

- **Patient Admissions**: Total patients admitted by month
- **Length of Stay**: Number of days between admission and discharge
- **Readmissions**: Patients readmitted within a follow-up period
- **Treatment Count**: Number of treatments received per patient
- **Treatment Cost**: Total and average treatment cost per patient
- **Follow-Up Flag**: Whether a patient required follow-up care
- **Doctor Workload**: Number of patients and treatment cost handled by doctor
- **Department Performance**: Activity and cost by department

## Streamlit dashboard

The dashboard reads from `hospital_analytics_metrics` and provides interactive analysis.

Main dashboard features:
- KPI cards for patient and cost metrics
- monthly admissions trend
- treatment cost by department
- diagnosis mix
- patient distribution by city
- doctor workload analysis
- specialization cost analysis
- filterable data table
- CSV export

## Project structure

```bash
HospitalAnalyticsProject/
│
├── 01_schema.sql
├── 02_seed_data.sql
├── 03_final_table.sql
├── streamlit_app.py
├── requirements.txt
└── README.md
```

## Setup instructions

### 1. Create and use the database

```sql
CREATE DATABASE IF NOT EXISTS HospitalAnalyticsProject;
USE HospitalAnalyticsProject;
```

### 2. Run the SQL files in order

```sql
-- Run in this order
01_schema.sql
02_seed_data.sql
03_final_table.sql
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

## requirements.txt

```txt
streamlit
pandas
plotly
sqlalchemy
pymysql
```

## Streamlit app configuration

Example database connection used in `streamlit_app.py`:

```python
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "HospitalAnalyticsProject"
DB_USER = "root"
DB_PASSWORD = "root1"
```

For deployment, database credentials should be stored in `.streamlit/secrets.toml` instead of hardcoding them.

## Run the dashboard

```bash
streamlit run streamlit_app.py
```

After running the command, open the local URL shown in the terminal, usually:

```bash
http://localhost:8501
```

## Dashboard tabs

- **Overview**: monthly admissions and department cost
- **Patients**: diagnosis mix, city analysis, and patient detail
- **Doctors**: workload and specialization cost
- **Data Export**: filtered hospital metrics and CSV download

## Learning outcomes

This project demonstrates:

- hospital data modeling in SQL
- multi-table joins
- healthcare KPI design
- date-based analytics
- readmission and stay-length analysis
- data visualization with Streamlit and Plotly
- end-to-end portfolio project building

## Future improvements

Possible next enhancements:

- 30-day readmission rate KPI
- bed occupancy analysis
- mortality or discharge outcome analysis
- insurance-based cost analysis
- doctor performance ranking with window functions
- cohort-style follow-up analysis
- deployment to Streamlit Community Cloud with remote MySQL

## Project title

**Hospital Patient Flow and Treatment Analytics Dashboard**
