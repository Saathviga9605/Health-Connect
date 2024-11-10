DROP TABLE Patients;
DROP TABLE Doctors;
DROP TABLE Departments;
DROP TABLE Authentication;

-- Creating Department table
CREATE TABLE Departments (
    Dept_id NUMBER PRIMARY KEY,
    D_Name VARCHAR2(50)
);

-- Creating Doctors table
CREATE TABLE Doctors (
    D_Id NUMBER PRIMARY KEY,
    Name VARCHAR2(50),
    Department NUMBER,
    FOREIGN KEY (Department) REFERENCES Departments(Dept_id)
);

-- Creating Patients table
CREATE TABLE Patients (
    ID NUMBER PRIMARY KEY,
    Name VARCHAR2(50),
    Contact_Number VARCHAR2(15),
    Disease_Name VARCHAR2(50),
    Treatment_Details VARCHAR2(100),
    Department NUMBER,
    Doctor_id NUMBER,
    FOREIGN KEY (Department) REFERENCES Departments(Dept_id),
    FOREIGN KEY (Doctor_id) REFERENCES Doctors(D_Id)
);

-- Insert values into Department table
INSERT INTO Departments (Dept_id, D_Name) VALUES (1, 'Cardiac');
INSERT INTO Departments (Dept_id, D_Name) VALUES (2, 'Pulmonology');
INSERT INTO Departments (Dept_id, D_Name) VALUES (3, 'Gastroenterology');
INSERT INTO Departments (Dept_id, D_Name) VALUES (4, 'Neurology');
INSERT INTO Departments (Dept_id, D_Name) VALUES (5, 'Orthopedics');
INSERT INTO Departments (Dept_id, D_Name) VALUES (6, 'Pediatrics');
INSERT INTO Departments (Dept_id, D_Name) VALUES (7, 'Oncology');
INSERT INTO Departments (Dept_id, D_Name) VALUES (8, 'Dermatology');
INSERT INTO Departments (Dept_id, D_Name) VALUES (9, 'Psychiatry');
INSERT INTO Departments (Dept_id, D_Name) VALUES (10, 'Nephrology');
INSERT INTO Departments (Dept_id, D_Name) VALUES (11, 'Urology');
INSERT INTO Departments (Dept_id, D_Name) VALUES (12, 'ENT');
INSERT INTO Departments (Dept_id, D_Name) VALUES (13, 'Endocrinology');
INSERT INTO Departments (Dept_id, D_Name) VALUES (14, 'Gynecology'); 
INSERT INTO Departments (Dept_id, D_Name) VALUES (15, 'Rheumatology');

-- Insert values into Doctors table
INSERT INTO Doctors (D_Id, Name, Department) VALUES (101, 'Arjun Mehta', 1);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (102, 'Sneha Patel', 2);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (103, 'Rajiv Kumar', 3);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (104, 'Priya Singh', 4);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (105, 'Vikram Rao', 5);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (106, 'Neha Das', 6);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (107, 'Sameer Shah', 7);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (108, 'Anita Roy', 8);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (109, 'Deepak Jain', 9);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (110, 'Kiran Gupta', 10);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (111, 'Rahul Reddy', 11);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (112, 'Maya Iyer', 12);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (113, 'Sunil Thakur', 13);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (114, 'Rani Nair', 14);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (115, 'Ajay Bhatt', 15);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (116, 'Pooja Verma', 1);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (117, 'Naveen Malik', 2);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (118, 'Suman Joshi', 3);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (119, 'Tarun Chandra', 4);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (120, 'Anjali Pandey', 5);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (121, 'Vishal Agarwal', 6);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (122, 'Preeti Kaur', 7);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (123, 'Amit Bansal', 8);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (124, 'Ritu Saxena', 9);
INSERT INTO Doctors (D_Id, Name, Department) VALUES (125, 'Gaurav Rathi', 10);

