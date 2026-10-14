-- AttendEase database schema + sample data.
-- WARNING: this script DROPS and recreates both tables, so running it again resets all data.

CREATE DATABASE IF NOT EXISTS attendease
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE attendease;

DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS students;

-- ---------------------------------------------------------
-- Table 1: students
-- ---------------------------------------------------------
CREATE TABLE students (
    student_id   INT          NOT NULL AUTO_INCREMENT,
    roll_number  VARCHAR(20)  NOT NULL,
    full_name    VARCHAR(100) NOT NULL,
    email        VARCHAR(100) NOT NULL,
    class_name   VARCHAR(50)  NOT NULL,
    created_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id),
    CONSTRAINT uq_students_roll_number UNIQUE (roll_number),
    CONSTRAINT uq_students_email UNIQUE (email)
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- Table 2: attendance
-- ---------------------------------------------------------
CREATE TABLE attendance (
    attendance_id   INT  NOT NULL AUTO_INCREMENT,
    student_id      INT  NOT NULL,
    attendance_date DATE NOT NULL,
    status          ENUM('Present', 'Absent') NOT NULL,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (attendance_id),
    -- Prevents duplicate attendance for the same student on the same date
    CONSTRAINT uq_attendance_student_date UNIQUE (student_id, attendance_date),
    -- Deleting a student also deletes their attendance records
    CONSTRAINT fk_attendance_student
        FOREIGN KEY (student_id) REFERENCES students (student_id)
        ON DELETE CASCADE,
    INDEX idx_attendance_date (attendance_date)
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- Sample data: 10 students in 2 classes
-- ---------------------------------------------------------
INSERT INTO students (roll_number, full_name, email, class_name) VALUES
('BCA1-001', 'Aarav Sharma',  'aarav.sharma@example.com',  'BCA-1'),
('BCA1-002', 'Diya Patel',    'diya.patel@example.com',    'BCA-1'),
('BCA1-003', 'Rohan Mehta',   'rohan.mehta@example.com',   'BCA-1'),
('BCA1-004', 'Ananya Singh',  'ananya.singh@example.com',  'BCA-1'),
('BCA1-005', 'Karan Verma',   'karan.verma@example.com',   'BCA-1'),
('BCA2-001', 'Priya Nair',    'priya.nair@example.com',    'BCA-2'),
('BCA2-002', 'Arjun Reddy',   'arjun.reddy@example.com',   'BCA-2'),
('BCA2-003', 'Sneha Gupta',   'sneha.gupta@example.com',   'BCA-2'),
('BCA2-004', 'Vikram Joshi',  'vikram.joshi@example.com',  'BCA-2'),
('BCA2-005', 'Isha Kapoor',   'isha.kapoor@example.com',   'BCA-2');

-- ---------------------------------------------------------
-- Sample attendance: the 10 days BEFORE today (today is left empty
-- so you can test marking attendance). Each student gets a different
-- number of Present days (4 to 9 out of 10), so percentages vary.
-- ---------------------------------------------------------
INSERT INTO attendance (student_id, attendance_date, status)
SELECT
    s.student_id,
    DATE_SUB(CURDATE(), INTERVAL d.n DAY),
    IF(MOD(s.student_id * 7 + d.n * 3, 10) < (4 + MOD(s.student_id, 6)),
       'Present', 'Absent')
FROM students s
CROSS JOIN (
    SELECT 1 AS n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
    UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8
    UNION ALL SELECT 9 UNION ALL SELECT 10
) d;