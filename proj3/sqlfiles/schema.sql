CREATE TABLE patients (
    patient_id INT PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL,
    gender VARCHAR(20),
    age INT,
    city VARCHAR(50),
    admission_date DATE NOT NULL,
    discharge_date DATE,
    department VARCHAR(50),
    diagnosis VARCHAR(100),
    admission_type VARCHAR(30),
    insurance_provider VARCHAR(50)
);

CREATE TABLE treatments (
    treatment_id INT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(50),
    treatment_date DATE NOT NULL,
    treatment_type VARCHAR(50),
    treatment_cost DECIMAL(10,2) NOT NULL,
    treatment_status VARCHAR(30),
    follow_up_required BOOLEAN,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);