-- Insert values into Patients table

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (201, 'Kumar S', '9845123456', 'Heart Disease', 'Angioplasty', 1, 101);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (202, 'Lakshmi M', '9845234567', 'Asthma', 'Inhaler Therapy', 2, 102);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (203, 'Ravi K', '9845345678', 'Gastric Ulcer', 'Endoscopy', 3, 103);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (204, 'Meena N', '9845456789', 'Migraine', 'Medication', 4, 104);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (205, 'Anand B', '9845567890', 'Arthritis', 'Physical Therapy', 5, 105);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (206, 'Priya L', '9845678901', 'Pneumonia', 'Antibiotics', 2, 102);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (207, 'Rajesh K', '9845789012', 'Leukemia', 'Chemotherapy', 7, 107);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (208, 'Rekha R', '9845890123', 'Skin Allergy', 'Allergy Medication', 8, 108);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (209, 'Vignesh T', '9845901234', 'Schizophrenia', 'Therapy', 9, 109);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (210, 'Kavitha P', '9846012345', 'Kidney Stones', 'Lithotripsy', 10, 110);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (211, 'Suresh A', '9846123456', 'Urinary Infection', 'Antibiotics', 11, 111);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (212, 'Divya V', '9846234567', 'Hearing Loss', 'Hearing Aids', 12, 112);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (213, 'Manoj S', '9846345678', 'Diabetes', 'Insulin Therapy', 13, 113);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (214, 'Swathi M', '9846456789', 'Anemia', 'Iron Supplements', 14, 114);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (215, 'Karthik R', '9846567890', 'Rheumatoid Arthritis', 'Steroid Injection', 15, 115);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (216, 'Deepa T', '9846678901', 'Hypertension', 'Medication', 1, 101);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (217, 'Naveen J', '9846789012', 'Chronic Bronchitis', 'Nebulization', 2, 102);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (218, 'Rani S', '9846890123', 'Gastritis', 'Antacids', 3, 103);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (219, 'Arun L', '9846901234', 'Stroke', 'Rehabilitation', 4, 104);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (220, 'Bhavya D', '9847012345', 'Fracture', 'Casting', 5, 105);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (221, 'Anjali P', '9847123456', 'Hypertension', 'Beta Blockers', 1, 101);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (222, 'Mohan S', '9847234567', 'COPD', 'Bronchodilators', 2, 102);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (223, 'Revathi R', '9847345678', 'Irritable Bowel Syndrome', 'Diet Modification', 3, 103);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (224, 'Surya K', '9847456789', 'Epilepsy', 'Anticonvulsants', 4, 104);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (225, 'Pooja N', '9847567890', 'Back Pain', 'Physical Therapy', 5, 105);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (226, 'Kannan T', '9847678901', 'Asthma', 'Inhaler Therapy', 2, 102);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (227, 'Sakthi M', '9847789012', 'Leukemia', 'Chemotherapy', 7, 107);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (228, 'Lakshmi S', '9847890123', 'Psoriasis', 'Topical Therapy', 8, 108);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (229, 'Bala P', '9847901234', 'Bipolar Disorder', 'Mood Stabilizers', 9, 109);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (230, 'Geetha L', '9848012345', 'Chronic Kidney Disease', 'Dialysis', 10, 110);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (231, 'Ramesh R', '9848123456', 'Urinary Tract Infection', 'Antibiotics', 11, 101);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (232, 'Kala V', '9848234567', 'Hearing Impairment', 'Hearing Aids', 12, 102);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (233, 'Veena B', '9848345678', 'Diabetes', 'Insulin Therapy', 13, 103);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (234, 'Ganesh N', '9848456789', 'Iron Deficiency Anemia', 'Iron Supplementation', 14, 104);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (235, 'Yamini S', '9848567890', 'Rheumatoid Arthritis', 'NSAIDs', 15, 105);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (236, 'Muthu K', '9848678901', 'Atherosclerosis', 'Statins', 1, 106);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (237, 'Indira J', '9848789012', 'Tuberculosis', 'Anti-TB Drugs', 2, 107);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (238, 'Selvi P', '9848890123', 'Acid Reflux', 'Proton Pump Inhibitors', 3, 108);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (239, 'Manikandan R', '9848901234', 'Alzheimer Disease', 'Cognitive Enhancers', 4, 109);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (240, 'Vidhya T', '9849012345', 'Osteoporosis', 'Calcium Supplements', 5, 110);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (241, 'Arjun V', '9849123456', 'Pneumonia', 'IV Antibiotics', 2, 111);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (242, 'Rani L', '9849234567', 'Breast Cancer', 'Radiation Therapy', 7, 112);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (243, 'Raja D', '9849345678', 'Eczema', 'Topical Steroids', 8, 113);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (244, 'Kalaivani M', '9849456789', 'Panic Disorder', 'Anxiolytics', 9, 114);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (245, 'Senthil K', '9849567890', 'Renal Failure', 'Kidney Transplant', 10, 115);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (246, 'Anitha R', '9849678901', 'Bladder Infection', 'Antibiotics', 11, 116);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (247, 'Karthika N', '9849789012', 'Tonsillitis', 'Tonsillectomy', 12, 117);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (248, 'Murugan J', '9849890123', 'Hyperthyroidism', 'Thyroidectomy', 13, 118);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (249, 'Sangeetha L', '9849901234', 'Hemophilia', 'Factor Replacement', 14, 119);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (250, 'Sundar M', '9840012345', 'Lupus', 'Immunosuppressants', 15, 120);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (251, 'Ravichandran N', '9840123456', 'Arrhythmia', 'Pacemaker Implant', 1, 121);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (252, 'Priya V', '9840234567', 'Asthma', 'Inhaler Therapy', 2, 122);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (253, 'Sundari R', '9840345678', 'Celiac Disease', 'Gluten-Free Diet', 3, 123);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (254, 'Vinod M', '9840456789', 'Migraine', 'Pain Management', 4, 124);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (255, 'Devika S', '9840567890', 'Fractured Ankle', 'Casting', 5, 125);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (256, 'Arun B', '9840678901', 'Bronchitis', 'Antibiotics', 2, 101);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (257, 'Saraswati D', '9840789012', 'Leukemia', 'Stem Cell Transplant', 7, 102);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (258, 'Karthik R', '9840890123', 'Acne', 'Retinoid Cream', 8, 103);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (259, 'Selvam K', '9840901234', 'Schizophrenia', 'Antipsychotics', 9, 104);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (260, 'Jayalakshmi T', '9841012345', 'Kidney Stones', 'Lithotripsy', 10, 105);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (261, 'Sivakumar M', '9841123456', 'Bladder Infection', 'Antibiotics', 11, 106);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (262, 'Divya P', '9841234567', 'Tinnitus', 'Sound Therapy', 12, 107);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (263, 'Prakash L', '9841345678', 'Type 2 Diabetes', 'Lifestyle Changes', 13, 108);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (264, 'Rajesh V', '9841456789', 'Anemia', 'B12 Injections', 14, 109);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (265, 'Madhavi N', '9841567890', 'Scleroderma', 'Immunosuppressants', 15, 110);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (266, 'Sathya T', '9841678901', 'Hypertrophic Cardiomyopathy', 'ACE Inhibitors', 1, 111);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (267, 'Latha M', '9841789012', 'COPD', 'Bronchodilators', 2, 112);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (268, 'Ashwin B', '9841890123', 'Gallstones', 'Cholecystectomy', 3, 113);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (269, 'Rekha S', '9841901234', 'Parkinson’s Disease', 'Dopamine Agonists', 4, 114);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (270, 'Nirmala J', '9842012345', 'Hip Fracture', 'Surgery', 5, 115);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (271, 'Naveen R', '9842123456', 'Chronic Bronchitis', 'Steroids', 2, 112);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (272, 'Bhavani L', '9842234567', 'Melanoma', 'Surgery', 8, 113);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (273, 'Sanjay K', '9842345678', 'Depression', 'Therapy', 9, 114);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (274, 'Pavithra S', '9842456789', 'Kidney Disease', 'Dialysis', 10, 115);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (275, 'Balaji V', '9842567890', 'Tonsillitis', 'Medication', 12, 116);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (276, 'Ramya G', '9842678901', 'Hyperthyroidism', 'Thyroidectomy', 13, 117);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (277, 'Ajay K', '9842789012', 'Sickle Cell Anemia', 'Blood Transfusion', 14, 118);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (278, 'Lalitha N', '9842890123', 'Rheumatoid Arthritis', 'Anti-Rheumatics', 15, 119);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (279, 'Vijay B', '9842901234', 'Atrial Fibrillation', 'Anti-Coagulants', 1, 120);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (280, 'Meena T', '9843012345', 'Pneumonia', 'IV Antibiotics', 2, 121);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (281, 'Kiran M', '9843123456', 'Peptic Ulcer', 'Proton Pump Inhibitors', 3, 122);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (282, 'Shanthi P', '9843234567', 'Epilepsy', 'Anti-Seizure Medication', 4, 123);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (283, 'Ganesh V', '9843345678', 'Rotator Cuff Injury', 'Physical Therapy', 5, 124);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (284, 'Anitha S', '9843456789', 'Bronchitis', 'Steroid Inhalers', 2, 125);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (285, 'Kavitha D', '9843567890', 'Osteoporosis', 'Bone Density Medication', 5, 115);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (286, 'Arvind N', '9843678901', 'Leukemia', 'Chemotherapy', 7, 116);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (287, 'Sushmita B', '9843789012', 'Acne Vulgaris', 'Topical Retinoid', 8, 117);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (288, 'Ramesh K', '9843890123', 'Anxiety Disorder', 'Cognitive Therapy', 9, 118);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (289, 'Lakshmi R', '9843901234', 'Kidney Infection', 'Oral Antibiotics', 10, 119);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (290, 'Srinivasan G', '9844012345', 'Urinary Tract Infection', 'Antibiotics', 11, 120);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (291, 'Vaishnavi P', '9844123456', 'Sinusitis', 'Nasal Spray', 2, 121);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (292, 'Karthik K', '9844234567', 'Gallbladder Disease', 'Surgery', 3, 122);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (293, 'Indira S', '9844345678', 'Multiple Sclerosis', 'Immunotherapy', 4, 123);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (294, 'Suresh B', '9844456789', 'Cirrhosis', 'Liver Transplant', 5, 124);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (295, 'Nithya A', '9844567890', 'AIDS', 'Antiretroviral Therapy', 12, 125);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (296, 'Siva N', '9844678901', 'Lung Cancer', 'Radiotherapy', 2, 101);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (297, 'Karthika M', '9844789012', 'Celiac Disease', 'Dietary Adjustment', 3, 102);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (298, 'Gowtham R', '9844890123', 'Seizure Disorder', 'Anticonvulsants', 4, 103);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (299, 'Anand B', '9844901234', 'Shoulder Pain', 'Physiotherapy', 5, 104);

INSERT INTO Patients (ID, Name, Contact_Number, Disease_Name, Treatment_Details, Department, Doctor_id)
VALUES (300, 'Shreya S', '9845012345', 'Skin Allergy', 'Antihistamines', 8, 105);

