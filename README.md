Healthcare Backend API
This project is a robust backend system for a healthcare application, built with Django and Django REST Framework. It features a comprehensive, role-based access control system for managing doctors, patients, and their interactions securely. The API is designed to be the backbone for a full-stack healthcare portal.

Key Features
Role-Based Access Control: A sophisticated permission system with three distinct user roles (Admin, Doctor, Patient), each with specific capabilities.

JWT Authentication: Secure user registration and login using JSON Web Tokens (JWT) for stateless authentication.

Profile Management: Separate, detailed profiles for doctors and patients, linked to their core user accounts.

Doctor-Specific Endpoints: Doctors can view all patients in the system and a list of patients specifically assigned to them.

Patient-Specific Endpoints: Patients can only view and manage their own profile and see a list of doctors they have been assigned to.

Admin-Managed Mappings: A secure system where only an Admin user can assign a patient to a doctor, reflecting a real-world workflow.

PostgreSQL Database: All data is stored in a powerful and scalable PostgreSQL database.

Professional Architecture: The project follows best practices, including a clean separation of concerns, environment variable management, and a logical API design.

Tech Stack
Backend: Python, Django

API: Django REST Framework (DRF)

Authentication: DRF Simple JWT

Database: PostgreSQL

Configuration: python-decouple, dj-database-url

CORS: django-cors-headers

Setup and Installation
Follow these steps to get the project running on your local machine.

1. Prerequisites
Python 3.8+

PostgreSQL installed and running.

Git

2. Clone the Repository
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name

3. Set Up Virtual Environment and Install Dependencies
# Create and activate a virtual environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install all required packages
pip install -r requirements.txt

4. Configure Environment Variables
In the root of the project, create a file named .env.

Copy the contents of the env.example file (or the template below) into your new .env file.

# .env file template
SECRET_KEY='your-django-secret-key-here'
DATABASE_URL='postgres://DB_USER:DB_PASSWORD@DB_HOST:DB_PORT/DB_NAME'

Replace the placeholder values in DATABASE_URL with your actual PostgreSQL credentials. For example:
DATABASE_URL='postgres://healthcare_user:password123@localhost:5432/health_db'

5. Set Up the Database
Run the migrations to create all the necessary tables in your PostgreSQL database.

python manage.py migrate

6. Create a Superuser (Admin)
To use the admin-only features, you need to create a superuser.

Run the command:

python manage.py createsuperuser

Follow the prompts to create your admin account.

Important: After creating the user, you must manually set their role in the database.

Connect to your database using pgAdmin or another tool.

Go to the api_profile table.

Find the row corresponding to your new superuser.

Set the value in the role column to admin.

7. Run the Development Server
python manage.py runserver

The API will now be running at http://127.0.0.1:8000/.

API Endpoints Guide
All protected endpoints require a Bearer Token in the Authorization header.

Authentication
Method

URL Path

Description

POST

/api/auth/register/patient/

Register a new Patient user.

POST

/api/auth/register/doctor/

Register a new Doctor user.

POST

/api/auth/login/

Log in any user to get a JWT.

Patient Endpoints (Requires Patient Role)
Method

URL Path

Description

GET

/api/patient-profile/

View your own patient profile.

PUT

/api/patient-profile/{user_id}/

Update your own patient profile.

GET

/api/patients/my-doctors/

View a list of doctors you are assigned to.

Doctor Endpoints (Requires Doctor Role)
Method

URL Path

Description

GET

/api/doctor-profile/

View your own doctor profile.

PUT

/api/doctor-profile/{user_id}/

Update your own doctor profile.

GET

/api/doctors/all-patients/

View a list of all patient profiles in the system.

GET

/api/doctors/my-patients/

View a list of patients assigned to you.

Admin Endpoints (Requires Admin Role)
Method

URL Path

Description

POST

/api/admin/assign-patient/

Assign a patient to a doctor. Body requires patient_id and doctor_id.

