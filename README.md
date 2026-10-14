# AttendEase — Student Attendance Management System

AttendEase is a web-based application designed to manage student records and track daily attendance efficiently.

## Features

- Dashboard for attendance overview
- Add and manage student records
- Mark student attendance
- View attendance history
- MySQL database integration

## Tech Stack

- **Backend:** Python, Flask
- **Database:** MySQL
- **Frontend:** HTML, CSS, Bootstrap, Jinja2

## Setup Instructions

1. Clone or download this repository.
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a MySQL database named `attendease`.
4. Execute the SQL commands in `schema.sql`.
5. Create a `.env` file using `.env.example` and configure your local database credentials and secret key.
6. Run the application:

   ```bash
   python -m flask --app app run --debug
   ```

7. Open `http://127.0.0.1:5000` in your browser.

## Security

Keep your `.env` file and database credentials private. Never commit secrets to version control.