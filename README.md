# DevTrack

DevTrack is a full-stack project and task management platform built with Django. It allows users to create and manage projects, organize tasks, assign work to project members, track task progress, and control access based on user roles.

## Features

* User registration and authentication
* Project creation and management
* Project members and owner-based permissions
* Task creation, editing, and deletion
* Task assignment to project members
* Task priorities and deadlines
* Task status tracking
* Role-based access control
* Dashboard with project and task statistics
* Django REST Framework API
* Responsive web interface
* PostgreSQL support for production
* SQLite support for local development
* Automated security and permission tests

## User Roles and Permissions

### Project Owner

The project owner can:

* Create projects
* Edit projects
* Delete projects
* Add and remove project members
* Create tasks
* Assign tasks to project members
* Edit task details
* Delete tasks
* View all project tasks

### Project Member

A project member can:

* View projects they belong to
* View all tasks within their projects
* View task details
* Update the status of tasks assigned to them

Project members cannot modify task details, assign tasks, delete tasks, or manage project members.

### Unrelated User

Users who are not owners or members of a project cannot access its projects or tasks.

## Technology Stack

### Backend

* Python
* Django
* Django REST Framework
* Django ORM

### Frontend

* HTML
* CSS
* JavaScript

### Database

* SQLite for development
* PostgreSQL for production

### Deployment

* Railway
* Gunicorn
* WhiteNoise

### Development Tools

* Git
* GitHub
* VS Code
* Postman

## Project Structure

```text
DevTrack/
├── accounts/
├── projects/
├── tasks/
├── devtrack/
├── templates/
├── static/
├── manage.py
├── requirements.txt
├── Procfile
├── .env
├── .env.example
└── README.md
```

## Application Flow

```text
User
  ↓
Django Authentication
  ↓
Dashboard
  ↓
Projects
  ↓
Project Members
  ↓
Tasks
  ↓
Role-Based Permissions
  ↓
Django ORM / PostgreSQL
```

The application also provides REST API endpoints through Django REST Framework.

## API

The application provides REST APIs for projects and tasks.

### Projects

```text
GET    /api/projects/
POST   /api/projects/
GET    /api/projects/{id}/
PUT    /api/projects/{id}/
PATCH  /api/projects/{id}/
DELETE /api/projects/{id}/
```

### Tasks

```text
GET    /api/tasks/
POST   /api/tasks/
GET    /api/tasks/{id}/
PUT    /api/tasks/{id}/
PATCH  /api/tasks/{id}/
DELETE /api/tasks/{id}/
```

Task permissions are enforced at the API level. Project owners have management access, while assigned project members can update their task status.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Mohan-R-Bodake/DevTrack.git
cd DevTrack
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

```powershell
venv\Scripts\activate
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file and add the required Django configuration, including the secret key and database settings.

Do not commit `.env` to GitHub.

### 6. Run migrations

```powershell
python manage.py migrate
```

### 7. Create an administrator

```powershell
python manage.py createsuperuser
```

### 8. Start the development server

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Testing

The project includes automated tests for:

* Authentication requirements
* Dashboard access
* Project permissions
* Project API access
* Task permissions
* Task status updates
* Unauthorized task access
* Project owner privileges
* Project member restrictions
* Task detail modification restrictions

Run the complete test suite with:

```powershell
python manage.py test
```

Current test suite:

```text
17 tests
17 passed
```

Run Django system checks with:

```powershell
python manage.py check
```

## Production Deployment

DevTrack is configured for deployment using Railway.

Production deployment uses:

* Gunicorn as the application server
* PostgreSQL as the production database
* WhiteNoise for static files
* Django migrations during deployment
* Environment variables for sensitive configuration

## Security

The application implements role-based access control at both the web-view and REST API levels.

Important security rules include:

* Users must authenticate before accessing protected resources.
* Project owners control project management.
* Project members can view project tasks.
* Only assigned members can update task status.
* Members cannot modify task details.
* Unrelated users cannot access private project resources.
* Sensitive environment variables are excluded from Git.

## Future Enhancements

Possible future improvements include:

* Email notifications
* Task comments
* File attachments
* Advanced project analytics
* Search and filtering
* Activity history
* Real-time notifications
* API documentation with Swagger/OpenAPI

## Author

**Mohan Bodake**

Computer Science and Design Engineering

GitHub: `Mohan-R-Bodake`

---

## License

This project is developed for educational and portfolio purposes.
