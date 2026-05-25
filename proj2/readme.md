# SaaSsubscriptionproject

A SaaS subscription analytics project built with **MySQL 8.0**, **SQL**, and **Streamlit** to analyze Monthly Recurring Revenue (MRR), churn, contraction, expansion, active customers, and cohort performance.

This project uses two source tables:
- `customers`
- `subscriptions`

It then creates a final analytics table:
- `saas_subscription_metrics`

The dashboard reads from that final table and visualizes revenue movement and customer trends.

## Project overview

This project is designed as an end-to-end portfolio project for subscription analytics. It covers:

- Database creation in MySQL
- Schema design for SaaS customer and subscription data
- Seed data with realistic lifecycle events
- SQL transformations for monthly metrics
- A Streamlit dashboard for interactive analysis

The final metrics table supports key SaaS business questions such as:

- How is MRR changing month by month?
- How much revenue came from new customers?
- How much revenue expanded from existing customers?
- How much revenue was lost from contraction or churn?
- How many active customers are there each month?
- Which cohorts and segments perform best?

## Tech stack

- **MySQL 8.0** for database storage and SQL transformations
- **Python** for the dashboard application
- **Streamlit** for dashboard UI
- **Pandas** for data loading and transformation in the app
- **SQLAlchemy + PyMySQL** for database connection
- **Plotly** for charts

## Database structure

### 1. `customers`
Stores customer-level attributes.

Suggested columns:
- `customer_id`
- `customer_name`
- `customer_email`
- `signup_date`
- `country`
- `industry`
- `company_size`
- `acquisition_channel`

### 2. `subscriptions`
Stores subscription lifecycle records.

Suggested columns:
- `subscription_id`
- `customer_id`
- `plan_name`
- `billing_cycle`
- `mrr_amount`
- `subscription_start_date`
- `subscription_end_date`
- `subscription_status`
- `change_type`

### 3. `saas_subscription_metrics`
The final reporting table used by the dashboard.

Example metrics:
- `metric_month`
- `cohort_month`
- `current_mrr`
- `prev_mrr`
- `new_mrr`
- `expansion_mrr`
- `contraction_mrr`
- `churned_mrr`
- `is_active_customer`
- `total_mrr`
- `total_active_customers`
- `revenue_change_type`

## SQL files

### `01_schema.sql`
Creates the database tables:
- `customers`
- `subscriptions`

### `02_seed_data.sql`
Inserts realistic sample data for:
- new subscriptions
- upgrades
- downgrades
- churn
- reactivation

### `03_final_table.sql`
Builds the final analytics table:
- `saas_subscription_metrics`

This SQL file uses:
- CTEs
- monthly date logic
- customer-month snapshots
- window functions such as `LAG()`
- revenue movement classification

## SaaS metrics included

The project focuses on common subscription metrics:

- **MRR**: Monthly recurring revenue in each period
- **New MRR**: Revenue from newly active customers
- **Expansion MRR**: Revenue gained from upgrades or account growth
- **Contraction MRR**: Revenue lost from downgrades
- **Churned MRR**: Revenue lost when customers become inactive
- **Active Customers**: Customers with positive MRR in a month
- **Cohort Month**: Customer signup month used for retention analysis

## Streamlit dashboard

The dashboard connects to MySQL and reads from `saas_subscription_metrics`.

Main dashboard features:
- KPI cards for MRR and customer metrics
- Monthly MRR trend chart
- Active customers by month chart
- Revenue movement analysis
- Customer breakdown by industry and company size
- Filterable data table
- CSV download for filtered data

## Project structure

```bash
SaaSsubscriptionproject/
│
├── 01_schema.sql
├── 02_seed_data.sql
├── 03_final_table.sql
├── streamlit_app.py
├── requirements.txt
└── README.md
```

## Setup instructions

### 1. Create and select the database

```sql
CREATE DATABASE IF NOT EXISTS SaaSsubscriptionproject;
USE SaaSsubscriptionproject;
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

Example database connection values used in `streamlit_app.py`:

```python
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "SaaSsubscriptionproject"
DB_USER = "root"
DB_PASSWORD = "root1"
```

For deployment, credentials should be stored in `.streamlit/secrets.toml` instead of hardcoding them.

## Run the dashboard

```bash
streamlit run streamlit_app.py
```

Then open the local URL shown in the terminal, usually:

```bash
http://localhost:8501
```

## Example dashboard sections

- **Overview**: MRR trend and active customers
- **Customers**: customer mix and top accounts
- **Revenue Movement**: new, expansion, contraction, and churned MRR
- **Data Export**: filtered metrics table and CSV export

## Learning outcomes

This project demonstrates:

- relational schema design
- SQL joins and transformations
- monthly recurring revenue modeling
- churn and retention analysis
- window functions in MySQL 8.0
- interactive dashboard development with Streamlit

## Future improvements

Possible enhancements:

- cohort retention heatmap
- NRR and GRR calculations
- plan-level performance analysis
- acquisition channel ROI tracking
- remote MySQL deployment
- Streamlit Cloud deployment with secrets

## Author

Project title:
**SaaS Subscription Dashboard – SQL + Streamlit**
