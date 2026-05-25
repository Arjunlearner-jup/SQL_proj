CREATE TABLE hospital_analytics_metrics AS
WITH patient_base AS (
    SELECT
        p.patient_id,
        p.patient_name,
        p.gender,
        p.age,
        p.city,
        p.admission_date,
        p.discharge_date,
        DATE_FORMAT(p.admission_date, '%Y-%m-01') AS report_month,
        p.department,
        p.diagnosis,
        p.admission_type,
        p.insurance_provider,
        DATEDIFF(p.discharge_date, p.admission_date) AS length_of_stay,
        CASE
            WHEN p.discharge_date IS NOT NULL THEN 1
            ELSE 0
        END AS is_discharged
    FROM patients p
),

patient_with_prev AS (
    SELECT
        pb.*,
        LAG(pb.discharge_date) OVER (
            PARTITION BY pb.patient_name
            ORDER BY pb.admission_date
        ) AS previous_discharge_date
    FROM patient_base pb
),

readmission_flagged AS (
    SELECT
        pwp.*,
        CASE
            WHEN previous_discharge_date IS NOT NULL
             AND DATEDIFF(admission_date, previous_discharge_date) <= 30 THEN 1
            ELSE 0
        END AS is_readmitted
    FROM patient_with_prev pwp
),

treatment_agg AS (
    SELECT
        t.patient_id,
        COUNT(*) AS treatment_count,
        SUM(t.treatment_cost) AS total_treatment_cost,
        AVG(t.treatment_cost) AS avg_treatment_cost,
        MAX(CASE WHEN t.follow_up_required = TRUE THEN 1 ELSE 0 END) AS follow_up_flag,
        MAX(t.doctor_name) AS doctor_name,
        MAX(t.specialization) AS specialization
    FROM treatments t
    GROUP BY t.patient_id
),

final_table AS (
    SELECT
        rf.report_month,
        rf.patient_id,
        rf.patient_name,
        rf.gender,
        rf.age,
        rf.city,
        rf.department,
        rf.diagnosis,
        rf.admission_type,
        rf.insurance_provider,
        rf.admission_date,
        rf.discharge_date,
        rf.length_of_stay,
        rf.is_discharged,
        rf.is_readmitted,
        COALESCE(ta.treatment_count, 0) AS treatment_count,
        COALESCE(ta.total_treatment_cost, 0) AS total_treatment_cost,
        ROUND(COALESCE(ta.avg_treatment_cost, 0), 2) AS avg_treatment_cost,
        COALESCE(ta.follow_up_flag, 0) AS follow_up_flag,
        COALESCE(ta.doctor_name, 'Unknown') AS doctor_name,
        COALESCE(ta.specialization, 'Unknown') AS specialization
    FROM readmission_flagged rf
    LEFT JOIN treatment_agg ta
        ON rf.patient_id = ta.patient_id
)

SELECT *
FROM final_table
ORDER BY report_month, patient_id;