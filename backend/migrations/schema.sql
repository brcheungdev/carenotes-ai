-- patients
CREATE TABLE IF NOT EXISTS patients (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  gender VARCHAR(10),
  dob DATE,
  mrn VARCHAR(64),
  ward VARCHAR(64),
  bed VARCHAR(32),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- encounters
CREATE TABLE IF NOT EXISTS encounters (
  id INT AUTO_INCREMENT PRIMARY KEY,
  patient_id INT NOT NULL,
  admit_time DATETIME,
  attending VARCHAR(100),
  FOREIGN KEY (patient_id) REFERENCES patients(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- notes
CREATE TABLE IF NOT EXISTS notes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  patient_id INT NOT NULL,
  encounter_id INT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  vitals JSON,
  pain_score INT,
  intake_ml INT,
  output_ml INT,
  subjective TEXT,
  objective TEXT,
  assessment TEXT,
  plan TEXT,
  med_given JSON,
  alerts JSON,
  signed TINYINT(1) DEFAULT 0,
  transcript LONGTEXT,
  FOREIGN KEY (patient_id) REFERENCES patients(id),
  FOREIGN KEY (encounter_id) REFERENCES encounters(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- audit_events
CREATE TABLE IF NOT EXISTS audit_events (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user VARCHAR(100),
  action VARCHAR(64),
  entity VARCHAR(64),
  entity_id INT,
  at DATETIME DEFAULT CURRENT_TIMESTAMP,
  diff_json JSON
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
